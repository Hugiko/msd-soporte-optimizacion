"""OPTIMIZADOR AUTOMATICO DEL SOPORTE - MSD 2026-27 (831_MSD_13_B, Soporte 6, acero S235)

  Objetivo:     minimizar la MASA
  Restriccion:  tension de von Mises (fuera de la singularidad de los pernos) <= 215 MPa
  Fijo:         posicion de los 4 agujeros de perno y de los 2 agujeros del bulon

COMO FUNCIONA (version corta para la defensa)
  Se prueban varias FAMILIAS de piezas, por turnos:
    - "simjeb":   los mejores disenos del concurso GE / SimJEB (mismos agujeros que el 0.stp) MODIFICADOS:
                  torneo inicial de los mas prometedores y despues collares (anaden) y aligeramientos (quitan).
    - "refuerzo": collares junto a los tornillos (el punto critico del original) + vaciado del resto.
    - "cero":     un soporte nuevo (cajon de torsion + orejetas + franja de pernos).
    - "vaciado":  el soporte original al que se le quita material (retirada: sin disenos validos; se conserva).
  Para cada familia:
    1. Reparto inicial (DOE Sobol): disenos repartidos por todo el espacio -> primera "foto".
    2. Aprende: procesos gaussianos (BoTorch) predicen masa(x), tension(x) y desplazamiento(x) con su incertidumbre.
    3. Ramas (arbol genealogico): cada rama prueba cambios alrededor de su mejor diseno (si mejora, alarga el paso;
       si no, lo acorta). Al terminar, su mejor diseno crea ramas hijas: fina, amplia y cruce (por turnos); cada 2 ramas
       nace una rama EXPLORADORA en una zona nunca probada, y si la familia se ESTANCA (25 disenos sin mejorar un 0,3 %)
       se lanzan 2 exploradoras mas. Las ramas no finas incluyen mutaciones grandes (2-5 variables a la vez).
    4. Antes de gastar ANSYS: piezas repetidas, filtro por prediccion y pasada rapida con malla gruesa.
    5. Cada candidato a NUEVO MEJOR se verifica con malla fina antes de aceptarlo.
  Cada nuevo mejor diseno: proyecto Workbench, historial, timelapse, GitHub y Discord.

ROBUSTEZ: guarda tras cada diseno; si se apaga el PC continua donde iba; nunca sobrescribe;
un diseno que falla (geometria/malla/solver) se registra, se penaliza y se sigue.
"""
import os, sys, json, time, math, csv, shutil, zipfile, subprocess, threading, datetime, traceback, glob, importlib
import warnings
warnings.filterwarnings("ignore")      # avisos internos de torch/botorch (obsolescencias): no son errores
import numpy as np
from scipy.stats import norm, qmc

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fem

ROOT = fem.ROOT
USER = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
CFG = dict(
    force=float(USER.get("carga_N", 37800.0)),
    sigma_y=float(USER.get("sigma_y_MPa", 215.0)),
    margin=float(USER.get("margen_optimizacion", 1.0)),
    budget=int(USER.get("presupuesto_por_familia", 150)),
    families=list(USER.get("familias", ["vaciado", "cero"])),
    git=bool(USER.get("subir_a_github", True)),
    workbench=bool(USER.get("crear_workbench_en_cada_mejora", True)),
    n_init=12, n_mass_cache=48, n_cand=3000, seed=2026,
    max_fail_streak=8,
    tr_init=0.30, tr_min=0.05, tr_max=0.6, tr_succ=2, tr_fail=4, max_restarts=3,
)
TEST = "--prueba" in sys.argv          # prueba corta en carpeta aparte (no toca los resultados reales)
if TEST:
    CFG.update(n_init=3, n_mass_cache=6, budget=8, git=False, workbench=False)
    USER["pruebas_por_rama"] = 2
SIG_OBJ = CFG["margin"] * CFG["sigma_y"]
U_LIM = float(USER.get("desplazamiento_max_mm", 0.25))     # 0 = sin limite de desplazamiento
M_ORIG = 2.4234     # masa del original con el MISMO modelo de EF (malla de 4 mm); la del CAD es 2,4115 kg


SCORE_P = float(USER.get("peso_seguridad", 0.5))    # 0 = solo masa; 0,5 = 1 % de masa vale 2 % de tension


def score(m):
    """Puntuacion de compromiso masa-seguridad (menor = mejor): masa x aprovechamiento^p.
    aprovechamiento = max(tension/limite, desplazamiento/limite) = 1 / coeficiente de seguridad."""
    return m["mass_kg"] * max(violation(m), 1e-6) ** SCORE_P


def fs(m):
    """Coeficiente de seguridad respecto al LIMITE ELASTICO (215 MPa / tension), el que se muestra."""
    return CFG["sigma_y"] / max(m["vm_metric"], 1e-6)


def violation(m):
    """>1 si incumple alguna condicion (tension o desplazamiento); se usa cuando aun no hay disenos validos."""
    v = m["vm_metric"] / SIG_OBJ
    if U_LIM > 0 and m.get("u_max") is not None:
        v = max(v, m["u_max"] / U_LIM)
    return v
TOP = os.path.join(ROOT, "runs", ("prueba_" if TEST else "opt_") + f"{int(round(CFG['force']))}N")
LOG = os.path.join(TOP, "optimizador.log")
FAMILIES = {
    "vaciado": ("geometry_vaciado", "Vaciado del original",
                [0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.5, 0.0]),   # 1er diseno: casi el original
    "refuerzo": ("geometry_refuerzo", "Refuerzo + vaciado",
                 [0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.5, 0.0, 0.667, 0.444, 0.75]),  # 1er diseno: collares, cortes minimos
    "cero": ("geometry", "Diseno desde cero", None),
    "simjeb": ("geometry_simjeb", "SimJEB modificado", "auto"),     # 1os disenos: torneo de candidatos SimJEB
}
BRANCH_PREFIX = {"vaciado": "V", "refuerzo": "R", "cero": "C", "simjeb": "S"}


# ============================================================================ utilidades
def log(msg):
    fem.log(msg, LOG)


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


def fmt_t(s):
    s = int(s)
    return f"{s // 3600}h{(s % 3600) // 60:02d}m" if s >= 3600 else f"{s // 60}m{s % 60:02d}s"


def fit_gp(X, y):
    import torch
    from botorch.models import SingleTaskGP
    from botorch.models.transforms import Standardize
    from botorch.fit import fit_gpytorch_mll
    from gpytorch.mlls import ExactMarginalLogLikelihood
    torch.manual_seed(CFG["seed"])
    m = SingleTaskGP(torch.tensor(np.asarray(X), dtype=torch.double),
                     torch.tensor(np.asarray(y), dtype=torch.double).unsqueeze(-1),
                     outcome_transform=Standardize(m=1))
    fit_gpytorch_mll(ExactMarginalLogLikelihood(m.likelihood, m))
    return m


def gp_predict(m, X):
    import torch
    with torch.no_grad():
        post = m.posterior(torch.tensor(np.asarray(X), dtype=torch.double))
        return (post.mean.squeeze(-1).numpy(), post.variance.clamp_min(1e-12).sqrt().squeeze(-1).numpy())


def gp_lengthscales(m):
    k = m.covar_module
    for _ in range(3):
        if getattr(k, "lengthscale", None) is not None:
            return k.lengthscale.detach().numpy().ravel()
        k = getattr(k, "base_kernel", None)
        if k is None:
            break
    return None


# ============================================================================ GitHub (segundo plano)
def find_git():
    """Ruta completa de git.exe (no depende del PATH heredado, que puede estar desactualizado)."""
    cands = [shutil.which("git"), r"C:\Program Files\Git\cmd\git.exe", r"C:\Program Files (x86)\Git\cmd\git.exe",
             os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe")]
    cands += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\GitHubDesktop\app-*\resources\app\git\cmd\git.exe"))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


class GitSync:
    def __init__(self, enabled):
        self.git = find_git()
        self.enabled = enabled and os.path.isdir(os.path.join(ROOT, ".git")) and self.git is not None
        if enabled and self.git is None:
            log("AVISO: no se encuentra git.exe -> no se subira nada a GitHub (el optimizador sigue igual)")
        elif self.enabled:
            log(f"GitHub: subidas activadas ({self.git})")
        self.th = None

    def push(self, msg, wait=False):
        if not self.enabled:
            return
        if self.th and self.th.is_alive():
            if not wait:
                return
            self.th.join(600)
        self.th = threading.Thread(target=self._run, args=(msg,), daemon=True)
        self.th.start()
        if wait:
            self.th.join(600)

    def _run(self, msg):
        try:
            g = lambda *a, t=300: subprocess.run([self.git, *a], cwd=ROOT, capture_output=True, text=True, timeout=t,
                                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            g("add", "-A"); g("commit", "-q", "-m", msg)
            r = g("push", "-q", "origin", "HEAD", t=600)
            if r.returncode != 0:
                log(f"  (GitHub: subida pendiente, se reintentara: {r.stderr.strip()[:100]})")
            else:
                log("  (GitHub: subido)")
        except Exception as e:
            log(f"  (GitHub: {e!r}; se reintentara)")


class CachedGeom:
    """Envuelve el modulo de geometria de una familia y recuerda las ultimas piezas construidas: la comprobacion de
    piezas repetidas y el calculo usan la MISMA geometria sin construirla dos veces."""
    def __init__(self, mod):
        self._mod, self._memo = mod, []

    def __getattr__(self, name):
        return getattr(self._mod, name)

    def build(self, p):
        key = tuple(round(float(p[k]), 6) for k in self._mod.NAMES)
        for k, val in self._memo:
            if k == key:
                return val
        val = self._mod.build(p)
        self._memo = ([(key, val)] + self._memo)[:3]
        return val


# ============================================================================ una familia
class Family:
    def __init__(self, key):
        modname, self.title, self.x_first = FAMILIES[key]
        self.key = key
        self.mod = CachedGeom(importlib.import_module(modname))
        self.names = self.mod.NAMES; self.lo = self.mod.LO; self.hi = self.mod.HI; self.D = len(self.names)
        self.out = os.path.join(TOP, key); os.makedirs(self.out, exist_ok=True)
        self.state_path = os.path.join(self.out, "estado.json")
        self.st = json.load(open(self.state_path)) if os.path.exists(self.state_path) else \
            dict(ramas={}, done=False, motivo_fin="")
        self.rng = np.random.default_rng(CFG["seed"] + {"vaciado": 0, "refuerzo": 3, "cero": 7, "simjeb": 5}.get(key, 11))
        if self.x_first == "auto":                       # primeros disenos propios de la familia (torneo SimJEB)
            self.x_first_list = [list(map(float, x)) for x in self.mod.first_designs()]
            self.n_init = CFG["n_init"] if TEST else max(CFG["n_init"], min(len(self.x_first_list),
                                                                            int(USER.get("torneo_simjeb_disenos", 40))))
        else:
            self.x_first_list = [] if self.x_first is None else [self.x_first]
            self.n_init = CFG["n_init"]
        self.cat_dims = [self.names.index(c) for c in getattr(self.mod, "CATEGORICAL", [])]
        self.cache = None
        self.pending = self.recover_interrupted()

    # ---- parametros <-> cubo unidad
    def to_params(self, xu):
        v = self.lo + np.clip(np.asarray(xu, float), 0, 1) * (self.hi - self.lo)
        return {k: round(float(x), 4) for k, x in zip(self.names, v)}

    def snap(self, X):
        """Redondea las variables categoricas a sus valores enteros (en el cubo unidad)."""
        X = np.array(X, float, copy=True)
        for d in self.cat_dims:
            g = max(self.hi[d] - self.lo[d], 1e-9)
            if X.ndim == 1:
                X[d] = np.round(X[d] * g) / g
            else:
                X[:, d] = np.round(X[:, d] * g) / g
        return X

    def to_unit(self, p):
        return (np.array([p[k] for k in self.names], float) - self.lo) / (self.hi - self.lo)

    def save_state(self):
        atomic_json(self.state_path, self.st)

    # ---- datos
    def runs(self):
        out = []
        for d in sorted(glob.glob(os.path.join(self.out, "[0-9][0-9][0-9]"))):
            mp, pp = os.path.join(d, "metrics.json"), os.path.join(d, "proposal.json")
            if os.path.exists(mp) and os.path.exists(pp):
                try:
                    out.append(dict(id=int(os.path.basename(d)), dir=d, m=json.load(open(mp, encoding="utf-8")),
                                    p=json.load(open(pp, encoding="utf-8")), fam=self.key))
                except Exception:
                    pass
        return out

    def recover_interrupted(self):
        pend = []
        for d in sorted(glob.glob(os.path.join(self.out, "[0-9][0-9][0-9]"))):
            if os.path.exists(os.path.join(d, "proposal.json")) and not os.path.exists(os.path.join(d, "metrics.json")):
                prop = json.load(open(os.path.join(d, "proposal.json"), encoding="utf-8"))
                bak = os.path.join(self.out, "_interrumpidos", f"{os.path.basename(d)}_{datetime.datetime.now():%Y%m%d_%H%M%S}")
                os.makedirs(os.path.dirname(bak), exist_ok=True)
                shutil.move(d, bak)
                pend.append((int(os.path.basename(d)), prop))
                log(f"[{self.key}] el diseno {os.path.basename(d)} se corto a medias: se repite igual.")
        return pend

    def mass_cache(self):
        if self.cache is not None:
            return self.cache
        path = os.path.join(self.out, "cache_masa.json")
        cache = json.load(open(path)) if os.path.exists(path) else []
        n = CFG["n_mass_cache"]
        if len(cache) < n:
            pts = qmc.Sobol(self.D, scramble=True, seed=CFG["seed"] + 1).random(64)[:n]
            log(f"[{self.key}] aprendiendo masa(x) con {n} geometrias rapidas (sin ANSYS); hechas {len(cache)}")
            for i in range(len(cache), n):
                try:
                    _, info = self.mod.build(self.to_params(pts[i]))
                    cache.append(dict(x=pts[i].tolist(), mass=info["mass_kg"], ok=True))
                except Exception as e:
                    cache.append(dict(x=pts[i].tolist(), mass=None, ok=False, err=str(e)[:150]))
                if (i + 1) % 6 == 0 or i + 1 == n:
                    atomic_json(path, cache)
                    print(f"   [{self.key}] geometria {i + 1}/{n} (fallos {sum(not c['ok'] for c in cache)})", flush=True)
        self.cache = cache
        return cache

    # ---- ramas (arbol genealogico) -----------------------------------------------------------------
    # Una RAMA es una linea de busqueda que arranca de un diseno semilla y hace sus pruebas alrededor de
    # su mejor diseno (region de confianza). Al terminar (N pruebas o paso diminuto) su MEJOR diseno
    # genera 2 ramas hijas: "fina" (pasos pequenos, afina) y "amplia" (pasos grandes, explora alrededor).
    # Siempre se trabaja en la rama activa cuyo origen es mejor. Todas comparten lo aprendido (mismos GP).
    def score_of(self, rs):
        ok = [r for r in rs if r and r["m"].get("status") == "ok"]
        val = [r for r in ok if category(r["m"]) == "valido"]
        if val:
            b = min(val, key=lambda r: score(r["m"])); return (0, score(b["m"])), b
        if ok:
            b = min(ok, key=lambda r: violation(r["m"])); return (1, violation(b["m"])), b
        return (2, 1e9), None

    def run_by_id(self, runs, rid):
        return next((r for r in runs if r["id"] == rid), None)

    def branch_runs(self, runs, bid):
        br = self.st["ramas"][bid]
        rs = [r for r in runs if r["p"].get("rama") == bid]
        seed = self.run_by_id(runs, br.get("semilla"))
        return rs + ([seed] if seed else [])

    def new_branch(self, bid, parent, seed_run, L, tipo, seed_score, seed_x=None, nota=""):
        self.st["ramas"][bid] = dict(id=bid, padre=parent, semilla=seed_run["id"] if seed_run else None, tipo=tipo, L=L, L0=L,
                                     succ=0, fail=0, n=0, best=None, prev_x=None, estado="activa", hijos=[],
                                     seed_score=list(seed_score), seed_x=seed_x, nota=nota,
                                     creada=datetime.datetime.now().isoformat())
        if parent:
            self.st["ramas"][parent]["hijos"].append(bid)

    def root_id(self):
        return BRANCH_PREFIX.get(self.key, self.key[0].upper()) + "0"

    def ensure_branches(self, runs):
        R = self.st.setdefault("ramas", {})
        root = self.root_id()
        if root not in R:
            R[root] = dict(id=root, padre=None, semilla=None, tipo="reparto inicial", L=None, L0=None, succ=0, fail=0,
                           n=sum(1 for r in runs if r["p"].get("rama") in (None, root)), best=None, prev_x=None,
                           estado="terminada", hijos=[], seed_score=[9, 0], creada=datetime.datetime.now().isoformat())
        if not R[root]["hijos"]:
            sc, b = self.score_of([r for r in runs if r["p"].get("rama") in (None, root)])
            R[root]["best"] = dict(score=list(sc), id=b["id"]) if b else None
            if b:
                self.new_branch(root[0] + "1", root, b, CFG["tr_init"], "inicial", sc)
                log(f"[{self.key}] reparto inicial terminado: la rama {root[0]}1 arranca del diseno {b['id']:03d}")
                if self.cat_dims:          # torneo de semillas: una rama por cada una de las 3 mejores semillas DISTINTAS
                    d0 = self.cat_dims[0]
                    used = {round(float(self.to_unit(b["p"]["params"])[d0]), 6)}
                    init = [r for r in runs if r["p"].get("rama") in (None, root) and r["m"].get("status") == "ok"]
                    k = 2
                    for rr in sorted(init, key=lambda q: self.score_of([q])[0]):
                        if k > int(USER.get("ramas_iniciales_simjeb", 3)):
                            break
                        sd = round(float(self.to_unit(rr["p"]["params"])[d0]), 6)
                        if sd in used:
                            continue
                        used.add(sd)
                        self.new_branch(f"{root[0]}{k}", root, rr, CFG["tr_init"], "inicial", self.score_of([rr])[0])
                        log(f"[{self.key}] la rama {root[0]}{k} arranca de otra semilla: el diseno {rr['id']:03d}")
                        k += 1
        self.save_state()

    def current(self):
        act = [b for b in self.st["ramas"].values() if b["estado"] == "activa"]
        if not act:
            return None
        if len(act) > 1 and self.rng.random() < float(USER.get("prob_rama_al_azar", 0.25)):
            return act[int(self.rng.integers(len(act)))]        # variedad: de vez en cuando, una rama activa al azar
        # la de mejor origen; entre ramas hermanas (mismo origen: fina, amplia, cruce) por turnos (la que menos lleva)
        return min(act, key=lambda b: (tuple(b["seed_score"]), b["n"], b["creada"]))

    # ---- propuesta: DOE -> rama activa (region de confianza) con modelos sustitutos
    def propose(self, runs):
        n = len(runs)
        if n < self.n_init:
            rows = self.x_first_list + qmc.Sobol(self.D, scramble=True, seed=CFG["seed"]).random(16).tolist()
            x = self.snap(np.array(rows[n]))
            if n < len(self.x_first_list) and hasattr(self.mod, "seed_info"):
                sd = self.mod.seed_info(self.to_params(x))
                why = (f"torneo de disenos SimJEB ({n + 1}/{self.n_init}): SimJEB n.o {sd['id']} ({sd['cat']}, {sd['autor']}) "
                       f"tal cual, sin modificar (tension estimada {sd['est']:.0f} MPa)")
            else:
                why = f"reparto inicial ({n + 1}/{self.n_init}): explorar todo el espacio"
            return x, why, None, "DOE", self.root_id()
        self.ensure_branches(runs)
        br = self.current()
        bid, L = br["id"], br["L"]
        if br.get("semilla") is None and br.get("seed_x") is not None and br["n"] == 0:
            txt = (f"cruce: mezcla de los parametros de {br.get('nota', '')}" if br["tipo"] == "cruce" else
                   f"exploradora: punto al azar en una zona nunca probada ({br.get('nota', '')})")
            return np.array(br["seed_x"]), f"[rama {bid}] {txt}", None, br["tipo"], bid
        cache = self.mass_cache()
        ok = [r for r in runs if r["m"].get("status") == "ok"]
        Xm = [c["x"] for c in cache if c["ok"]] + [self.to_unit(r["p"]["params"]).tolist() for r in runs if r["m"].get("mass_cad_kg")]
        ym = [math.log(c["mass"]) for c in cache if c["ok"]] + [math.log(r["m"]["mass_cad_kg"]) for r in runs if r["m"].get("mass_cad_kg")]
        gm = fit_gp(Xm, ym)
        gs = fit_gp([self.to_unit(r["p"]["params"]) for r in ok], [math.log(r["m"]["vm_metric"]) for r in ok])
        gu = fit_gp([self.to_unit(r["p"]["params"]) for r in ok], [math.log(max(r["m"]["u_max"], 1e-6)) for r in ok]) \
            if U_LIM > 0 else None
        bsc, center_r = self.score_of(self.branch_runs(runs, bid))
        if center_r is None:                       # rama de cruce cuyo primer diseno fallo: se parte de la mezcla
            bsc, center_r = self.score_of(runs)
        c = self.to_unit(center_r["p"]["params"])
        feas_b = bsc[0] == 0
        # candidatos: (a) caja alrededor del mejor de la rama; (b) cambios de 1-3 parametros; (c) seguir la direccion que funciono
        # ramas FINAS: solo se mueven los parametros que mas influyen (segun los modelos sustitutos)
        dims = np.arange(self.D)
        if br["tipo"] == "fina":
            ls_s, ls_m = gp_lengthscales(gs), gp_lengthscales(gm)
            if ls_s is not None and ls_m is not None:
                imp = (1 / ls_s) / np.sum(1 / ls_s) + (1 / ls_m) / np.sum(1 / ls_m)
                dims = np.argsort(imp)[::-1][:max(3, (self.D + 1) // 2)]
        mask = np.zeros(self.D); mask[dims] = 1.0
        box = np.clip(c + (self.rng.random((CFG["n_cand"], self.D)) - 0.5) * L * mask, 0, 1)
        few = np.repeat(c[None], 1200, 0)
        for row in few:
            idx = self.rng.choice(dims, min(len(dims), self.rng.integers(1, 4)), replace=False)
            row[idx] = np.clip(row[idx] + self.rng.normal(0, L / 2, len(idx)), 0, 1)
        cand = [box, few]
        if br["tipo"] != "fina":                 # MUTACIONES GRANDES: 2-5 variables con saltos amplios
            big = np.repeat(c[None], 800, 0)
            for row in big:
                idx = self.rng.choice(self.D, int(self.rng.integers(min(2, self.D), min(5, self.D) + 1)), replace=False)
                row[idx] = np.clip(row[idx] + self.rng.normal(0, 0.25, len(idx)), 0, 1)
            cand.append(big)
        if br.get("prev_x") is not None and br.get("succ", 0) > 0:
            dvec = c - np.array(br["prev_x"])
            if np.linalg.norm(dvec) > 1e-6:
                t = self.rng.uniform(0.3, 2.0, (300, 1))
                cand.append(np.clip(c + t * dvec + self.rng.normal(0, L / 8, (300, self.D)), 0, 1))
        cand = np.vstack(cand)
        for d in self.cat_dims:                  # variable categorica (p. ej. que diseno SimJEB): valores enteros
            cand[:, d] = self.snap(cand)[:, d]
            if br["tipo"] in ("fina", "inicial", "cruce"):
                cand[:, d] = c[d]                # se afina sobre la misma semilla
            elif br["tipo"] == "amplia":
                keep = self.rng.random(len(cand)) < 0.7
                cand[keep, d] = c[d]
        allX = np.array([self.to_unit(r["p"]["params"]) for r in runs])
        dmin_req = float(USER.get("distancia_minima", 0.03))   # cambios REALES: nada casi identico a lo ya probado
        far = np.min(np.linalg.norm(cand[:, None] - allX[None], axis=2), axis=1) > dmin_req
        cand = cand[far] if far.sum() >= 50 else cand
        mu_m, sd_m = gp_predict(gm, cand)
        mu_s, sd_s = gp_predict(gs, cand)
        pof = norm.cdf((math.log(SIG_OBJ) - mu_s) / sd_s)          # P(tension <= limite)
        if gu is not None:
            mu_u, sd_u = gp_predict(gu, cand)
            pof = pof * norm.cdf((math.log(U_LIM) - mu_u) / sd_u)  # x P(desplazamiento <= limite)
        bad = [cc["x"] for cc in cache if not cc["ok"]] + [self.to_unit(r["p"]["params"]).tolist() for r in runs if r["m"].get("status") != "ok"]
        pen = np.ones(len(cand))
        if bad:
            db = np.min(np.linalg.norm(cand[:, None] - np.array(bad)[None], axis=2), axis=1)
            pen = 1 - 0.9 * np.exp(-(db / 0.06) ** 2)
        if feas_b:
            lu = mu_s - math.log(SIG_OBJ)                              # log del aprovechamiento previsto (tension)
            if gu is not None:
                lu = np.maximum(lu, mu_u - math.log(U_LIM))
            mu_sc = mu_m + SCORE_P * lu
            sd_sc = np.sqrt(sd_m ** 2 + (SCORE_P * sd_s) ** 2)
            imp = math.log(score(center_r["m"])) - mu_sc
            z = imp / sd_sc
            acq = (imp * norm.cdf(z) + sd_sc * norm.pdf(z)) * pof * pen
            mode = "mejorar masa"
        else:
            acq = (pof + 0.02 * (mu_s.max() - mu_s)) * pen           # rama aun sin disenos validos: bajar tension
            mode = "buscar diseno valido"
        i = int(np.argmax(acq)); x = cand[i]
        moved = np.flatnonzero(np.abs(x - c) > 0.02)
        what = ", ".join(self.names[j] for j in moved[:4]) + ("..." if len(moved) > 4 else "")
        if br["n"] == 0:
            why = f"rama nueva ({br['tipo']}, paso {L:.2f}) desde el diseno {br['semilla']:03d}; cambia {what}"
        elif br.get("succ", 0) > 0:
            why = f"el ultimo paso mejoro: sigue en esa linea (paso {L:.2f}); cambia {what}"
        elif br.get("fail", 0) >= 2:
            why = f"varios pasos sin mejora: paso mas corto ({L:.2f}); cambia {what}"
        else:
            why = f"pequeno cambio alrededor del mejor de la rama (paso {L:.2f}); cambia {what}"
        if br["tipo"] == "fina" and len(dims) < self.D:
            why += f" (rama fina: solo mueve {', '.join(self.names[j] for j in dims)})"
        why = f"[rama {bid}] " + ("[aun sin disenos validos] " if not feas_b else "") + why
        pred = dict(mass_kg=float(math.exp(mu_m[i])), stress_mpa=float(math.exp(mu_s[i])), p_cumple=float(pof[i]),
                    paso=L, modo=mode)
        ls = gp_lengthscales(gs)
        pred["importancia_tension"] = None if ls is None else dict(zip(self.names, map(float, (1 / ls) / np.sum(1 / ls))))
        return x, why, pred, "aprende", bid

    def far_point(self, runs, n=2048):
        """Punto al azar en la zona MENOS explorada: de n candidatos aleatorios, el mas alejado de todos los disenos probados."""
        cand = qmc.Sobol(self.D, scramble=True, seed=int(self.rng.integers(1e9))).random(n)
        X = np.array([self.to_unit(r["p"]["params"]) for r in runs]) if runs else np.zeros((1, self.D)) + 0.5
        dmin = np.min(np.linalg.norm(cand[:, None] - X[None], axis=2), axis=1)
        top = np.argsort(dmin)[::-1][:20]               # los 20 mas alejados; se elige uno al azar entre ellos
        i = int(self.rng.choice(top))
        return self.snap(cand[i]), float(dmin[i])

    def spawn_explorer(self, runs, sc, nota=""):
        """Rama EXPLORADORA: arranca de un punto al azar lejos de todo lo probado y se trabaja en ella enseguida."""
        R = self.st["ramas"]
        xe, dmin = self.far_point(runs)
        k = 1 + sum(1 for b in R.values() if b["tipo"] == "exploradora")
        eid = f"{self.root_id()[0]}X{k}"
        while eid in R:
            k += 1; eid = f"{self.root_id()[0]}X{k}"
        self.new_branch(eid, self.root_id(), None, CFG["tr_init"], "exploradora", (sc[0], sc[1] * (1 - 1e-9)),
                        seed_x=xe.tolist(), nota=f"a {dmin:.2f} del diseno probado mas cercano" + nota)
        return eid

    def check_stagnation(self, runs):
        """ANTI-ESTANCAMIENTO: si en los ultimos N disenos la familia no ha mejorado su mejor puntuacion ni un 0,3 %,
        se lanzan 2 ramas exploradoras nuevas (saltos a zonas nunca probadas) y se cierran las ramas finas
        que ya no avanzan. Devuelve las ramas creadas (o None)."""
        N = int(USER.get("estancamiento_disenos", 25))
        if N <= 0 or len(runs) < self.n_init + N or len(runs) - int(self.st.get("ultimo_estancamiento", 0)) < N:
            return None
        rs = sorted(runs, key=lambda r: r["id"])
        so, _ = self.score_of(rs[:-N]); sn, _ = self.score_of(rs)
        if sn[0] < so[0] or (sn[0] == so[0] and sn[1] < so[1] * (1 - 0.003)):
            return None
        self.st["ultimo_estancamiento"] = len(runs)
        cerradas = []
        for b in self.st["ramas"].values():       # ramas finas que llevan muchas pruebas sin mejorar: se cierran
            if b["estado"] == "activa" and b["tipo"] == "fina" and b["n"] >= 6 and b.get("fail", 0) >= 2:
                b["estado"] = "terminada"; b["motivo_fin"] = "estancamiento (sin mejora)"; cerradas.append(b["id"])
        new = [self.spawn_explorer(runs, sn, nota=" (anti-estancamiento)") for _ in range(2)]
        self.save_state()
        return new, cerradas

    def update_branch(self, runs, r_new):
        """Actualiza la rama del diseno recien calculado: paso mas largo si mejora, mas corto si no; al terminar
        la rama, su mejor diseno genera dos ramas hijas."""
        R = self.st.get("ramas", {})
        bid = r_new["p"].get("rama")
        if bid not in R or R[bid]["estado"] != "activa":
            if len(runs) >= self.n_init:
                self.ensure_branches(runs)
            return
        br = R[bid]; br["n"] += 1
        sc, b = self.score_of(self.branch_runs(runs, bid))
        last = br.get("best")
        if last is None:
            improved = False
        else:
            ls = tuple(last["score"])
            improved = sc[0] < ls[0] or (sc[0] == ls[0] and sc[1] < ls[1] * (1 - 1e-4))
        if b is not None and (last is None or improved):
            if last is not None:
                prev = self.run_by_id(runs, last["id"])
                br["prev_x"] = self.to_unit(prev["p"]["params"]).tolist() if prev else None
            br["best"] = dict(score=list(sc), id=b["id"])
        if improved:
            br["succ"] += 1; br["fail"] = 0
            if br["succ"] >= CFG["tr_succ"]:
                br["L"] = min(2 * br["L"], CFG["tr_max"]); br["succ"] = 0
        elif last is not None:
            br["fail"] += 1; br["succ"] = 0
            if br["fail"] >= CFG["tr_fail"]:
                br["L"] /= 2; br["fail"] = 0
        n_max = int(USER.get("pruebas_por_rama", 30))
        if br["n"] >= n_max or br["L"] < CFG["tr_min"]:
            br["estado"] = "terminada"
            br["motivo_fin"] = f"{br['n']} pruebas" if br["n"] >= n_max else "paso diminuto (ya no mejora)"
            best_r = self.run_by_id(runs, br["best"]["id"]) if br.get("best") else None
            if best_r is not None:
                for k, (tipo, L0) in enumerate((("fina", 0.10), ("amplia", 0.35)), 1):
                    self.new_branch(f"{bid}.{k}", bid, best_r, L0, tipo, sc)
                msg = f"crea las ramas {bid}.1 (fina) y {bid}.2 (amplia)"
                # CRUCE: si otra rama terminada tiene un buen diseno distinto, se mezclan los parametros de ambos
                others = []
                for ob in R.values():
                    if ob["id"] != bid and ob["estado"] == "terminada" and ob.get("best") and ob["padre"] is not None:
                        orr = self.run_by_id(runs, ob["best"]["id"])
                        if orr is not None and orr["id"] != best_r["id"]:
                            others.append((tuple(ob["best"]["score"]), ob["id"], orr))
                if others:
                    osc, oid, orr = min(others)
                    xa, xb = self.to_unit(best_r["p"]["params"]), self.to_unit(orr["p"]["params"])
                    if np.linalg.norm(xa - xb) > 0.05:
                        pick = self.rng.random(self.D) < 0.5
                        xc = np.where(pick, xa, xb)
                        self.new_branch(f"{bid}.3", bid, None, 0.20, "cruce", min(sc, osc), seed_x=xc.tolist(),
                                        nota=f"{bid} (#{best_r['id']:03d}) y {oid} (#{orr['id']:03d})")
                        msg += f" y {bid}.3 (cruce con la rama {oid})"
                # EXPLORADORA: cada N ramas terminadas, una rama que parte de un punto al azar lejos de todo lo probado
                every = int(USER.get("rama_exploradora_cada", 3))
                n_fin = sum(1 for b in R.values() if b["estado"] == "terminada" and b["padre"] is not None)
                if every > 0 and n_fin % every == 0:
                    eid = self.spawn_explorer(runs, sc)
                    msg += f"; ademas nace la rama exploradora {eid}"
                log(f"[{self.key}] rama {bid} terminada ({br['motivo_fin']}); su mejor diseno ({best_r['id']:03d}) {msg}")
        self.save_state()


# ============================================================================ clasificacion, historial, paquetes
REG_COLS = ["familia", "rama", "iter", "fecha", "motivo", "params", "masa_kg", "tension_MPa", "tension_bruta_MPa", "desp_max_mm",
            "cumple", "categoria", "pred_masa_kg", "pred_tension_MPa", "pred_P_cumple", "paso", "nodos", "tiempo_s", "estado", "error"]


def category(m):
    if m.get("status") == "filtrado":
        return "filtrado"            # descartado por el modelo sin gastar ANSYS
    if m.get("status") != "ok":
        return "fallido"
    v = violation(m)            # tension y desplazamiento a la vez
    if v <= 1.0 and m.get("verif_ok") is False:
        return "cerca_del_limite"   # cumplia con la malla normal pero NO con la malla fina de verificacion
    return "valido" if v <= 1.0 else ("cerca_del_limite" if v <= 1.1 else "descartado")


def append_registro(fam, r):
    m, p = r["m"], r["p"]; pr = p.get("pred") or {}
    row = dict(familia=fam.key, rama=p.get("rama"), iter=r["id"], fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), motivo=p["motivo"],
               params=" ".join(f"{k}={v}" for k, v in p["params"].items()), masa_kg=m.get("mass_kg") or m.get("mass_cad_kg"),
               tension_MPa=m.get("vm_metric"), tension_bruta_MPa=m.get("vm_max_raw"), desp_max_mm=m.get("u_max"),
               cumple=category(m) == "valido", categoria=category(m), pred_masa_kg=pr.get("mass_kg"),
               pred_tension_MPa=pr.get("stress_mpa"), pred_P_cumple=pr.get("p_cumple"), paso=pr.get("paso"),
               nodos=m.get("n_nodes"), tiempo_s=round(m.get("total_s", 0), 1), estado=m.get("status"), error=(m.get("error") or "")[:150])
    for path in (os.path.join(fam.out, "registro_iteraciones.csv"), os.path.join(TOP, "registro_global.csv")):
        new = not os.path.exists(path)
        with open(path, "a", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=REG_COLS, delimiter=";")
            if new:
                w.writeheader()
            w.writerow({k: (f"{v:.4f}".replace(".", ",") if isinstance(v, float) else v) for k, v in row.items()})


def package_apdl(wd):
    inp = os.path.join(wd, "model.inp")
    if not os.path.exists(inp):
        return
    gui = ("! Mechanical APDL: File > Change Directory (esta carpeta) > File > Read Input from > abrir_en_ansys.inp\n"
           "/INPUT,model,inp\n/POST1\nSET,LAST\n/EFACET,1\n/VIEW,1,1,-1.5,1\n/AUTO,1\nCMSEL,S,FIJO\nFSUM\nALLSEL\nPLNSOL,S,EQV\n")
    with zipfile.ZipFile(os.path.join(wd, "modelo_apdl.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(inp, "model.inp"); z.writestr("abrir_en_ansys.inp", gui)


def write_clasificacion(fam, runs):
    groups = {k: [] for k in ("valido", "cerca_del_limite", "descartado", "fallido", "filtrado")}
    for r in runs:
        groups[category(r["m"])].append(r)
    groups["valido"].sort(key=lambda r: score(r["m"]))
    title = {"valido": f"VALIDOS, ordenados por puntuacion masa-seguridad (tension <= {SIG_OBJ:.0f} MPa" + (f" y desplazamiento <= {U_LIM:.2f} mm" if U_LIM > 0 else "") + ")",
             "cerca_del_limite": "CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina",
             "descartado": "DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen",
             "fallido": "FALLIDOS (geometria / malla / solver): registrados y penalizados",
             "filtrado": "FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS"}
    L = [f"# {fam.title}: clasificacion de disenos", "", f"Limite: {SIG_OBJ:.0f} MPa | carga {CFG['force']:.0f} N | "
         f"actualizado {datetime.datetime.now():%Y-%m-%d %H:%M}", ""]
    for k, lst in groups.items():
        L += [f"## {title[k]} ({len(lst)})", "", "| # | masa (kg) | tension (MPa) | motivo | imagen |", "|---|---|---|---|---|"]
        for j, r in enumerate(lst):
            m = r["m"]; tag = " **MEJOR**" if (k == "valido" and j == 0) else ""
            ten = "-" if m.get("vm_metric") is None else f"{m['vm_metric']:.1f}"
            img = f"[ver]({os.path.basename(r['dir'])}/vonmises.png)" if os.path.exists(os.path.join(r["dir"], "vonmises.png")) else "-"
            L.append(f"| {r['id']:03d}{tag} | {(m.get('mass_kg') or m.get('mass_cad_kg') or 0):.3f} | {ten} | {r['p']['motivo']} | {img} |")
        L.append("")
    open(os.path.join(fam.out, "CLASIFICACION.md"), "w", encoding="utf-8").write("\n".join(L))


PEND = os.path.join(TOP, "pendientes_workbench.json")


def load_pending():
    return json.load(open(PEND, encoding="utf-8")) if os.path.exists(PEND) else []


def do_workbench(job):
    """Crea el proyecto .wbpj (+ .wbpz para GitHub). Devuelve True si quedo montado."""
    try:
        import exportar_workbench as EW
        ok, _, _ = EW.export(job["step"], job["out"], job["name"], CFG["force"], log=LOG, half=job["half"], timeout=1800,
                             iface=job.get("iface"))
        return ok
    except Exception as e:
        log(f"  (Workbench: {e!r})")
        return False


def retry_pending_workbench(git):
    pend = load_pending()
    if not pend:
        return
    job = pend.pop(0)
    job["intentos"] = job.get("intentos", 0) + 1
    log(f"Reintentando proyecto Workbench pendiente: {job['name']} (intento {job['intentos']})")
    if do_workbench(job):
        git.push(f"proyecto Workbench {job['name']}")
    elif job["intentos"] < 6:
        pend.append(job)
    else:
        log(f"  se abandona el proyecto Workbench {job['name']} tras 6 intentos (el diseno sigue guardado)")
    atomic_json(PEND, pend)


def gb_score(gb):
    """Puntuacion del ultimo mejor registrado (compatible con registros antiguos sin puntuacion)."""
    if gb.get("puntuacion") is not None:
        return gb["puntuacion"]
    return score(dict(mass_kg=gb["mass_kg"], vm_metric=gb["vm_metric"], u_max=gb.get("u_max") or 0.0))


def global_best():
    path = os.path.join(TOP, "MEJOR_GLOBAL.json")
    return json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None


def register_new_best(fam, r, git):
    """Nuevo mejor diseno de TODAS las familias: Workbench, historial, timelapse y GitHub."""
    m, wd = r["m"], r["dir"]
    hist = os.path.join(TOP, "historial"); os.makedirs(hist, exist_ok=True)
    k = len(glob.glob(os.path.join(hist, "[0-9][0-9]_*"))) + 1
    name = f"{k:02d}_{fam.key}_{r['id']:03d}_{m['mass_kg']:.3f}kg"
    hd = os.path.join(hist, name); os.makedirs(hd, exist_ok=True)
    for f in ("resumen.png", "geometria.png", "vonmises.png", "params.json", "metrics.json", "proposal.json", "geometria.step", "modelo_apdl.zip"):
        if os.path.exists(os.path.join(wd, f)):
            shutil.copy(os.path.join(wd, f), os.path.join(hd, f))
    wb_ok = False
    if CFG["workbench"]:
        job = dict(step=os.path.join(hd, "geometria.step"), out=os.path.join(hd, "workbench"),
                   name=f"soporte_{fam.key}_{r['id']:03d}", half=r["p"]["params"].get("t_lug", 6.4) / 2, intentos=0,
                   iface=m.get("interfaces"))
        wb_ok = do_workbench(job)
        if not wb_ok:
            pend = load_pending(); pend.append(job); atomic_json(PEND, pend)
            log("  (proyecto Workbench pendiente: se reintentara en las siguientes iteraciones;"
                " si teneis Workbench abierto, cerradlo: la licencia Student solo admite una sesion)")
    best = dict(familia=fam.key, titulo=fam.title, iter=r["id"], carpeta=hd, mass_kg=m["mass_kg"], vm_metric=m["vm_metric"],
                puntuacion=score(m), coef_seguridad=fs(m),
                vm_max_raw=m.get("vm_max_raw"), u_max=m.get("u_max"), params=r["p"]["params"], workbench=wb_ok,
                fecha=datetime.datetime.now().isoformat())
    atomic_json(os.path.join(TOP, "MEJOR_GLOBAL.json"), best)
    for f in ("resumen.png", "geometria.png", "vonmises.png"):
        if os.path.exists(os.path.join(wd, f)):
            shutil.copy(os.path.join(wd, f), os.path.join(TOP, "MEJOR_" + f))
    # fotograma del timelapse
    try:
        from PIL import Image, ImageDraw, ImageFont
        tl = os.path.join(TOP, "timelapse"); os.makedirs(tl, exist_ok=True)
        im = Image.open(os.path.join(wd, "vonmises.png")).convert("RGB"); dr = ImageDraw.Draw(im)
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except Exception:
            font = ImageFont.load_default()
        dr.rectangle([0, im.height - 58, im.width, im.height], fill=(255, 255, 255))
        dr.text((18, im.height - 50), f"Mejora {k}: {fam.title}, diseno {r['id']} | {m['mass_kg']:.3f} kg | {m['vm_metric']:.0f} MPa",
                fill=(0, 0, 0), font=font)
        im.save(os.path.join(tl, f"frame_{k:03d}.png"))
    except Exception as e:
        log(f"  (timelapse: {e!r})")
    # historial legible
    rows = []
    for d in sorted(glob.glob(os.path.join(hist, "[0-9][0-9]_*"))):
        try:
            mm = json.load(open(os.path.join(d, "metrics.json"), encoding="utf-8"))
            wb = glob.glob(os.path.join(d, "workbench", "*.wbpz"))
            rows.append(f"| {os.path.basename(d)[:2]} | {os.path.basename(d)} | {mm['mass_kg']:.3f} | {mm['vm_metric']:.1f} | "
                        f"![](historial/{os.path.basename(d)}/resumen.png) | "
                        + (f"[Workbench](historial/{os.path.basename(d)}/workbench/{os.path.basename(wb[0])})" if wb else "-") + " |")
        except Exception:
            pass
    open(os.path.join(TOP, "HISTORIAL.md"), "w", encoding="utf-8").write(
        "# Historial de la evolucion de la pieza\n\nCada fila es un diseno que mejoro a TODOS los anteriores.\n\n"
        f"Original: 2,411 kg (CAD) | limite {SIG_OBJ:.0f} MPa | carga {CFG['force']:.0f} N\n\n"
        "| n | diseno | masa (kg) | tension (MPa) | geometria | proyecto |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    log(f"  >>> NUEVO MEJOR DISENO GLOBAL #{k}: {m['mass_kg']:.3f} kg  ({fam.title}, diseno {r['id']})"
        + (" | proyecto Workbench creado" if wb_ok else ""))


FAMS = []          # familias activas (lo rellena main) para el panel
GAL = os.path.join(TOP, "galeria")
VERD = {"valido": "VALIDO", "cerca_del_limite": "CASI", "descartado": "NO_VALIDO", "fallido": "FALLO", "filtrado": "FILTRADO"}


def fig_of(r):
    """Ficha de un diseno: la copia de la galeria (la que se sube a GitHub) o, si no hay, la de su carpeta."""
    g = r["m"].get("galeria")
    if g and os.path.exists(os.path.join(TOP, g)):
        return os.path.join(TOP, g)
    return os.path.join(r["dir"], "resumen.png")


def add_to_gallery(fam, r):
    """Copia comprimida de la ficha (o tarjeta de fallo) con nombre FECHA_HORA_familia_n_veredicto_masa.jpg."""
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(GAL, exist_ok=True)
    m = r["m"]; cat = category(m)
    mass = m.get("mass_kg") or m.get("mass_cad_kg") or 0.0
    name = f"{datetime.datetime.now():%Y%m%d_%H%M%S}_{fam.key}_{r['id']:03d}_{VERD[cat]}_{mass:.3f}kg.jpg"
    src = os.path.join(r["dir"], "resumen.png")
    if os.path.exists(src):
        im = Image.open(src).convert("RGB")
        if im.width > 1200:
            im = im.resize((1200, int(im.height * 1200 / im.width)))
    else:                       # diseno fallido: tarjeta con el motivo
        im = Image.new("RGB", (1200, 500), (250, 245, 245)); dr = ImageDraw.Draw(im)
        try:
            font = ImageFont.truetype("arial.ttf", 30); small = ImageFont.truetype("arial.ttf", 22)
        except Exception:
            font = small = ImageFont.load_default()
        head = ("FILTRADO por el modelo (no se calculo en ANSYS)" if m.get("status") == "filtrado"
                else f"FALLO ({m.get('status')})")
        dr.text((30, 30), f"{fam.title} - diseno {r['id']:03d}: {head}", fill=(160, 0, 0), font=font)
        err = (m.get("error") or "")[:400]
        for i in range(0, len(err), 80):
            dr.text((30, 100 + 30 * (i // 80)), err[i:i + 80], fill=(40, 40, 40), font=small)
        dr.text((30, 440), "Motivo de la propuesta: " + r["p"]["motivo"][:85], fill=(60, 60, 60), font=small)
    im.save(os.path.join(GAL, name), "JPEG", quality=80, optimize=True)
    m["galeria"] = "galeria/" + name
    atomic_json(os.path.join(r["dir"], "metrics.json"), m)


def write_tree():
    """ARBOL.md: arbol genealogico de ramas de cada familia (diagrama Mermaid, GitHub lo dibuja)."""
    gb = global_best()
    allv = []
    for f in FAMS:
        for r in f.runs():
            if category(r["m"]) == "valido":
                allv.append((score(r["m"]), f.key, r["id"]))
    best_glob = min(allv) if allv else None
    L = ["# Arbol genealogico de la busqueda", "",
         "Cada caja es una **rama**: una linea de busqueda que parte de un diseno y prueba cambios a su alrededor.",
         "Al terminar, su mejor diseno crea dos ramas hijas: **fina** (cambios pequenos) y **amplia** (cambios grandes).",
         "Azul = activa | gris = terminada | verde grueso = contiene el MEJOR diseno de todos.", ""]
    for f in FAMS:
        R = f.st.get("ramas", {})
        if not R:
            continue
        runs = {r["id"]: r for r in f.runs()}
        L += [f"## {f.title}", "", "```mermaid", "graph TD",
              "classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000",
              "classDef fin fill:#eeeeee,stroke:#888,color:#000",
              "classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000"]
        for bid, b in sorted(R.items(), key=lambda kv: kv[1]["creada"]):
            nid = bid.replace(".", "_")
            best = runs.get((b.get("best") or {}).get("id")) if b.get("best") else None
            if best is None and b["padre"] is None:      # raiz (reparto inicial)
                best = runs.get((b.get("best") or {}).get("id"))
            if best and category(best["m"]) == "valido":
                res = f"mejor: {best['m']['mass_kg']:.3f} kg, {best['m']['vm_metric']:.0f} MPa (#{best['id']:03d})"
            elif best and best["m"].get("vm_metric"):
                res = f"aun sin validos; el mas cercano {best['m']['vm_metric']:.0f} MPa (#{best['id']:03d})"
            else:
                res = "sin resultados aun"
            n = b["n"] if b["padre"] else sum(1 for r in runs.values() if r["p"].get("rama") in (None, bid))
            tipo = b["tipo"] + (f", paso {b['L0']:.2f}" if b.get("L0") else "")
            label = f"{bid} - {tipo}<br/>{n} pruebas<br/>{res}"
            cls = "activa" if b["estado"] == "activa" else "fin"
            if best_glob and best_glob[1] == f.key and runs.get(best_glob[2]) is not None \
                    and runs[best_glob[2]]["p"].get("rama", f.root_id()) == bid:
                cls = "mejor"                     # rama donde SE ENCONTRO el mejor diseno de todos
            L.append(f'{nid}["{label}"]:::{cls}')
            if b["padre"]:
                L.append(f"{b['padre'].replace('.', '_')} --> {nid}")
        L += ["```", ""]
    open(os.path.join(TOP, "ARBOL.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    try:
        tree_png(best_glob)
    except Exception as e:
        log(f"(imagen del arbol: {e!r})")


def tree_png(best_glob, max_nodes=26):
    """arbol.png para el README: una fila por familia. Si hay muchas ramas se muestran el camino al mejor diseno
    y las ramas activas (las demas se agrupan)."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fams = [f for f in FAMS if f.st.get("ramas")]
    if not fams:
        return
    fig, axes = plt.subplots(len(fams), 1, figsize=(16, 4.2 * len(fams)), squeeze=False)
    for ax, f in zip(axes[:, 0], fams):
        R = f.st["ramas"]; runs = {r["id"]: r for r in f.runs()}
        best_b = None
        if best_glob and best_glob[1] == f.key and best_glob[2] in runs:
            best_b = runs[best_glob[2]]["p"].get("rama")
        keep = set(R)
        if len(R) > max_nodes:                          # poda: camino al mejor + activas + sus antecesores
            keep = set()
            seeds = [b for b in R if R[b]["estado"] == "activa"] + ([best_b] if best_b in R else [])
            for b in seeds:
                while b:
                    keep.add(b); b = R[b]["padre"]
        kids = {b: [c for c in R[b]["hijos"] if c in keep] for b in keep}
        root = f.root_id()
        pos, cnt = {}, [0]

        def place(b, d):
            ch = kids.get(b, [])
            for c in ch:
                place(c, d + 1)
            x = np.mean([pos[c][0] for c in ch]) if ch else cnt[0]
            if not ch:
                cnt[0] += 1
            pos[b] = (x, -d)
        place(root, 0)
        for b, (x, y) in pos.items():
            for c in kids.get(b, []):
                ax.plot([x, pos[c][0]], [y, pos[c][1]], c="#888", lw=1, zorder=1)
        for b, (x, y) in pos.items():
            br = R[b]; best = runs.get((br.get("best") or {}).get("id"))
            if best and category(best["m"]) == "valido":
                res = f"{best['m']['mass_kg']:.3f} kg"
            elif best and best["m"].get("vm_metric"):
                res = f"{best['m']['vm_metric']:.0f} MPa"
            else:
                res = "-"
            n = br["n"] if br["padre"] else sum(1 for r in runs.values() if r["p"].get("rama") in (None, b))
            fc, ec, lw = ("#d6eaff", "#1f6fb5", 1) if br["estado"] == "activa" else ("#eeeeee", "#888888", 1)
            if b == best_b:
                fc, ec, lw = "#c8f0c0", "#1a9850", 3
            hidden = len(R[b]["hijos"]) - len(kids.get(b, []))
            txt = f"{b}\n{br['tipo']}\n{n} pr. | {res}" + (f"\n(+{hidden} ramas)" if hidden > 0 else "")
            ax.text(x, y, txt, ha="center", va="center", fontsize=7.5, zorder=3,
                    bbox=dict(boxstyle="round,pad=0.35", fc=fc, ec=ec, lw=lw))
        ax.set_title(f"{f.title}: {len(R)} ramas" + (" (se muestran el camino al mejor y las activas)" if len(R) > max_nodes else ""),
                     fontsize=11)
        xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
        ax.set_xlim(min(xs) - 0.8, max(xs) + 0.8); ax.set_ylim(min(ys) - 0.7, 0.7); ax.axis("off")
    fig.suptitle("Arbol genealogico de la busqueda  (azul = activa, gris = terminada, verde = rama del mejor diseno)", fontsize=12)
    fig.tight_layout(); fig.savefig(os.path.join(TOP, "arbol.png"), dpi=110); plt.close(fig)


def write_gallery_md():
    """GALERIA.md: TODAS las fichas (validas o no) en orden cronologico, la mas reciente arriba."""
    rows = []
    for f in sorted(glob.glob(os.path.join(GAL, "*.jpg")), reverse=True):
        p = os.path.basename(f)[:-4].split("_")       # fecha, hora, familia, n, veredicto..., masa
        try:
            fecha = f"{p[0][6:8]}/{p[0][4:6]} {p[1][:2]}:{p[1][2:4]}"
            fam_t = FAMILIES.get(p[2], ("", p[2]))[1]
            verd = " ".join(p[4:-1]).replace("NO VALIDO", "no valido")
            rows.append(f"| {fecha} | {fam_t} {p[3]} | {verd} | {p[-1].replace('kg', ' kg')} | "
                        f"<a href=\"galeria/{os.path.basename(f)}\"><img src=\"galeria/{os.path.basename(f)}\" width=\"420\"></a> |")
        except IndexError:
            pass
    open(os.path.join(TOP, "GALERIA.md"), "w", encoding="utf-8").write(
        "# Galeria: todos los disenos calculados, en orden cronologico (el mas reciente arriba)\n\n"
        "Cada ficha: geometria 3D | tension de von Mises | deformada | radiografia del interior.\n"
        "Veredicto: VALIDO (cumple tension y desplazamiento), CASI (hasta +10 %), no valido, FALLO.\n\n"
        "| fecha | diseno | veredicto | masa | ficha (clic para ampliar) |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")

HEAVY = ("campos.npz", "geometria.step", "modelo_apdl.zip", "solve.out", "progreso.log", "vonmises.png", "geometria.png",
         "res_glob.txt", "res_nod.txt")


def dir_mb(path):
    tot = 0
    for dp, _, fs in os.walk(path):
        for f in fs:
            try:
                tot += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    return tot / 1e6


def cleanup():
    """Libera espacio: borra los ficheros pesados de disenos antiguos ya superados.
    Nunca borra params/metrics/proposal (el modelo aprende de ellos) ni resumen.png."""
    keep_recent = int(USER.get("limpieza_mantener_ultimos", 20))
    keep_best = int(USER.get("limpieza_mantener_mejores", 5))
    keep_wb = int(USER.get("mantener_proyectos_workbench_resueltos", 3))
    freed = 0.0
    for f in FAMS:
        rs = f.runs()
        best = sorted([r for r in rs if category(r["m"]) == "valido"], key=lambda r: score(r["m"]))[:keep_best]
        protect = {r["id"] for r in best} | {r["id"] for r in rs[-keep_recent:]}
        for r in rs:
            if r["id"] in protect:
                continue
            for name in HEAVY:
                p = os.path.join(r["dir"], name)
                if os.path.exists(p):
                    freed += os.path.getsize(p) / 1e6
                    try:
                        os.remove(p)
                    except OSError:
                        pass
        bak = os.path.join(f.out, "_interrumpidos")
        if os.path.isdir(bak):
            freed += dir_mb(bak); shutil.rmtree(bak, ignore_errors=True)
    # proyectos Workbench resueltos: solo los ultimos 'keep_wb' mejores (de los antiguos queda el .wbpz)
    hist = sorted(glob.glob(os.path.join(TOP, "historial", "[0-9][0-9]_*")))
    for d in hist[:-keep_wb] if keep_wb > 0 else hist:
        wbd = os.path.join(d, "workbench")
        for item in glob.glob(os.path.join(wbd, "*_files")) + glob.glob(os.path.join(wbd, "*.wbpj")):
            freed += dir_mb(item) if os.path.isdir(item) else os.path.getsize(item) / 1e6
            if os.path.isdir(item):
                shutil.rmtree(item, ignore_errors=True)
            else:
                try:
                    os.remove(item)
                except OSError:
                    pass
    keep_z = int(USER.get("mantener_wbpz_github", 10))       # en GitHub solo los .wbpz de los ultimos N mejores
    for d in (hist[:-keep_z] if keep_z > 0 else []):
        for z in glob.glob(os.path.join(d, "workbench", "*.wbpz")):
            freed += os.path.getsize(z) / 1e6
            try:
                os.remove(z)
            except OSError:
                pass
    if freed > 0.5:
        log(f"Limpieza automatica: liberados {freed:.0f} MB (disenos antiguos ya superados)")


def write_dashboard(estado="EN MARCHA"):
    """README.md del repositorio = panel de un vistazo (lo primero que muestra GitHub)."""
    md_path = os.path.join(ROOT, "README.md") if not TEST else os.path.join(TOP, "PANEL.md")
    base = os.path.dirname(md_path)
    rel = lambda p: os.path.relpath(p, base).replace("\\", "/")
    allruns = []
    for f in FAMS:
        for r in f.runs():
            r["title"] = f.title; allruns.append(r)
    allruns.sort(key=lambda r: r["p"].get("fecha", ""))
    # hora en la que se obtuvo cada resultado (inicio de la propuesta + tiempo de calculo)
    def t_of(r):
        try:
            return datetime.datetime.fromisoformat(r["p"]["fecha"]) + datetime.timedelta(seconds=r["m"].get("total_s", 0) or 0)
        except Exception:
            return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(r["dir"], "metrics.json")))
    for r in allruns:
        r["t"] = t_of(r)
    allruns.sort(key=lambda r: r["t"])
    improvements, best = [], None              # TODAS las mejoras del mejor valido (aunque sean pequenas)
    for r in allruns:
        if category(r["m"]) == "valido" and (best is None or score(r["m"]) < best):
            best = score(r["m"]); improvements.append(r)
    col = {"vaciado": "#2c7fb8", "refuerzo": "#7b3294", "cero": "#d95f0e"}
    # grafica estatica (README): eje horizontal = HORA real
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt, matplotlib.dates as mdates
        fig, ax = plt.subplots(1, 2, figsize=(13, 4.2))
        for r in allruns:
            m = r["m"]; c = category(m); mass = m.get("mass_kg") or m.get("mass_cad_kg")
            if mass:
                ax[0].scatter(r["t"], mass, s=22, c=col.get(r["fam"], "k"), marker="o" if c == "valido" else "x", alpha=0.85)
            if m.get("vm_metric"):
                ax[1].scatter(r["t"], m["vm_metric"], s=22, c=col.get(r["fam"], "k"), marker="o" if c == "valido" else "x", alpha=0.85)
        if improvements:
            tx = [r["t"] for r in improvements] + [allruns[-1]["t"]]
            ty = [r["m"]["mass_kg"] for r in improvements] + [improvements[-1]["m"]["mass_kg"]]
            ax[0].step(tx, ty, where="post", c="k", lw=2, label="mejor valido (en el tiempo)")
        ax[0].axhline(M_ORIG, c="0.5", ls=":", label=f"original {M_ORIG:.3f} kg")
        for k, v in col.items():
            ax[0].scatter([], [], c=v, label=FAMILIES[k][1])
        ax[0].scatter([], [], c="k", marker="x", label="no cumple")
        ax[0].set_ylabel("Masa (kg)"); ax[0].legend(fontsize=7); ax[0].grid(alpha=.3)
        ax[1].axhline(SIG_OBJ, c="#d73027", ls="--", label=f"limite {SIG_OBJ:.0f} MPa"); ax[1].set_yscale("log")
        ax[1].set_ylabel("Tension von Mises (MPa)"); ax[1].legend(fontsize=7); ax[1].grid(alpha=.3, which="both")
        for a in ax:
            a.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m %H:%M")); a.set_xlabel("Hora")
            plt.setp(a.get_xticklabels(), rotation=30, ha="right")
        fig.tight_layout(); fig.savefig(os.path.join(TOP, "evolucion_global.png"), dpi=110); plt.close(fig)
    except Exception as e:
        log(f"(grafica de evolucion: {e!r})")
    # grafica INTERACTIVA (html): pasar el raton / clicar en un punto muestra hora, diseno, masa, tension...
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        figp = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                             subplot_titles=("Masa de cada diseno (kg)", "Tension de von Mises (MPa, escala log)"))
        for fk, ftitle in ((k, FAMILIES[k][1]) for k in CFG["families"]):
            for ok_, sym, lab in ((True, "circle", "cumple"), (False, "x", "no cumple")):
                rr = [r for r in allruns if r["fam"] == fk and (category(r["m"]) == "valido") == ok_ and (r["m"].get("mass_kg") or r["m"].get("mass_cad_kg"))]
                if not rr:
                    continue
                txt = [f"<b>{ftitle} - diseno {r['id']:03d}</b><br>hora: {r['t']:%d/%m %H:%M:%S}<br>masa: {(r['m'].get('mass_kg') or r['m'].get('mass_cad_kg')):.4f} kg"
                       f"<br>tension: {r['m'].get('vm_metric') or 0:.1f} MPa<br>desplazamiento: {r['m'].get('u_max') or 0:.4f} mm"
                       f"<br>resultado: {category(r['m'])}<br>motivo: {r['p']['motivo'][:90]}" for r in rr]
                figp.add_trace(go.Scatter(x=[r["t"] for r in rr], y=[r["m"].get("mass_kg") or r["m"].get("mass_cad_kg") for r in rr],
                                          mode="markers", marker=dict(symbol=sym, size=9, color=col.get(fk, "black")),
                                          name=f"{ftitle} ({lab})", text=txt, hoverinfo="text", legendgroup=fk), 1, 1)
                rs_ = [r for r in rr if r["m"].get("vm_metric")]
                figp.add_trace(go.Scatter(x=[r["t"] for r in rs_], y=[r["m"]["vm_metric"] for r in rs_], mode="markers",
                                          marker=dict(symbol=sym, size=9, color=col.get(fk, "black")), showlegend=False,
                                          text=[t for r, t in zip(rr, txt) if r["m"].get("vm_metric")], hoverinfo="text", legendgroup=fk), 2, 1)
        if improvements:
            figp.add_trace(go.Scatter(x=[r["t"] for r in improvements] + [allruns[-1]["t"]],
                                      y=[r["m"]["mass_kg"] for r in improvements] + [improvements[-1]["m"]["mass_kg"]],
                                      mode="lines", line=dict(shape="hv", color="black", width=3), name="mejor valido"), 1, 1)
        figp.add_hline(y=M_ORIG, line_dash="dot", line_color="gray", annotation_text=f"original {M_ORIG:.3f} kg", row=1, col=1)
        figp.add_hline(y=SIG_OBJ, line_dash="dash", line_color="red", annotation_text=f"limite {SIG_OBJ:.0f} MPa", row=2, col=1)
        figp.update_yaxes(type="log", row=2, col=1)
        figp.update_layout(title=f"Evolucion del optimizador (actualizado {datetime.datetime.now():%d/%m %H:%M})",
                           height=850, hovermode="closest", template="plotly_white")
        figp.write_html(os.path.join(TOP, "evolucion_interactiva.html"), include_plotlyjs="cdn")
    except Exception as e:
        log(f"(grafica interactiva: {e!r})")
    gb = global_best()        # ultimo diseno REGISTRADO (con proyecto de Workbench e historial)
    vals = [r for r in allruns if category(r["m"]) == "valido"]
    tb = min(vals, key=lambda r: score(r["m"])) if vals else None   # mejor diseno REAL (compromiso masa-seguridad)
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    L = ["# Optimizacion del soporte - panel en directo", "",
         f"> **Ultima actualizacion:** {now} &nbsp;|&nbsp; **Estado:** {estado} &nbsp;|&nbsp; carga {CFG['force']:.0f} N "
         f"&nbsp;|&nbsp; limites: {SIG_OBJ:.0f} MPa (coef. seguridad >= {CFG['sigma_y'] / SIG_OBJ:.2f} sobre sy = {CFG['sigma_y']:.0f} MPa)" + (f" y {U_LIM:.2f} mm" if U_LIM > 0 else "") + " &nbsp;|&nbsp; acero S235", "",
         "| Familia | disenos calculados | cumplen | mejor masa | estado |", "|---|---|---|---|---|"]
    for f in FAMS:
        rs = f.runs(); val = [r for r in rs if category(r["m"]) == "valido"]
        bb = min(val, key=lambda r: score(r["m"])) if val else None
        bm = f"{bb['m']['mass_kg']:.3f} kg (CS {fs(bb['m']):.2f})" if bb else "-"
        L.append(f"| {f.title} | {len(rs)} | {len(val)} | {bm} | {'terminada: ' + f.st.get('motivo_fin', '') if f.st.get('done') else 'en marcha'} |")
    L.append("")
    # ahorro de calculo y fiabilidad del modelo
    n_filt = sum(1 for r in allruns if r["m"].get("status") == "filtrado")
    n_rap = sum(1 for r in allruns if str(r["m"].get("fidelidad", "")).startswith("rapida"))
    n_dup = sum(1 for r in allruns if r["m"].get("duplicado_de"))
    fiab = [model_reliability(f.runs()) for f in FAMS]
    rel_txt = " | ".join(f"{f.title}: " + (f"error tipico {e * 100:.0f} %" if e is not None else "aun aprendiendo")
                         for f, (n_, e) in zip(FAMS, fiab))
    L += [f"**Calculos ahorrados:** {n_filt} descartados por el modelo sin ANSYS, {n_rap} descartados en la pasada rapida, "
          f"{n_dup} piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** {rel_txt}", ""]
    if tb:
        tm = tb["m"]; red = (1 - tm["mass_kg"] / M_ORIG) * 100
        L += ["## Mejor diseno actual", "",
              f"**{tm['mass_kg']:.4f} kg** ({-red:+.2f} % de masa frente al original, {M_ORIG:.3f} kg con el mismo modelo) &nbsp;|&nbsp; tension **{tm['vm_metric']:.1f} MPa** "
              f"&nbsp;|&nbsp; desplazamiento **{(tm.get('u_max') or 0):.3f} mm** &nbsp;|&nbsp; coef. seguridad **{fs(tm):.2f}** "
              f"&nbsp;|&nbsp; puntuacion **{score(tm):.4f}** &nbsp;|&nbsp; {tb['title']}, diseno {tb['id']:03d} "
              f"&nbsp;|&nbsp; calculado {tb['p'].get('fecha', '')[:16].replace('T', ' ')}"
              + (f" &nbsp;|&nbsp; **verificado con malla fina: {tm['verif_vm']:.1f} MPa**" if tm.get("verif_vm") else ""), ""]
        same = gb and gb["familia"] == tb["fam"] and gb["iter"] == tb["id"]
        if gb:
            wb = glob.glob(os.path.join(gb["carpeta"], "workbench", "*.wbpz"))
            links = []
            if wb:
                links.append(f"[Proyecto Workbench (.wbpz)]({rel(wb[0])})")
            if os.path.exists(os.path.join(gb["carpeta"], "modelo_apdl.zip")):
                links.append(f"[Modelo APDL]({rel(os.path.join(gb['carpeta'], 'modelo_apdl.zip'))})")
            if os.path.exists(os.path.join(gb["carpeta"], "geometria.step")):
                links.append(f"[Geometria STEP]({rel(os.path.join(gb['carpeta'], 'geometria.step'))})")
            if not same:
                gap = (1 - tm["mass_kg"] / gb["mass_kg"]) * 100
                L += [f"> Mejora pequena ({gap:.2f} % sobre el ultimo registrado, {gb['mass_kg']:.4f} kg): aun sin proyecto propio. "
                      f"El proyecto de Workbench y la entrada del historial se crean cuando la mejora acumulada llega al "
                      f"{100 * float(USER.get('mejora_minima_para_nuevo_mejor', 0.0001)):.2f} %. Proyectos del ultimo registrado:", ""]
            L += [" &nbsp;|&nbsp; ".join(links), ""]
        img = fig_of(tb)
        if os.path.exists(img):
            L += [f"![mejor diseno]({rel(img)})", ""]
    else:
        L += ["## Mejor diseno actual", "", "Aun ningun diseno cumple el limite.", ""]
    if os.path.exists(os.path.join(TOP, "evolucion_global.png")):
        L += ["## Evolucion en el tiempo", "", f"![evolucion]({rel(os.path.join(TOP, 'evolucion_global.png'))})", "",
              f"Grafico interactivo (hora y datos de cada punto al pasar el raton): "
              f"[evolucion_interactiva.html]({rel(os.path.join(TOP, 'evolucion_interactiva.html'))}) "
              "- descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).", "",
              f"**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico]({rel(os.path.join(TOP, 'GALERIA.md'))})** "
              f"- {len(glob.glob(os.path.join(GAL, '*.jpg')))} fichas.", "",
              f"## Arbol genealogico de la busqueda", "",
              (f"![arbol]({rel(os.path.join(TOP, 'arbol.png'))})" if os.path.exists(os.path.join(TOP, "arbol.png")) else ""), "",
              f"Detalle de cada rama: [ARBOL.md]({rel(os.path.join(TOP, 'ARBOL.md'))})", ""]
    if improvements:
        # historial = TODAS las mejoras (cada vez que aparece un diseno valido mas ligero); las que superaron
        # el umbral tienen ademas proyecto de Workbench en historial/
        reg = {}
        for d in glob.glob(os.path.join(TOP, "historial", "[0-9][0-9]_*")):
            parts = os.path.basename(d).split("_")       # NN_familia_iter_masa
            try:
                wbz = glob.glob(os.path.join(d, "workbench", "*.wbpz"))
                reg[(parts[1], int(parts[2]))] = rel(wbz[0]) if wbz else None
            except (IndexError, ValueError):
                pass
        L += ["## Historial de mejoras (todas; la mas reciente arriba)", "",
              "| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |",
              "|---|---|---|---|---|---|---|---|---|"]
        rows_imp, prev = [], None
        for n, r in enumerate(improvements, 1):
            gain = "-" if prev is None else f"-{(1 - score(r['m']) / prev) * 100:.2f} % (punt.)"
            img = fig_of(r)
            key = (r["fam"], r["id"])
            proj = f"[Workbench]({reg[key]})" if reg.get(key) else ("registrado" if key in reg else "-")
            rows_imp.append(f"| {n} | {r['t']:%d/%m %H:%M} | {r['m']['mass_kg']:.4f} kg | {gain} | {r['m']['vm_metric']:.1f} MPa | "
                            f"{(r['m'].get('u_max') or 0):.3f} mm | {r['title']} {r['id']:03d} | {proj} | "
                            + (f"<img src=\"{rel(img)}\" width=\"320\">" if os.path.exists(img) else "-") + " |")
            prev = score(r["m"])
        L += rows_imp[::-1][:60] + [""]
    L += ["## Ultimos disenos calculados", "", "| familia | # | masa | tension | resultado | motivo | ficha |", "|---|---|---|---|---|---|---|"]
    for r in allruns[-10:][::-1]:
        m = r["m"]; img = fig_of(r)
        ten = f"{m['vm_metric']:.1f}" if m.get("vm_metric") else "-"
        L.append(f"| {r['title']} | {r['id']:03d} | {(m.get('mass_kg') or m.get('mass_cad_kg') or 0):.3f} | {ten} | {category(m)} | "
                 f"{r['p']['motivo'][:70]} | " + (f"[ver]({rel(img)})" if os.path.exists(img) else "-") + " |")
    L += ["", "---", "", "**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). "
          "Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del "
          "mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL "
          "(SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.", "",
          "**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. "
          "Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`."]
    open(md_path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def make_video():
    frames = sorted(glob.glob(os.path.join(TOP, "timelapse", "frame_*.png")))
    if len(frames) < 2:
        return
    import imageio.v2 as imageio
    with imageio.get_writer(os.path.join(TOP, "timelapse", "evolucion.mp4"), fps=2, macro_block_size=8) as w:
        for f in frames:
            img = imageio.imread(f)
            for _ in range(2):
                w.append_data(img)
        for _ in range(6):
            w.append_data(img)


# ============================================================================ bucle principal
def acquire_lock():
    lk = os.path.join(TOP, "EN_EJECUCION.lock")
    if os.path.exists(lk):
        try:
            pid = int(open(lk).read().split()[0])
            r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
            if str(pid) in r.stdout and "python" in r.stdout.lower():
                print(f"\nYa hay un optimizador en marcha (PID {pid}). Esta ventana se cierra.")
                time.sleep(8); sys.exit(2)
        except (ValueError, OSError):
            pass
    open(lk, "w").write(f"{os.getpid()} {datetime.datetime.now().isoformat()}")
    return lk


def model_reliability(runs, last=15):
    """Error tipico del modelo de tension en los ultimos disenos calculados (prediccion frente a ANSYS)."""
    errs = []
    for r in runs[::-1]:
        pr = r["p"].get("pred") or {}
        if r["m"].get("status") == "ok" and not r["m"].get("duplicado_de") and pr.get("stress_mpa"):
            errs.append(abs(math.log(pr["stress_mpa"] / r["m"]["vm_metric"])))
            if len(errs) >= last:
                break
    return (len(errs), float(np.median(errs)) if errs else None)


def model_filter(fam, runs, prop):
    """Devuelve el motivo si el disenyo NO merece calcularse (modelo fiable + casi seguro que no cumple)."""
    pr = prop.get("pred") or {}
    if not pr or pr.get("modo") != "mejorar masa":
        return None
    p_min = float(USER.get("filtro_prob_minima", 0.05))
    n, err = model_reliability(runs)
    if n < 8 or err is None or err > float(USER.get("filtro_error_max", 0.10)):
        return None                                   # modelo aun no fiable: se calcula todo
    if pr.get("p_cumple", 1.0) >= p_min:
        return None
    if fam.rng.random() < 0.10:                       # control de calidad: 1 de cada 10 se calcula igualmente
        prop["motivo"] += " [control de calidad del filtro: se calcula aunque el modelo lo descartaria]"
        return None
    return (f"el modelo (error tipico {err * 100:.0f} %) predice {pr['stress_mpa']:.0f} MPa y "
            f"P(cumplir) = {pr['p_cumple']:.3f} < {p_min}")


def find_duplicate(fam, params, runs):
    """Construye la geometria (unos segundos) y la compara con todas las calculadas: si el volumen coincide
    (< 0,5 mm3) la pieza es la misma y se reutiliza su resultado."""
    try:
        _, info = fam.mod.build(params)
    except Exception:
        return None                       # que evaluate() registre el fallo de geometria como siempre
    v = info["volume_mm3"]
    for r in runs:
        if r["m"].get("status") == "ok" and r["m"].get("volume_cad_mm3") is not None and not r["m"].get("duplicado_de") \
                and abs(r["m"]["volume_cad_mm3"] - v) < 0.5:
            return r
    return None


DISCORD = None        # avisos a Discord (se crea en main; si no hay enlaces no hace nada)
REPO_URL = None


def _repo_url():
    try:
        g = find_git()
        u = subprocess.run([g, "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
        return u[:-4] if u.endswith(".git") else u
    except Exception:
        return None


def _gal_path(r):
    g = r["m"].get("galeria")
    p = os.path.join(TOP, g) if g else None
    return p if p and os.path.exists(p) else None


def notify_design(fam, r, cat):
    """Canal 'todo': ficha de cada diseno calculado (validos, no validos, fallidos y filtrados)."""
    m, p = r["m"], r["p"]
    verd = {"valido": "VALIDO", "cerca_del_limite": "casi (hasta +10 %)", "descartado": "no valido",
            "fallido": "FALLO", "filtrado": "filtrado por el modelo (sin ANSYS)"}[cat]
    mass = m.get("mass_kg") or m.get("mass_cad_kg")
    fields = [dict(name="Resultado", value=verd, inline=True),
              dict(name="Masa", value=f"{mass:.3f} kg" if mass else "-", inline=True),
              dict(name="Tension", value=f"{m['vm_metric']:.1f} MPa" if m.get("vm_metric") else "-", inline=True),
              dict(name="Desplazamiento", value=f"{m['u_max']:.3f} mm" if m.get("u_max") else "-", inline=True),
              dict(name="Rama", value=str(p.get("rama") or "-"), inline=True)]
    desc = p.get("motivo", "")
    if m.get("error"):
        desc += f"\n**Motivo del descarte / fallo:** {m['error'][:300]}"
    DISCORD.design(f"{fam.title} - diseno {r['id']:03d}", cat, fields, desc, _gal_path(r))


def _tree_signature():
    sig = []
    for f in FAMS:
        for bid, b in sorted(f.st.get("ramas", {}).items()):
            sig.append([f.key, bid, b["estado"], (b.get("best") or {}).get("id")])
    return sig


def notify_tree():
    """Canal 'arbol': imagen nueva solo cuando cambia la estructura del arbol o el mejor de alguna rama."""
    path = os.path.join(TOP, "discord_arbol_firma.json")
    sig = _tree_signature()
    old = json.load(open(path)) if os.path.exists(path) else None
    png = os.path.join(TOP, "arbol.png")
    if sig == old or not os.path.exists(png):
        return
    atomic_json(path, sig)
    lines = []
    for f in FAMS:
        R = f.st.get("ramas", {})
        if R:
            act = sum(1 for b in R.values() if b["estado"] == "activa")
            lines.append(f"**{f.title}**: {len(R)} ramas ({act} activas)")
    shot = os.path.join(TOP, "discord_arbol.png")
    shutil.copy(png, shot)            # copia: el original se reescribe en cada diseno
    DISCORD.tree(shot, "\n".join(lines) or "-")


def notify_top(force=False):
    """Canal 'top': UN mensaje con el mejor diseno, que se edita al mejorar (y cada 15 disenos como senal de vida)."""
    path = os.path.join(TOP, "discord_top.json")
    st = json.load(open(path)) if os.path.exists(path) else {}
    allr = [r for f in FAMS for r in f.runs()]
    vals = [r for r in allr if category(r["m"]) == "valido"]
    n_tot = len(allr)
    tb = min(vals, key=lambda r: score(r["m"])) if vals else None
    key = [tb["fam"], tb["id"]] if tb else None
    if not force and key == st.get("key") and n_tot - st.get("n", 0) < 15:
        return
    atomic_json(path, dict(key=key, n=n_tot))
    stamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    footer = (f"Actualizado {stamp} | {n_tot} disenos calculados, {len(vals)} validos | carga {CFG['force']:.0f} N | "
              f"limites {SIG_OBJ:.0f} MPa y {U_LIM:.2f} mm")
    if tb is None:
        DISCORD.top("Mejor diseno actual: aun ninguno cumple", [dict(name="Estado", value="buscando el primer diseno valido")],
                     None, footer, REPO_URL)
        return
    m = tb["m"]; red = (1 - m["mass_kg"] / M_ORIG) * 100
    fam_t = FAMILIES[tb["fam"]][1]
    fiab = model_reliability([r for r in allr if r["fam"] == tb["fam"]])
    fields = [dict(name="Masa", value=f"**{m['mass_kg']:.4f} kg** ({-red:+.2f} % frente al original {M_ORIG:.3f} kg)", inline=False),
              dict(name="Tension", value=f"{m['vm_metric']:.1f} / {SIG_OBJ:.0f} MPa", inline=True),
              dict(name="Desplazamiento", value=f"{m['u_max']:.3f} / {U_LIM:.2f} mm", inline=True),
              dict(name="Coef. seguridad", value=f"{fs(m):.2f} (minimo {CFG['sigma_y'] / SIG_OBJ:.2f})", inline=True),
              dict(name="Puntuacion (masa x aprovechamiento^p)", value=f"{score(m):.4f} (p = {SCORE_P:g})", inline=True),
              dict(name="Origen", value=f"{fam_t}, rama {tb['p'].get('rama')}, diseno {tb['id']:03d}", inline=False),
              dict(name="Encontrado", value=tb["p"].get("fecha", "")[:16].replace("T", " "), inline=True),
              dict(name="Fiabilidad del modelo", value=(f"error tipico {fiab[1] * 100:.0f} %" if fiab[1] is not None else "aprendiendo"), inline=True)]
    if m.get("verif_vm"):
        fields.append(dict(name="Verificacion (malla fina)", value=f"{m['verif_vm']:.1f} MPa, {m['verif_u']:.3f} mm - confirmado", inline=False))
    gb = global_best()
    if gb and REPO_URL:
        wb = glob.glob(os.path.join(gb["carpeta"], "workbench", "*.wbpz"))
        if wb:
            relp = os.path.relpath(wb[0], ROOT).replace("\\", "/")
            fields.append(dict(name="Proyecto Workbench", value=f"[descargar .wbpz]({REPO_URL}/blob/main/{relp})", inline=False))
    DISCORD.top("Mejor diseno actual", fields, _gal_path(tb), footer, REPO_URL)


def disk_guard():
    """Si queda poco disco: limpieza inmediata; si queda muy poco, pausa hasta que haya sitio."""
    free = shutil.disk_usage(ROOT).free / 1e9
    if free < float(USER.get("disco_minimo_gb", 5.0)):
        log(f"Poco espacio en disco ({free:.1f} GB): limpieza inmediata")
        try:
            cleanup()
        except Exception as e:
            log(f"(limpieza: {e!r})")
        free = shutil.disk_usage(ROOT).free / 1e9
        warned = False
        while free < 1.0:
            if not warned:
                DISCORD.alert(f"El disco esta casi lleno ({free:.1f} GB libres). El optimizador esta en PAUSA hasta que haya "
                              "al menos 1 GB libre; despues continua solo.")
                warned = True
            log(f"  disco casi lleno ({free:.2f} GB): en pausa, se vuelve a comprobar en 10 min")
            time.sleep(600)
            free = shutil.disk_usage(ROOT).free / 1e9


def verify_fine(fam, r):
    """Recalcula un candidato a nuevo mejor con malla fina (h = 3,5 mm). Si ahi no cumple, no se acepta."""
    from evaluate import evaluate
    m = r["m"]; vd = os.path.join(r["dir"], "verificacion")
    log(f"  candidato a NUEVO MEJOR: verificacion con malla fina...")
    try:
        mv = evaluate(r["p"]["params"], vd, force=CFG["force"], geom=fam.mod, log=LOG, images=False,
                      h=float(USER.get("verificacion_h_mm", 3.5)), hmin=1.0)
    except Exception as e:
        mv = dict(status="error", error=repr(e))
    if mv.get("status") == "ok":
        m.update(verif_vm=mv["vm_metric"], verif_u=mv["u_max"], verif_nodes=mv.get("n_nodes"),
                 verif_ok=violation(mv) <= 1.0)
        log(f"  verificacion (malla fina, {mv.get('n_nodes')} nodos): {mv['vm_metric']:.1f} MPa, {mv['u_max']:.3f} mm -> "
            + ("CONFIRMADO" if m["verif_ok"] else "NO se confirma: no se acepta como nuevo mejor"))
    else:
        m.update(verif_ok=None, verif_error=str(mv.get("error"))[:200])
        log(f"  verificacion no disponible ({str(mv.get('error'))[:80]}): se acepta con la malla normal")
    for f in glob.glob(os.path.join(vd, "*")):
        if not f.endswith(("metrics.json", "params.json")):
            try:
                os.remove(f)
            except OSError:
                pass
    atomic_json(os.path.join(r["dir"], "metrics.json"), m)


def step(fam, git, t_session):
    from evaluate import evaluate
    try:
        retry_pending_workbench(git)
    except Exception as e:
        log(f"(pendientes Workbench: {e!r})")
    disk_guard()
    runs = fam.runs()
    n = max([r["id"] for r in runs], default=0)
    fails = 0
    for r in reversed(runs):
        if r["m"].get("status") == "ok":
            break
        fails += 1
    if fam.st.get("done"):
        return False
    if len(runs) >= CFG["budget"] and not fam.pending:
        fam.st["done"] = True; fam.st["motivo_fin"] = f"presupuesto de {CFG['budget']} disenos agotado"; fam.save_state(); return False
    if fails >= CFG["max_fail_streak"]:
        fam.st["done"] = True; fam.st["motivo_fin"] = f"{fails} fallos seguidos (revisar optimizador.log)"; fam.save_state(); return False
    if fam.pending:
        iid, prop = fam.pending.pop(0)
    else:
        iid = n + 1
        try:
            x, why, pred, fase, rama = fam.propose(runs)
        except Exception as e:
            log(f"[{fam.key}] aviso: el modelo sustituto fallo ({e!r}); se prueba un punto aleatorio")
            x, why, pred, fase = fam.rng.random(fam.D), "aleatorio (respaldo)", None, "respaldo"
            rama = (fam.current() or {}).get("id")
        prop = dict(params=fam.to_params(x), motivo=why, pred=pred, fase=fase, familia=fam.key, rama=rama,
                    fecha=datetime.datetime.now().isoformat())
    wd = os.path.join(fam.out, f"{iid:03d}"); os.makedirs(wd, exist_ok=True)
    atomic_json(os.path.join(wd, "proposal.json"), prop)
    gb = global_best()
    print("\n" + "=" * 86)
    log(f"[{fam.title}] DISENO {iid:03d}  |  mejor global: "
        + (f"{gb['mass_kg']:.3f} kg ({gb['titulo']} #{gb['iter']:03d})" if gb else "aun ninguno valido"))
    log(f"  motivo: {prop['motivo']}")
    if prop.get("pred"):
        pr = prop["pred"]
        log(f"  el modelo predice: masa {pr['mass_kg']:.3f} kg | tension {pr['stress_mpa']:.0f} MPa | P(cumplir) {pr['p_cumple']:.2f}")
    filt = model_filter(fam, runs, prop)
    dup = None if filt else find_duplicate(fam, prop["params"], runs)
    if filt:
        m = dict(status="filtrado", params=prop["params"], mass_kg=None, mass_cad_kg=prop["pred"]["mass_kg"],
                 pred_vm=prop["pred"]["stress_mpa"], error=filt, total_s=0.0)
        json.dump(prop["params"], open(os.path.join(wd, "params.json"), "w"), indent=1)
        atomic_json(os.path.join(wd, "metrics.json"), m)
        log(f"  FILTRADO sin ANSYS: {filt}")
    elif dup is not None:
        # geometria IDENTICA a un diseno ya calculado: mismo resultado, sin gastar ANSYS
        m = {k: v for k, v in dup["m"].items() if k not in ("traceback",)}
        m.update(params=prop["params"], duplicado_de=dup["id"], total_s=0.0)
        json.dump(prop["params"], open(os.path.join(wd, "params.json"), "w"), indent=1)
        atomic_json(os.path.join(wd, "metrics.json"), m)
        for f in ("resumen.png", "vonmises.png", "geometria.png"):
            if os.path.exists(os.path.join(dup["dir"], f)):
                shutil.copy(os.path.join(dup["dir"], f), os.path.join(wd, f))
        log(f"  geometria IDENTICA al diseno {dup['id']:03d} (estos cambios no tocan la pieza): se reutiliza su resultado sin ANSYS")
    else:
        m = evaluate(prop["params"], wd, force=CFG["force"], geom=fam.mod, log=LOG,
                     prescreen=(float(USER.get("cribado_rapido", 1.5)) or None)
                     if fam.key in USER.get("cribado_rapido_familias", ["cero"]) else None)
    r = dict(id=iid, dir=wd, m=m, p=prop, fam=fam.key)
    cat = category(m)
    min_gain = float(USER.get("mejora_minima_para_nuevo_mejor", 0.0001))
    if cat == "valido" and not m.get("duplicado_de") and USER.get("verificar_mejores", True) \
            and (gb is None or score(m) < gb_score(gb) * (1 - min_gain)):
        verify_fine(fam, r)          # candidato a nuevo mejor: se recalcula con malla fina antes de aceptarlo
        cat = category(m)
    try:
        add_to_gallery(fam, r)      # ficha con fecha en la galeria (validos y no validos)
        write_gallery_md()
    except Exception as e:
        log(f"(galeria: {e!r})")
    try:
        notify_design(fam, r, cat)  # Discord: canal de todo lo generado
    except Exception as e:
        log(f"(Discord: {e!r})")
    append_registro(fam, r)
    if cat in ("valido", "cerca_del_limite"):
        package_apdl(wd)
    if os.path.exists(os.path.join(wd, "model.inp")):
        os.remove(os.path.join(wd, "model.inp"))
    runs = fam.runs()
    fam.update_branch(runs, r)
    try:
        stg = fam.check_stagnation(runs)
    except Exception as e:
        stg = None; log(f"(anti-estancamiento: {e!r})")
    if stg:
        new, cerradas = stg
        txt = (f"[{fam.key}] ESTANCADA: {USER.get('estancamiento_disenos', 25)} disenos sin mejorar ni un 0,3 % -> "
               f"nuevas ramas exploradoras {', '.join(new)}" + (f"; se cierran las ramas finas {', '.join(cerradas)}" if cerradas else ""))
        log("  " + txt)
        DISCORD.alert(txt)
    try:
        write_tree()
        notify_tree()               # Discord: imagen del arbol si ha cambiado
    except Exception as e:
        log(f"(arbol: {e!r})")
    write_clasificacion(fam, runs)
    if m.get("status") == "ok":
        verdict = {"valido": "CUMPLE", "cerca_del_limite": "casi (hasta +10 %)", "descartado": "NO cumple"}[cat]
        log(f"  RESULTADO: masa {m['mass_kg']:.3f} kg | tension {m['vm_metric']:.1f} MPa (bruta {m['vm_max_raw']:.0f}) | {verdict}")
    else:
        log(f"  RESULTADO: FALLO ({m.get('status')}): {(m.get('error') or '')[:100]} -> se penaliza y se sigue")
    # nuevo mejor = cumple (tambien con malla fina) y pesa menos que el anterior -> proyecto Workbench + historial + GitHub
    is_best = cat == "valido" and (gb is None or score(m) < gb_score(gb) * (1 - min_gain))
    if is_best:
        register_new_best(fam, r, git)       # Workbench + historial + timelapse (solo en mejoras)
    try:
        write_dashboard()
    except Exception as e:
        log(f"(panel: {e!r})")
    try:
        notify_top()                # Discord: mensaje del mejor diseno (se edita)
    except Exception as e:
        log(f"(Discord: {e!r})")
    if is_best:
        gb2 = global_best()
        git.push(f"NUEVO MEJOR DISENO: {gb2['mass_kg']:.3f} kg, {gb2['vm_metric']:.0f} MPa ({fam.title} {iid:03d})")
    else:
        git.push(f"[{fam.key}] diseno {iid:03d}: {cat}")
    return True


def geometry_version():
    return {k: importlib.import_module(FAMILIES[k][0]).VERSION for k in CFG["families"]}


def archive_if_outdated():
    """POR FAMILIA: si los resultados guardados de una familia son de una version anterior de SU geometria, se archiva
    solo esa familia (no se borra nada). Las demas familias, el historial y el mejor global se conservan.
    Anadir una familia nueva no archiva nada."""
    vpath = os.path.join(TOP, "version_geometria.json")
    now = geometry_version()
    os.makedirs(TOP, exist_ok=True)
    old = json.load(open(vpath, encoding="utf-8")) if os.path.exists(vpath) else {}
    stamp = datetime.datetime.now()
    for k, v in now.items():
        d = os.path.join(TOP, k)
        if os.path.isdir(d) and os.listdir(d) and old.get(k) != v:
            dest = os.path.join(ROOT, "runs", "archivo", f"{os.path.basename(TOP)}_{k}_{stamp:%Y%m%d_%H%M%S}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(d, dest)
            print(f"La geometria de la familia '{k}' ha cambiado ({old.get(k)} -> {v}).\n"
                  f"Sus resultados anteriores se han archivado en {dest}; esa familia empieza de nuevo.", flush=True)
    merged = dict(old); merged.update(now)
    atomic_json(vpath, merged)


def main():
    os.makedirs(TOP, exist_ok=True)
    acquire_lock()                 # 1) si ya hay otro optimizador en marcha, esta ventana se cierra aqui
    try:
        os.remove(os.path.join(TOP, "EN_EJECUCION.lock"))
        archive_if_outdated()      # 2) archiva resultados de una geometria anterior (si los hay)
    except Exception as e:
        print(f"\nNo se pudieron archivar los resultados antiguos ({e}).\n"
              "Cierra Workbench y cualquier archivo abierto de la carpeta runs y vuelve a lanzar optimizar.bat.")
        time.sleep(30); sys.exit(3)
    lock = acquire_lock()          # 3) bloqueo definitivo
    git = GitSync(CFG["git"])
    print("=" * 86)
    print("  OPTIMIZADOR AUTOMATICO DEL SOPORTE  -  acero S235, carga %.0f N" % CFG["force"])
    print(f"  minimizar masa | tension <= {SIG_OBJ:.0f} MPa | familias: {', '.join(CFG['families'])}")
    print("  Se puede cerrar esta ventana en cualquier momento: al volver a abrirla continua donde iba.")
    print("=" * 86)
    global DISCORD, REPO_URL
    import discord_notify
    DISCORD = discord_notify.make(ROOT, TOP, log, test=TEST)
    REPO_URL = _repo_url()
    if DISCORD.enabled:
        log("Discord: avisos activados (canales: mejor diseno, arbol y todo lo generado)")
    fams = [Family(k) for k in CFG["families"]]
    FAMS[:] = fams
    retiradas = USER.get("familias_retiradas", {}) or {}
    for f in fams:                 # familias retiradas: se conservan (panel, galeria, historial) pero ya no se calculan
        if f.key in retiradas and not f.st.get("retirada"):
            f.st.update(done=True, retirada=True, motivo_fin=f"retirada: {retiradas[f.key]}"); f.save_state()
            log(f"[{f.title}] retirada ({retiradas[f.key]}); sus resultados se conservan")
        elif f.key not in retiradas and f.st.get("retirada"):
            f.st.update(done=False, retirada=False, motivo_fin=""); f.save_state()
            log(f"[{f.title}] vuelve a estar activa")
    turnos = USER.get("turnos_por_ronda", {}) or {}
    crash_streak = 0
    t0 = time.time()
    final_state = "DETENIDO (al relanzar optimizar.bat continua)"
    try:
        while True:
            active = [f for f in fams if not f.st.get("done")]
            if not active:
                break
            rnd = getattr(main, "_round", 0) + 1; main._round = rnd
            sched = [f for f in active for _ in range(max(1, int(turnos.get(f.key, 1))))]
            for f in sched:
                if f.st.get("done"):
                    continue
                rs_f = f.runs()
                # reparto del tiempo: una familia sin NINGUN diseno valido tras 30 intentos (y fuera de su reparto
                # inicial) solo juega 1 de cada 3 rondas
                if len(active) > 1 and len(rs_f) >= max(30, f.n_init) and not any(category(r["m"]) == "valido" for r in rs_f) \
                        and rnd % 3:
                    continue
                try:
                    alive = step(f, git, t0)
                    crash_streak = 0
                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    # error inesperado: se registra, se avisa y se sigue (el diseno a medias se repetira)
                    crash_streak += 1
                    tbk = traceback.format_exc()
                    log(f"ERROR INESPERADO ({crash_streak} seguidos) en {f.title}: {e!r}")
                    with open(os.path.join(TOP, "errores.log"), "a", encoding="utf-8") as fe:
                        fe.write(f"\n[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}] {f.key}\n{tbk}")
                    DISCORD.alert(f"Error inesperado en {f.title} ({crash_streak} seguidos): `{e!r}`"[:1500]
                                  + "\nEl optimizador sigue; detalle en errores.log.")
                    if crash_streak >= 5:
                        DISCORD.alert("5 errores inesperados seguidos: el optimizador se detiene. optimizar.bat lo reiniciara en 1 minuto.")
                        raise
                    time.sleep(30)
                    continue
                if not alive:
                    log(f"[{f.title}] TERMINADA: {f.st.get('motivo_fin')}")
                    DISCORD.alert(f"La familia **{f.title}** ha terminado: {f.st.get('motivo_fin')}.")
                n_steps = sum(len(ff.runs()) for ff in fams)
                if n_steps % int(USER.get("limpieza_cada_n_disenos", 10)) == 0:
                    try:
                        cleanup()
                    except Exception as e:
                        log(f"(limpieza: {e!r})")
        log("TODAS LAS FAMILIAS HAN TERMINADO.")
        final_state = "TERMINADO"
        DISCORD.alert("**Optimizacion terminada.** El mensaje del canal del mejor diseno tiene el resultado final.")
    except KeyboardInterrupt:
        log("Detenido por el usuario. Progreso guardado: al relanzar continua donde iba.")
    finally:
        try:
            for f in fams:
                write_clasificacion(f, f.runs())
            make_video()
            import report
            for f in fams:
                report.make(f)
        except Exception as e:
            log(f"(informe final incompleto: {e!r})")
        try:
            write_dashboard(final_state)
        except Exception as e:
            log(f"(panel: {e!r})")
        git.push("checkpoint / estado final", wait=True)
        try:
            notify_top(force=True)
            DISCORD.flush(90)
        except Exception:
            pass
        try:
            os.remove(lock)
        except OSError:
            pass


if __name__ == "__main__":
    main()
