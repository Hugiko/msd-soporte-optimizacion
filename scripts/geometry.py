"""Geometria parametrica del soporte con cadquery + shapely (version 2: extremos tipo original).

Idea estructural (carga horizontal perpendicular al bulon, aplicada a ~45 mm de altura):
  la fuerza crea un momento de vuelco que viaja como TORSION por el puente que une la fila
  delantera y la trasera de pernos -> seccion cerrada (cajon, opcionalmente hueco).
  Como en el soporte original, los pernos quedan en una FRANJA PLANA en cada extremo (asiento de
  arandela a la cota del original) y el cajon arranca detras con paredes INCLINADAS.

Sistema local: s = direccion de la carga, a = eje del bulon, z = vertical (z del STEP).
Construccion:
  cuerpo = prisma(seccion s-z) INTERSECCION prisma(alzado a-z)
     seccion s-z : trapecio del cajon + orejeta (envolvente circulo-pie) + pestana de la base
     alzado  a-z : trapecio con extremos inclinados (angulo phi_end) + columnas de orejetas + pestana
  - hueco interior opcional (pared t_w), dividido por las orejetas que bajan como almas
  - vaciados pasantes en la pestana fuera del marco (barras a los pernos, anillos de perno)
  - alojamientos de cabeza/arandela como en el original y los 6 agujeros fijos
Todos los acuerdos entrantes se generan en 2D con un cierre morfologico (buffer +r, -r):
no hay esquinas vivas entrantes ni dependencia del fillet 3D de OCC.
"""
import os, json, math
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon, LineString, Point, box as sbox
from shapely.ops import unary_union, nearest_points

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = json.load(open(os.path.join(ROOT, "cad", "agujeros_fijos.json")))

Z0, Z1 = H["pernos_z"]                 # cara inferior y asiento de arandela (cotas del original)
ZC = H["bulon"]["centers"][0][2]       # altura del eje del bulon
RP = H["bulon"]["r"]                   # radio agujero bulon
AX = np.array(H["bulon"]["axis"]) / np.linalg.norm(H["bulon"]["axis"])
DX = np.array([AX[1], -AX[0], 0.0])    # horizontal perpendicular al bulon
THETA = math.degrees(math.atan2(DX[1], DX[0]))
P0 = np.mean(np.array(H["bulon"]["centers"])[:, :2], axis=0)   # punto medio entre orejetas (xy)
CLEAR = 5.4                            # alojamiento cabeza/arandela: r = R + 5,4 = 10,54 mm (como el original)
QS = 6                                 # segmentos por cuarto de circulo en los perfiles 2D
try:   # reglas de impresion 3D (opcionales) y angulo minimo de voladizo (docs/fabricacion_aditiva.md)
    _cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
except Exception:
    _cfg = {}
AM_ON = bool(_cfg.get("reglas_impresion_3d", False))
AM_ANGLE = float(_cfg.get("angulo_voladizo_deg", 45.0))
VERSION = "cero-v7-" + (f"impresion3d-{AM_ANGLE:g}" if AM_ON else "libre")   # si cambia, se archivan los resultados antiguos
AM_T = math.tan(math.radians(AM_ANGLE))   # cambia si cambia la geometria: los resultados antiguos se archivan


def to_local(xy):
    v = np.asarray(xy, float) - P0
    c, s = math.cos(math.radians(THETA)), math.sin(math.radians(THETA))
    return np.array([c * v[0] + s * v[1], -s * v[0] + c * v[1]])


BOLTS = [dict(sa=to_local(b["c"]), r=b["r"], c=b["c"]) for b in H["pernos"]]
LUG_A = [float(to_local(c[:2])[1]) for c in H["bulon"]["centers"]]   # coord. a de cada orejeta
A_BOLT = min(abs(b["sa"][1]) for b in BOLTS)                          # ~74 mm
R_BOLT = max(b["r"] for b in BOLTS)

# --------------------------------------------------------------------------- parametros
PARAMS = [  # nombre, min, max, valor por defecto, descripcion
    ("R_pocket", 10.54, 16.0, 10.54, "radio del pozo de cabeza (mm); asiento plano hasta r=8 y acuerdo R_pocket-8 (original: 10,54 / 2,54)"),
    ("w_bar", 8.0, 30.0, 16.0, "ancho de las barras de la base hacia los pernos (mm)"),
    ("phi_end", 25.0, 85.0, 60.0, "inclinacion de las paredes extremas del cajon (grados)"),
    ("H", 14.0, 30.0, 26.0, "altura del cajon hasta el techo (mm)"),
    ("W_top", 14.0, 40.0, 28.0, "ancho del techo del cajon / pie de orejeta (mm)"),
    ("W_bot", 34.0, 95.0, 70.0, "ancho inferior del cajon en la direccion de la carga (mm)"),
    ("x_box", 0.0, 40.0, 25.0, "desplazamiento del cajon hacia los pernos (mm)"),
    ("g_end", -12.0, 20.0, 0.0, "pie de la pared extrema respecto al borde del alojamiento (mm); <0 = bloque con pozos tallados, como el original"),
    ("t_w", 2.5, 12.0, 5.0, "espesor de pared del cajon (mm); grande = macizo"),
    ("e_lug", 4.0, 14.0, 9.0, "material de la orejeta alrededor del agujero (mm)"),
    ("t_lug", 6.35, 14.0, 9.0, "espesor de cada orejeta (mm)"),
    ("r_f", 2.0, 7.0, 4.0, "radio de los acuerdos (mm); el pie de orejeta usa 2,5 r_f"),
]
NAMES = [p[0] for p in PARAMS]
LO = np.array([p[1] for p in PARAMS]); HI = np.array([p[2] for p in PARAMS])


def default_params():
    return {p[0]: p[3] for p in PARAMS}


class GeometryError(Exception):
    pass


# --------------------------------------------------------------------------- utilidades 2D
def closing(geom, r):
    """Rellena las esquinas entrantes con acuerdos de radio r (las salientes quedan igual)."""
    return geom.buffer(r, quad_segs=QS).buffer(-r, quad_segs=QS)


def opening(geom, r):
    """Redondea las esquinas salientes con radio r."""
    return geom.buffer(-r, quad_segs=QS).buffer(r, quad_segs=QS)


def largest(geom):
    if geom.is_empty:
        return geom
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        polys = [g for g in geom.geoms if g.geom_type == "Polygon"]
        return max(polys, key=lambda g: g.area) if polys else Polygon()
    return geom


def polys(geom, min_area=1.0):
    if geom.is_empty:
        return []
    gs = geom.geoms if hasattr(geom, "geoms") else [geom]
    return [g for g in gs if g.geom_type == "Polygon" and g.area > min_area]


def tent45(poly, z_floor, min_half=3.0):
    """Mayor triangulo con lados a 45 grados (techo autoportante para impresion 3D) apoyado en el suelo
    z_floor y contenido en poly. Devuelve None si no cabe uno util."""
    if poly.is_empty:
        return None
    strip = poly.intersection(sbox(-1e4, z_floor - 0.01, 1e4, z_floor + 0.6))
    if strip.is_empty:
        return None
    x0, _, x1, _ = strip.bounds
    c = 0.5 * (x0 + x1)
    big = poly.buffer(1e-3)
    lo, hi = 0.0, 0.5 * (x1 - x0)
    for _ in range(30):
        w = 0.5 * (lo + hi)
        tri = Polygon([(c - w, z_floor), (c + w, z_floor), (c, z_floor + w * AM_T)])
        if big.contains(tri):
            lo = w
        else:
            hi = w
    if lo < min_half:
        return None
    return Polygon([(c - lo, z_floor), (c + lo, z_floor), (c, z_floor + lo * AM_T)])


def clean_coords(coords, tol=0.02):
    """Quita puntos duplicados/consecutivos casi coincidentes (aristas de longitud ~0 rompen OCC)."""
    pts = [tuple(c) for c in coords]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    out = []
    for p in pts:
        if not out or math.dist(p, out[-1]) > tol:
            out.append(p)
    while len(out) > 3 and math.dist(out[0], out[-1]) <= tol:
        out.pop()
    if len(out) < 3:
        raise GeometryError("perfil 2D degenerado")
    return out


def prep(poly):
    poly = poly.simplify(0.01)
    if not poly.is_valid:
        poly = poly.buffer(0)
    return largest(poly)


def _wire(coords, map3):
    pts = [cq.Vector(*map3(x, y)) for x, y in clean_coords(list(coords))]
    return cq.Wire.makePolygon(pts, close=True)


def prism(poly, map3, direction, length, both=True):
    """Extruye un poligono 2D (con agujeros) mapeado a 3D por map3 a lo largo de direction."""
    poly = prep(poly)
    outer = _wire(poly.exterior.coords, map3)
    inner = [_wire(i.coords, map3) for i in poly.interiors if Polygon(i).area > 1.0]
    face = cq.Face.makeFromWires(outer, inner)
    d = cq.Vector(*direction)
    if both:
        face = face.translate(d * (-length))
        return cq.Solid.extrudeLinear(face, d * (2 * length))
    return cq.Solid.extrudeLinear(face, d * length)


def revolve_z(poly2d, cx, cy):
    """Solido de revolucion alrededor del eje vertical (cx, cy) a partir de un perfil (r, z)."""
    pts = clean_coords(list(prep(poly2d).exterior.coords))
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val() \
        .translate(cq.Vector(cx, cy, 0))


# planos locales: (s,z) extruido en a ; (a,z) extruido en s ; (s,a) extruido en z
SZ = lambda u, v: (u, 0.0, v)
AZ = lambda u, v: (0.0, u, v)
SA = lambda u, v: (u, v, 0.0)


# --------------------------------------------------------------------------- construccion
def build(p):
    """Devuelve (solido cadquery en coordenadas globales del STEP, info dict)."""
    p = {k: float(p[k]) for k in NAMES}
    for k, lo, hi in zip(NAMES, LO, HI):
        if not (lo - 1e-9 <= p[k] <= hi + 1e-9):
            raise GeometryError(f"{k}={p[k]} fuera de [{lo}, {hi}]")
    Rpk, wbar, phi, Hh, Wt, Wb, xb, g, tw, e, tl, r = (p[k] for k in NAMES)
    zb = Z1                      # suelo del hueco interior = cota del asiento (fondo de 7,22 mm)
    zr = Z0 + Hh                 # techo del cajon
    Ro = RP + e                  # radio exterior de la orejeta
    a_lug = max(abs(a) for a in LUG_A)
    R_SEAT = 8.0                 # asiento plano hasta r = 8,0 mm (medido en 0.stp: cabeza D16)
    rp = max(0.3, Rpk - R_SEAT)  # acuerdo del fondo del alojamiento (fuera del asiento)
    Rc = Rpk                     # radio del alojamiento
    info = {"clamped": []}

    # ---- restricciones geometricas que se corrigen (y se registran) en vez de fallar
    zr_max = ZC - RP - max(4.0, r + 1.5)          # el acuerdo orejeta-techo no puede invadir el agujero
    if zr > zr_max:
        info["clamped"].append(f"H {Hh:.2f}->{zr_max - Z0:.2f} (techo bajo el agujero)")
        zr = zr_max
    if zr < Z1 + 6.0:
        zr = Z1 + 6.0
        info["clamped"].append("H elevado a asiento+6")
    A = min(A_BOLT, A_BOLT - Rc - g)              # pie de la pared extrema SOBRE la franja (cota Z1)
    A_need = a_lug + tl / 2 + r + 2.0             # el techo debe sostener las dos orejetas
    A_top = A - (zr - Z1) / math.tan(math.radians(phi))
    if A_top < A_need:
        info["clamped"].append(f"pared extrema mas vertical (techo {A_top:.1f}->{A_need:.1f} mm)")
        A_top = min(A_need, A - 1.0)
    if A_top <= 0 or A < A_need:
        raise GeometryError(f"el cajon no cabe entre las orejetas y los pernos (A={A:.1f})")

    # extension en s de la pestana: cubre el cajon y las filas de pernos
    Rb = R_BOLT + max(5.0, wbar / 2)
    s_b = [b["sa"][0] for b in BOLTS]
    s0, s1 = xb - Wb / 2 - 2 * r, xb + Wb / 2 + 2 * r
    s_lo, s_hi = min(s0, min(s_b) - Rb) - 2, max(s1, max(s_b) + Rb) + 2
    a_hi = A_BOLT + Rb + 2

    # ---- prisma 1: seccion s-z
    trap1 = Polygon([(xb - Wb / 2, Z0), (xb + Wb / 2, Z0), (Wt / 2, zr), (-Wt / 2, zr)])
    if not trap1.is_valid or trap1.area < 50:
        raise GeometryError("seccion del cajon degenerada")
    lug = unary_union([Point(0, ZC).buffer(Ro, quad_segs=4 * QS),
                       LineString([(-Wt / 2, zr - 0.5), (Wt / 2, zr - 0.5)])]).convex_hull
    r_foot = 2.5 * r             # acuerdo del pie de orejeta (zona critica a flexion en su plano)
    flange1 = sbox(s_lo, Z0, s_hi, Z1)
    P1 = largest(closing(closing(unary_union([trap1, lug]), r_foot).union(flange1), r))
    # ---- prisma 2: alzado a-z
    a_bot = A + (Z1 - Z0) / math.tan(math.radians(phi))   # la pared pasa por (A, Z1)
    trap2 = Polygon([(-a_bot, Z0), (a_bot, Z0), (A_top, zr), (-A_top, zr)])
    cols = [sbox(a - tl / 2, Z0 + 1, a + tl / 2, ZC + Ro + 2) for a in LUG_A]
    flange2 = sbox(-a_hi, Z0, a_hi, Z1)
    P2 = largest(closing(unary_union([trap2, *cols, flange2]), r))
    body = prism(P1, SZ, (0, 1, 0), a_hi + 5).intersect(prism(P2, AZ, (1, 0, 0), 300))

    # ---- hueco interior (cajon cerrado de pared t_w); las orejetas bajan como almas interiores
    floor = sbox(-500, zb, 500, 500)
    in1 = opening(trap1.buffer(-tw, join_style="mitre").intersection(floor), 0.75 * r)
    webs = unary_union([sbox(a - tl / 2, -500, a + tl / 2, 500) for a in LUG_A])
    a_cav = A_BOLT - Rc - tw - r                  # el hueco nunca alcanza los pozos de los pernos
    in2 = trap2.buffer(-tw, join_style="mitre").intersection(floor).difference(webs)
    in2 = opening(in2.intersection(sbox(-a_cav, -500, a_cav, 500)), 0.75 * r)
    info["hueco"] = False; info["camaras"] = 0; info["drenajes"] = 0
    # FABRICACION ADITIVA: cada seccion del hueco se sustituye por el mayor triangulo a 45 grados que cabe
    # dentro (techo autoportante en ambas direcciones -> camaras con techo a cuatro aguas)
    if AM_ON:
        p1s = [t for t in (tent45(q, zb) for q in polys(in1, 15)) if t is not None]
        p2s = [t for t in (tent45(q, zb) for q in polys(in2, 15)) if t is not None]
    else:                                         # sin reglas de impresion 3D: hueco con la forma de la seccion
        p1s, p2s = polys(in1, 15), polys(in2, 15)
    drains = []
    if p1s and p2s:
        cav = None
        for ch in p2s:
            c = prism(max(p1s, key=lambda q: q.area), SZ, (0, 1, 0), a_hi).intersect(prism(ch, AZ, (1, 0, 0), 300))
            if c.Volume() <= 1.0:
                continue
            # todas las aristas de la camara redondeadas: sin esquinas interiores vivas (entallas)
            done = False
            for rc in (0.75 * r, 0.5 * r, 0.3 * r):
                try:
                    cf = c.fillet(rc, c.Edges())
                    if cf.isValid() and cf.Volume() > 0.5 * c.Volume():
                        c, done = cf, True
                        break
                except Exception:
                    pass
            if not done:
                info["clamped"].append("camara del hueco sin redondear -> se deja maciza")
                continue
            cav = c if cav is None else cav.fuse(c)
            info["camaras"] += 1
            s_c = max(p1s, key=lambda q: q.area).centroid.x; a_c = ch.centroid.x
            drains.append((s_c, a_c))
        if cav is not None:
            body = body.cut(cav)
            info["hueco"] = True
            # agujero de evacuacion del polvo (D5) desde el suelo de cada camara hasta la cara inferior
            for s_c, a_c in (drains if AM_ON else []):
                d = cq.Solid.makeCylinder(2.5, zb - Z0 + 2.0, cq.Vector(s_c, a_c, Z0 - 1.0))
                cut_d = body.cut(d)
                if cut_d.isValid():
                    body = cut_d; info["drenajes"] += 1

    # ---- marco de la base (plano s-a): lo que NO es marco se vacia (agujeros pasantes en la pestana)
    rect = sbox(s0, -A - 2 * r, s1, A + 2 * r)
    parts = [rect]
    for b in BOLTS:
        c = Point(*b["sa"])
        parts.append(c.buffer(Rb, quad_segs=4 * QS))
        q = nearest_points(rect, c)[0]
        parts.append(LineString([q, c]).buffer(wbar / 2, quad_segs=QS))
    rows = [(0, 1), (2, 3)]
    for i, j in rows:
        parts.append(LineString([BOLTS[i]["sa"], BOLTS[j]["sa"]]).buffer(max(wbar, 2 * Rb) / 2, quad_segs=QS))
        # franja del extremo: une la fila de pernos con el pie de la pared extrema
        sgn = np.sign(BOLTS[i]["sa"][1])
        sa_i, sa_j = BOLTS[i]["sa"], BOLTS[j]["sa"]
        parts.append(Polygon([(sa_i[0], sgn * (A - r)), (sa_j[0], sgn * (A - r)), sa_j, sa_i]).buffer(wbar / 2, quad_segs=QS))
    frame2d = largest(closing(unary_union(parts), r))
    windows = sbox(s_lo - 5, -a_hi - 5, s_hi + 5, a_hi + 5).difference(frame2d)
    for w_ in polys(windows, 2.0):
        cut = prism(w_, SA, (0, 0, 1), Z1 - Z0 + 1.0, both=False).translate(cq.Vector(0, 0, Z0 - 0.5))
        body = body.cut(cut)
    solid = body

    # ---- alojamientos cabeza/arandela (asiento plano hasta Rc, acuerdo de fondo fuera del asiento)
    for b in BOLTS:
        x, y = b["sa"]
        Rt = Rc                  # pozo de radio Rc con acuerdo de fondo rp (asiento plano hasta Rc - rp >= 10,1)
        corner = sbox(Rt - rp, Z1 - 0.01, Rt + 0.01, Z1 + rp).difference(Point(Rt - rp, Z1 + rp).buffer(rp, quad_segs=4 * QS))
        solid = solid.cut(revolve_z(sbox(0, Z1, Rt, Z1 + 120).difference(corner), x, y))
    # ---- agujeros fijos (nunca se mueven)
    for b in BOLTS:
        x, y = b["sa"]
        solid = solid.cut(cq.Solid.makeCylinder(b["r"], Z1 - Z0 + 2, cq.Vector(x, y, Z0 - 1)))
    span = a_lug + tl / 2 + 1.0
    solid = solid.cut(cq.Solid.makeCylinder(RP, 2 * span, cq.Vector(0, -span, ZC), cq.Vector(0, 1, 0)))

    solid = solid.clean().fix()
    solid = solid.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), THETA).translate(cq.Vector(P0[0], P0[1], 0))
    sols = sorted(solid.Solids(), key=lambda s: s.Volume(), reverse=True)
    if len(sols) > 1 and sum(s.Volume() for s in sols[1:]) < 1e-3 * sols[0].Volume():
        info["clamped"].append(f"eliminadas {len(sols) - 1} virutas sueltas ({sum(s.Volume() for s in sols[1:]):.2f} mm3)")
        solid = sols[0]
    if len(solid.Solids()) != 1:
        raise GeometryError(f"la pieza no es un unico solido ({len(solid.Solids())} trozos)")
    if not solid.isValid():
        raise GeometryError("solido no valido tras las operaciones booleanas")
    if AM_ON and len(solid.Shells()) > 1:
        raise GeometryError("impresion 3D: queda una cavidad cerrada sin salida para el polvo")
    info.update(volume_mm3=solid.Volume(), mass_kg=solid.Volume() * 7.85e-6,
                pin_half_width=tl / 2, A_eff=A, A_top=A_top, H_eff=zr - Z0)
    info["holes"] = check_holes(solid, tl)
    return solid, info


# --------------------------------------------------------------------------- verificacion de los 6 agujeros
def check_holes(solid, t_lug):
    """Comprueba que los 4 agujeros de perno y los 2 del bulon estan exactamente en su sitio."""
    from OCP.BRepAdaptor import BRepAdaptor_Surface
    from OCP.GeomAbs import GeomAbs_Cylinder
    cyl = []
    for f in solid.Faces():
        s = BRepAdaptor_Surface(f.wrapped)
        if s.GetType() != GeomAbs_Cylinder:
            continue
        c = s.Cylinder(); ax = c.Axis(); d = ax.Direction(); o = ax.Location()
        cyl.append((c.Radius(), np.array([d.X(), d.Y(), d.Z()]), np.array([o.X(), o.Y(), o.Z()]), f.Area(),
                    np.array(f.Center().toTuple())))
    res = {"pernos": [], "bulon": None}
    for b in H["pernos"]:
        area = sum(A for R, d, o, A, cen in cyl if abs(R - b["r"]) < 1e-4 and abs(abs(d[2]) - 1) < 1e-6
                   and np.hypot(o[0] - b["c"][0], o[1] - b["c"][1]) < 1e-3)
        res["pernos"].append(round(area / (2 * math.pi * b["r"] * (Z1 - Z0)), 4))
    c = np.array(H["bulon"]["centers"][0])   # los dos agujeros son coaxiales
    tot = 0.0
    for R, d, o, A, cen in cyl:
        if abs(R - RP) < 1e-4 and abs(abs(d @ AX) - 1) < 1e-5:
            v = c - o
            if np.linalg.norm(v - (v @ d) * d) < 1e-3:
                if any(abs((cen - np.array(cc)) @ AX) <= t_lug / 2 + 0.05 for cc in H["bulon"]["centers"]):
                    tot += A
    res["bulon"] = round(tot / (2 * 2 * math.pi * RP * t_lug), 4)
    ok = all(abs(x - 1) < 0.01 for x in res["pernos"]) and abs(res["bulon"] - 1) < 0.01
    if not ok:
        raise GeometryError(f"agujeros fijos alterados: {res}")
    return res


def export(solid, path):
    cq.exporters.export(cq.Workplane().add(solid), path)


if __name__ == "__main__":
    import sys, time
    p = default_params()
    for a in sys.argv[1:]:
        k, v = a.split("="); p[k] = float(v)
    t0 = time.time()
    s, info = build(p)
    os.makedirs(os.path.join(ROOT, "tests", "geom"), exist_ok=True)
    export(s, os.path.join(ROOT, "tests", "geom", "prueba.step"))
    print(json.dumps(info, indent=1), f"\n{time.time()-t0:.1f}s")
