"""Localiza los agujeros de pernos (R~5.155) y de bulon (R~9.525) en un STEP.
Agrupa caras cilindricas por (radio, eje) y guarda cad/agujeros.json."""
import sys, json, math
from collections import defaultdict
import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder

path = sys.argv[1] if len(sys.argv) > 1 else "cad/0.stp"
shape = cq.importers.importStep(path).val()
print("volumen = %.1f mm3" % shape.Volume())

groups = defaultdict(list)
for f in shape.Faces():
    s = BRepAdaptor_Surface(f.wrapped)
    if s.GetType() != GeomAbs_Cylinder:
        continue
    c = s.Cylinder()
    r = c.Radius()
    ax = c.Axis()
    d = ax.Direction(); p = ax.Location()
    dv = (d.X(), d.Y(), d.Z())
    if max(dv, key=abs) < 0:
        dv = tuple(-x for x in dv)
    # punto del eje mas proximo al centro de la cara (proyeccion)
    cm = f.Center()
    t = (cm.x - p.X()) * dv[0] + (cm.y - p.Y()) * dv[1] + (cm.z - p.Z()) * dv[2]
    q = (p.X() + t * dv[0], p.Y() + t * dv[1], p.Z() + t * dv[2])
    bb = f.BoundingBox()
    groups[round(r, 3)].append(dict(r=r, axis=[round(x, 5) for x in dv],
                                    center=[round(x, 3) for x in q], area=round(f.Area(), 2),
                                    zrange=[round(bb.zmin, 2), round(bb.zmax, 2)]))

print("radios distintos:", sorted(groups))
out = {}
for name, R in (("pernos", 10.31 / 2), ("bulon", 19.05 / 2)):
    cand = [g for r, lst in groups.items() if abs(r - R) < 0.2 for g in lst]
    print(f"\n{name} (R={R:.4f}): {len(cand)} caras")
    for c in cand:
        print("  ", c)
    out[name] = cand
json.dump(out, open("cad/agujeros.json", "w"), indent=1)
