"""Formas puras INSCRITAS en lo que ya se habia vaciado (planta y altura): nunca quitan material nuevo."""
import sys, os, json, math, itertools
sys.path.insert(0, r"C:\Users\hugof\Desktop\Universidad\MSD\Trabajo\scripts")
import numpy as np, operaciones as O
from shapely.geometry import Point, LineString, box
from shapely.ops import unary_union
from shapely import affinity
from shapely.prepared import prep

ST = r"C:\Users\hugof\Desktop\Universidad\MSD\Trabajo\runs\opt_42258N\estado.json"
PA2 = O.PIN_A[:2] / np.linalg.norm(O.PIN_A[:2]); PP2 = O.PIN_P[:2]
ANG = math.degrees(math.atan2(PA2[1], PA2[0]))
TOL = 0.8          # mm de tolerancia (la forma pura puede asomar como mucho esto fuera de lo ya vaciado)


def mirror2(g):
    c = tuple(PP2)
    return affinity.rotate(affinity.scale(affinity.rotate(g, -ANG, origin=c), xfact=-1, yfact=1, origin=c), ANG, origin=c)


def mpt(x, y):
    return tuple(O.mirror_pt((x, y, 0.0))[:2])


def best_inscribed(U, zmap=None, z0=-1.0, max_shapes=3, min_area=60.0):
    """Hasta 'max_shapes' formas (circulo u obround) inscritas en U (y bajo el techo zmap si se da), voraz por area."""
    out = []
    R = U
    placed = []                                               # formas ya elegidas (geometria)

    def web_ok(g):
        """Sin paredes finas: la forma nueva se solapa con las elegidas o queda a >= 4 mm de ellas."""
        for h_ in placed:
            d_ = g.distance(h_)
            if 0.0 < d_ < 4.0 and not g.intersects(h_):
                return False
        return True
    for _ in range(max_shapes):
        if R.is_empty or R.area < min_area:
            break
        minx, miny, maxx, maxy = R.bounds
        gx, gy = np.meshgrid(np.arange(minx, maxx, 1.0), np.arange(miny, maxy, 1.0))
        P = np.c_[gx.ravel(), gy.ravel()]
        Rb = R.buffer(TOL); pr = prep(Rb)
        inside = np.array([pr.contains(Point(p)) for p in P])
        P = P[inside]
        if not len(P):
            break
        bd = Rb.boundary
        rr = np.array([bd.distance(Point(p)) for p in P])
        if zmap is not None:                                  # el techo de 45 grados no puede pasar del vaciado original
            rr = np.minimum(rr, np.array([zmap(p) - z0 for p in P]))
        order = np.argsort(-rr)[:120]
        best = None
        for i in order:                                       # circulos
            r = math.floor(rr[i] * 2) / 2
            if r >= 3 and (best is None or math.pi * r * r > best[0]) and web_ok(Point(P[i]).buffer(r)):
                best = (math.pi * r * r, dict(kind="circulo", x=float(P[i][0]), y=float(P[i][1]), r=r))
        for i, j in itertools.combinations(order[:80], 2):    # ranuras (obround)
            p, q = P[i], P[j]
            L = float(np.linalg.norm(q - p))
            if L < 4:
                continue
            ts = np.linspace(0, 1, max(3, int(L)))
            seg = p[None, :] + ts[:, None] * (q - p)[None, :]
            r = min(bd.distance(Point(s_)) for s_ in seg)
            if zmap is not None:
                r = min(r, min(zmap(s_) - z0 for s_ in seg))
            r = math.floor(r * 2) / 2
            if r < 3:
                continue
            a = math.pi * r * r + 2 * r * L
            if (best is None or a > best[0]) and web_ok(LineString([tuple(p), tuple(q)]).buffer(r)):
                best = (a, dict(kind="ranura", x1=float(p[0]), y1=float(p[1]), x2=float(q[0]), y2=float(q[1]), r=r))
        if best is None or best[0] < min_area:
            break
        sh = best[1]
        g = (Point(sh["x"], sh["y"]).buffer(sh["r"]) if sh["kind"] == "circulo"
             else LineString([(sh["x1"], sh["y1"]), (sh["x2"], sh["y2"])]).buffer(sh["r"]))
        out.append((best[0], sh))
        placed.append(g)
        R = R.difference(g)
    return out


def roof_height(op, p):
    """Altura del techo (45 grados) de un bolsillo original en el punto p (o -inf si p queda fuera)."""
    x, y = p
    if not (op["x0"] <= x <= op["x1"] and op["y0"] <= y <= op["y1"]):
        return -1e9
    dmin = min(x - op["x0"], op["x1"] - x, y - op["y0"], op["y1"] - y)
    return min(op["z1"], op["z0"] + dmin * O.G.AM_T)


if __name__ == "__main__":
    ops = json.load(open(ST, encoding="utf-8"))["mejor"]["ops"]
    thr = [k for k, o in enumerate(ops) if o["tipo"] == "agujero"]
    pk = [k for k, o in enumerate(ops) if o["tipo"] == "hueco" and o["z0"] < 0]
    # ---- aligeramientos pasantes: union (con simetricos) -> componentes -> formas inscritas
    circ = [Point(ops[k]["x"], ops[k]["y"]).buffer(ops[k]["r"], quad_segs=32) for k in thr]
    Ut = unary_union(circ + [mirror2(c) for c in circ])
    comps = list(Ut.geoms) if hasattr(Ut, "geoms") else [Ut]
    new = []
    print("ALIGERAMIENTOS PASANTES")
    for comp in sorted(comps, key=lambda g: -g.area):
        members = [k for k, c in zip(thr, circ) if c.intersects(comp)]
        if len(members) == 1 and abs(Point(ops[members[0]]["x"], ops[members[0]]["y"]).buffer(ops[members[0]]["r"]).area - comp.area) < 5:
            o = ops[members[0]]; new.append(dict(tipo="agujero", x=o["x"], y=o["y"], r=o["r"]))   # ya es un circulo puro
            print(f"  ops {[m + 1 for m in members]}: ya es un circulo -> se queda"); continue
        if any(c.intersects(comp) for c in circ) is False:
            continue                                                         # es la copia simetrica de otro grupo
        sh = best_inscribed(comp)
        tot = sum(a for a, _ in sh)
        print(f"  ops {[m + 1 for m in members]} ({comp.area:.0f} mm2) -> {len(sh)} formas puras inscritas ({tot:.0f} mm2, "
              f"{tot / comp.area * 100:.0f} % del hueco): {[ (s_['kind'], round(s_.get('r', 0), 1)) for _, s_ in sh]}")
        for _, s_ in sh:
            if s_["kind"] == "circulo":
                new.append(dict(tipo="agujero", x=round(s_["x"], 1), y=round(s_["y"], 1), r=s_["r"]))
            else:
                new.append(dict(tipo="ranura", x1=round(s_["x1"], 1), y1=round(s_["y1"], 1), r1=s_["r"],
                                x2=round(s_["x2"], 1), y2=round(s_["y2"], 1), r2=s_["r"]))
    # quitar duplicados simetricos (sym() ya aplica el simetrico de cada operacion)
    ded = []
    for o in new:
        c = (o.get("x", (o.get("x1", 0) + o.get("x2", 0)) / 2), o.get("y", (o.get("y1", 0) + o.get("y2", 0)) / 2))
        mc = mpt(*c)
        if any(math.hypot(mc[0] - d_[0], mc[1] - d_[1]) < 2.0 and math.hypot(*np.subtract(c, mc)) > 2.0 for d_, _ in ded):
            continue
        ded.append((c, o))
    new_thr = [o for _, o in ded]
    # ---- bolsillos desde la cara de apoyo: union de huellas + techo maximo -> ranuras inscritas
    print("BOLSILLOS DESDE LA CARA DE APOYO")
    fps = [box(ops[k]["x0"], ops[k]["y0"], ops[k]["x1"], ops[k]["y1"]) for k in pk]
    allpk = [ops[k] for k in pk] + [dict(ops[k], **dict(zip(("x0", "x1", "y0", "y1"), (
        min(mpt(ops[k]["x0"], ops[k]["y0"])[0], mpt(ops[k]["x1"], ops[k]["y1"])[0]),
        max(mpt(ops[k]["x0"], ops[k]["y0"])[0], mpt(ops[k]["x1"], ops[k]["y1"])[0]),
        min(mpt(ops[k]["x0"], ops[k]["y0"])[1], mpt(ops[k]["x1"], ops[k]["y1"])[1]),
        max(mpt(ops[k]["x0"], ops[k]["y0"])[1], mpt(ops[k]["x1"], ops[k]["y1"])[1]))))) for k in pk]
    zmap = lambda p: max(roof_height(o, p) for o in allpk) + TOL
    Up = unary_union(fps + [mirror2(f) for f in fps])
    comps = list(Up.geoms) if hasattr(Up, "geoms") else [Up]
    new_pk = []
    done = []
    for comp in sorted(comps, key=lambda g: -g.area):
        members = [k for k, f in zip(pk, fps) if f.intersects(comp)]
        if not members:
            continue
        mc = mirror2(comp).centroid
        if any(mc.distance(d_) < 3.0 for d_ in done):
            print(f"  ops {[m + 1 for m in members]}: es el reflejo de otro grupo (lo pone la simetria) -> se omite")
            continue
        done.append(comp.centroid)
        sh = best_inscribed(comp, zmap=zmap, max_shapes=3, min_area=150.0)
        tot = sum(a for a, _ in sh)
        print(f"  ops {[m + 1 for m in members]} ({comp.area:.0f} mm2) -> {len(sh)} ranuras inscritas ({tot:.0f} mm2): "
              f"{[(s_['kind'], s_['r']) for _, s_ in sh]}")
        for _, s_ in sh:
            if s_["kind"] == "circulo":
                s_.update(x1=s_["x"], y1=s_["y"], x2=s_["x"], y2=s_["y"])
            zt = max(zmap((s_["x1"], s_["y1"])), zmap((s_["x2"], s_["y2"]))) - TOL
            new_pk.append(dict(tipo="bolsillo_ranura", x1=round(s_["x1"], 1), y1=round(s_["y1"], 1), x2=round(s_["x2"], 1),
                               y2=round(s_["y2"], 1), r=s_["r"], z1=round(min(12.0, max(zt, 4.0)), 1)))
    keep = [o for k, o in enumerate(ops) if k not in thr and k not in pk and not (o["tipo"] == "hueco" and o["z0"] >= 0)]
    result = keep + new_thr + new_pk
    print(f"\n{len(ops)} operaciones -> {len(result)}")
    import operaciones as O2
    for k, o in enumerate(result, 1):
        print(f"  {k:2d}. {O2.describe(o)}")
    json.dump(result, open(os.path.join(os.path.dirname(__file__), "ops_puras.json"), "w"), indent=1)
