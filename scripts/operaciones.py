"""OPERACIONES DE DISENO sobre la pieza (cadquery).

La pieza es SIEMPRE: 0.stp (la del enunciado) + una lista ordenada de operaciones. Cada operacion la decide una REGLA
(scripts/reglas.py) a partir del mapa de tensiones de la pieza actual, con su justificacion. Se puede reconstruir
cualquier pieza desde cero repitiendo sus operaciones.

QUITAN material (donde no trabaja):
  agujero    aligeramiento vertical pasante (paredes verticales: imprimible sin soportes)
  rebaje     rebaje desde arriba de una zona (suelo horizontal y acuerdos redondeados)
  hueco      hueco interior con techo a cuatro aguas a 45 grados + agujero de evacuacion del polvo (D5)
ANADEN o REFORMAN material (donde esta el pico de tension, o FORMAS NUEVAS en la trayectoria de la carga):
  collar     anillo de refuerzo alrededor del alojamiento de un perno
  alojamiento alojamiento de cabeza mas ancho con acuerdo de fondo mayor (menor concentracion de tensiones)
  redondeo   redondeo de las aristas junto al pico (acuerdo: baja el factor de concentracion Kt)
  orejeta    engrosa el anillo de material alrededor del bulon en las dos orejetas
  nervio     FORMA NUEVA: pared vertical (nervio / cartela) en la direccion principal de tension (trayectoria de carga)
Las que ANADEN nunca invaden el paso de los tornillos, de sus cabezas ni del bulon, ni el hueco entre orejetas, y no
salen de la caja que ocupa el soporte original (volumen de diseno).
Las operaciones que QUITAN nunca tocan las zonas protegidas (alrededor de los 4 pernos y de las orejetas).
Los 6 agujeros del enunciado se verifican al final de cada pieza (geometry.check_holes).
"""
import os, math, json
import numpy as np
import cadquery as cq
import geometry as G
import fem
from shapely.geometry import Point as SPt, box as sbox

STEP0 = os.path.join(G.ROOT, "cad", "0.stp")
RHO_KG_MM3 = 7.85e-6
R_POCKET0 = 10.541             # radio del alojamiento de cabeza del original
R_HEAD = 10.84                 # alojamiento + 0,3 mm
PIN_A = np.array(fem.HOLES["bulon"]["axis"], float); PIN_A /= np.linalg.norm(PIN_A)
PIN_C = [np.array(c, float) for c in fem.HOLES["bulon"]["centers"]]
PIN_P = np.mean(np.array(PIN_C), axis=0)
GeometryError = G.GeometryError
# zonas protegidas (las operaciones que QUITAN no entran): se pueden ajustar con los datos del estudio (reglas.py)
PROT = dict(perno=R_HEAD + 3.0, bulon=G.RP + 6.0)
# SIMETRIA (obligatoria por defecto): cada operacion se aplica tambien en su simetrico respecto al plano medio de las
# orejetas (perpendicular al bulon por su centro, donde se aplica la carga). Los agujeros fijos de los pernos no son
# simetricos (enunciado), asi que la pieza es simetrica salvo donde lo impiden ellos.
SIM = bool(G._cfg.get("simetria", True))


def mirror_pt(p):
    p = np.asarray(p, float)
    return p - 2.0 * ((p - PIN_P) @ PIN_A) * PIN_A


def sym(sh):
    """La forma y su simetrica (si SIM). Si se solapan se unen en un solido."""
    if not SIM:
        return sh
    m = sh.mirror(cq.Vector(*PIN_A), cq.Vector(*PIN_P))
    try:
        u = sh.fuse(m, tol=1e-4)
        if u.isValid():
            return u
    except Exception:
        pass
    return cq.Compound.makeCompound([sh, m])


def set_protection(perno=None, bulon=None):
    if perno:
        PROT["perno"] = float(perno)
    if bulon:
        PROT["bulon"] = float(bulon)
    _PROT.clear()


_ORIG = []
_PROT = []


def original():
    if not _ORIG:
        _ORIG.append(cq.importers.importStep(STEP0).val())
    return _ORIG[0]


def protected():
    """Cilindros alrededor de los 4 pernos (alojamiento + 3 mm) y del bulon (cubre las 2 orejetas)."""
    if not _PROT:
        s = None
        for b in G.BOLTS:
            c = cq.Solid.makeCylinder(PROT["perno"], 160.0, cq.Vector(b["c"][0], b["c"][1], -20.0))
            s = c if s is None else s.fuse(c)
        st = PIN_P - 26.0 * PIN_A
        pin = cq.Solid.makeCylinder(PROT["bulon"], 52.0, cq.Vector(*st), cq.Vector(*PIN_A))
        _PROT.append(s.fuse(pin))
    return _PROT[0]


def in_protected(xyz, extra=0.0):
    """Mascara de puntos dentro de las zonas protegidas (para el analisis del campo de tensiones)."""
    xyz = np.asarray(xyz, float)
    m = np.zeros(len(xyz), bool)
    for b in G.BOLTS:
        m |= np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1]) < PROT["perno"] + extra
    v = xyz - PIN_P; t = v @ PIN_A
    rho = np.linalg.norm(v - np.outer(t, PIN_A), axis=1)
    m |= (rho < PROT["bulon"] + extra) & (np.abs(t) < 26.0 + extra)
    return m


# ------------------------------------------------------------------------------------------- booleanas robustas
def boolean(op, vol_ok, what, split_msg=None):
    """Prueba tolerancias difusas crecientes hasta obtener UN solido valido con un volumen coherente.
    Si el resultado se parte en dos trozos grandes (> 1 %), es la geometria la que se parte: error."""
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
        if not big.isValid():
            big = _heal(big)
        if split_msg and rest and rest[0] > 0.01 * big.Volume() and big.isValid():
            raise GeometryError(split_msg)
        if big.isValid() and sum(rest) < 1.0 and vol_ok(big.Volume()):
            return big
        last = f"{len(sols)} solidos, resto {sum(rest):.0f} mm3"
    raise GeometryError(f"{what} ha fallado ({last})")


def _heal(solid):
    """Solido marcado como no valido por OCC tras una booleana (tolerancias): ida y vuelta por STEP, que lo reconstruye
    con tolerancias coherentes. Si sigue sin ser valido se devuelve tal cual (y la booleana prueba otra tolerancia)."""
    import tempfile
    try:
        fd, p = tempfile.mkstemp(suffix=".step"); os.close(fd)
        G.export(solid, p)
        s2 = cq.importers.importStep(p).val()
        os.remove(p)
        s2 = sorted(s2.Solids(), key=lambda q: q.Volume(), reverse=True)[0]
        if s2.isValid() and abs(s2.Volume() - solid.Volume()) < 1e-3 * solid.Volume() + 1.0:
            return s2
    except Exception:
        pass
    return solid


def cut(solid, tool, what):
    v0 = solid.Volume()
    new = boolean(lambda tol: solid.cut(tool, tol=tol), lambda v: v <= v0 + 1.0, what, split_msg=f"{what} parte la pieza en dos")
    if v0 - new.Volume() < 1.0:
        raise GeometryError(f"{what} no quita material (cae fuera de la pieza o dentro de zona protegida)")
    return new


def fuse(solid, tool, what):
    v0 = solid.Volume(); va = tool.Volume()
    new = boolean(lambda tol: solid.fuse(tool, tol=tol), lambda v: v0 - 1.0 <= v <= v0 + va + 1.0, what)
    if new.Volume() - v0 < 1.0:
        raise GeometryError(f"{what} no anade material (ya estaba dentro de la pieza)")
    return new


def rounded(solid, r):
    for rr in (r, 0.7 * r, 0.45 * r):
        try:
            f = solid.fillet(rr, solid.Edges())
            if f.isValid():
                return f
        except Exception:
            pass
    raise GeometryError("no se pudo redondear la herramienta de corte")


def fill_closed_voids(solid):
    """Rellena las cavidades interiores CERRADAS (polvo atrapado en impresion 3D)."""
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


# ------------------------------------------------------------------------------------------- operaciones
def op_agujero(solid, x, y, r):
    tool = sym(cq.Solid.makeCylinder(r, 180.0, cq.Vector(x, y, -30.0))).cut(protected())
    if tool.Volume() < 1.0:
        raise GeometryError("el aligeramiento cae entero dentro de una zona protegida")
    return cut(solid, tool, "el aligeramiento")


def op_rebaje(solid, x0, x1, y0, y1, zc, rr=3.0):
    if x1 - x0 < 2 * rr + 1 or y1 - y0 < 2 * rr + 1:
        raise GeometryError("rebaje demasiado pequeno")
    tool = sym(rounded(cq.Solid.makeBox(x1 - x0, y1 - y0, 220.0 - zc, cq.Vector(x0, y0, zc)), rr)).cut(protected())
    return cut(solid, tool, "el rebaje")


def hip_box(x0, x1, y0, y1, z0, z1):
    """Caja con techo a cuatro aguas (pendiente = angulo de voladizo, 45 grados): se imprime sin soportes."""
    box = cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))
    if not G.AM_ON:
        return box
    Lx, Ly = x1 - x0, y1 - y0
    w1 = cq.Wire.makePolygon([cq.Vector(x0, y0 - 5, z0 - 1), cq.Vector(x1, y0 - 5, z0 - 1), cq.Vector(x1, y0 - 5, z0),
                              cq.Vector((x0 + x1) / 2, y0 - 5, z0 + Lx / 2 * G.AM_T), cq.Vector(x0, y0 - 5, z0)], close=True)
    tent_x = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w1), cq.Vector(0, Ly + 10, 0))
    w2 = cq.Wire.makePolygon([cq.Vector(x0 - 5, y0, z0 - 1), cq.Vector(x0 - 5, y1, z0 - 1), cq.Vector(x0 - 5, y1, z0),
                              cq.Vector(x0 - 5, (y0 + y1) / 2, z0 + Ly / 2 * G.AM_T), cq.Vector(x0 - 5, y0, z0)], close=True)
    tent_y = cq.Solid.extrudeLinear(cq.Face.makeFromWires(w2), cq.Vector(Lx + 10, 0, 0))
    return box.intersect(tent_x).intersect(tent_y)


def op_hueco(solid, x0, x1, y0, y1, z0, z1, rr=2.0):
    if min(x1 - x0, y1 - y0, z1 - z0) < 2 * rr + 1:
        raise GeometryError("hueco demasiado pequeno")
    cav = sym(rounded(hip_box(x0, x1, y0, y1, z0, z1), rr))
    new = cut(solid, cav, "el hueco interior")
    if G.AM_ON:   # agujero de evacuacion del polvo (D5) desde el suelo del hueco hasta la cara inferior
        drain = sym(cq.Solid.makeCylinder(2.5, z0 + 2.0 + 1.0, cq.Vector((x0 + x1) / 2, (y0 + y1) / 2, -1.0)))
        new = cut(new, drain, "el agujero de evacuacion del hueco")
    return new


def op_collar(solid, perno, t, z, r_in=R_HEAD):
    x, y = G.BOLTS[int(perno)]["c"]
    ring = cq.Solid.makeCylinder(r_in + t, z - 1.0, cq.Vector(x, y, 1.0)).cut(
        cq.Solid.makeCylinder(r_in, z + 1.0, cq.Vector(x, y, 0.0)))
    new = fuse(solid, ring, "el collar")
    return fill_closed_voids(new)


def op_alojamiento(solid, perno, R):
    """Alojamiento de la cabeza mas ancho (radio R) con acuerdo de fondo R - 8 (asiento plano hasta r = 8 mm)."""
    if R <= R_POCKET0 + 0.05:
        raise GeometryError("alojamiento no mayor que el original")
    rp = R - 8.0
    corner = sbox(R - rp, G.Z1 - 0.01, R + 0.01, G.Z1 + rp).difference(SPt(R - rp, G.Z1 + rp).buffer(rp, quad_segs=4 * G.QS))
    b = G.BOLTS[int(perno)]
    tool = G.revolve_z(sbox(0, G.Z1, R, G.Z1 + 140).difference(corner), b["c"][0], b["c"][1])
    return cut(solid, tool, "el alojamiento")


def op_redondeo(solid, x, y, z, r, d=6.0):
    p = cq.Vertex.makeVertex(x, y, z)

    def on_fixed_hole(e):        # aristas de los 6 agujeros del enunciado: no se tocan nunca
        for u in (0.0, 0.37, 0.71):
            c = np.array(e.positionAt(u).toTuple())
            for b in G.BOLTS:
                if abs(math.hypot(c[0] - b["c"][0], c[1] - b["c"][1]) - b["r"]) < 0.3 and c[2] < G.Z1 + 0.3:
                    return True
            v = c - PIN_P; t = v @ PIN_A
            if abs(np.linalg.norm(v - t * PIN_A) - G.RP) < 0.3:
                return True
        return False
    pts = [p] + ([cq.Vertex.makeVertex(*mirror_pt((x, y, z)))] if SIM else [])
    edges = [e for e in solid.Edges() if min(e.distance(q) for q in pts) < d and not on_fixed_hole(e)]
    if not edges:
        raise GeometryError("no hay aristas junto al pico (salvo las de los agujeros fijos, que no se tocan)")
    last = None
    for rr in (r, 0.7 * r, 0.5 * r):
        try:
            f = solid.fillet(rr, edges)
            if f.isValid() and len(f.Solids()) == 1:
                return f
        except Exception as e:
            last = e
    raise GeometryError(f"el redondeo no se puede hacer en esas aristas ({type(last).__name__ if last else 'invalido'})")


def op_orejeta(solid, ro, t_lug=G.T_LUG):
    """Anillo de material alrededor del bulon, de radio exterior ro, en las dos orejetas (mismo espesor)."""
    new = solid
    for c in PIN_C:
        st = c - PIN_A * t_lug / 2
        ring = cq.Solid.makeCylinder(ro, t_lug, cq.Vector(*st), cq.Vector(*PIN_A)).cut(
            cq.Solid.makeCylinder(G.RP + 1.0, t_lug + 2, cq.Vector(*(st - PIN_A)), cq.Vector(*PIN_A)))
        new = fuse(new, ring, "el engrosamiento de la orejeta")
    return new


_KEEP = []
_ENV = []


def keep_out():
    """Zonas donde NUNCA se anade material: paso de los 4 tornillos y de sus cabezas, paso del bulon y hueco entre
    las orejetas (donde entra la pieza que se une)."""
    if not _KEEP:
        s = None
        for b in G.BOLTS:
            c = cq.Solid.makeCylinder(R_HEAD, 240.0, cq.Vector(b["c"][0], b["c"][1], -30.0))
            s = c if s is None else s.fuse(c)
        st = PIN_P - 60.0 * PIN_A
        s = s.fuse(cq.Solid.makeCylinder(G.RP + 0.5, 120.0, cq.Vector(*st), cq.Vector(*PIN_A)))
        gap = float(np.linalg.norm(PIN_C[1] - PIN_C[0])) - G.T_LUG - 0.2          # entre las caras interiores
        st = PIN_P - PIN_A * gap / 2
        s = s.fuse(cq.Solid.makeCylinder(G.RP + 14.0, gap, cq.Vector(*st), cq.Vector(*PIN_A)))
        _KEEP.append(s)
    return _KEEP[0]


def envelope():
    """Volumen de diseno: la caja que ocupa el soporte original (la pieza nueva no sale de ella)."""
    if not _ENV:
        bb = original().BoundingBox()
        _ENV.append(cq.Solid.makeBox(bb.xlen + 1, bb.ylen + 1, bb.zlen + 0.5, cq.Vector(bb.xmin - 0.5, bb.ymin - 0.5, bb.zmin)))
    return _ENV[0]


def op_nervio(solid, x0, y0, x1, y1, zt0, zt1, t, zb=0.0):
    """Nervio: pared vertical de espesor t sobre el segmento (x0,y0)-(x1,y1), desde zb hasta un borde superior
    inclinado (zt0 -> zt1). Vertical = imprimible sin soportes; nace de la base."""
    L = math.hypot(x1 - x0, y1 - y0)
    if L < 6.0 or t < 2.0:
        raise GeometryError("nervio demasiado pequeno")
    u = np.array([x1 - x0, y1 - y0]) / L
    n = np.array([-u[1], u[0]])
    o = -n * t / 2
    pts = [cq.Vector(x0 + o[0], y0 + o[1], zb), cq.Vector(x1 + o[0], y1 + o[1], zb),
           cq.Vector(x1 + o[0], y1 + o[1], zt1), cq.Vector(x0 + o[0], y0 + o[1], zt0)]
    rib = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.makePolygon(pts, close=True)), cq.Vector(n[0] * t, n[1] * t, 0))
    try:
        rib = rounded(rib, min(1.5, t / 3))
    except GeometryError:
        pass
    rib = sym(rib).intersect(envelope()).cut(keep_out())
    if rib.Volume() < 1.0:
        raise GeometryError("el nervio cae entero en zonas reservadas (tornillos, bulon) o fuera del volumen de diseno")
    new = fuse(solid, rib, "el nervio")
    return root_fillet(new, solid, rib, r=min(3.0, max(1.5, t / 2)))


def root_fillet(new, part, rib, r=3.0):
    """Acuerdo (radio r) en la RAIZ del nervio: las aristas nuevas donde el nervio se une a la pieza son esquinas entrantes
    (entallas); un acuerdo baja su concentracion de tensiones (Peterson). Si OCC no puede hacerlo, se deja sin acuerdo."""
    bb = rib.BoundingBox()
    pf = cq.Compound.makeCompound(part.Faces()); rf = cq.Compound.makeCompound(rib.Faces())
    edges = []
    for e in new.Edges():
        c = e.Center()
        if not (bb.xmin - 2 <= c.x <= bb.xmax + 2 and bb.ymin - 2 <= c.y <= bb.ymax + 2 and bb.zmin - 2 <= c.z <= bb.zmax + 2):
            continue
        v = cq.Vertex.makeVertex(*e.positionAt(0.5).toTuple())
        if v.distance(pf) < 0.05 and v.distance(rf) < 0.05:
            edges.append(e)
    if not edges:
        return new
    for rr in (r, 0.6 * r, 0.4 * r):
        try:
            f = new.fillet(rr, edges)
            if f.isValid() and len(f.Solids()) == 1 and f.Volume() >= new.Volume() - 1.0:
                return f
        except Exception:
            pass
    return new


OPS = dict(agujero=op_agujero, rebaje=op_rebaje, hueco=op_hueco, collar=op_collar, alojamiento=op_alojamiento,
           redondeo=op_redondeo, orejeta=op_orejeta, nervio=op_nervio)
QUITA = ("agujero", "rebaje", "hueco")
ANADE = ("collar", "alojamiento", "redondeo", "orejeta", "nervio")


def apply(solid, op):
    kw = {k: v for k, v in op.items() if k not in ("tipo", "regla", "id")}
    return OPS[op["tipo"]](solid, **kw)


def describe(op):
    d = _describe(op)
    return d + (" (y su simetrico)" if SIM and op["tipo"] in ("agujero", "rebaje", "hueco", "redondeo", "nervio") else "")


def _describe(op):
    t = op["tipo"]
    if t == "agujero":
        return f"aligeramiento pasante vertical D{2 * op['r']:.0f} mm en ({op['x']:.0f}, {op['y']:.0f})"
    if t == "rebaje":
        return (f"rebaje desde arriba hasta z = {op['zc']:.0f} mm en x {op['x0']:.0f}..{op['x1']:.0f}, "
                f"y {op['y0']:.0f}..{op['y1']:.0f} mm (esquinas R{op.get('rr', 3.0):g})")
    if t == "hueco":
        return (f"hueco interior {op['x1'] - op['x0']:.0f} x {op['y1'] - op['y0']:.0f} x {op['z1'] - op['z0']:.0f} mm "
                f"(techo a 45 grados + evacuacion D5) en ({(op['x0'] + op['x1']) / 2:.0f}, {(op['y0'] + op['y1']) / 2:.0f})")
    if t == "collar":
        return f"collar de {op['t']:.1f} mm alrededor del perno {int(op['perno']) + 1} hasta z = {op['z']:.0f} mm"
    if t == "alojamiento":
        return f"alojamiento del perno {int(op['perno']) + 1} con radio {op['R']:.2f} mm (acuerdo de fondo {op['R'] - 8:.2f} mm)"
    if t == "redondeo":
        return f"redondeo R{op['r']:.1f} de las aristas junto a ({op['x']:.0f}, {op['y']:.0f}, {op['z']:.0f})"
    if t == "orejeta":
        return f"anillo de las orejetas hasta radio {op['ro']:.1f} mm (ligamento {op['ro'] - G.RP:.1f} mm)"
    if t == "nervio":
        return (f"nervio de {op['t']:.0f} mm de ({op['x0']:.0f}, {op['y0']:.0f}) a ({op['x1']:.0f}, {op['y1']:.0f}), "
                f"borde superior de z = {op['zt0']:.0f} a {op['zt1']:.0f} mm")
    return t


def size(op):
    """Tamano caracteristico (para reducir a la mitad una operacion rechazada)."""
    t = op["tipo"]
    if t == "agujero":
        return op["r"]
    if t in ("rebaje", "hueco", "rebaje_nervio"):
        return (op["x1"] - op["x0"]) * (op["y1"] - op["y0"])
    if t == "nervio":
        return math.hypot(op["x1"] - op["x0"], op["y1"] - op["y0"]) * op["t"]
    return op.get("t", op.get("r", op.get("R", op.get("ro", 1.0))))


def box_of(op):
    """Caja (x0,x1,y0,y1,z0,z1) que ocupa la herramienta (para distancias y solapes)."""
    t = op["tipo"]
    if t == "agujero":
        return (op["x"] - op["r"], op["x"] + op["r"], op["y"] - op["r"], op["y"] + op["r"], -30.0, 150.0)
    if t in ("rebaje", "rebaje_nervio"):
        return (op["x0"], op["x1"], op["y0"], op["y1"], op["zc"], 220.0)
    if t == "nervio":
        h = op["t"] / 2
        return (min(op["x0"], op["x1"]) - h, max(op["x0"], op["x1"]) + h, min(op["y0"], op["y1"]) - h,
                max(op["y0"], op["y1"]) + h, op.get("zb", 0.0), max(op["zt0"], op["zt1"]))
    if t == "hueco":
        return (op["x0"], op["x1"], op["y0"], op["y1"], op["z0"], op["z1"])
    return None


def dist_to_op(p, op):
    b = box_of(op)
    if b is None:
        return 1e9
    d = [max(b[0] - p[0], 0, p[0] - b[1]), max(b[2] - p[1], 0, p[1] - b[3]), max(b[4] - p[2], 0, p[2] - b[5])]
    if op["tipo"] == "agujero":
        return max(math.hypot(p[0] - op["x"], p[1] - op["y"]) - op["r"], 0.0)
    return math.sqrt(sum(x * x for x in d))


def overlap(a, b):
    """Fraccion de la caja de a que solapa con la de b (en planta)."""
    A, B = box_of(a), box_of(b)
    if A is None or B is None:
        return 0.0
    ix = max(0.0, min(A[1], B[1]) - max(A[0], B[0])); iy = max(0.0, min(A[3], B[3]) - max(A[2], B[2]))
    area = max((A[1] - A[0]) * (A[3] - A[2]), 1e-9)
    return ix * iy / area


def finish(solid):
    """Comprobaciones finales comunes: un solido, valido, sin cavidades cerradas (3D) y con los 6 agujeros en su sitio."""
    sols = sorted(solid.Solids(), key=lambda s: s.Volume(), reverse=True)
    if len(sols) > 1 and sum(s.Volume() for s in sols[1:]) < 1e-3 * sols[0].Volume():
        solid = sols[0]
    if len(solid.Solids()) != 1:
        raise GeometryError(f"la pieza no es un unico solido ({len(solid.Solids())} trozos)")
    if not solid.isValid():
        raise GeometryError("solido no valido tras las operaciones")
    if G.AM_ON and len(solid.Shells()) > 1:
        solid = fill_closed_voids(solid)
        if len(solid.Shells()) > 1:
            raise GeometryError("impresion 3D: queda una cavidad cerrada sin salida para el polvo")
    holes = G.check_holes(solid)
    return solid, holes


def build(ops, base=None, n_base=0):
    """Pieza = 0.stp + ops. Si se da 'base' (la pieza con las n_base primeras operaciones ya hechas) solo se aplican
    las restantes (mas rapido)."""
    solid = original() if base is None else base
    for k, op in enumerate(ops[n_base:] if base is not None else ops, start=(n_base if base is not None else 0) + 1):
        try:
            solid = apply(solid, op)
        except GeometryError as e:
            raise GeometryError(f"operacion {k} ({op['tipo']}): {e}")
        except Exception as e:
            raise GeometryError(f"operacion {k} ({op['tipo']}): {type(e).__name__}: {e}")
    solid, holes = finish(solid)
    return solid, holes


class Pieza:
    """Adaptador para evaluate.evaluate(): una pieza ya construida (no tiene parametros continuos)."""
    NAMES = []

    def __init__(self, solid, holes, ops, titulo=""):
        self.solid, self.ops, self.titulo = solid, ops, titulo
        self.info = dict(volume_mm3=solid.Volume(), mass_kg=solid.Volume() * RHO_KG_MM3, pin_half_width=G.T_LUG / 2,
                         hueco=any(o["tipo"] == "hueco" for o in ops), clamped=[], holes=holes,
                         ficha_lineas=[f"  {k + 1:2d}. {describe(o)}" for k, o in enumerate(ops)][-14:] or ["  (pieza original)"])

    def build(self, p=None):
        return self.solid, dict(self.info)

    @staticmethod
    def export(solid, path):
        G.export(solid, path)


if __name__ == "__main__":
    import sys, time
    t0 = time.time()
    ops = json.loads(sys.argv[1]) if len(sys.argv) > 1 else []
    s, h = build(ops)
    print(f"volumen {s.Volume():.0f} mm3, masa {s.Volume() * RHO_KG_MM3:.4f} kg, agujeros {h} ({time.time() - t0:.1f} s)")
