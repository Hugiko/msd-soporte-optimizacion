"""FAMILIA D: DISENOS DE SIMJEB (los soportes del concurso de GE) + REFUERZO.

SimJEB (Whalen, Beyene, Mueller, 2021; doi:10.1111/cgf.14353) recoge ~380 disenos del GE Jet Engine Bracket Challenge,
todos en el MISMO sistema de coordenadas que nuestro 0.stp (el 0.stp del enunciado es el diseno n.o 0 de SimJEB) y con los
agujeros en las mismas posiciones. Su tabla da la tension maxima en el caso HORIZONTAL (37,8 kN), que es nuestro caso.

Candidatos: disenos mas ligeros que el original cuya tension horizontal, escalada con el factor medido en el original
(nuestra metrica / tension bruta SimJEB = 212,9 / 414,3), queda por debajo de ~260 MPa. Se ordenan de mas ligero a mas pesado.

Variables (MODIFICACIONES sobre el diseno elegido):
  semilla   : que diseno de SimJEB se usa (indice en la lista de candidatos; variable categorica)
  t_col_del : collar alrededor de los 2 pernos delanteros (refuerzo del punto critico habitual) (mm)  -> AnADE material
  t_col_tra : collar alrededor de los 2 pernos traseros (mm)                                           -> AnADE material
  z_col     : altura de los collares (mm)
  ali1_x, ali1_y, ali1_r ; ali2_x, ali2_y, ali2_r : dos ALIGERAMIENTOS (agujeros verticales pasantes, en la direccion
              de impresion: paredes verticales, sin voladizos ni polvo atrapado) donde la pieza no trabaja  -> QUITA material.
              Nunca tocan las zonas protegidas (alrededor de los 4 pernos y de las orejetas del bulon).
Los agujeros de cada diseno se detectan en la malla (cada autor los modelo a su manera).
"""
import os, csv, json, math
import numpy as np
import cadquery as cq
import geometry as G
import fem

ROOT = G.ROOT
DATA = os.path.join(ROOT, "datos_simjeb")
STEP_DIR = os.path.join(DATA, "stp")
FACTOR = 212.9 / 414.3286          # nuestra metrica / tension bruta de SimJEB, medido en el original (diseno 0)
EST_MAX = 260.0                    # MPa estimados como maximo para entrar en la lista
VOL_ORIG = 307642.7


COMPAT = os.path.join(DATA, "compatibilidad.json")   # comprobacion previa de los agujeros (python geometry_simjeb.py --comprobar)


def _pool():
    """Lista determinista de candidatos (id SimJEB, volumen, tension estimada, categoria), de mas ligero a mas pesado.
    Se excluyen los disenos cuyos agujeros NO son los del enunciado (bulon macizo, agujeros de perno agrandados...)."""
    path = os.path.join(DATA, "metadata.tab")
    comp = json.load(open(COMPAT, encoding="utf-8")) if os.path.exists(COMPAT) else {}
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8", errors="ignore")):
        try:
            i, vol, hor = int(r["id"]), float(r["volume"]), float(r["max_hor_stress"])
        except (ValueError, KeyError):
            continue
        if comp.get(str(i), {}).get("ok", True) is False:
            continue
        if hor * FACTOR <= EST_MAX and vol < VOL_ORIG and os.path.exists(os.path.join(STEP_DIR, f"{i}.stp")):
            out.append(dict(id=i, vol=vol, est=hor * FACTOR, cat=r.get("category", ""), autor=r.get("author", "")))
    out.sort(key=lambda d: (d["vol"], d["id"]))
    return out


POOL = _pool() if os.path.isdir(STEP_DIR) else []
K = max(len(POOL), 2)
PARAMS = [
    ("semilla", 0.0, float(K - 1), 0.0, "diseno de SimJEB usado como base (0 = el mas ligero de la lista)"),
    ("t_col_del", 0.0, 9.0, 0.0, "espesor del collar en los 2 pernos delanteros (mm); 0 = sin collar"),
    ("t_col_tra", 0.0, 9.0, 0.0, "espesor del collar en los 2 pernos traseros (mm); 0 = sin collar"),
    ("z_col", 8.0, 30.0, 18.0, "altura del borde superior de los collares (mm)"),
    ("ali1_x", -35.0, 62.0, 13.5, "aligeramiento 1: posicion x del agujero vertical pasante (mm)"),
    ("ali1_y", -158.0, 12.0, -73.0, "aligeramiento 1: posicion y (mm)"),
    ("ali1_r", 0.0, 10.0, 0.0, "aligeramiento 1: radio (mm); < 1,5 = sin agujero"),
    ("ali2_x", -35.0, 62.0, 13.5, "aligeramiento 2: posicion x (mm)"),
    ("ali2_y", -158.0, 12.0, -73.0, "aligeramiento 2: posicion y (mm)"),
    ("ali2_r", 0.0, 10.0, 0.0, "aligeramiento 2: radio (mm); < 1,5 = sin agujero"),
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])
CATEGORICAL = ["semilla"]
GeometryError = G.GeometryError
export = G.export
VERSION = f"simjeb-v2-{K}candidatos-aligeramientos"
FRONT = (0, 1)
R_HEAD = 10.84                     # holgura para cabeza/arandela del tornillo (como el alojamiento del original)
_CACHE = {}


def default_params():
    return {p[0]: p[3] for p in PARAMS}


def _sig_obj():
    try:
        c = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
        return float(c.get("sigma_y_MPa", 215.0)) * float(c.get("margen_optimizacion", 1.0))
    except Exception:
        return 187.0


def first_designs():
    """Torneo inicial: cada candidato TAL CUAL (sin collares ni aligeramientos), en el cubo unidad, del MAS PROMETEDOR
    al menos (primero los que segun SimJEB ya cumplirian, ordenados por masa x (tension/limite)^0,15)."""
    so = _sig_obj()
    order = sorted(range(len(POOL)), key=lambda i: (POOL[i]["est"] > so * 1.05,
                                                     POOL[i]["vol"] * 7.85e-6 * (POOL[i]["est"] / so) ** 0.15))
    return [[i / (K - 1), 0.0, 0.0, 0.5, 0.5, 0.5, 0.0, 0.5, 0.5, 0.0] for i in order]


def seed_info(p):
    return POOL[int(round(float(p["semilla"])))]


def _fill_closed_voids(solid):
    shells = solid.Shells()
    if len(shells) <= 1:
        return solid
    outer = max(shells, key=lambda sh: sh.BoundingBox().DiagonalLength)
    for sh in shells:
        if sh.isSame(outer):
            continue
        try:
            plug = cq.Solid.makeSolid(sh)
            if plug.Volume() < 0:
                plug = cq.Solid(plug.wrapped.Reversed())
            solid = solid.fuse(plug, tol=1e-4)
        except Exception:
            pass
    return sorted(solid.Solids(), key=lambda x: x.Volume(), reverse=True)[0]


_PROT = []


def protected():
    """Zonas que los aligeramientos NUNCA tocan: cilindros alrededor de los 4 pernos (alojamiento de la cabeza + 3 mm)
    y un cilindro alrededor del bulon que cubre las dos orejetas (radio del agujero + 6 mm)."""
    if not _PROT:
        s = None
        for b in G.BOLTS:
            c = cq.Solid.makeCylinder(R_HEAD + 3.0, 140.0, cq.Vector(b["c"][0], b["c"][1], -20.0))
            s = c if s is None else s.fuse(c)
        a = np.array(fem.HOLES["bulon"]["axis"], float); a /= np.linalg.norm(a)
        P = np.mean(np.array(fem.HOLES["bulon"]["centers"], float), axis=0)
        st = P - 26.0 * a
        pin = cq.Solid.makeCylinder(G.RP + 6.0, 52.0, cq.Vector(*st), cq.Vector(*a))
        _PROT.append(s.fuse(pin))
    return _PROT[0]


def _boolean(op, vol_ok, what, split_msg=None):
    """Booleana robusta: prueba tolerancias difusas crecientes hasta obtener UN solido valido con un volumen coherente.
    Si el resultado se parte en dos trozos grandes (> 1 %), es la geometria la que se parte: error (split_msg)."""
    last = "sin resultado"
    for tol in (1e-4, 1e-3, 1e-2, 0.05):
        try:
            res = op(tol)
        except Exception as e:
            last = f"{type(e).__name__}"; continue
        sols = sorted(res.Solids(), key=lambda q: q.Volume(), reverse=True)
        if not sols:
            last = "sin solidos"; continue
        big, rest = sols[0], [q.Volume() for q in sols[1:]]
        if split_msg and rest and rest[0] > 0.01 * big.Volume() and big.isValid() and vol_ok(big.Volume() + sum(rest)):
            raise GeometryError(split_msg)
        if big.isValid() and sum(rest) < 1.0 and vol_ok(big.Volume()):
            return big
        last = f"{len(sols)} solidos, resto {sum(rest):.0f} mm3"
    raise GeometryError(f"{what} ha fallado ({last})")


def _load(idx):
    if idx not in _CACHE:
        sid = POOL[idx]["id"]
        shp = cq.importers.importStep(os.path.join(STEP_DIR, f"{sid}.stp")).val()
        sols = sorted(shp.Solids(), key=lambda s: s.Volume(), reverse=True)
        if not sols:
            raise GeometryError(f"SimJEB {sid}: el archivo no contiene un solido")
        _CACHE.clear()                      # solo se guarda el ultimo (los STEP pueden ser grandes)
        _CACHE[idx] = sols[0]
    return _CACHE[idx]


def build(p):
    p = {k: float(p[k]) for k in NAMES}
    for k, lo, hi in zip(NAMES, LO, HI):
        if not (lo - 1e-9 <= p[k] <= hi + 1e-9):
            raise GeometryError(f"{k}={p[k]} fuera de [{lo}, {hi}]")
    if not POOL:
        raise GeometryError("no estan descargados los disenos de SimJEB (datos_simjeb/)")
    idx = int(round(p["semilla"]))
    seed = POOL[idx]
    base = _load(idx)
    solid = base
    info = {"clamped": [], "hueco": False}
    rings = []
    for i, b in enumerate(G.BOLTS):
        t = p["t_col_del"] if i in FRONT else p["t_col_tra"]
        if t < 0.5:
            continue
        x, y = b["c"]
        rings.append(cq.Solid.makeCylinder(R_HEAD + t, p["z_col"] - 1.0, cq.Vector(x, y, 1.0)).cut(
            cq.Solid.makeCylinder(R_HEAD, p["z_col"] + 1.0, cq.Vector(x, y, 0.0))))
    if rings:
        # las superficies de muchos disenos SimJEB son tipo malla (B-spline): las booleanas de OCC son fragiles.
        # Se unen todos los collares a la vez y, si sale mal, se repite con tolerancia difusa creciente.
        v_add = sum(r.Volume() for r in rings)
        solid = _boolean(lambda tol: base.fuse(*rings, tol=tol),
                         lambda v: base.Volume() - 1.0 <= v <= base.Volume() + v_add + 1.0, "la union de los collares")
    if G.AM_ON and len(solid.Shells()) > 1:
        solid = _fill_closed_voids(solid)
        info["clamped"].append("cavidad cerrada rellenada (impresion 3D)")
    n_ali = 0
    for k in (1, 2):
        r = p[f"ali{k}_r"]
        if r < 1.5:
            continue
        tool = cq.Solid.makeCylinder(r, 140.0, cq.Vector(p[f"ali{k}_x"], p[f"ali{k}_y"], -20.0)).cut(protected())
        if tool.Volume() < 1.0:
            info["clamped"].append(f"aligeramiento {k} entero dentro de zona protegida: no se aplica")
            continue
        v0 = solid.Volume()
        new = _boolean(lambda tol, sol=solid, tl=tool: sol.cut(tl, tol=tol), lambda v, v0=v0: v <= v0 + 1.0,
                       f"el aligeramiento {k}", split_msg=f"el aligeramiento {k} parte la pieza en dos")
        if v0 - new.Volume() > 1.0:
            n_ali += 1
        solid = new
    info["aligeramientos"] = n_ali
    info.update(volume_mm3=solid.Volume(), mass_kg=solid.Volume() * 7.85e-6, pin_half_width=None,
                auto_interfaces=True, holes={"deteccion": "en la malla"}, simjeb_id=seed["id"],
                simjeb_categoria=seed["cat"], simjeb_autor=seed["autor"], simjeb_tension_estimada=round(seed["est"], 1))
    return solid, info


def check_pool():
    """Malla cada candidato tal cual y comprueba que se reconocen los 4 agujeros de perno (M10) y el del bulon.
    Guarda el resultado en datos_simjeb/compatibilidad.json (se hace una vez)."""
    import time
    from evaluate import mesh_with_timeout
    comp = json.load(open(COMPAT, encoding="utf-8")) if os.path.exists(COMPAT) else {}
    tmp = os.path.join(DATA, "_comprobacion"); os.makedirs(tmp, exist_ok=True)
    for k, d in enumerate(POOL):
        if str(d["id"]) in comp:
            continue
        t0 = time.time()
        try:
            p = default_params(); p["semilla"] = k
            sol, _ = build(p); st = os.path.join(tmp, "c.step"); export(sol, st)
            nodes, tets, tris = mesh_with_timeout(st, 4.0, 1.0, 10, False, logfile=None, timeout=90)
            fem.IFACE = fem.detect_interfaces(nodes, tris)
            inf = fem.write_inp(os.path.join(tmp, "c.inp"), nodes, tets, tris, force=37800.0, pin_half=None)
            comp[str(d["id"])] = dict(ok=True, nodos=len(nodes), pernos=inf["nodes_per_bolt"], orejetas=inf["nodes_per_lug"])
        except fem.InterfaceError as e:
            comp[str(d["id"])] = dict(ok=False, motivo=str(e))
        except Exception as e:                     # fallo de malla: no se excluye (el optimizador lo reintentara)
            comp[str(d["id"])] = dict(ok=None, motivo=f"{type(e).__name__}: {e}"[:200])
        finally:
            fem.IFACE = None
        print(f"  {k + 1:2d}/{len(POOL)} SimJEB {d['id']:4d}: {comp[str(d['id'])]} ({time.time() - t0:.0f} s)", flush=True)
        json.dump(comp, open(COMPAT, "w", encoding="utf-8"), indent=1)
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return comp


if __name__ == "__main__":
    import sys
    if "--comprobar" in sys.argv:
        check_pool()
        sys.exit(0)
    print(f"{len(POOL)} candidatos de SimJEB:")
    for i, d in enumerate(POOL):
        print(f"  {i:3d}: SimJEB {d['id']:4d} {d['cat']:9s} {d['vol'] * 7.85e-6:.3f} kg acero | tension estimada {d['est']:.0f} MPa | {d['autor']}")
