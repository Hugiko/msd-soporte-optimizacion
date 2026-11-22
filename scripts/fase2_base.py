"""Fase 2: modelo base (soporte original 0.stp, acero S235, carga 2) + estudio de convergencia.
Uso: python fase2_base.py h1 h2 ...   (tamanos de malla en mm)
Resultados en runs/base/h<h>/ y resumen en runs/base/convergencia.csv
"""
import os, sys, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import fem
from run_mapdl import run

ROOT = fem.ROOT
OUT = os.path.join(ROOT, "runs", "base")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "progreso.log")
STEP = os.path.join(ROOT, "cad", "0.stp")
EXCL = (2.0, 3.0, 5.0)

pairs = [tuple(float(v) for v in a.split(":")) for a in sys.argv[1:]] or [(6, 2.5), (5, 2.0), (4, 1.5)]
hs = pairs
fem.log(f"=== FASE 2: modelo base, tamanos {hs} ===", LOG)
rows = []
for h, hmin in hs:
    wd = os.path.join(OUT, f"h{h:g}_m{hmin:g}")
    os.makedirs(wd, exist_ok=True)
    fem.log(f"--- h = {h} mm: mallando", LOG)
    try:
        nodes, tets, surf = fem.mesh_step(STEP, h, hmin=hmin, logfile=LOG)
        info = fem.write_inp(os.path.join(wd, "model.inp"), nodes, tets, surf)
        fem.log(f"  pernos: {info['nodes_per_bolt']} nodos  orejetas: {info['nodes_per_lug']} nodos", LOG)
        r = run(wd, "model.inp", timeout=1800, np_=4, job="base", logfile=LOG)
        if r["status"] != "ok":
            fem.log(f"  FALLO MAPDL: {r}", LOG)
            continue
        m, s, u = fem.read_results(wd, nodes, excl=EXCL)
        m.update(info, h=h, hmin=hmin, solve_s=r["seconds"])
        np.save(os.path.join(wd, "nodes.npy"), nodes)
        np.save(os.path.join(wd, "vm.npy"), s)
        np.save(os.path.join(wd, "u.npy"), u)
        np.save(os.path.join(wd, "tris.npy"), surf)
        json.dump(m, open(os.path.join(wd, "metrics.json"), "w"), indent=1)
        fem.log(f"  masa={m['mass_kg']:.4f} kg  err_reac={m['reaction_err_pct']:.4f}%  "
                f"vM_bruto={m['vm_max_raw']:.1f}  METRICA={m['vm_metric']:.1f}  "
                f"P99.9={m['vm_p999']:.1f} MPa  umax={m['u_max']:.4f} mm", LOG)
        rows.append(m)
    except Exception as e:
        fem.log(f"  ERROR h={h}: {e!r}", LOG)

import csv
keys = ["h", "hmin", "n_nodes", "n_elems", "mass_kg", "reaction_err_pct", "vm_max_raw", "vm_metric", "vm_metric_p999", "fs_metric", "vm_p999"] + \
       [f"vm_metric_ex{e:g}" for e in EXCL] + ["u_max", "ux_max", "uy_max", "uz_max", "solve_s"]
with open(os.path.join(OUT, "convergencia.csv"), "a", newline="") as f:
    wr = csv.writer(f)
    if f.tell() == 0:
        wr.writerow(keys)
    for m in rows:
        wr.writerow([m.get(k) for k in keys])
fem.log("=== FIN FASE 2 ===", LOG)
