"""Nucleo de EF: STEP -> malla tet10 (gmsh) -> entrada MAPDL -> solucion -> metricas.

Unidades mm-N-MPa-t. Sistema de 0.stp: Z vertical (normal a la placa base),
eje del bulon ~ +Y, carga 2 (Fz de la Tabla 2 = horizontal perpendicular al bulon) -> X del STEP.
"""
import os, json, math, time, datetime
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLES = json.load(open(os.path.join(ROOT, "cad", "agujeros_fijos.json")))

E, NU, RHO, SY = 210000.0, 0.30, 7.85e-9, 215.0
# Metrica de tension robusta (ver bitacora, Fase 2):
EX_BOLT = 5.0   # mm alrededor de cada agujero de perno (zona de arandela/cabeza M10, singularidad del empotramiento)
EX_PIN = 2.0    # mm alrededor de la superficie del bulon (esquinas del RBE3)


def stress_metric(nodes, s, pin_half=None, ex_bolt=None, ex_pin=None):
    ex_bolt = EX_BOLT if ex_bolt is None else ex_bolt
    ex_pin = EX_PIN if ex_pin is None else ex_pin
    keep = np.ones(len(nodes), bool)
    if ex_bolt > 0:
        keep &= ~bolt_mask(nodes, extra=ex_bolt)
    if ex_pin > 0:
        keep &= ~pin_mask(nodes, extra=ex_pin, half=pin_half)
    i = np.flatnonzero(keep)[s[keep].argmax()]
    return float(s[i]), nodes[i].tolist(), float(np.percentile(s[keep & (s != 0)], 99.9))


def log(msg, logfile=None):
    line = f"[{datetime.datetime.now():%H:%M:%S}] {msg}"
    print(line, flush=True)
    if logfile:
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")


# ---------------------------------------------------------------- geometria de agujeros
def pin_axis():
    a = np.array(HOLES["bulon"]["axis"], float)
    return a / np.linalg.norm(a)


def load_dir():
    """Direccion horizontal perpendicular al bulon (Z de la Tabla 2)."""
    a = pin_axis()
    d = np.cross(a, [0, 0, 1.0])
    return -d / np.linalg.norm(d)   # sentido -X (convenio del grupo); con RBE3 lineal, vM no depende del signo


# Interfaces DETECTADAS en la malla (disenos externos, p. ej. SimJEB, donde cada autor modelo los agujeros a su
# manera: otra longitud, alojamiento o superficie no cilindrica). Si es None se usan los agujeros exactos de 0.stp.
IFACE = None


class InterfaceError(RuntimeError):
    """No se encuentran en la malla los agujeros de pernos / bulon (no tiene sentido reintentar la malla)."""


def detect_interfaces(nodes, tris):
    """Localiza en la superficie de la malla los agujeros de los 4 pernos y del bulon (mismas POSICIONES que 0.stp)."""
    corners = np.unique(np.asarray(tris)[:, :3] - 1)
    X = nodes[corners]
    bolts = []
    for b in HOLES["pernos"]:
        r = np.hypot(X[:, 0] - b["c"][0], X[:, 1] - b["c"][1])
        cand = (r < 7.5) & (X[:, 2] < 45.0)
        if not cand.any():
            raise InterfaceError(f"no se encuentra el agujero del perno en {b['c']}")
        R = float(np.min(r[cand]))
        hole = cand & (r < R + 0.2)
        Rm = float(np.median(r[hole]))
        if not (4.8 <= Rm <= 5.9):
            raise InterfaceError(f"agujero de perno en {b['c']} con radio {Rm:.2f} mm (no es el de un perno M10)")
        bolts.append(dict(c=b["c"], r=Rm, z0=float(X[hole, 2].min()), z1=float(X[hole, 2].max())))
    a = pin_axis(); P = np.mean(np.array(HOLES["bulon"]["centers"]), axis=0)
    v = X - P; t = v @ a; rho = np.linalg.norm(v - np.outer(t, a), axis=1)
    cand = (rho < 12.0) & (np.abs(t) < 40.0)
    if not cand.any():
        raise InterfaceError("no se encuentra el agujero del bulon")
    Rp = float(np.median(rho[cand & (rho < rho[cand].min() + 0.2)]))
    if not (9.0 <= Rp <= 10.6):
        raise InterfaceError(f"agujero del bulon con radio {Rp:.2f} mm")
    th = np.sort(t[cand & (np.abs(rho - Rp) < 0.2)])
    spans, lo = [], th[0]
    for k in range(1, len(th)):
        if th[k] - th[k - 1] > 2.0:
            spans.append((float(lo), float(th[k - 1]))); lo = th[k]
    spans.append((float(lo), float(th[-1])))
    spans = [sp for sp in spans if sp[1] - sp[0] > 1.0]
    return dict(bolts=bolts, pin=dict(r=Rp, P=P.tolist(), spans=spans), tol=0.2)


def bolt_mask(xyz, extra=0.0, tol=0.05):
    """Nodos sobre (extra=0) o cerca (radio R+extra) de las superficies de pernos."""
    m = np.zeros(len(xyz), bool)
    if IFACE is not None:
        tol = max(tol, IFACE["tol"])
        for b in IFACE["bolts"]:
            r = np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1])
            inz = (xyz[:, 2] > b["z0"] - tol - extra) & (xyz[:, 2] < b["z1"] + tol + extra)
            m |= inz & ((np.abs(r - b["r"]) < tol) if extra == 0.0 else (r < b["r"] + extra))
        return m
    z0, z1 = HOLES["pernos_z"]
    for b in HOLES["pernos"]:
        r = np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1])
        inz = (xyz[:, 2] > z0 - tol - extra) & (xyz[:, 2] < z1 + tol + extra)
        if extra == 0.0:
            m |= inz & (np.abs(r - b["r"]) < tol)
        else:
            m |= inz & (r < b["r"] + extra)
    return m


def pin_mask(xyz, which=None, tol=0.05, extra=0.0, half=None):
    a = pin_axis()
    if IFACE is not None:
        tol = max(tol, IFACE["tol"]); pi = IFACE["pin"]
        v = xyz - np.array(pi["P"]); t = v @ a
        rad = np.linalg.norm(v - np.outer(t, a), axis=1)
        m = np.zeros(len(xyz), bool)
        for i, (lo, hi) in enumerate(pi["spans"]):
            if which is not None and i != which:
                continue
            if extra == 0.0:
                m |= (np.abs(rad - pi["r"]) < tol) & (t > lo - tol) & (t < hi + tol)
            else:
                m |= (rad < pi["r"] + extra) & (t > lo - extra) & (t < hi + extra)
        return m
    R = HOLES["bulon"]["r"]
    half = HOLES["bulon"]["half_width"] if half is None else half
    m = np.zeros(len(xyz), bool)
    for i, c in enumerate(HOLES["bulon"]["centers"]):
        if which is not None and i != which:
            continue
        v = xyz - np.array(c)
        t = v @ a
        rad = np.linalg.norm(v - np.outer(t, a), axis=1)
        if extra == 0.0:
            m |= (np.abs(rad - R) < tol) & (np.abs(t) < half + tol)
        else:
            m |= (rad < R + extra) & (np.abs(t) < half + extra)
    return m


# ---------------------------------------------------------------- mallado
GMSH2ANSYS = [0, 1, 2, 3, 4, 5, 6, 7, 9, 8]  # tet10 gmsh -> SOLID187 (verificado en check_tet10)


def mesh_step(step_path, h, hmin=None, curv_n=0, logfile=None, refine=None, algo3d=10, heal=False):
    """Malla tet10. Devuelve nodes(N,3), tets(M,10, orden ANSYS, ids 1-based), surf_nodes(ids)."""
    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    gmsh.option.setNumber("General.NumThreads", 1)  # determinista
    try:
        for k, v in (("Geometry.Tolerance", 1e-4), ("Geometry.OCCFixDegenerated", 1), ("Geometry.OCCFixSmallEdges", 1),
                     ("Geometry.OCCFixSmallFaces", 1), ("Geometry.OCCSewFaces", 1), ("Geometry.OCCMakeSolids", 1)):
            if heal:
                gmsh.option.setNumber(k, v)   # reparacion de la geometria al importar (solo como ultimo recurso)
        gmsh.model.occ.importShapes(step_path)
        gmsh.model.occ.synchronize()
        gmsh.option.setNumber("Mesh.MeshSizeMax", h)
        gmsh.option.setNumber("Mesh.MeshSizeMin", hmin or 1.0)
        gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", curv_n)
        gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 1)
        gmsh.option.setNumber("Mesh.Algorithm", 6)
        gmsh.option.setNumber("Mesh.Algorithm3D", algo3d)  # 10=HXT (determinista con 1 hilo), 1=Delaunay, 4=Frontal
        gmsh.option.setNumber("Mesh.ElementOrder", 2)
        gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)  # aristas rectas: sin distorsion
        gmsh.option.setNumber("Mesh.HighOrderOptimize", 0)
        gmsh.option.setNumber("Mesh.Optimize", 1)
        gmsh.option.setNumber("Mesh.OptimizeNetgen", 1)
        if refine:  # refinamiento local: lista de (puntos xyz, tamano, radio)
            fields = []
            for pts, hs, rad in refine:
                pt_tags = [gmsh.model.occ.addPoint(*p) for p in pts]
                gmsh.model.occ.synchronize()
                fd = gmsh.model.mesh.field.add("Distance")
                gmsh.model.mesh.field.setNumbers(fd, "PointsList", pt_tags)
                ft = gmsh.model.mesh.field.add("Threshold")
                gmsh.model.mesh.field.setNumber(ft, "InField", fd)
                gmsh.model.mesh.field.setNumber(ft, "SizeMin", hs)
                gmsh.model.mesh.field.setNumber(ft, "SizeMax", h)
                gmsh.model.mesh.field.setNumber(ft, "DistMin", rad)
                gmsh.model.mesh.field.setNumber(ft, "DistMax", 2 * rad)
                fields.append(ft)
            fm = gmsh.model.mesh.field.add("Min")
            gmsh.model.mesh.field.setNumbers(fm, "FieldsList", fields)
            gmsh.model.mesh.field.setAsBackgroundMesh(fm)
        t0 = time.time()
        gmsh.model.mesh.generate(3)
        et_chk, _, _ = gmsh.model.mesh.getElements(3)
        if 11 not in list(et_chk):
            raise RuntimeError("gmsh no genero elementos tet10 (volumen no reconocido)")
        tags, coords, _ = gmsh.model.mesh.getNodes()
        idx = {t: i for i, t in enumerate(tags)}
        nodes = coords.reshape(-1, 3)
        et, etag, enodes = gmsh.model.mesh.getElements(3)
        k = list(et).index(11)  # 11 = tet10
        tets = np.array([idx[t] for t in enodes[k]]).reshape(-1, 10)
        st, stag, snodes = gmsh.model.mesh.getElements(2)
        k2 = list(st).index(9)  # 9 = tri6
        tris = np.array([idx[t] for t in snodes[k2]]).reshape(-1, 6)
        log(f"  malla h={h}: {len(nodes)} nodos, {len(tets)} tet10 ({time.time()-t0:.1f}s)", logfile)
    finally:
        gmsh.finalize()
    # compactar (quitar nodos sueltos de puntos auxiliares)
    used = np.unique(tets)
    remap = -np.ones(len(nodes), int)
    remap[used] = np.arange(len(used))
    nodes = nodes[used]
    tets = remap[tets][:, GMSH2ANSYS]
    tris = remap[tris]
    check_tet10(nodes, tets)
    return nodes, tets + 1, tris + 1


def check_tet10(nodes, tets):
    """Verifica que los nodos intermedios estan en la arista correcta (orden SOLID187) y volumen>0."""
    pairs = [(0, 1), (1, 2), (2, 0), (0, 3), (1, 3), (2, 3)]
    sample = tets[:: max(1, len(tets) // 2000)]
    for k, (i, j) in enumerate(pairs):
        mid = 0.5 * (nodes[sample[:, i]] + nodes[sample[:, j]])
        L = np.linalg.norm(nodes[sample[:, i]] - nodes[sample[:, j]], axis=1)
        err = np.linalg.norm(nodes[sample[:, 4 + k]] - mid, axis=1) / L
        assert np.median(err) < 0.05, f"orden tet10 incorrecto en arista {i}-{j}"
    a, b, c, d = (nodes[tets[:, i]] for i in range(4))
    vol = np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a) / 6
    assert (vol > 0).mean() > 0.999, "tetraedros con volumen negativo"


# ---------------------------------------------------------------- entrada MAPDL
def face_nodes(nodes, tris, maskfn):
    """Nodos (1-based) de los triangulos de superficie cuyos 3 vertices cumplen maskfn."""
    t = tris - 1
    ok = maskfn(nodes[t[:, 0]]) & maskfn(nodes[t[:, 1]]) & maskfn(nodes[t[:, 2]])
    return np.unique(t[ok]) + 1


def write_inp(path, nodes, tets, tris, force=42258.0, results="res", pin_half=None):
    fixed = face_nodes(nodes, tris, bolt_mask)
    pin = face_nodes(nodes, tris, lambda x: pin_mask(x, half=pin_half))
    if len(fixed) < 20 or len(pin) < 20:
        raise RuntimeError(f"seleccion de superficies fallida: pernos={len(fixed)} bulon={len(pin)}")
    # nodos de cada perno (para comprobar que estan los 4) y de cada orejeta
    bl = IFACE["bolts"] if IFACE is not None else HOLES["pernos"]
    nper = [len(face_nodes(nodes, tris, lambda x, b=b: bolt_mask_one(x, b))) for b in bl]
    nl = len(IFACE["pin"]["spans"]) if IFACE is not None else 2
    nlug = [len(face_nodes(nodes, tris, lambda x, i=i: pin_mask(x, which=i, half=pin_half))) for i in range(nl)]
    if min(nper) < 5 or min(nlug) < 5:
        raise RuntimeError(f"falta algun agujero en la malla: pernos={nper} orejetas={nlug}")
    d = load_dir()
    pilot = np.mean(HOLES["bulon"]["centers"], axis=0)
    nn = len(nodes)
    L = []
    w = L.append
    w("! Soporte MSD (831_MSD_13_B) - modelo generado automaticamente (scripts/fem.py)\n! Unidades mm-N-MPa-t | SOLID187 | S235 | carga 2 por RBE3 | pernos empotrados\n/NERR,200,99999999\n/PREP7\nET,1,SOLID187\nET,2,MASS21,,,2\nR,2,1e-9\n")
    w(f"MP,EX,1,{E}\nMP,PRXY,1,{NU}\nMP,DENS,1,{RHO}\n")
    w(f"NBLOCK,6,SOLID,{nn},{nn}\n(3i9,6e21.13e3)\n")
    for i, (x, y, z) in enumerate(nodes, 1):
        w(f"{i:9d}{0:9d}{0:9d}{x:21.13e}{y:21.13e}{z:21.13e}\n")
    w("N,R5.3,LOC,       -1,\n")
    ne = len(tets)
    w(f"EBLOCK,19,SOLID,{ne},{ne}\n(19i10)\n")
    for k, t in enumerate(tets, 1):
        w(("%10d" * 19 + "\n") % (1, 1, 1, 1, 0, 0, 0, 0, 10, 0, k, *t[:8]))
        w(("%10d" * 2 + "\n") % (t[8], t[9]))
    w(f"{-1:10d}\n")
    # componentes
    def comp(name, ids):
        w("NSEL,NONE\n")
        for c in range(0, len(ids), 8):
            chunk = ids[c:c + 8]
            w("".join(f"NSEL,A,NODE,,{i}\n" for i in chunk))
        w(f"CM,{name},NODE\n")
    comp("FIJO", fixed)
    comp("BULON", pin)
    w("ALLSEL\n")
    pid = nn + 1
    w(f"N,{pid},{pilot[0]},{pilot[1]},{pilot[2]}\nTYPE,2\nREAL,2\nE,{pid}\n")
    w(f"RBE3,{pid},ALL,BULON\n")
    w("CMSEL,S,FIJO\nD,ALL,ALL,0\nALLSEL\n")
    w(f"! ---- CARGA: cambiar FUERZA (N) si se desea (37800 = Fig. 2 horizontal | 42258 = Tabla 2)\n*SET,FUERZA,{force}\n")
    w(f"F,{pid},FX,FUERZA*({d[0]:.8f})\nF,{pid},FY,FUERZA*({d[1]:.8f})\nF,{pid},FZ,FUERZA*({d[2]:.8f})\n")
    w("FINISH\n/SOLU\nANTYPE,STATIC\nEQSLV,SPARSE\nSOLVE\nFINISH\n")
    # post
    w("/POST1\nSET,LAST\nALLSEL\n")
    w("CMSEL,S,FIJO\nFSUM\n*GET,RX,FSUM,0,ITEM,FX\n*GET,RY,FSUM,0,ITEM,FY\n*GET,RZ,FSUM,0,ITEM,FZ\nALLSEL\n")
    w("ESEL,S,TYPE,,1\nETABLE,EV,VOLU\nSSUM\n*GET,VOLT,SSUM,0,ITEM,EV\nALLSEL\n")
    w(f"*CFOPEN,{results}_glob,txt\n*VWRITE,RX,RY,RZ,VOLT\n(4E18.9)\n*CFCLOS\n")
    w("ESEL,S,TYPE,,1\nNSLE,S\n*GET,NMAX,NODE,0,NUM,MAX\n")
    w("*DIM,NM,ARRAY,NMAX\n*DIM,UX_,ARRAY,NMAX\n*DIM,UY_,ARRAY,NMAX\n*DIM,UZ_,ARRAY,NMAX\n*DIM,SE_,ARRAY,NMAX\n")
    w("*VGET,NM,NODE,1,NSEL\n*VGET,UX_,NODE,1,U,X\n*VGET,UY_,NODE,1,U,Y\n*VGET,UZ_,NODE,1,U,Z\n*VGET,SE_,NODE,1,S,EQV\n")
    w(f"*CFOPEN,{results}_nod,txt\n*VMASK,NM\n*VWRITE,UX_(1),UY_(1),UZ_(1),SE_(1)\n(4E16.7)\n*CFCLOS\n")
    w("ALLSEL\nFINISH\n")
    with open(path, "w") as f:
        f.writelines(L)
    return dict(n_fixed=len(fixed), n_pin=len(pin), nodes_per_bolt=nper, nodes_per_lug=nlug,
                pilot=pilot.tolist(), load_dir=d.tolist(), n_nodes=nn, n_elems=ne)


def bolt_mask_one(xyz, b, tol=0.05):
    if "z0" in b:                                   # agujero detectado en la malla
        tol = max(tol, IFACE["tol"] if IFACE else 0.2)
        r = np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1])
        return (xyz[:, 2] > b["z0"] - tol) & (xyz[:, 2] < b["z1"] + tol) & (np.abs(r - b["r"]) < tol)
    z0, z1 = HOLES["pernos_z"]
    r = np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1])
    return (xyz[:, 2] > z0 - tol) & (xyz[:, 2] < z1 + tol) & (np.abs(r - b["r"]) < tol)


# ---------------------------------------------------------------- metricas
def read_results(workdir, nodes, results="res", force=42258.0, excl=(3.0,), pin_half=None):
    g = np.loadtxt(os.path.join(workdir, f"{results}_glob.txt"))
    nod = np.loadtxt(os.path.join(workdir, f"{results}_nod.txt"))
    n = len(nodes)
    u = nod[:n, :3]
    s = nod[:n, 3]
    corner = s != 0.0   # MAPDL no calcula tensiones en los nodos intermedios de SOLID187 (quedan a 0)
    umag = np.linalg.norm(u, axis=1)
    R = g[:3]
    d = np.array(load_dir())
    out = dict(
        volume_mm3=float(g[3]), mass_kg=float(g[3] * RHO * 1000),
        reaction=R.tolist(), reaction_err_pct=float(min(np.linalg.norm(R - force * d), np.linalg.norm(R + force * d)) / force * 100),
        vm_max_raw=float(s.max()), vm_p999=float(np.percentile(s[corner], 99.9)),
        u_max=float(umag.max()), ux_max=float(np.abs(u[:, 0]).max()),
        uy_max=float(np.abs(u[:, 1]).max()), uz_max=float(np.abs(u[:, 2]).max()),
        vm_max_raw_xyz=nodes[int(s.argmax())].tolist(),
    )
    out["vm_metric"], out["vm_metric_xyz"], out["vm_metric_p999"] = stress_metric(nodes, s, pin_half)
    # sensibilidad de la metrica a las zonas de exclusion (trazabilidad para el informe)
    for eb, ep in ((0.0, 0.0), (3.0, 0.0), (5.0, 0.0), (3.0, 2.0), (8.0, 2.0)):
        out[f"vm_ex_b{eb:g}_p{ep:g}"] = stress_metric(nodes, s, pin_half, eb, ep)[0]
    out["fs_metric"] = SY / out["vm_metric"]
    for e in excl:
        keep = ~bolt_mask(nodes, extra=e)  # solo pernos
        out[f"vm_metric_ex{e:g}"] = float(s[keep].max())
        out[f"vm_metric_ex{e:g}_xyz"] = nodes[np.flatnonzero(keep)[s[keep].argmax()]].tolist()
    return out, s, u
