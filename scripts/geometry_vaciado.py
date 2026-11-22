"""FAMILIA B: VACIADO DEL ORIGINAL.

Se parte del soporte original (0.stp), que ya esta en el limite de tension, y se le quita material
donde casi no trabaja (zonas azules del mapa de von Mises):
  1. HUECO interior cerrado (caja con TODAS las aristas redondeadas) en el bloque.
  2. RECORTE del bloque por el lado alejado de las orejetas (plano inclinado, herramienta redondeada).
Las herramientas de corte son solidos convexos con todas sus aristas redondeadas (el fillet 3D de OCC
es fiable en solidos convexos): la pieza resultante no tiene esquinas vivas entrantes nuevas.
Los cortes nunca alcanzan las orejetas ni los alojamientos de los pernos (limites + mapa de alturas),
y los 6 agujeros se verifican en cada diseno.
"""
import os, json, math
import numpy as np
import cadquery as cq
import geometry as G          # reutiliza sistema local, verificacion de agujeros y exportacion

ROOT = G.ROOT
STEP0 = os.path.join(ROOT, "cad", "0.stp")
HMAP = os.path.join(ROOT, "cad", "mapa_alturas_original.npz")
T_MIN = 3.0                   # espesor minimo de pared que debe quedar sobre el hueco (mm)
VERSION = "vaciado-v4-" + (f"impresion3d-{G.AM_ANGLE:g}" if G.AM_ON else "libre")   # cambia si cambia la geometria: los resultados antiguos se archivan

PARAMS = [  # nombre, min, max, valor por defecto, descripcion
    ("cav_s0", 15.0, 45.0, 25.0, "inicio del hueco interior en la direccion de la carga (mm, desde el bulon)"),
    ("cav_len", 10.0, 65.0, 40.0, "longitud del hueco en la direccion de la carga (mm)"),
    ("cav_a", 8.0, 52.0, 35.0, "semiancho del hueco a lo largo del bulon (mm)"),
    ("cav_z0", 5.0, 12.0, 6.0, "cota del suelo del hueco = espesor de la base bajo el hueco (mm)"),
    ("cav_z1", 12.0, 45.0, 30.0, "cota del techo del hueco (mm); se limita para dejar 3 mm de pared"),
    ("trim_s0", 20.0, 75.0, 50.0, "inicio del recorte superior del lado alejado (mm)"),
    ("trim_z", 8.0, 45.0, 30.0, "altura del plano de recorte al inicio (mm)"),
    ("trim_ang", 0.0, 35.0, 15.0, "inclinacion del plano de recorte, bajando hacia los pernos (grados)"),
    ("trim_a", 20.0, 55.0, 45.0, "semiancho del recorte a lo largo del bulon (mm)"),
    ("r_cut", 2.0, 6.0, 4.0, "radio de redondeo de huecos y recortes (mm)"),
    ("R_pocket", 10.54, 12.0, 10.54, "radio del alojamiento de cabeza (original 10,54); mayor = acuerdo de fondo mayor (R-8), menos concentracion"),
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])
GeometryError = G.GeometryError
export = G.export
_ORIG = None


def default_params():
    return {p[0]: p[3] for p in PARAMS}


def original():
    global _ORIG
    if _ORIG is None:
        _ORIG = cq.importers.importStep(STEP0).val()
    return _ORIG


def heightmap():
    """Altura de la cara superior del original sobre una rejilla (s, a) local. Se calcula una vez."""
    if os.path.exists(HMAP):
        d = np.load(HMAP)
        return d["s"], d["a"], d["z"]
    import pyvista as pv
    import render
    mesh = render.step_to_polydata(STEP0, tol=0.1)
    s = np.arange(-25, 96, 2.0); a = np.arange(-92, 93, 2.0)
    z = np.full((len(a), len(s)), np.nan)
    c, sn = math.cos(math.radians(G.THETA)), math.sin(math.radians(G.THETA))
    for i, aa in enumerate(a):
        for j, ss in enumerate(s):
            x = G.P0[0] + c * ss - sn * aa; y = G.P0[1] + sn * ss + c * aa
            pts, _ = mesh.ray_trace((x, y, 200.0), (x, y, -50.0), first_point=True)
            if len(pts):
                z[i, j] = pts[2]
    np.savez(HMAP, s=s, a=a, z=z)
    return s, a, z


def min_height(s0, s1, a0, a1, margin=3.0):
    s, a, z = heightmap()
    ms = (s >= s0 - margin) & (s <= s1 + margin); ma = (a >= a0 - margin) & (a <= a1 + margin)
    sub = z[np.ix_(ma, ms)]
    if np.isnan(sub).any():
        return -1.0          # el hueco se saldria de la planta de la pieza
    return float(np.min(sub))


def rounded(solid, r):
    for rr in (r, 0.7 * r, 0.45 * r):
        try:
            f = solid.fillet(rr, solid.Edges())
            if f.isValid():
                return f
        except Exception:
            pass
    raise GeometryError("no se pudo redondear la herramienta de corte")


def hip_cavity(s0, s1, ha, z0, z1):
    """Hueco con techo a cuatro aguas (45 grados): caja INTERSECCION dos 'tiendas' triangulares.
    Todas las caras del techo forman 45 con la horizontal -> se imprime sin soportes."""
    Ls = s1 - s0
    box = cq.Solid.makeBox(Ls, 2 * ha, z1 - z0, cq.Vector(s0, -ha, z0))
    w1 = cq.Wire.makePolygon([cq.Vector(s0, -ha - 5, z0 - 1), cq.Vector(s1, -ha - 5, z0 - 1),
                              cq.Vector(s1, -ha - 5, z0), cq.Vector((s0 + s1) / 2, -ha - 5, z0 + Ls / 2 * G.AM_T),
                              cq.Vector(s0, -ha - 5, z0)], close=True)
    tent_s = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w1), cq.Vector(0, 2 * ha + 10, 0))
    w2 = cq.Wire.makePolygon([cq.Vector(s0 - 5, -ha, z0 - 1), cq.Vector(s0 - 5, ha, z0 - 1),
                              cq.Vector(s0 - 5, ha, z0), cq.Vector(s0 - 5, 0, z0 + ha * G.AM_T),
                              cq.Vector(s0 - 5, -ha, z0)], close=True)
    tent_a = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w2), cq.Vector(Ls + 10, 0, 0))
    return box.intersect(tent_s).intersect(tent_a)


def to_global(sh):
    return sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), G.THETA).translate(cq.Vector(G.P0[0], G.P0[1], 0))


def build(p, base=None):
    p = {k: float(p[k]) for k in NAMES}
    for k, lo, hi in zip(NAMES, LO, HI):
        if not (lo - 1e-9 <= p[k] <= hi + 1e-9):
            raise GeometryError(f"{k}={p[k]} fuera de [{lo}, {hi}]")
    r = p["r_cut"]
    info = {"clamped": [], "hueco": False, "recorte": False}
    solid = original() if base is None else base

    # ---- recorte superior del lado alejado (prisma convexo redondeado)
    s0, zt, ang, at = p["trim_s0"], p["trim_z"], math.radians(p["trim_ang"]), p["trim_a"]
    S1 = 140.0
    zend = zt - (S1 - s0) * math.tan(ang)
    prof = [(s0, zt), (S1, zend), (S1, 120.0), (s0, 120.0)]
    wire = cq.Wire.makePolygon([cq.Vector(x, -at, z) for x, z in prof], close=True)
    tool = cq.Solid.extrudeLinear(cq.Face.makeFromWires(wire), cq.Vector(0, 2 * at, 0))
    tool = to_global(rounded(tool, r))
    v0 = solid.Volume()
    cut = solid.cut(tool, tol=1e-4)      # booleana difusa: sin ella OCC falla en silencio con el original
    if cut.isValid() and cut.Volume() < v0 - 1.0:
        solid = cut; info["recorte"] = True

    # ---- hueco interior cerrado (caja redondeada), siempre con >= 3 mm de pared encima
    cs0, cl, ca, cz0, cz1 = p["cav_s0"], p["cav_len"], p["cav_a"], p["cav_z0"], p["cav_z1"]
    cs1 = min(cs0 + cl, 86.0)
    top = min_height(cs0, cs1, -ca, ca)
    if info["recorte"]:          # techo tras el recorte (plano) dentro de su huella
        if cs1 > s0 and ca + 3 > 0:
            top = min(top, zt - (min(cs1 + 3, S1) - s0) * math.tan(ang)) if cs1 + 3 > s0 else top
    lim = top - T_MIN
    if cz1 > lim:
        info["clamped"].append(f"techo del hueco {cz1:.1f}->{lim:.1f} mm (pared minima {T_MIN} mm)")
        cz1 = lim
    # FABRICACION ADITIVA: techo a cuatro aguas con pendientes de 45 (autoportante) y parte plana <= 3 mm
    hc = cz1 - cz0
    wmax = 2 * hc / G.AM_T + 3.0 if G.AM_ON else 1e9   # techo con la pendiente minima de voladizo (solo impresion 3D)
    if cs1 - cs0 > wmax:
        info["clamped"].append(f"hueco acortado {cs1 - cs0:.1f}->{wmax:.1f} mm (techo a 45 para impresion 3D)")
        cs1 = cs0 + wmax
    if 2 * ca > wmax:
        info["clamped"].append(f"hueco estrechado {2 * ca:.1f}->{wmax:.1f} mm (techo a 45 para impresion 3D)")
        ca = wmax / 2
    if hc >= 2 * r + 1.0 and cs1 - cs0 >= 2 * r + 2.0 and 2 * ca >= 2 * r + 2.0:
        cav = hip_cavity(cs0, cs1, ca, cz0, cz1) if G.AM_ON else \
            cq.Solid.makeBox(cs1 - cs0, 2 * ca, cz1 - cz0, cq.Vector(cs0, -ca, cz0))
        cav = to_global(rounded(cav, r))
        cut2 = solid.cut(cav, tol=1e-4)
        if not cut2.isValid() or cut2.Volume() > solid.Volume() - 1.0:
            raise GeometryError("el corte del hueco no es valido")
        # agujero de evacuacion del polvo (D5) desde el suelo del hueco hasta la cara inferior
        drain = to_global(cq.Solid.makeCylinder(2.5, cz0 + 2.0, cq.Vector((cs0 + cs1) / 2, 0.0, -1.0)))
        cut3 = cut2.cut(drain, tol=1e-4)
        if G.AM_ON and cut3.isValid():
            cut2 = cut3; info["drenajes"] = 1
        solid = cut2; info["hueco"] = True
    else:
        info["clamped"].append("hueco demasiado pequeno -> no se hace")

    # ---- remodelado de los alojamientos de cabeza (zona critica del original): pozo mayor con acuerdo de fondo mayor
    Rk = p["R_pocket"]
    if Rk > 10.7:
        from shapely.geometry import Point as SPt, box as sbox
        rp = Rk - 8.0                               # asiento plano hasta r = 8 mm (como el original)
        for b in G.BOLTS:
            corner = sbox(Rk - rp, G.Z1 - 0.01, Rk + 0.01, G.Z1 + rp).difference(
                SPt(Rk - rp, G.Z1 + rp).buffer(rp, quad_segs=4 * G.QS))
            tool = to_global(G.revolve_z(sbox(0, G.Z1, Rk, G.Z1 + 120).difference(corner), b["sa"][0], b["sa"][1]))
            cut3 = solid.cut(tool, tol=1e-4)
            if not cut3.isValid():
                raise GeometryError("el remodelado del alojamiento no es valido")
            solid = cut3
        info["alojamientos"] = f"R={Rk:.2f}, acuerdo {rp:.2f} mm"
    sols = sorted(solid.Solids(), key=lambda s: s.Volume(), reverse=True)
    if len(sols) > 1 and sum(s.Volume() for s in sols[1:]) < 1e-3 * sols[0].Volume():
        info["clamped"].append(f"eliminadas {len(sols) - 1} virutas sueltas"); solid = sols[0]
    if len(solid.Solids()) != 1:
        raise GeometryError(f"la pieza no es un unico solido ({len(solid.Solids())} trozos)")
    if not solid.isValid():
        raise GeometryError("solido no valido tras las operaciones booleanas")
    if G.AM_ON and len(solid.Shells()) > 1:
        raise GeometryError("impresion 3D: queda una cavidad cerrada sin salida para el polvo")
    info.update(volume_mm3=solid.Volume(), mass_kg=solid.Volume() * 7.85e-6, pin_half_width=3.2)
    info["holes"] = G.check_holes(solid, 6.35)
    return solid, info


if __name__ == "__main__":
    import sys, time
    p = default_params()
    for arg in sys.argv[1:]:
        k, v = arg.split("="); p[k] = float(v)
    t0 = time.time()
    s, info = build(p)
    os.makedirs(os.path.join(ROOT, "tests", "geom"), exist_ok=True)
    export(s, os.path.join(ROOT, "tests", "geom", "vaciado.step"))
    print(json.dumps(info, indent=1), f"\n{time.time() - t0:.1f}s")
