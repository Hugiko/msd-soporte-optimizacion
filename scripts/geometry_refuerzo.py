"""FAMILIA C: REFUERZO + VACIADO DEL ORIGINAL.

El punto debil del original esta junto a los alojamientos de los tornillos, donde el bloque tiene cavidades
interiores. Esta familia:
  1. RELLENA las cavidades interiores del original en un radio r_relleno alrededor de cada perno
     (material nuevo, siempre por debajo de la superficie exterior: no cambia la forma por fuera ni los
     alojamientos de las cabezas);
  2. aplica despues las mismas operaciones de VACIADO que la familia «vaciado» (hueco interior, recorte,
     alojamientos).
Idea: si se refuerza donde la tension es maxima, queda margen para quitar mucho mas material donde no trabaja.
"""
import os, json, math
import numpy as np
import cadquery as cq
import geometry as G
import geometry_vaciado as V

PARAMS = V.PARAMS + [
    ("r_relleno", 0.0, 22.0, 16.0, "radio alrededor de cada perno donde se rellenan las cavidades interiores (mm); 0 = nada"),
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])
GeometryError = G.GeometryError
export = G.export
VERSION = "refuerzo-v1-" + V.VERSION
CELL = 4.0            # tamano de las celdas del relleno (mm)
_CACHE = {}


def default_params():
    return {p[0]: p[3] for p in PARAMS}


def fill_closed_voids(solid):
    """Cavidades que han quedado CERRADAS (sin salida al exterior): se rellenan enteras. En impresion 3D el polvo
    atrapado no se podria sacar; en cualquier caso, una cavidad cerrada solo aporta problemas."""
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
    sols = sorted(solid.Solids(), key=lambda x: x.Volume(), reverse=True)
    return sols[0]


def filled_original(r):
    """Original con las cavidades interiores rellenas en un radio r alrededor de cada perno."""
    key = round(r * 2) / 2
    if key in _CACHE:
        return _CACHE[key]
    base = V.original()
    if key < 2.0:
        _CACHE[key] = base
        return base
    from shapely.geometry import box as sbox
    from shapely.ops import unary_union
    s, a, z = V.heightmap()
    cells = []                                     # (cuadrado en planta, altura maxima permitida)
    for b in G.BOLTS:
        bs, ba = b["sa"]
        for s0 in np.arange(bs - key, bs + key, CELL):
            for a0 in np.arange(ba - key, ba + key, CELL):
                sc, ac = s0 + CELL / 2, a0 + CELL / 2
                if math.hypot(sc - bs, ac - ba) > key:
                    continue
                ms = (s >= s0 - 1) & (s <= s0 + CELL + 1); ma = (a >= a0 - 1) & (a <= a0 + CELL + 1)
                sub = z[np.ix_(ma, ms)]
                if sub.size == 0 or np.isnan(sub).any():
                    continue                       # celda fuera de la pieza o sobre un agujero: no se toca
                top = float(np.min(sub)) - 0.6     # siempre por debajo de la superficie exterior
                if top > 1.0:
                    cells.append((sbox(s0, a0, s0 + CELL, a0 + CELL), top))
    if not cells:
        _CACHE[key] = base
        return base
    # relleno por CAPAS: cada capa es una sola region en planta extruida -> pocas caras, booleanas fiables
    STEP = 4.0
    slabs = []
    zmax = max(t for _, t in cells)
    zk = 0.3
    while zk < zmax - 0.2:
        z1 = min(zk + STEP, zmax)
        region = unary_union([c for c, t in cells if t >= z1 - 1e-6])
        if not region.is_empty:
            region = region.buffer(1.5, quad_segs=3).buffer(-1.5, quad_segs=3).simplify(0.5)   # contornos suaves: pocas caras
            for poly in G.polys(region, 4.0):
                slabs.append(G.prism(poly, G.SA, (0, 0, 1), z1 - zk, both=False).translate(cq.Vector(0, 0, zk)))
        zk = z1
    if not slabs:
        _CACHE[key] = base
        return base
    fill = slabs[0]
    for sl in slabs[1:]:
        fill = fill.fuse(sl)
    fill = V.to_global(fill.clean())
    solid = base.fuse(fill, tol=1e-4)
    if sum(x.Volume() for x in solid.Solids()) < base.Volume() - 1.0 or max(x.Volume() for x in solid.Solids()) < 0.9 * base.Volume():
        raise GeometryError("la union del relleno con el original ha fallado")
    for b in G.BOLTS:                               # agujeros de los pernos: se vuelven a tallar exactos
        solid = solid.cut(cq.Solid.makeCylinder(b["r"], G.Z1 - G.Z0 + 2, cq.Vector(b["c"][0], b["c"][1], G.Z0 - 1)), tol=1e-4)
    sols = sorted(solid.Solids(), key=lambda x: x.Volume(), reverse=True)
    solid = fill_closed_voids(sols[0])
    if solid.Volume() < base.Volume() - 1.0:
        raise GeometryError("el relleno ha perdido material del original")
    if not solid.isValid():
        raise GeometryError("el relleno de las cavidades no es valido")
    _CACHE[key] = solid
    return solid


def build(p):
    p = {k: float(p[k]) for k in NAMES}
    for k, lo, hi in zip(NAMES, LO, HI):
        if not (lo - 1e-9 <= p[k] <= hi + 1e-9):
            raise GeometryError(f"{k}={p[k]} fuera de [{lo}, {hi}]")
    base = filled_original(p["r_relleno"])
    solid, info = V.build(p, base=base)
    info["relleno_mm"] = p["r_relleno"]
    info["masa_relleno_kg"] = (base.Volume() - V.original().Volume()) * 7.85e-6
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
