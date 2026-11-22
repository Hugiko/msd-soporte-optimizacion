"""Crea un proyecto de ANSYS WORKBENCH listo para abrir (doble clic en el .wbpj o el .wbpz) con:
   geometria (STEP), material S235, Fixed Support en los 4 agujeros de pernos, Remote Force
   (Deformable) en los 2 agujeros del bulon, malla cuadratica, resultados y el calculo ya resuelto.

Uso: python exportar_workbench.py <geometria.step> <carpeta_salida> [nombre] [carga_N] [tamano_malla_mm]
"""
import os, sys, json, subprocess, time, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fem

RUNWB2 = r"C:\Program Files\ANSYS Inc\ANSYS Student\v261\Framework\bin\Win64\RunWB2.exe"

MECH_BODY = r'''
# -*- coding: utf-8 -*-
# Script de Mechanical (generado automaticamente)
import math
ExtAPI.Application.ActiveUnitSystem = MechanicalUnitSystem.StandardNMM
BOLTS = __BOLTS__
PIN_C = __PINC__
PIN_A = __PINA__
PIN_R = __PINR__
HALF = __HALF__
Z0, Z1 = __Z0__, __Z1__
F = __F__
D = __D__
PILOT = __PILOT__
TOL = 0.08
LOGF = r"__LOG__"
def L(msg):
    f = open(LOGF, "a"); f.write(str(msg) + "\n"); f.close()
L("inicio script Mechanical")
SCALE = [1000.0]
def verts(face):
    pts = []
    for e in face.Edges:
        for v in e.Vertices:
            pts.append((v.X * SCALE[0], v.Y * SCALE[0], v.Z * SCALE[0]))
    return pts
def on_bolt(p, b):
    return abs(math.hypot(p[0] - b[0], p[1] - b[1]) - b[2]) < TOL and Z0 - TOL <= p[2] <= Z1 + TOL
def pin_ok(p):
    v = [p[i] - PIN_C[0][i] for i in range(3)]
    t = sum(v[i] * PIN_A[i] for i in range(3))
    rad = math.sqrt(max(0.0, sum(x * x for x in v) - t * t))
    if abs(rad - PIN_R) > TOL:
        return False
    for c in PIN_C:
        tc = sum((p[i] - c[i]) * PIN_A[i] for i in range(3))
        if abs(tc) <= HALF + TOL:
            return True
    return False
body_geo = DataModel.GeoData.Assemblies[0].Parts[0].Bodies[0]
L("caras del solido: %d" % body_geo.Faces.Count)
def find_faces():
    bolt_ids, pin_ids, per_bolt = [], [], [0, 0, 0, 0]
    for f in body_geo.Faces:
        if "Cylind" not in str(f.SurfaceType):
            continue
        vs = verts(f)
        if not vs:
            continue
        for i, b in enumerate(BOLTS):
            if all(on_bolt(p, b) for p in vs):
                bolt_ids.append(f.Id); per_bolt[i] += 1
                break
        else:
            if all(pin_ok(p) for p in vs):
                pin_ids.append(f.Id)
    return bolt_ids, pin_ids, per_bolt
for sc in (1000.0, 1.0):          # GeoData puede venir en m o en mm
    SCALE[0] = sc
    bolt_ids, pin_ids, per_bolt = find_faces()
    L("escala %s -> caras pernos por agujero %s, caras bulon %d" % (sc, per_bolt, len(pin_ids)))
    if min(per_bolt) > 0 and len(pin_ids) >= 2:
        break
if min(per_bolt) == 0 or len(pin_ids) < 2:
    raise Exception("No se han encontrado todas las caras: pernos %s, bulon %d" % (per_bolt, len(pin_ids)))
def named(name, ids):
    s = ExtAPI.SelectionManager.CreateSelectionInfo(SelectionTypeEnum.GeometryEntities)
    s.Ids = ids
    ns = Model.AddNamedSelection()
    ns.Location = s
    ns.Name = name
    return ns
ns_b = named("PERNOS_fijos", bolt_ids)
ns_p = named("BULON_carga", pin_ids)
# material S235
body = Model.Geometry.GetChildren(DataModelObjectCategory.Body, True)[0]
body.Material = "Acero S235"
# malla
mesh = Model.Mesh
mesh.ElementOrder = ElementOrder.Quadratic
mesh.ElementSize = Quantity(__H__, "mm")
try:
    mesh.CaptureCurvature = False
except:
    pass
try:
    mesh.CaptureProximity = False
except:
    pass
an = Model.Analyses[0]
fs = an.AddFixedSupport()
fs.Location = ns_b
rf = an.AddRemoteForce()
rf.Location = ns_p
rf.XCoordinate = Quantity(PILOT[0], "mm")
rf.YCoordinate = Quantity(PILOT[1], "mm")
rf.ZCoordinate = Quantity(PILOT[2], "mm")
rf.DefineBy = LoadDefineBy.Components
rf.XComponent.Output.DiscreteValues = [Quantity(F * D[0], "N")]
rf.YComponent.Output.DiscreteValues = [Quantity(F * D[1], "N")]
rf.ZComponent.Output.DiscreteValues = [Quantity(0.0, "N")]
rf.Behavior = LoadBehavior.Deformable
rf.Name = "Carga 2 (%.0f N, -X)" % F
sol = an.Solution
s1 = sol.AddEquivalentStress()
s2 = sol.AddTotalDeformation()
for ax, nm in ((NormalOrientationType.XAxis, "X"), (NormalOrientationType.YAxis, "Y"), (NormalOrientationType.ZAxis, "Z")):
    dd = sol.AddDirectionalDeformation()
    dd.NormalOrientation = ax
    dd.Name = "Desplazamiento " + nm
sol.AddEquivalentElasticStrain()
fr = sol.AddForceReaction()
fr.BoundaryConditionSelection = fs
L("condiciones creadas; mallando")
Model.Mesh.GenerateMesh()
L("malla: %s nodos, %s elementos" % (Model.Mesh.Nodes, Model.Mesh.Elements))
L("MONTAJE OK")
'''

SOLVE = r'''
LOGF = r"__LOG__"
def L(msg):
    f = open(LOGF, "a"); f.write(str(msg) + "\n"); f.close()
try:
    an = Model.Analyses[0]
    an.Solve(True)
    L("resuelto. estado: %s" % an.Solution.ObjectState)
    for r in an.Solution.Children:
        try:
            L("%s: max %s" % (r.Name, r.Maximum))
        except:
            pass
    L("FIN OK")
except Exception as e:
    import traceback
    L("ERROR al resolver: " + traceback.format_exc())
'''

MECH = MECH_BODY + r'''
'''
JOURNAL = r'''# encoding: utf-8
SetScriptVersion(Version="26.1")
template1 = GetTemplate(TemplateName="Static Structural", Solver="ANSYS")
system1 = template1.CreateSystem()
ed = system1.GetContainer(ComponentName="Engineering Data")
mat = ed.CreateMaterial(Name="Acero S235")
p1 = mat.CreateProperty(Name="Density")
p1.SetData(Variables=["Density"], Values=[["7850 [kg m^-3]"]])
p2 = mat.CreateProperty(Name="Elasticity", Behavior="Isotropic")
p2.SetData(Variables=["Young's Modulus"], Values=[["2.1E+11 [Pa]"]])
p2.SetData(Variables=["Poisson's Ratio"], Values=[["0.3"]])
p3 = mat.CreateProperty(Name="Tensile Yield Strength")
p3.SetData(Variables=["Tensile Yield Strength"], Values=[["2.15E+08 [Pa]"]])
geo = system1.GetContainer(ComponentName="Geometry")
geo.SetFile(FilePath=r"__STEP__")
system1.GetComponent(Name="Model").Refresh()
model1 = system1.GetContainer(ComponentName="Model")
model1.Edit(Interactive=False)
model1.SendCommand(Language="Python", Command=open(r"__MECH__").read())
model1.Exit()
Save(FilePath=r"__WBPJ__", Overwrite=True)
Archive(FilePath=r"__WBPZ__", IncludeExternalImportedFiles=True)
model1.Edit(Interactive=False)
model1.SendCommand(Language="Python", Command=open(r"__SOLVE__").read())
model1.Exit()
Save(Overwrite=True)
'''


def export(step, out, name="soporte", force=None, h=4.0, timeout=3600, log=None, half=None):
    force = float(json.load(open(os.path.join(fem.ROOT, "config.json"), encoding="utf-8-sig"))["carga_N"]) if force is None else force
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)
    H = fem.HOLES
    stepc = os.path.join(out, name + ".stp")
    if os.path.abspath(step) != stepc:
        shutil.copy(step, stepc)
    pilot = list(map(float, sum(map(lambda c: __import__("numpy").array(c), H["bulon"]["centers"])) / 2))
    a = fem.pin_axis().tolist()
    mech = (MECH.replace("__BOLTS__", repr([[b["c"][0], b["c"][1], b["r"]] for b in H["pernos"]]))
            .replace("__PINC__", repr(H["bulon"]["centers"])).replace("__PINA__", repr(a))
            .replace("__PINR__", repr(H["bulon"]["r"])).replace("__HALF__", repr(half if half is not None else _half(stepc)))
            .replace("__Z0__", repr(H["pernos_z"][0])).replace("__Z1__", repr(H["pernos_z"][1]))
            .replace("__F__", repr(force)).replace("__D__", repr(fem.load_dir().tolist()))
            .replace("__PILOT__", repr(pilot)).replace("__H__", repr(h))
            .replace("__LOG__", os.path.join(out, "_mechanical.log")))
    body = mech.split("\n")
    mech = "import traceback\ntry:\n" + "\n".join("    " + l for l in body) + \
           "\nexcept Exception as _e:\n    open(r\"" + os.path.join(out, "_mechanical.log") + "\", \"a\").write(\"ERROR: \" + traceback.format_exc())\n"
    mp = os.path.join(out, "_mechanical.py"); open(mp, "w").write(mech)
    sp = os.path.join(out, "_resolver.py"); open(sp, "w").write(SOLVE.replace("__LOG__", os.path.join(out, "_mechanical.log")))
    if os.path.exists(os.path.join(out, "_mechanical.log")):
        os.remove(os.path.join(out, "_mechanical.log"))
    wbpj = os.path.join(out, name + ".wbpj"); wbpz = os.path.join(out, name + ".wbpz")
    jr = (JOURNAL.replace("__STEP__", stepc).replace("__MECH__", mp).replace("__WBPJ__", wbpj).replace("__WBPZ__", wbpz)
          .replace("__SOLVE__", sp))
    jp = os.path.join(out, "_crear_proyecto.wbjn"); open(jp, "w").write(jr)
    fem.log(f"Workbench (sin ventana): creando {name}.wbpj con F = {force:.0f} N ...", log)
    t0 = time.time()
    p = subprocess.Popen([RUNWB2, "-B", "-R", jp], cwd=out, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="ignore")
    try:
        txt, _ = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        txt = "TIMEOUT"
    open(os.path.join(out, "_workbench.log"), "w", errors="ignore").write(txt or "")
    lp = os.path.join(out, "_mechanical.log")
    mlog = open(lp, errors="ignore").read() if os.path.exists(lp) else ""
    ok = os.path.exists(wbpj) and "MONTAJE OK" in mlog
    solved = "FIN OK" in mlog
    fem.log(f"Workbench termino en {time.time()-t0:.0f} s: montaje {'OK' if ok else 'FALLO'}, "
            f"resuelto {'SI' if solved else 'NO'}", log)
    return ok, wbpj, wbpz


def _half(step):
    """Semiespesor de las orejetas: del params.json vecino si existe; si no, el del original."""
    pj = os.path.join(os.path.dirname(step), "params.json")
    if os.path.exists(pj):
        p = json.load(open(pj))
        if "t_lug" in p:
            return p["t_lug"] / 2
    return fem.HOLES["bulon"]["half_width"]


if __name__ == "__main__":
    step, out = sys.argv[1], sys.argv[2]
    name = sys.argv[3] if len(sys.argv) > 3 else "soporte"
    F = float(sys.argv[4]) if len(sys.argv) > 4 else None
    h = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
    ok, wbpj, wbpz = export(step, out, name, F, h)
    print("OK" if ok else "FALLO", wbpj)
