"""OPTIMIZADOR GUIADO POR REGLAS - MSD 2026-27 (831_MSD_13_B, Soporte 6, acero S235)

  Objetivo:     la pieza mas ligera (compromiso masa-seguridad entre las validas)
  Obligatorio:  coeficiente de seguridad >= 1 (von Mises <= 215 MPa fuera de la singularidad de los pernos)
                y desplazamiento <= 0,25 mm
  Fijo:         los 4 agujeros de los pernos y los 2 del bulon (se verifican en cada pieza)

COMO FUNCIONA (version corta para la defensa)
  0. ESTUDIO (una vez): las 381 soluciones publicadas (SimJEB) se calculan con NUESTRA carga y NUESTRO limite y de
     ellas, y de nuestros calculos anteriores, se sacan REGLAS DE DISENO con datos (DESIGN_RULES.md).
  1. Se parte SIEMPRE de la pieza del enunciado (0.stp), calculada en ANSYS.
  2. Cada ITERACION:
       a) mapa de tensiones de la pieza actual: que material trabaja, cual esta ocioso y donde esta el pico;
       b) las reglas proponen hasta 3 modificaciones (anadir donde esta el pico, quitar donde no trabaja, o crear
          FORMAS NUEVAS: nervios en la direccion principal de tension dimensionados con la carga que llevan, Michell),
          cada una con su PORQUE y lo que se espera;
       c) EVALUACION RAPIDA (malla gruesa) de cada una, comparada con la pieza actual en la MISMA malla: las que no
          van a mejorar se descartan ahi;
       d) la mas prometedora pasa a la EVALUACION COMPLETA (malla de 4 mm validada);
       e) se ACEPTA si cumple y mejora (o si acerca al limite una pieza que aun no cumple); si no, se REVIERTE y
          se registra el motivo (la regla aprende: cerca de un corte rechazado solo se proponen cortes menores).
  3. Para cuando ninguna regla consigue mejorar la pieza. Verificacion final con malla fina y proyecto Workbench.
  Trazabilidad: ITERACIONES.md (cada cambio con su porque y su antes/despues), un commit por iteracion en GitHub y un
  mensaje por iteracion en Discord.

ROBUSTEZ: guarda tras cada iteracion; si se apaga el PC continua donde iba.
"""
import os, sys, json, time, math, csv, shutil, zipfile, subprocess, threading, datetime, traceback, glob
import warnings
warnings.filterwarnings("ignore")
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fem

ROOT = fem.ROOT
USER = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
TEST = "--prueba" in sys.argv          # prueba corta en carpeta aparte (sin GitHub ni Discord)
FORCE = float(USER.get("carga_N", 42258.0))
SY = float(USER.get("sigma_y_MPa", 215.0))
SIG_OBJ = SY * float(USER.get("margen_optimizacion", 1.0))
U_LIM = float(USER.get("desplazamiento_max_mm", 0.25))
SCORE_P = float(USER.get("peso_seguridad", 0.15))
N_CAND = int(USER.get("candidatos_por_iteracion", 3))
TOL_Q = float(USER.get("descarte_rapido_tolerancia", 0.03))
MAX_SIN_MEJORA = int(USER.get("max_iteraciones_sin_mejora", 8))
MAX_INV = int(USER.get("max_inversiones_seguidas", 2))
M_ORIG = 2.4234            # masa del original con el MISMO modelo de EF (malla de 4 mm); la del CAD es 2,4115 kg
TOP = os.path.join(ROOT, "runs", ("prueba_" if TEST else "opt_") + f"{int(round(FORCE))}N")
LOG = os.path.join(TOP, "optimizador.log")
STATE = os.path.join(TOP, "estado.json")
ITD = os.path.join(TOP, "iteraciones")
GAL = os.path.join(TOP, "galeria")
PIEZA_STEP = os.path.join(TOP, "pieza_actual.step")
REG_COLS = ["iteracion", "fecha", "candidato", "regla", "modificacion", "fase", "masa_kg", "tension_MPa", "desp_mm", "coef_seguridad",
            "puntuacion", "decision", "motivo", "porque", "tiempo_s"]


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


K_FINO = [1.0, 1.0]     # calibracion malla normal -> malla fina (tension, desplazamiento); se actualiza en cada verificacion


def k_fino(st):
    """Cociente malla fina / malla normal medido en las ultimas verificaciones (mediana de las 3 ultimas, >= 1).
    La malla de 4 mm da el pico algo mas bajo que la fina: para aceptar una pieza se exige que cumpla CORREGIDA."""
    ks = st.get("k_fino", [])[-3:]
    if not ks:
        return [1.0, 1.0]
    return [max(1.0, float(np.median([k[0] for k in ks]))), max(1.0, float(np.median([k[1] for k in ks])))]


def violation(m):
    """max(tension / limite, desplazamiento / limite), con la correccion a malla fina: > 1 = no cumple."""
    v = m["vm_metric"] * K_FINO[0] / SIG_OBJ
    if U_LIM > 0 and m.get("u_max") is not None:
        v = max(v, m["u_max"] * K_FINO[1] / U_LIM)
    return v


def valid(m):
    return m.get("status", "ok") == "ok" and m.get("vm_metric") is not None and violation(m) <= 1.0


def score(m):
    """masa x aprovechamiento^p (menor = mejor)."""
    return m["mass_kg"] * max(violation(m), 1e-6) ** SCORE_P


def fs(m):
    return SY / max(m["vm_metric"], 1e-6)


def summ(m):
    """Resumen de una evaluacion (lo que se guarda en el estado)."""
    out = {k: m.get(k) for k in ("mass_kg", "vm_metric", "u_max", "vm_metric_xyz", "n_nodes")}
    if m.get("vm_metric") is not None:
        out.update(cs=fs(m), viol=violation(m), score=score(m), valido=valid(m))
    return out


def txt_m(s):
    return f"{s['mass_kg']:.4f} kg | {s['vm_metric']:.1f} MPa | CS {s['cs']:.2f} | {s['u_max']:.3f} mm"


# ============================================================================ GitHub
def find_git():
    cands = [shutil.which("git"), r"C:\Program Files\Git\cmd\git.exe", r"C:\Program Files (x86)\Git\cmd\git.exe",
             os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe")]
    cands += glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\GitHubDesktop\app-*\resources\app\git\cmd\git.exe"))
    for c in cands:
        if c and os.path.exists(c):
            return c
    return None


class GitSync:
    """Un COMMIT por iteracion (con su mensaje descriptivo, en el momento) y la subida (push) en segundo plano."""
    def __init__(self, enabled):
        self.git = find_git()
        self.enabled = enabled and os.path.isdir(os.path.join(ROOT, ".git")) and self.git is not None
        if enabled and self.git is None:
            log("AVISO: no se encuentra git.exe -> no se subira nada a GitHub (el optimizador sigue igual)")
        self.th = None
        self.lock = threading.Lock()

    def _g(self, *a, t=300):
        return subprocess.run([self.git, *a], cwd=ROOT, capture_output=True, text=True, timeout=t,
                              creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def commit(self, title, body="", push=True, wait=False):
        if not self.enabled:
            return
        try:
            with self.lock:
                self._g("add", "-A")
                args = ["commit", "-q", "-m", title[:200]]
                if body:
                    args += ["-m", body[:6000]]
                self._g(*args)
        except Exception as e:
            log(f"  (GitHub: commit no hecho: {e!r})")
            return
        if push and not (self.th and self.th.is_alive()):
            self.th = threading.Thread(target=self._push, daemon=True)
            self.th.start()
        if wait and self.th:
            self.th.join(600)

    def _push(self):
        try:
            with self.lock:
                r = self._g("push", "-q", "origin", "HEAD", t=600)
            log("  (GitHub: subido)" if r.returncode == 0 else f"  (GitHub: subida pendiente: {r.stderr.strip()[:100]})")
        except Exception as e:
            log(f"  (GitHub: {e!r}; se reintentara)")


# ============================================================================ estado
def new_state():
    return dict(iter=0, actual=None, mejor=None, verificado=None, tau_idx=0, rechazos=[], stats={}, sin_mejora=0,
                inversiones=0, inversion_desde=None, wb_masa=None, fin=False, motivo_fin="", historia=[],
                creado=datetime.datetime.now().isoformat(timespec="seconds"))


def load_state():
    return json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else new_state()


def save_state(st):
    atomic_json(STATE, st)


def rule_stats(st, rid):
    return st["stats"].setdefault(rid, dict(intentos=0, descartadas_rapido=0, evaluadas=0, aceptadas=0, rechazadas=0,
                                            dsig=[], dm=[], ejemplos=[]))


# ============================================================================ geometria actual
class Current:
    """La pieza actual en memoria (para aplicar la siguiente operacion sin reconstruir todo)."""
    solid = None
    key = None


def ops_key(ops):
    return json.dumps(ops, sort_keys=True)


def current_solid(ops):
    import operaciones as O
    import cadquery as cq
    k = ops_key(ops)
    if Current.key == k and Current.solid is not None:
        return Current.solid
    side = PIEZA_STEP + ".json"
    if os.path.exists(PIEZA_STEP) and os.path.exists(side) and open(side, encoding="utf-8").read() == k:
        s = cq.importers.importStep(PIEZA_STEP).val()
        s = sorted(s.Solids(), key=lambda q: q.Volume(), reverse=True)[0]
    else:
        log(f"  reconstruyendo la pieza actual desde el 0.stp ({len(ops)} operaciones)...")
        s, _ = O.build(ops)
    set_current(s, ops)
    return s


def set_current(solid, ops):
    import geometry as G
    Current.solid, Current.key = solid, ops_key(ops)
    try:
        G.export(solid, PIEZA_STEP)
        open(PIEZA_STEP + ".json", "w", encoding="utf-8").write(Current.key)
    except Exception as e:
        log(f"  (no se pudo guardar pieza_actual.step: {e})")


def build_candidate(cand, ops_cur):
    import operaciones as O
    new_ops = cand["ops_nuevas"]
    if cand.get("reconstruir") or new_ops[: len(ops_cur)] != ops_cur:
        return O.build(new_ops)
    return O.build(new_ops, base=current_solid(ops_cur), n_base=len(ops_cur))


# ============================================================================ evaluaciones
def run_eval(ops, solid, holes, wd, quick=False, title=""):
    import operaciones as O
    from evaluate import evaluate, PRE_H, PRE_HMIN
    geom = O.Pieza(solid, holes, ops, title)
    if quick:
        return evaluate({}, wd, force=FORCE, geom=geom, log=LOG, images=False, h=PRE_H, hmin=PRE_HMIN,
                        n_strategies=3, mesh_timeout=45)
    return evaluate({}, wd, force=FORCE, geom=geom, log=LOG, images=True)


def light_dir(wd, keep=("metrics.json", "params.json")):
    for f in glob.glob(os.path.join(wd, "*")):
        if os.path.isfile(f) and not f.endswith(keep):
            try:
                os.remove(f)
            except OSError:
                pass


FOT = os.path.join(TOP, "fotos")


def snap(wd, title, name):
    """Foto (von Mises, con el pico marcado) de cualquier calculo, antes de borrar sus ficheros pesados.
    Se guarda en fotos/ (en el PC) y se envia a Discord."""
    try:
        import render
        from PIL import Image
        d = np.load(os.path.join(wd, "campos.npz"))
        mm = json.load(open(os.path.join(wd, "metrics.json"), encoding="utf-8"))
        os.makedirs(FOT, exist_ok=True)
        png = os.path.join(FOT, name + ".png")
        render.results_png(d["nodes"], d["tris"], d["vm"], png, title, marker=mm.get("vm_metric_xyz"))
        jpg = png[:-4] + ".jpg"
        Image.open(png).convert("RGB").save(jpg, "JPEG", quality=80, optimize=True)
        os.remove(png)
        return jpg
    except Exception as e:
        log(f"  (foto no generada: {e!r})")
        return None


def notify_calc(title, cat, fields, desc, img):
    try:
        DISCORD.design(title, cat, fields, desc, img)
    except Exception as e:
        log(f"(Discord: {e!r})")


def current_quick(st):
    """Evaluacion rapida de la pieza ACTUAL (referencia para comparar a los candidatos en la misma malla)."""
    a = st["actual"]
    if a.get("rapida"):
        return a["rapida"]
    wd = os.path.join(ITD, f"{st['iter']:03d}", "actual_rapida")
    log("  evaluacion rapida de la pieza actual (referencia para comparar en la misma malla gruesa)")
    import operaciones as O
    s = current_solid(a["ops"])
    m = run_eval(a["ops"], s, O.finish(s)[1], wd, quick=True)
    if m.get("status") == "ok":
        img = snap(wd, f"iteracion {st['iter']}: pieza actual (malla gruesa) {m['mass_kg']:.3f} kg, {m['vm_metric']:.0f} MPa",
                   f"it{st['iter']:03d}_referencia_rapida")
        notify_calc(f"Iteracion {st['iter']} - referencia: pieza actual con la malla gruesa", "info",
                    [dict(name="Masa", value=f"{m['mass_kg']:.4f} kg", inline=True),
                     dict(name="Tension (malla gruesa)", value=f"{m['vm_metric']:.1f} MPa", inline=True)],
                    "Calculo de referencia: las propuestas de esta iteracion se comparan con la pieza actual en la MISMA malla "
                    "gruesa, asi el error de la malla gruesa se cancela.", img)
    light_dir(wd)
    if m.get("status") != "ok":
        raise RuntimeError(f"la evaluacion rapida de la pieza actual ha fallado: {m.get('error')}")
    a["rapida"] = summ(m)
    return a["rapida"]


def predict(mq, ref_q, ref_full):
    """Valores previstos en la malla completa: la malla gruesa se corrige con la pieza actual (misma malla)."""
    p = dict(mass_kg=mq["mass_kg"] * ref_full["mass_kg"] / ref_q["mass_kg"],
             vm_metric=mq["vm_metric"] * ref_full["vm_metric"] / ref_q["vm_metric"],
             u_max=mq["u_max"] * ref_full["u_max"] / max(ref_q["u_max"], 1e-9))
    return summ(p)


# ============================================================================ registro, galeria, iteraciones
def append_registro(row):
    path = os.path.join(TOP, "registro.csv")
    new = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=REG_COLS, delimiter=";")
        if new:
            w.writeheader()
        w.writerow({k: (f"{v:.4f}".replace(".", ",") if isinstance(v, float) else v) for k, v in row.items() if k in REG_COLS})


def add_to_gallery(wd, it, decision, mass):
    from PIL import Image
    src = os.path.join(wd, "resumen.png")
    if not os.path.exists(src):
        return None
    os.makedirs(GAL, exist_ok=True)
    name = f"{datetime.datetime.now():%Y%m%d_%H%M%S}_it{it:03d}_{decision.replace(' ', '_')}_{mass:.3f}kg.jpg"
    im = Image.open(src).convert("RGB")
    if im.width > 1200:
        im = im.resize((1200, int(im.height * 1200 / im.width)))
    im.save(os.path.join(GAL, name), "JPEG", quality=80, optimize=True)
    return "galeria/" + name


def write_gallery_md():
    rows = []
    for f in sorted(glob.glob(os.path.join(GAL, "*.jpg")), reverse=True):
        p = os.path.basename(f)[:-4].split("_")
        try:
            fecha = f"{p[0][6:8]}/{p[0][4:6]} {p[1][:2]}:{p[1][2:4]}"
            rows.append(f"| {fecha} | {p[2].replace('it', 'iteracion ')} | {' '.join(p[3:-1])} | {p[-1].replace('kg', ' kg')} | "
                        f"<a href=\"galeria/{os.path.basename(f)}\"><img src=\"galeria/{os.path.basename(f)}\" width=\"420\"></a> |")
        except IndexError:
            pass
    open(os.path.join(TOP, "GALERIA.md"), "w", encoding="utf-8").write(
        "# Galeria: todas las piezas calculadas con la malla completa (la mas reciente arriba)\n\n"
        "Cada ficha: geometria 3D | tension de von Mises | deformada | radiografia del interior, con la lista de operaciones "
        "aplicadas al original.\n\n| fecha | iteracion | decision | masa | ficha (clic para ampliar) |\n|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n")


def write_iteraciones(st):
    """ITERACIONES.md: registro de cambios (changelog) con el porque y el antes/despues de cada iteracion."""
    L = ["# Registro de iteraciones (changelog de la pieza)", "",
         f"Carga {FORCE:.0f} N | limite {SIG_OBJ:.0f} MPa (coef. de seguridad >= {SY / SIG_OBJ:.2f}) y {U_LIM:.2f} mm | "
         f"reglas: [DESIGN_RULES.md](../../DESIGN_RULES.md) | la mas reciente arriba", ""]
    for h in reversed(st["historia"]):
        L += [f"## Iteracion {h['iter']} - {h['decision']}" + (f": {h.get('regla', '')} {h.get('titulo', '')}" if h.get("regla") else ""),
              "", f"*{h['fecha'][:16].replace('T', ' ')}*", ""]
        if h.get("antes"):
            L.append(f"- **Pieza de partida:** {h['antes']}")
        if h.get("porque"):
            L.append(f"- **Por que (regla {h.get('regla')}):** {h['porque']}")
        if h.get("espero"):
            L.append(f"- **Se esperaba:** {h['espero']}")
        if h.get("despues"):
            L.append(f"- **Resultado (malla completa):** {h['despues']}")
        if h.get("motivo"):
            L.append(f"- **Decision:** {h['decision']} - {h['motivo']}")
        for d in h.get("descartes", []):
            L.append(f"- Descartada en la evaluacion rapida: [{d['regla']}] {d['titulo']} -> {d['motivo']}")
        for n in h.get("notas", []):
            L.append(f"- Nota: {n}")
        if h.get("galeria"):
            L += ["", f"<img src=\"{h['galeria']}\" width=\"520\">"]
        L.append("")
    open(os.path.join(TOP, "ITERACIONES.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")


def camino_png(st):
    """Camino de la pieza: masa y tension de la pieza actual tras cada iteracion, con la regla aplicada."""
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    H = [h for h in st["historia"] if h.get("m_actual")]
    if not H:
        return None
    fig, ax = plt.subplots(2, 1, figsize=(13, 6.5), sharex=True)
    xs = [h["iter"] for h in H]
    ax[0].step(xs, [h["m_actual"]["mass_kg"] for h in H], where="post", c="k", lw=2)
    ax[1].step(xs, [h["m_actual"]["vm_metric"] for h in H], where="post", c="k", lw=2)
    col = {"ACEPTADA": "#1a9850", "INVERSION": "#fdae61", "RECHAZADA": "#d73027", "SIN CAMBIO": "#888888", "INICIO": "#1f6fb5",
           "DESHECHA": "#7b3294"}
    for h in H:
        c = col.get(h["decision"], "#888")
        if h.get("m_cand"):
            ax[0].scatter(h["iter"], h["m_cand"]["mass_kg"], c=c, s=40, zorder=3)
            ax[1].scatter(h["iter"], h["m_cand"]["vm_metric"], c=c, s=40, zorder=3)
        if h["decision"] in ("ACEPTADA", "INVERSION", "INICIO", "DESHECHA"):
            ax[0].annotate(h.get("regla", "0.stp"), (h["iter"], h["m_actual"]["mass_kg"]), textcoords="offset points",
                           xytext=(0, 7), ha="center", fontsize=8)
    ax[0].axhline(M_ORIG, c="0.5", ls=":", label=f"original {M_ORIG:.3f} kg")
    ax[1].axhline(SIG_OBJ, c="#d73027", ls="--", label=f"limite {SIG_OBJ:.0f} MPa")
    for k, v in col.items():
        ax[0].scatter([], [], c=v, label=k.lower())
    from matplotlib.ticker import MaxNLocator
    ax[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    ax[0].set_ylabel("masa (kg)"); ax[1].set_ylabel("tension (MPa)"); ax[1].set_xlabel("iteracion")
    ax[0].legend(fontsize=7, ncol=4); ax[1].legend(fontsize=7); ax[0].grid(alpha=.3); ax[1].grid(alpha=.3)
    fig.suptitle("Camino de la pieza: linea = pieza actual; puntos = modificacion probada en cada iteracion (color = decision)")
    fig.tight_layout()
    path = os.path.join(TOP, "camino.png")
    fig.savefig(path, dpi=105); plt.close(fig)
    return path


def evolution_html(st):
    try:
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        H = [h for h in st["historia"] if h.get("m_cand") or h.get("m_actual")]
        f = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("masa (kg)", "tension (MPa)"))
        for dec, c in (("ACEPTADA", "green"), ("INVERSION", "orange"), ("RECHAZADA", "red"), ("INICIO", "blue")):
            hh = [h for h in H if h["decision"] == dec and (h.get("m_cand") or h.get("m_actual"))]
            if not hh:
                continue
            mm = [h.get("m_cand") or h["m_actual"] for h in hh]
            txt = [f"<b>iteracion {h['iter']}: {dec}</b><br>{h.get('regla', '')} {h.get('titulo', '')}<br>"
                   f"masa {m['mass_kg']:.4f} kg<br>tension {m['vm_metric']:.1f} MPa<br>{(h.get('motivo') or '')[:120]}" for h, m in zip(hh, mm)]
            f.add_trace(go.Scatter(x=[h["iter"] for h in hh], y=[m["mass_kg"] for m in mm], mode="markers", name=dec.lower(),
                                   marker=dict(color=c, size=10), text=txt, hoverinfo="text"), 1, 1)
            f.add_trace(go.Scatter(x=[h["iter"] for h in hh], y=[m["vm_metric"] for m in mm], mode="markers", showlegend=False,
                                   marker=dict(color=c, size=10), text=txt, hoverinfo="text"), 2, 1)
        A = [h for h in st["historia"] if h.get("m_actual")]
        f.add_trace(go.Scatter(x=[h["iter"] for h in A], y=[h["m_actual"]["mass_kg"] for h in A], mode="lines",
                               line=dict(shape="hv", color="black"), name="pieza actual"), 1, 1)
        f.add_hline(y=SIG_OBJ, line_dash="dash", line_color="red", row=2, col=1)
        f.update_layout(title="Evolucion de la pieza (pasar el raton por cada punto)", height=800, template="plotly_white")
        f.write_html(os.path.join(TOP, "evolucion_interactiva.html"), include_plotlyjs="cdn")
    except Exception as e:
        log(f"(grafica interactiva: {e!r})")


# ============================================================================ mejores, Workbench, verificacion
PEND = os.path.join(TOP, "pendientes_workbench.json")


def do_workbench(job):
    try:
        import exportar_workbench as EW
        ok, _, _ = EW.export(job["step"], job["out"], job["name"], FORCE, log=LOG, half=job["half"], timeout=1800)
        return ok
    except Exception as e:
        log(f"  (Workbench: {e!r})")
        return False


def verify_fine(st, best):
    """Malla fina (h = 3,5 mm) del mejor diseno. Devuelve True/False/None (None = no se pudo calcular)."""
    import operaciones as O
    log("  verificacion con malla fina del mejor diseno...")
    s, holes = O.build(best["ops"]) if ops_key(best["ops"]) != Current.key else (Current.solid, O.finish(Current.solid)[1])
    from evaluate import evaluate
    wd = os.path.join(best["dir"], "verificacion")
    try:
        mv = evaluate({}, wd, force=FORCE, geom=O.Pieza(s, holes, best["ops"]), log=LOG, images=False,
                      h=float(USER.get("verificacion_h_mm", 3.5)), hmin=1.0)
    except Exception as e:
        mv = dict(status="error", error=repr(e))
    img_v = None
    if mv.get("status") == "ok":
        img_v = snap(wd, f"verificacion malla fina (iteracion {best['iter']}): {mv['vm_metric']:.0f} MPa", f"it{best['iter']:03d}_verificacion_fina")
    light_dir(wd)
    if mv.get("status") != "ok":
        log(f"  verificacion no disponible ({str(mv.get('error'))[:80]})")
        return None
    ok = valid(mv)
    notify_calc(f"Verificacion con malla fina del mejor diseno (iteracion {best['iter']})", "valido" if ok else "descartado",
                [dict(name="Malla fina", value=f"{mv['vm_metric']:.1f} MPa, {mv['u_max']:.3f} mm ({mv.get('n_nodes')} nodos)", inline=False),
                 dict(name="Resultado", value="CONFIRMADO" if ok else "NO se confirma", inline=True)],
                "Antes de registrar un hito (proyecto Workbench) el diseno se recalcula con una malla mas fina (h = 3,5 mm).", img_v)
    best["verif"] = dict(vm_metric=mv["vm_metric"], u_max=mv["u_max"], n_nodes=mv.get("n_nodes"), ok=ok)
    kk = [mv["vm_metric"] / best["m"]["vm_metric"], mv["u_max"] / max(best["m"]["u_max"], 1e-9)]
    st.setdefault("k_fino", []).append([round(kk[0], 4), round(kk[1], 4)])
    K_FINO[:] = k_fino(st)
    log(f"  calibracion: malla fina / malla normal = {kk[0]:.3f} en tension ({kk[1]:.3f} en desplazamiento); desde ahora "
        f"para aceptar una pieza se exige tension x {K_FINO[0]:.3f} <= {SIG_OBJ:.0f} MPa (es decir <= {SIG_OBJ / K_FINO[0]:.1f} MPa "
        f"con la malla normal)")
    log(f"  verificacion (malla fina, {mv.get('n_nodes')} nodos): {mv['vm_metric']:.1f} MPa, {mv['u_max']:.3f} mm -> "
        + ("CONFIRMADO" if ok else "NO se confirma"))
    return ok


def O_describe(o):
    import operaciones as O
    try:
        return O.describe(o)
    except Exception:
        return str(o.get("tipo"))


def register_best(st, git, final=False):
    """Hito: el mejor diseno se verifica con malla fina y se guarda en historial/ con su proyecto Workbench."""
    best = st["mejor"]
    if not best:
        return
    if USER.get("verificar_mejores", True) and not best.get("verif"):
        ok = verify_fine(st, best)
        if ok is False:
            prev = st.get("verificado")
            msg = (f"la malla fina NO confirma el mejor diseno ({best['verif']['vm_metric']:.1f} MPa): se vuelve al ultimo "
                   "diseno verificado" if prev else "la malla fina no confirma el mejor diseno: deja de contar como mejor")
            log("  " + msg); DISCORD.alert(msg)
            prev_ops = prev["ops"] if prev else []
            nuevos = [o for o in best["ops"] if o not in prev_ops]
            for o in nuevos:          # R9: en esa zona solo se probaran cambios menores (no se repite el mismo camino)
                st["rechazos"].append(dict(op=o, motivo_tipo="tension", regla="verificacion", iter=best["iter"],
                                           motivo=f"malla fina {best['verif']['vm_metric']:.1f} MPa"))
            if nuevos:
                log(f"  se anotan como rechazados los {len(nuevos)} cambios desde el ultimo diseno verificado: "
                    + "; ".join(O_describe(o) for o in nuevos))
            st["mejor"] = prev
            if prev:
                st["actual"] = dict(ops=prev["ops"], dir=prev["dir"], m=prev["m"], rapida=None)
                Current.key = None
            return
    st["verificado"] = best
    hist = os.path.join(TOP, "historial"); os.makedirs(hist, exist_ok=True)
    k = len(glob.glob(os.path.join(hist, "[0-9][0-9]_*"))) + 1
    name = f"{k:02d}_it{best['iter']:03d}_{best['m']['mass_kg']:.3f}kg"
    hd = os.path.join(hist, name); os.makedirs(hd, exist_ok=True)
    for f in ("resumen.png", "geometria.png", "vonmises.png", "metrics.json", "modelo_apdl.zip"):
        if os.path.exists(os.path.join(best["dir"], f)):
            shutil.copy(os.path.join(best["dir"], f), os.path.join(hd, f))
    import operaciones as O, geometry as G
    s = Current.solid if ops_key(best["ops"]) == Current.key else O.build(best["ops"])[0]
    G.export(s, os.path.join(hd, "geometria.step"))
    atomic_json(os.path.join(hd, "operaciones.json"), dict(operaciones=best["ops"], descripcion=[O.describe(o) for o in best["ops"]]))
    wb_ok = False
    if USER.get("crear_workbench_en_cada_mejora", True) and not TEST:
        wb_ok = do_workbench(dict(step=os.path.join(hd, "geometria.step"), out=os.path.join(hd, "workbench"),
                                  name=f"soporte_it{best['iter']:03d}", half=G.T_LUG / 2))
    st["wb_masa"] = best["m"]["mass_kg"]
    best["historial"] = hd
    gb = dict(iter=best["iter"], carpeta=hd, mass_kg=best["m"]["mass_kg"], vm_metric=best["m"]["vm_metric"],
              u_max=best["m"]["u_max"], coef_seguridad=best["m"]["cs"], puntuacion=best["m"]["score"], workbench=wb_ok,
              verificacion=best.get("verif"), operaciones=[O.describe(o) for o in best["ops"]],
              fecha=datetime.datetime.now().isoformat(timespec="seconds"), final=final)
    atomic_json(os.path.join(TOP, "MEJOR_GLOBAL.json"), gb)
    for f in ("resumen.png", "geometria.png", "vonmises.png"):
        if os.path.exists(os.path.join(best["dir"], f)):
            shutil.copy(os.path.join(best["dir"], f), os.path.join(TOP, "MEJOR_" + f))
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
        "# Historial de hitos (verificados con malla fina, con proyecto Workbench)\n\n"
        f"Original: {M_ORIG:.3f} kg | limite {SIG_OBJ:.0f} MPa | carga {FORCE:.0f} N\n\n"
        "| n | diseno | masa (kg) | tension (MPa) | ficha | proyecto |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    log(f"  >>> HITO {k}: {best['m']['mass_kg']:.3f} kg (iteracion {best['iter']})" + (" | proyecto Workbench creado" if wb_ok else ""))


# ============================================================================ panel (README.md)
def write_dashboard(st, estado="EN MARCHA"):
    md_path = os.path.join(ROOT, "README.md") if not TEST else os.path.join(TOP, "PANEL.md")
    base = os.path.dirname(md_path)
    rel = lambda p: os.path.relpath(p, base).replace("\\", "/")
    H = st["historia"]
    n_it = sum(1 for h in H if h["decision"] != "INICIO")
    cnt = {k: sum(1 for h in H if h["decision"] == k) for k in ("ACEPTADA", "INVERSION", "RECHAZADA", "SIN CAMBIO")}
    n_q = sum(len(h.get("descartes", [])) for h in H)
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    L = ["# Optimizacion del soporte guiada por reglas - panel en directo", "",
         f"> **Ultima actualizacion:** {now} &nbsp;|&nbsp; **Estado:** {estado} &nbsp;|&nbsp; carga **{FORCE:.0f} N** &nbsp;|&nbsp; "
         f"limite **{SIG_OBJ:.0f} MPa** (coef. de seguridad >= {SY / SIG_OBJ:.2f}, obligatorio) y {U_LIM:.2f} mm &nbsp;|&nbsp; acero S235", "",
         "La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** "
         "(sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone "
         "anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal "
         "de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. "
         "Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](" + rel(os.path.join(TOP, "ITERACIONES.md")) + ").", "",
         "| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |",
         "|---|---|---|---|---|---|",
         f"| {n_it} | {cnt['ACEPTADA']} | {cnt['INVERSION']} | {cnt['RECHAZADA']} | {cnt['SIN CAMBIO']} | {n_q} |", ""]
    a = st.get("actual"); b = st.get("mejor")
    if b:
        m = b["m"]; red = (1 - m["mass_kg"] / M_ORIG) * 100
        L += ["## Mejor diseno", "",
              f"**{m['mass_kg']:.4f} kg** ({-red:+.1f} % frente al original, {M_ORIG:.3f} kg) &nbsp;|&nbsp; tension **{m['vm_metric']:.1f} MPa** "
              f"&nbsp;|&nbsp; coef. seguridad **{m['cs']:.2f}** &nbsp;|&nbsp; desplazamiento **{m['u_max']:.3f} mm** &nbsp;|&nbsp; iteracion {b['iter']}"
              + (f" &nbsp;|&nbsp; **malla fina: {b['verif']['vm_metric']:.1f} MPa**" if b.get("verif") else ""), ""]
        import operaciones as O
        L += ["Operaciones sobre el original:", ""] + [f"{i + 1}. {O.describe(o)}" for i, o in enumerate(b["ops"])] + [""]
        gb = os.path.join(TOP, "MEJOR_GLOBAL.json")
        if os.path.exists(gb):
            g = json.load(open(gb, encoding="utf-8"))
            links = []
            wb = glob.glob(os.path.join(g["carpeta"], "workbench", "*.wbpz"))
            if wb:
                links.append(f"[Proyecto Workbench (.wbpz)]({rel(wb[0])})")
            if os.path.exists(os.path.join(g["carpeta"], "geometria.step")):
                links.append(f"[Geometria STEP]({rel(os.path.join(g['carpeta'], 'geometria.step'))})")
            if links:
                L += [f"Ultimo hito verificado ({g['mass_kg']:.3f} kg, iteracion {g['iter']}): " + " &nbsp;|&nbsp; ".join(links), ""]
        img = os.path.join(b["dir"], "resumen.png")
        gimg = b.get("galeria") and os.path.join(TOP, b["galeria"])
        if gimg and os.path.exists(gimg):
            L += [f"![mejor diseno]({rel(gimg)})", ""]
    elif a:
        L += ["## Aun ningun diseno cumple", "", f"Pieza actual: {txt_m(a['m'])}. Primero hay que llevarla por debajo del limite.", ""]
    if os.path.exists(os.path.join(TOP, "camino.png")):
        L += ["## Camino de la pieza", "", f"![camino]({rel(os.path.join(TOP, 'camino.png'))})", "",
              f"Grafico interactivo: [evolucion_interactiva.html]({rel(os.path.join(TOP, 'evolucion_interactiva.html'))}) "
              f"&nbsp;|&nbsp; [Galeria de todas las piezas]({rel(os.path.join(TOP, 'GALERIA.md'))}) &nbsp;|&nbsp; "
              f"[Hitos con proyecto Workbench]({rel(os.path.join(TOP, 'HISTORIAL.md'))})", ""]
    L += ["## Ultimas iteraciones", "", "| iteracion | decision | regla | modificacion | resultado | motivo |", "|---|---|---|---|---|---|"]
    for h in list(reversed(H))[:12]:
        res = (f"{h['m_cand']['mass_kg']:.3f} kg, {h['m_cand']['vm_metric']:.0f} MPa" if h.get("m_cand") else "-")
        L.append(f"| {h['iter']} | {h['decision']} | {h.get('regla', '-')} | {(h.get('titulo') or '-')[:70]} | {res} | {(h.get('motivo') or '')[:90]} |")
    arch = sorted(glob.glob(os.path.join(ROOT, "runs", "archivo", "*")))
    L += ["", "---", "", "**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con "
          "datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) "
          "para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta "
          "o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).", ""]
    if arch:
        L.append("Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC "
                 "(`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.")
    open(md_path, "w", encoding="utf-8").write("\n".join(L) + "\n")


# ============================================================================ Discord
DISCORD = None
REPO_URL = None


def _repo_url():
    try:
        u = subprocess.run([find_git(), "remote", "get-url", "origin"], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
        return u[:-4] if u.endswith(".git") else u
    except Exception:
        return None


def notify_iteration(h):
    cat = {"ACEPTADA": "valido", "INVERSION": "cerca_del_limite", "RECHAZADA": "descartado", "INICIO": "info",
           "SIN CAMBIO": "fallido", "DESHECHA": "cerca_del_limite"}.get(h["decision"], "info")
    fields = [dict(name="Decision", value=h["decision"], inline=True)]
    if h.get("regla"):
        fields.append(dict(name="Regla", value=h["regla"], inline=True))
    if h.get("antes"):
        fields.append(dict(name="Antes", value=h["antes"][:1000], inline=False))
    if h.get("despues"):
        fields.append(dict(name="Despues", value=h["despues"][:1000], inline=False))
    if h.get("espero"):
        fields.append(dict(name="Se esperaba", value=h["espero"][:1000], inline=False))
    desc = ""
    if h.get("porque"):
        desc += f"**Por que:** {h['porque']}\n"
    if h.get("motivo"):
        desc += f"**Decision:** {h['motivo']}\n"
    for d in h.get("descartes", [])[:3]:
        desc += f"- descartada en la evaluacion rapida: [{d['regla']}] {d['titulo'][:70]} ({d['motivo'][:90]})\n"
    for n in h.get("notas", [])[:3]:
        desc += f"- nota: {n[:200]}\n"
    img = os.path.join(TOP, h["galeria"]) if h.get("galeria") else None
    DISCORD.design(f"Iteracion {h['iter']}: {h['decision']}" + (f" - {h.get('titulo', '')}"[:150] if h.get("titulo") else ""),
                   cat, fields, desc, img if img and os.path.exists(img) else None)


def notify_top(st):
    b = st.get("mejor")
    footer = f"Actualizado {datetime.datetime.now():%d/%m/%Y %H:%M} | carga {FORCE:.0f} N | limites {SIG_OBJ:.0f} MPa y {U_LIM:.2f} mm"
    if not b:
        a = st.get("actual")
        DISCORD.top("Mejor diseno: aun ninguno cumple", [dict(name="Pieza actual", value=txt_m(a["m"]) if a else "-")], None, footer, REPO_URL)
        return
    import operaciones as O
    m = b["m"]
    fields = [dict(name="Masa", value=f"**{m['mass_kg']:.4f} kg** ({(m['mass_kg'] / M_ORIG - 1) * 100:+.1f} % frente al original)", inline=False),
              dict(name="Tension", value=f"{m['vm_metric']:.1f} / {SIG_OBJ:.0f} MPa", inline=True),
              dict(name="Coef. seguridad", value=f"{m['cs']:.2f}", inline=True),
              dict(name="Desplazamiento", value=f"{m['u_max']:.3f} mm", inline=True),
              dict(name="Operaciones", value="\n".join(f"{i + 1}. {O.describe(o)}" for i, o in enumerate(b["ops"]))[:1000] or "-", inline=False)]
    if b.get("verif"):
        fields.append(dict(name="Malla fina", value=f"{b['verif']['vm_metric']:.1f} MPa - " + ("confirmado" if b["verif"]["ok"] else "NO"), inline=True))
    img = os.path.join(TOP, b["galeria"]) if b.get("galeria") else None
    DISCORD.top("Mejor diseno actual", fields, img if img and os.path.exists(img) else None, footer, REPO_URL)


# ============================================================================ una iteracion
def record(st, h, git, changed):
    """Todo lo que deja rastro de una iteracion: estado, ITERACIONES.md, panel, graficas, Discord y commit."""
    h["m_actual"] = st["actual"]["m"] if st.get("actual") else None
    st["historia"].append(h)
    save_state(st)
    path = None
    try:
        write_iteraciones(st); write_gallery_md()
        path = camino_png(st); evolution_html(st)
        write_dashboard(st)
        import reglas as R
        R.write_doc(R.load_evidence(), st["stats"])
    except Exception as e:
        log(f"(documentos: {e!r})")
    try:
        notify_iteration(h)
        if changed and path:
            shot = os.path.join(TOP, "discord_camino.png"); shutil.copy(path, shot)
            DISCORD.tree(shot, f"Pieza actual tras la iteracion {h['iter']}: {txt_m(st['actual']['m'])}")
        notify_top(st)
    except Exception as e:
        log(f"(Discord: {e!r})")
    title = f"Iteracion {h['iter']} [{h['decision']}]" + (f" {h.get('regla', '')}: {h.get('titulo', '')}" if h.get("regla") else "")
    if h.get("m_cand") and h.get("m_antes"):
        a, d = h["m_antes"], h["m_cand"]
        title += f" | masa {a['mass_kg']:.3f}->{d['mass_kg']:.3f} kg, tension {a['vm_metric']:.0f}->{d['vm_metric']:.0f} MPa"
    body = "\n".join(x for x in [f"Por que: {h['porque']}" if h.get("porque") else "", f"Se esperaba: {h['espero']}" if h.get("espero") else "",
                                 f"Resultado: {h['despues']}" if h.get("despues") else "", f"Decision: {h['motivo']}" if h.get("motivo") else ""]
                     + [f"Descartada (rapida): [{d['regla']}] {d['titulo']} -> {d['motivo']}" for d in h.get("descartes", [])]
                     + [f"Nota: {n}" for n in h.get("notas", [])] if x)
    git.commit(title, body)


def start(st, git):
    """Iteracion 0: la pieza del enunciado, tal cual, calculada con la malla completa."""
    import operaciones as O
    log("ITERACION 0: la pieza del enunciado (0.stp) tal cual")
    s, holes = O.build([])
    wd = os.path.join(ITD, "000", "completa")
    m = run_eval([], s, holes, wd)
    if m.get("status") != "ok":
        raise RuntimeError(f"no se ha podido calcular la pieza original: {m.get('error')}")
    set_current(s, [])
    sm = summ(m)
    st["actual"] = dict(ops=[], dir=wd, m=sm, rapida=None)
    gal = add_to_gallery(wd, 0, "INICIO", sm["mass_kg"])
    st["actual"]["galeria"] = gal
    if sm["valido"]:
        st["mejor"] = dict(ops=[], dir=wd, m=sm, iter=0, galeria=gal)
    h = dict(iter=0, fecha=datetime.datetime.now().isoformat(), decision="INICIO", titulo="pieza del enunciado (0.stp)",
             despues=txt_m(sm), galeria=gal, m_cand=sm,
             motivo=("cumple: se empieza a quitar material donde no trabaja" if sm["valido"] else
                     f"NO cumple ({sm['vm_metric']:.0f} MPa > {SIG_OBJ:.0f}): primero hay que reforzar donde esta el pico"))
    log(f"  original: {txt_m(sm)} -> {h['motivo']}")
    record(st, h, git, True)


def step(st, git, E):
    import operaciones as O, reglas as R, campo as CA
    st["iter"] += 1
    it = st["iter"]
    a = st["actual"]; ma = a["m"]
    itd = os.path.join(ITD, f"{it:03d}"); os.makedirs(itd, exist_ok=True)
    print("\n" + "=" * 90)
    log(f"ITERACION {it} | pieza actual: {txt_m(ma)}" + (f" | mejor: {st['mejor']['m']['mass_kg']:.4f} kg" if st.get("mejor") else ""))
    mfull = json.load(open(os.path.join(a["dir"], "metrics.json"), encoding="utf-8"))
    K_FINO[:] = k_fino(st)
    for d in (ma, ):                      # validez de la pieza actual con la calibracion vigente
        d.update(summ(dict(d)))
    if st.get("verificado") and ops_key(st["verificado"]["ops"]) == ops_key(a["ops"]):
        ma["valido"] = True; ma["viol"] = min(ma["viol"], 1.0)   # verificada con malla fina: cumple
    C = CA.from_npz(os.path.join(a["dir"], "campos.npz"), SIG_OBJ / K_FINO[0], mfull)
    cands, notes, pk = R.propose(C, mfull, a["ops"], st, E, st["stats"], N_CAND)
    for n in notes:
        log(f"  nota: {n}")
    h = dict(iter=it, fecha=datetime.datetime.now().isoformat(), antes=txt_m(ma), m_antes=ma, notas=notes, descartes=[])
    if not cands:
        st["fin"] = True
        st["motivo_fin"] = ("ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa un corte "
                            "y el pico no admite refuerzo)")
        h.update(decision="SIN CAMBIO", motivo=st["motivo_fin"])
        record(st, h, git, False)
        return
    log(f"  pico: {pk['tension']:.0f} MPa en {CA.ZONA_TXT.get(pk['zona'], pk['zona'])} (concentracion x{pk['kt_aparente']:.1f}) | "
        f"{len(cands)} modificaciones propuestas:")
    for k, c in enumerate(cands, 1):
        log(f"   {k}. [{c['regla']}] {c['titulo']}")
        log(f"      porque: {c['porque'][:300]}")
    ref_q = current_quick(st)
    surv = []
    for k, c in enumerate(cands, 1):
        rs = rule_stats(st, c["regla"]); rs["intentos"] += 1
        t0 = time.time()
        log(f"  [{k}/{len(cands)}] evaluacion rapida: [{c['regla']}] {c['titulo']}")
        try:
            s, holes = build_candidate(c, a["ops"])
        except Exception as e:
            why = f"la geometria no se puede construir ({str(e)[:150]})"
            log(f"      DESCARTADA: {why}")
            h["descartes"].append(dict(regla=c["regla"], titulo=c["titulo"], motivo=why))
            st["rechazos"].append(dict(op=c["op"], motivo_tipo="geometria", regla=c["regla"], iter=it))
            rs["descartadas_rapido"] += 1
            append_registro(dict(iteracion=it, fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), candidato=k, regla=c["regla"],
                                 modificacion=c["titulo"], fase="geometria", decision="descartada", motivo=why, porque=c["porque"],
                                 tiempo_s=round(time.time() - t0, 1)))
            notify_calc(f"Iteracion {it} - propuesta {k}/{len(cands)}: [{c['regla']}] {c['titulo']}"[:250], "fallido",
                        [dict(name="Resultado", value="DESCARTADA (geometria)", inline=True)],
                        f"**Por que se propuso:** {c['porque'][:600]}\n**Motivo del descarte:** {why}", None)
            continue
        wq = os.path.join(itd, f"cand{k}_rapida")
        mq = run_eval(c["ops_nuevas"], s, holes, wq, quick=True)
        img_q = None
        if mq.get("status") == "ok":
            img_q = snap(wq, f"iteracion {it}, propuesta {k} [{c['regla']}] (malla gruesa): {mq['mass_kg']:.3f} kg, {mq['vm_metric']:.0f} MPa",
                         f"it{it:03d}_propuesta{k}_{c['regla']}_rapida")
        light_dir(wq)
        if mq.get("status") != "ok":
            why = f"la malla o el calculo han fallado ({str(mq.get('error'))[:120]})"
            log(f"      DESCARTADA: {why}")
            h["descartes"].append(dict(regla=c["regla"], titulo=c["titulo"], motivo=why))
            st["rechazos"].append(dict(op=c["op"], motivo_tipo="geometria", regla=c["regla"], iter=it))
            rs["descartadas_rapido"] += 1
            notify_calc(f"Iteracion {it} - propuesta {k}/{len(cands)}: [{c['regla']}] {c['titulo']}"[:250], "fallido",
                        [dict(name="Resultado", value="DESCARTADA (malla)", inline=True)],
                        f"**Por que se propuso:** {c['porque'][:600]}\n**Motivo del descarte:** {why}", None)
            continue
        p = predict(summ(mq), ref_q, ma)
        dsig = (p["vm_metric"] / ma["vm_metric"] - 1) * 100; dm = (p["mass_kg"] - ma["mass_kg"]) * 1000
        log(f"      prevision: {txt_m(p)}  (tension {dsig:+.1f} %, masa {dm:+.0f} g; se esperaba {c['espero'].get('txt', '')})")
        why = None
        if ma["valido"]:
            if p["viol"] > 1.0 + TOL_Q:
                why = f"tension prevista {p['vm_metric']:.0f} MPa: supera el limite ({SIG_OBJ:.0f} MPa)"
            elif p["score"] >= ma["score"] and c["regla"] not in ("R4", "R6", "R7", "R8"):
                why = f"no mejora la pieza (puntuacion {p['score']:.4f} >= {ma['score']:.4f})"
        elif p["viol"] >= ma["viol"] - 1e-3:
            why = f"no acerca la pieza al limite (prevision {p['vm_metric']:.0f} MPa frente a {ma['vm_metric']:.0f} MPa)"
        append_registro(dict(iteracion=it, fecha=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), candidato=k, regla=c["regla"],
                             modificacion=c["titulo"], fase="rapida (prevision)", masa_kg=p["mass_kg"], tension_MPa=p["vm_metric"],
                             desp_mm=p["u_max"], coef_seguridad=p["cs"], puntuacion=p["score"],
                             decision="descartada" if why else "pasa", motivo=why or "", porque=c["porque"], tiempo_s=round(time.time() - t0, 1)))
        notify_calc(f"Iteracion {it} - propuesta {k}/{len(cands)}: [{c['regla']}] {c['titulo']}"[:250],
                    "descartado" if why else "cerca_del_limite",
                    [dict(name="Evaluacion rapida", value="DESCARTADA" if why else "pasa", inline=True),
                     dict(name="Prevision", value=txt_m(p), inline=False),
                     dict(name="Cambio", value=f"tension {dsig:+.1f} %, masa {dm:+.0f} g", inline=True),
                     dict(name="Se esperaba", value=c["espero"].get("txt", "")[:200] or "-", inline=True)],
                    f"**Por que se propuso:** {c['porque'][:900]}" + (f"\n**Motivo del descarte:** {why}" if why else ""), img_q)
        if why:
            log(f"      DESCARTADA en la evaluacion rapida: {why}")
            h["descartes"].append(dict(regla=c["regla"], titulo=c["titulo"], motivo=why))
            st["rechazos"].append(dict(op=c["op"], motivo_tipo="tension" if "supera" in why else "puntuacion", regla=c["regla"], iter=it))
            rs["descartadas_rapido"] += 1
            continue
        surv.append((c, s, holes, p))
    if not surv:
        st["sin_mejora"] += 1
        h.update(decision="SIN CAMBIO", motivo="todas las modificaciones propuestas se descartaron en la evaluacion rapida")
        log(f"  SIN CAMBIO: {h['motivo']} ({st['sin_mejora']} iteraciones seguidas sin mejora)")
        maybe_finish(st)
        record(st, h, git, False)
        return
    keyf = (lambda t: (t[3]["viol"] > 1.0, t[3]["viol"] if not ma["valido"] else t[3]["score"]))
    c, s, holes, p = min(surv, key=keyf)
    for c2, _, _, p2 in surv:
        if c2 is not c:
            h["descartes"].append(dict(regla=c2["regla"], titulo=c2["titulo"],
                                       motivo=f"pasa la evaluacion rapida ({txt_m(p2)}) pero otra es mas prometedora; se podra proponer de nuevo"))
    rs = rule_stats(st, c["regla"]); rs["evaluadas"] += 1
    log(f"  EVALUACION COMPLETA de la mas prometedora: [{c['regla']}] {c['titulo']}")
    wd = os.path.join(itd, "completa")
    t0 = time.time()
    m = run_eval(c["ops_nuevas"], s, holes, wd)
    h.update(regla=c["regla"], titulo=c["titulo"], porque=c["porque"],
             espero=c["espero"].get("txt", "") + (f" (prevision rapida: {txt_m(p)})"))
    if m.get("status") != "ok":
        h.update(decision="RECHAZADA", motivo=f"el calculo completo ha fallado: {str(m.get('error'))[:150]}")
        st["rechazos"].append(dict(op=c["op"], motivo_tipo="geometria", regla=c["regla"], iter=it))
        rs["rechazadas"] += 1; st["sin_mejora"] += 1
        record(st, h, git, False)
        return
    sm = summ(m)
    dsig = (sm["vm_metric"] / ma["vm_metric"] - 1) * 100; dm = (sm["mass_kg"] - ma["mass_kg"]) * 1000
    rs["dsig"].append(round(dsig, 2)); rs["dm"].append(round(dm, 1))
    rs.setdefault("dsig_prev", []).append(round((p["vm_metric"] / ma["vm_metric"] - 1) * 100, 2))   # calibracion malla rapida
    h.update(m_cand=sm, despues=txt_m(sm) + f" (tension {dsig:+.1f} %, masa {dm:+.0f} g)")
    best = st.get("mejor")
    decision, why = "RECHAZADA", ""
    if sm["valido"] and (best is None or sm["score"] < best["m"]["score"] * (1 - 1e-4)):
        decision = "ACEPTADA"
        why = ("primera pieza que CUMPLE" if best is None else
               f"cumple y mejora al mejor (puntuacion {best['m']['score']:.4f} -> {sm['score']:.4f}; masa {best['m']['mass_kg']:.4f} -> {sm['mass_kg']:.4f} kg)")
    elif not ma["valido"] and sm["viol"] < ma["viol"] - 2e-3:
        decision = "ACEPTADA"
        why = (f"aun no cumple pero se acerca al limite ({ma['vm_metric']:.0f} -> {sm['vm_metric']:.0f} MPa)" if not sm["valido"]
               else "ya cumple")
    elif (sm["valido"] and c["regla"] in ("R4", "R6", "R7", "R8") and ma["vm_metric"] / SIG_OBJ > 0.97 and dm > 0
          and -dsig >= 2.0 * (dm / 1000 / ma["mass_kg"] * 100) and st["inversiones"] < MAX_INV):
        decision = "INVERSION"
        why = (f"refuerzo eficiente: compra {-dsig:.1f} % de margen de tension con +{dm:.0f} g ({dm / 10 / ma['mass_kg']:.1f} % de masa); "
               "ese margen se gastara aligerando en las siguientes iteraciones (si no, se deshace)")
    else:
        if not sm["valido"]:
            why = f"la tension sube a {sm['vm_metric']:.1f} MPa (> {SIG_OBJ:.0f} MPa): no cumple" if sm["vm_metric"] > SIG_OBJ else \
                f"desplazamiento {sm['u_max']:.3f} mm > {U_LIM:.2f} mm"
            mt = "tension"
        else:
            why = (f"cumple pero no mejora al mejor (puntuacion {sm['score']:.4f} frente a "
                   f"{best['m']['score']:.4f})" if best else "no mejora")
            mt = "puntuacion"
        st["rechazos"].append(dict(op=c["op"], motivo_tipo=mt, regla=c["regla"], iter=it))
    h.update(decision=decision, motivo=why)
    gal = add_to_gallery(wd, it, decision, sm["mass_kg"])
    h["galeria"] = gal
    rs["ejemplos"] = (rs["ejemplos"] + [[it, f"{decision.lower()}: {c['titulo'][:60]} (tension {dsig:+.1f} %, masa {dm:+.0f} g)"]])[-8:]
    log(f"  RESULTADO: {txt_m(sm)} (tension {dsig:+.1f} %, masa {dm:+.0f} g) -> {decision}: {why}")
    changed = decision in ("ACEPTADA", "INVERSION")
    if changed:
        rs["aceptadas"] += 1
        set_current(s, c["ops_nuevas"])
        st["actual"] = dict(ops=c["ops_nuevas"], dir=wd, m=sm, rapida=None, galeria=gal)
        if decision == "INVERSION":
            st["inversiones"] += 1
            st["inversion_desde"] = st["inversion_desde"] or it
        if sm["valido"] and (best is None or sm["score"] < best["m"]["score"] * (1 - 1e-4)):
            st["mejor"] = dict(ops=c["ops_nuevas"], dir=wd, m=sm, iter=it, galeria=gal)
            st["sin_mejora"] = 0; st["inversiones"] = 0; st["inversion_desde"] = None
        elif decision == "ACEPTADA":
            st["sin_mejora"] = 0
        else:
            st["sin_mejora"] += 1
        package_apdl(wd)
    else:
        rs["rechazadas"] += 1
        st["sin_mejora"] += 1
        light_dir(wd, keep=("metrics.json", "resumen.png"))
    if os.path.exists(os.path.join(wd, "model.inp")):
        os.remove(os.path.join(wd, "model.inp"))
    # inversion que no se recupera -> se deshace
    if st.get("inversion_desde") and it - st["inversion_desde"] >= 3 and st.get("mejor"):
        b = st["mejor"]
        log(f"  la inversion de la iteracion {st['inversion_desde']} no se ha recuperado en 3 iteraciones: se vuelve al mejor diseno")
        h.setdefault("notas", []).append(f"se deshace la inversion de la iteracion {st['inversion_desde']} (no se recupero en 3 "
                                         f"iteraciones): se vuelve al mejor ({b['m']['mass_kg']:.4f} kg)")
        st["actual"] = dict(ops=b["ops"], dir=b["dir"], m=b["m"], rapida=None, galeria=b.get("galeria"))
        Current.key = None
        st["inversiones"] = 0; st["inversion_desde"] = None
        changed = True
    maybe_finish(st)
    # hito: Workbench + verificacion con malla fina
    b = st.get("mejor")
    if b and changed and b["iter"] == it:
        last = st.get("wb_masa")
        if last is None or (1 - b["m"]["mass_kg"] / last) * 100 >= float(USER.get("workbench_mejora_minima_pct", 1.0)):
            register_best(st, git)
    record(st, h, git, changed)


def package_apdl(wd):
    inp = os.path.join(wd, "model.inp")
    if not os.path.exists(inp):
        return
    gui = ("! Mechanical APDL: File > Change Directory (esta carpeta) > File > Read Input from > abrir_en_ansys.inp\n"
           "/INPUT,model,inp\n/POST1\nSET,LAST\n/EFACET,1\n/VIEW,1,1,-1.5,1\n/AUTO,1\nCMSEL,S,FIJO\nFSUM\nALLSEL\nPLNSOL,S,EQV\n")
    with zipfile.ZipFile(os.path.join(wd, "modelo_apdl.zip"), "w", zipfile.ZIP_DEFLATED) as z:
        z.write(inp, "model.inp"); z.writestr("abrir_en_ansys.inp", gui)


def maybe_finish(st):
    if st["sin_mejora"] >= MAX_SIN_MEJORA:
        st["fin"] = True
        st["motivo_fin"] = f"{st['sin_mejora']} iteraciones seguidas sin mejorar: las reglas ya no encuentran mejoras"


def cleanup(st):
    """Borra los ficheros pesados de iteraciones antiguas (nunca metrics.json ni la ficha); conserva actual y mejor."""
    keep = {os.path.normpath(d) for d in (st["actual"]["dir"] if st.get("actual") else "", (st.get("mejor") or {}).get("dir", ""),
                                          (st.get("verificado") or {}).get("dir", "")) if d}
    freed = 0.0
    for d in glob.glob(os.path.join(ITD, "*", "completa")):
        if os.path.normpath(d) in keep:
            continue
        for name in ("campos.npz", "geometria.step", "solve.out", "vonmises.png", "geometria.png", "res_glob.txt", "res_nod.txt"):
            p = os.path.join(d, name)
            if os.path.exists(p):
                freed += os.path.getsize(p) / 1e6
                try:
                    os.remove(p)
                except OSError:
                    pass
    hist = sorted(glob.glob(os.path.join(TOP, "historial", "[0-9][0-9]_*")))
    kw = int(USER.get("mantener_proyectos_workbench_resueltos", 3))
    for d in hist[:-kw] if kw > 0 else hist:
        for item in glob.glob(os.path.join(d, "workbench", "*_files")) + glob.glob(os.path.join(d, "workbench", "*.wbpj")):
            try:
                shutil.rmtree(item, ignore_errors=True) if os.path.isdir(item) else os.remove(item)
            except OSError:
                pass
    if freed > 0.5:
        log(f"Limpieza automatica: liberados {freed:.0f} MB")


def acquire_lock():
    import estudio_simjeb as ES
    lk = os.path.join(TOP, "EN_EJECUCION.lock")
    if ES.lock_alive(lk):
        print(f"\nYa hay un optimizador en marcha. Esta ventana se cierra.")
        time.sleep(8); sys.exit(2)
    open(lk, "w").write(f"{os.getpid()} {datetime.datetime.now().isoformat()}")   # reservado ANTES de esperar
    waited = False
    while not TEST and ES.lock_alive(ES.LOCK):
        if not waited:
            print("\nEl estudio de las soluciones publicadas esta calculando en otra ventana (la licencia de ANSYS solo admite "
                  "una sesion). Esta ventana espera a que termine y despues continua sola...", flush=True)
            waited = True
        time.sleep(60)
    open(lk, "w").write(f"{os.getpid()} {datetime.datetime.now().isoformat()}")
    return lk


def main():
    global DISCORD, REPO_URL
    os.makedirs(ITD, exist_ok=True)
    lock = acquire_lock()
    git = GitSync(bool(USER.get("subir_a_github", True)) and not TEST)
    print("=" * 90)
    print(f"  OPTIMIZADOR GUIADO POR REGLAS  -  acero S235, carga {FORCE:.0f} N, limite {SIG_OBJ:.0f} MPa (CS >= {SY / SIG_OBJ:.2f})")
    print("  Se puede cerrar esta ventana en cualquier momento: al volver a abrirla continua donde iba.")
    print("=" * 90)
    import discord_notify, reglas as R, estudio_simjeb as ES
    DISCORD = discord_notify._Null() if TEST else discord_notify.make(ROOT, TOP, log)
    REPO_URL = _repo_url()
    st = load_state()
    final_state = "DETENIDO (al relanzar optimizar.bat continua)"
    try:
        # ---- 0. estudio de las soluciones publicadas -> reglas
        if USER.get("estudio_simjeb", True) and not TEST and ES.pending():
            log(f"ESTUDIO de las soluciones publicadas: quedan {len(ES.pending())} disenos por calcular con {FORCE:.0f} N")
            DISCORD.alert(f"Empieza (o continua) el estudio de las soluciones publicadas SimJEB con {FORCE:.0f} N: "
                          f"quedan {len(ES.pending())} disenos. Despues se sacan las reglas y empieza la optimizacion.")
            ES.run(notify=DISCORD if DISCORD.enabled else None, checkpoint=lambda msg: git.commit(msg))
        E = R.evidence(log)
        try:
            R.render_valid_images(E, log=log)
        except Exception as e:
            log(f"(imagenes del estudio: {e!r})")
        R.write_doc(E, st["stats"])
        rs = E.get("_resumen", {})
        if rs and not st.get("estudio_anunciado"):
            msg = (f"Estudio de las soluciones publicadas: {rs.get('n')} disenos calculados con {FORCE:.0f} N, {rs.get('valido')} cumplen. "
                   "Reglas de diseno actualizadas en DESIGN_RULES.md.")
            log(msg); DISCORD.alert(msg)
            git.commit("Estudio SimJEB y reglas de diseno (DESIGN_RULES.md)", msg)
            st["estudio_anunciado"] = True; save_state(st)
        # ---- 1. pieza de partida
        if not st.get("actual"):
            start(st, git)
        # ---- 2. iteraciones
        crash = 0
        while not st.get("fin"):
            if TEST and st["iter"] >= int(os.environ.get("PRUEBA_ITERACIONES", "3")):
                break
            try:
                step(st, git, E)
                crash = 0
            except KeyboardInterrupt:
                raise
            except Exception as e:
                crash += 1
                tb = traceback.format_exc()
                log(f"ERROR INESPERADO ({crash} seguidos): {e!r}")
                with open(os.path.join(TOP, "errores.log"), "a", encoding="utf-8") as fe:
                    fe.write(f"\n[{datetime.datetime.now():%Y-%m-%d %H:%M:%S}]\n{tb}")
                DISCORD.alert(f"Error inesperado ({crash} seguidos): `{e!r}`"[:1500] + "\nEl optimizador sigue; detalle en errores.log.")
                save_state(st)
                if crash >= 5:
                    raise
                time.sleep(20)
            if st["iter"] % int(USER.get("limpieza_cada_n_disenos", 10)) == 0:
                try:
                    cleanup(st)
                except Exception as e:
                    log(f"(limpieza: {e!r})")
        if st.get("fin"):
            log(f"OPTIMIZACION TERMINADA: {st['motivo_fin']}")
            if st.get("mejor") and (not st.get("verificado") or st["verificado"]["iter"] != st["mejor"]["iter"]):
                register_best(st, git, final=True)
            final_state = "TERMINADO: " + st["motivo_fin"]
            DISCORD.alert(f"**Optimizacion terminada.** {st['motivo_fin']}." + (
                f" Mejor diseno: {txt_m(st['mejor']['m'])}" if st.get("mejor") else " Ningun diseno cumple."))
    except KeyboardInterrupt:
        log("Detenido por el usuario. Progreso guardado: al relanzar continua donde iba.")
    finally:
        save_state(st)
        try:
            write_dashboard(st, final_state)
            if st.get("mejor"):
                notify_top(st)
        except Exception as e:
            log(f"(panel: {e!r})")
        git.commit(f"Estado: {final_state}", wait=True)
        try:
            DISCORD.flush(90)
        except Exception:
            pass
        try:
            os.remove(lock)
        except OSError:
            pass


if __name__ == "__main__":
    main()
