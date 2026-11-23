"""FAMILIA D: DISENOS DE SIMJEB (los soportes del concurso de GE) + REFUERZO.

SimJEB (Whalen, Beyene, Mueller, 2021; doi:10.1111/cgf.14353) recoge ~380 disenos del GE Jet Engine Bracket Challenge,
todos en el MISMO sistema de coordenadas que nuestro 0.stp (el 0.stp del enunciado es el diseno n.o 0 de SimJEB) y con los
agujeros en las mismas posiciones. Su tabla da la tension maxima en el caso HORIZONTAL (37,8 kN), que es nuestro caso.

Candidatos: disenos mas ligeros que el original cuya tension horizontal, escalada con el factor medido en el original
(nuestra metrica / tension bruta SimJEB = 212,9 / 414,3), queda por debajo de ~260 MPa. Se ordenan de mas ligero a mas pesado.

Variables:
  semilla   : que diseno de SimJEB se usa (indice en la lista de candidatos; variable categorica)
  t_col_del : collar alrededor de los 2 pernos delanteros (refuerzo del punto critico habitual) (mm)
  t_col_tra : collar alrededor de los 2 pernos traseros (mm)
  z_col     : altura de los collares (mm)
Los agujeros de cada diseno se detectan en la malla (cada autor los modelo a su manera).
"""
import os, csv, json, math
import numpy as np
import cadquery as cq
import geometry as G

ROOT = G.ROOT
DATA = os.path.join(ROOT, "datos_simjeb")
STEP_DIR = os.path.join(DATA, "stp")
FACTOR = 212.9 / 414.3286          # nuestra metrica / tension bruta de SimJEB, medido en el original (diseno 0)
EST_MAX = 260.0                    # MPa estimados como maximo para entrar en la lista
VOL_ORIG = 307642.7


def _pool():
    """Lista determinista de candidatos (id SimJEB, volumen, tension estimada, categoria), de mas ligero a mas pesado."""
    path = os.path.join(DATA, "metadata.tab")
    out = []
    for r in csv.DictReader(open(path, encoding="utf-8", errors="ignore")):
        try:
            i, vol, hor = int(r["id"]), float(r["volume"]), float(r["max_hor_stress"])
        except (ValueError, KeyError):
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
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])
CATEGORICAL = ["semilla"]
GeometryError = G.GeometryError
export = G.export
VERSION = f"simjeb-v1-{K}candidatos"
FRONT = (0, 1)
R_HEAD = 10.84                     # holgura para cabeza/arandela del tornillo (como el alojamiento del original)
_CACHE = {}


def default_params():
    return {p[0]: p[3] for p in PARAMS}


def first_designs():
    """Torneo inicial: cada candidato tal cual (sin collares), en el cubo unidad."""
    return [[i / (K - 1), 0.0, 0.0, 0.5] for i in range(len(POOL))]


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
    for i, b in enumerate(G.BOLTS):
        t = p["t_col_del"] if i in FRONT else p["t_col_tra"]
        if t < 0.5:
            continue
        x, y = b["c"]
        ring = cq.Solid.makeCylinder(R_HEAD + t, p["z_col"] - 1.0, cq.Vector(x, y, 1.0)).cut(
            cq.Solid.makeCylinder(R_HEAD, p["z_col"] + 1.0, cq.Vector(x, y, 0.0)))
        solid = solid.fuse(ring, tol=1e-4)
    if solid is not base:
        sols = sorted(solid.Solids(), key=lambda s: s.Volume(), reverse=True)
        solid = sols[0]
        if not solid.isValid() or solid.Volume() < base.Volume() - 1.0:
            raise GeometryError("la union de los collares con el diseno ha fallado")
    if G.AM_ON and len(solid.Shells()) > 1:
        solid = _fill_closed_voids(solid)
        info["clamped"].append("cavidad cerrada rellenada (impresion 3D)")
    info.update(volume_mm3=solid.Volume(), mass_kg=solid.Volume() * 7.85e-6, pin_half_width=None,
                auto_interfaces=True, holes={"deteccion": "en la malla"}, simjeb_id=seed["id"],
                simjeb_categoria=seed["cat"], simjeb_autor=seed["autor"], simjeb_tension_estimada=round(seed["est"], 1))
    return solid, info


if __name__ == "__main__":
    print(f"{len(POOL)} candidatos de SimJEB:")
    for i, d in enumerate(POOL):
        print(f"  {i:3d}: SimJEB {d['id']:4d} {d['cat']:9s} {d['vol'] * 7.85e-6:.3f} kg acero | tension estimada {d['est']:.0f} MPa | {d['autor']}")
