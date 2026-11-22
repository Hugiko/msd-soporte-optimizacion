"""FAMILIA C: REFUERZO (COLLARES) + VACIADO DEL ORIGINAL.

El punto critico del original esta en el alojamiento de la cabeza del tornillo delantero (212,9 MPa de un limite
de 215: sin margen). Esta familia:
  1. anade un COLLAR cilindrico alrededor de cada alojamiento (material nuevo: rellena las cavidades interiores del
     original junto a los pernos y, si sobresale, forma una protuberancia). Prueba en ANSYS: con 6 mm de espesor el
     pico baja de 212,9 a 181,2 MPa (+159 g);
  2. con ese margen, aplica las operaciones de VACIADO de la familia «vaciado» (hueco interior, recorte, alojamientos)
     para quitar material donde no trabaja.
El optimizador decide cuanto reforzar (delante y detras por separado) y cuanto vaciar.
Version 2: formas simples y suaves (cilindros). La v1 (relleno escalonado) no se podia mallar.
"""
import os, json, math
import numpy as np
import cadquery as cq
import geometry as G
import geometry_vaciado as V

R_POCKET0 = 10.541            # radio del alojamiento del original
PARAMS = V.PARAMS + [
    ("t_col_del", 0.0, 9.0, 6.0, "espesor del collar en los 2 pernos delanteros (lado de la carga) (mm); 0 = sin collar"),
    ("t_col_tra", 0.0, 9.0, 4.0, "espesor del collar en los 2 pernos traseros (mm); 0 = sin collar"),
    ("z_col", 10.0, 26.0, 22.0, "altura del borde superior de los collares (mm)"),
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])
GeometryError = G.GeometryError
export = G.export
VERSION = "refuerzo-v2-collares-" + V.VERSION
FRONT = (0, 1)                # indices de los pernos delanteros en G.BOLTS (y ~ 0); traseros: 2, 3
_CACHE = {}


def default_params():
    return {p[0]: p[3] for p in PARAMS}


def fill_closed_voids(solid):
    """Cavidades que han quedado CERRADAS (sin salida al exterior) se rellenan enteras (polvo atrapado en impresion 3D)."""
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


def collared(t_f, t_r, z_top):
    """Original con collares cilindricos alrededor de los alojamientos de las cabezas de los tornillos."""
    key = (round(t_f, 1), round(t_r, 1), round(z_top, 1))
    if key in _CACHE:
        return _CACHE[key]
    base = V.original()
    solid = base
    for i, b in enumerate(G.BOLTS):
        t = key[0] if i in FRONT else key[1]
        if t < 0.5:
            continue
        x, y = b["c"]
        r_in = R_POCKET0 + 0.3          # 0,3 mm de holgura: no coincide con la pared del alojamiento (booleanas fiables)
        ring = cq.Solid.makeCylinder(r_in + t, key[2] - 1.0, cq.Vector(x, y, 1.0)).cut(
            cq.Solid.makeCylinder(r_in, key[2] + 1.0, cq.Vector(x, y, 0.0)))
        solid = solid.fuse(ring, tol=1e-4)
    sols = sorted(solid.Solids(), key=lambda q: q.Volume(), reverse=True)
    solid = fill_closed_voids(sols[0])
    if not solid.isValid() or solid.Volume() < base.Volume() - 1.0:
        raise GeometryError("la union de los collares con el original ha fallado")
    _CACHE[key] = solid
    return solid


def build(p):
    p = {k: float(p[k]) for k in NAMES}
    for k, lo, hi in zip(NAMES, LO, HI):
        if not (lo - 1e-9 <= p[k] <= hi + 1e-9):
            raise GeometryError(f"{k}={p[k]} fuera de [{lo}, {hi}]")
    base = collared(p["t_col_del"], p["t_col_tra"], p["z_col"])
    solid, info = V.build(p, base=base)
    info["masa_collares_kg"] = (base.Volume() - V.original().Volume()) * 7.85e-6
    return solid, info


if __name__ == "__main__":
    import sys, time
    p = default_params()
    for arg in sys.argv[1:]:
        k, v = arg.split("="); p[k] = float(v)
    t0 = time.time()
    s, info = build(p)
    os.makedirs(os.path.join(G.ROOT, "tests", "geom"), exist_ok=True)
    export(s, os.path.join(G.ROOT, "tests", "geom", "refuerzo.step"))
    print(json.dumps({k: v for k, v in info.items() if k != "clamped"}, indent=1, default=str), f"\n{time.time() - t0:.1f}s")
