"""Utilidades geometricas comunes: agujeros fijos del enunciado, sistema local, verificacion y exportacion.

Los 4 agujeros de los pernos y los 2 del bulon NO se mueven nunca (cad/agujeros_fijos.json, extraidos de 0.stp con
find_holes.py). check_holes() comprueba en cada pieza que siguen exactamente en su sitio.
(La antigua familia «desde cero» se elimino el 23/11/2026: 101 disenos, ninguno valido.)
"""
import os, json, math
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = json.load(open(os.path.join(ROOT, "cad", "agujeros_fijos.json")))

Z0, Z1 = H["pernos_z"]                 # cara inferior y asiento de arandela (cotas del original)
ZC = H["bulon"]["centers"][0][2]       # altura del eje del bulon
RP = H["bulon"]["r"]                   # radio agujero bulon
AX = np.array(H["bulon"]["axis"]) / np.linalg.norm(H["bulon"]["axis"])
DX = np.array([AX[1], -AX[0], 0.0])    # horizontal perpendicular al bulon
THETA = math.degrees(math.atan2(DX[1], DX[0]))
P0 = np.mean(np.array(H["bulon"]["centers"])[:, :2], axis=0)   # punto medio entre orejetas (xy)
QS = 6                                 # segmentos por cuarto de circulo en los perfiles 2D
T_LUG = 6.35                           # espesor de cada orejeta del original (longitud de cada agujero del bulon)
try:   # reglas de impresion 3D (opcionales) y angulo minimo de voladizo (docs/fabricacion_aditiva.md)
    _cfg = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
except Exception:
    _cfg = {}
AM_ON = bool(_cfg.get("reglas_impresion_3d", False))
AM_ANGLE = float(_cfg.get("angulo_voladizo_deg", 45.0))
AM_T = math.tan(math.radians(AM_ANGLE))


def to_local(xy):
    v = np.asarray(xy, float) - P0
    c, s = math.cos(math.radians(THETA)), math.sin(math.radians(THETA))
    return np.array([c * v[0] + s * v[1], -s * v[0] + c * v[1]])


BOLTS = [dict(sa=to_local(b["c"]), r=b["r"], c=b["c"]) for b in H["pernos"]]
FRONT = (0, 1)                         # pernos delanteros (y ~ 0); traseros: 2, 3


class GeometryError(Exception):
    pass


def largest(geom):
    if geom.is_empty:
        return geom
    if geom.geom_type in ("MultiPolygon", "GeometryCollection"):
        polys = [g for g in geom.geoms if g.geom_type == "Polygon"]
        return max(polys, key=lambda g: g.area) if polys else Polygon()
    return geom


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


def revolve_z(poly2d, cx, cy):
    """Solido de revolucion alrededor del eje vertical (cx, cy) a partir de un perfil (r, z)."""
    pts = clean_coords(list(prep(poly2d).exterior.coords))
    return cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0)).val() \
        .translate(cq.Vector(cx, cy, 0))


# --------------------------------------------------------------------------- verificacion de los 6 agujeros
def check_holes(solid, t_lug=T_LUG):
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
