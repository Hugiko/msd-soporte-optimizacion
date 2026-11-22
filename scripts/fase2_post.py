"""Post-proceso Fase 2: tabla y curva de convergencia + mapas de von Mises/desplazamiento del original."""
import os, sys, json, glob
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
import fem

B = os.path.join(fem.ROOT, "runs", "base")
FIG = os.path.join(fem.ROOT, "figuras")
os.makedirs(FIG, exist_ok=True)

ms = []
for f in glob.glob(os.path.join(B, "h*", "metrics.json")):
    m = json.load(open(f)); m["dir"] = os.path.dirname(f); ms.append(m)
ms.sort(key=lambda m: m["n_nodes"])

print(f"{'malla':>10} {'nodos':>7} {'elem':>6} {'masa kg':>8} {'errR %':>7} {'vM bruto':>9} {'METRICA':>8} {'FS':>5} {'umax mm':>8}")
for m in ms:
    print(f"{os.path.basename(m['dir']):>10} {m['n_nodes']:7d} {m['n_elems']:6d} {m['mass_kg']:8.4f} {m['reaction_err_pct']:7.4f} "
          f"{m['vm_max_raw']:9.1f} {m['vm_metric']:8.1f} {m['fs_metric']:5.2f} {m['u_max']:8.4f}")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
n = [m["n_nodes"] / 1000 for m in ms]
ax[0].plot(n, [m["vm_max_raw"] for m in ms], "s--", c="0.5", label="σvM máx. bruto (singular)")
ax[0].plot(n, [m["vm_metric"] for m in ms], "o-", c="C0", lw=2, label="Métrica robusta (exclusión 5 mm pernos / 2 mm bulón)")
ax[0].axhline(fem.SY, c="C3", ls=":", label="σy = 215 MPa")
ax[0].set_xlabel("Nº de nodos (miles)"); ax[0].set_ylabel("Tensión de von Mises (MPa)")
ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
ax[1].plot(n, [m["u_max"] for m in ms], "o-", c="C2")
ax[1].set_xlabel("Nº de nodos (miles)"); ax[1].set_ylabel("Desplazamiento máximo (mm)"); ax[1].grid(alpha=.3)
fig.suptitle("Convergencia de malla – soporte original, acero S235, carga 2 (42 258 N)")
fig.tight_layout(); fig.savefig(os.path.join(FIG, "fase2_convergencia.png"), dpi=150)

# mapa de von Mises de la malla mas fina
import pyvista as pv
pv.OFF_SCREEN = True
m = ms[-1]; d = m["dir"]
nodes = np.load(os.path.join(d, "nodes.npy")); s = np.load(os.path.join(d, "vm.npy"))
u = np.load(os.path.join(d, "u.npy")); tris = np.load(os.path.join(d, "tris.npy")) - 1
faces = np.hstack([np.full((len(tris), 1), 3), tris[:, :3]]).ravel()
mesh = pv.PolyData(nodes, faces)
mesh["vM (MPa)"] = s
mesh["|u| (mm)"] = np.linalg.norm(u, axis=1)
for name, scal, clim, cmap in (("fase2_vonmises_original.png", "vM (MPa)", [0, 250], "turbo"),
                               ("fase2_desplazamiento_original.png", "|u| (mm)", None, "viridis")):
    p = pv.Plotter(off_screen=True, window_size=(1400, 1000))
    p.add_mesh(mesh, scalars=scal, cmap=cmap, clim=clim, show_edges=False,
               scalar_bar_args=dict(title=scal, title_font_size=28, label_font_size=24, n_labels=6, fmt="%.0f" if "vM" in scal else "%.3f",
                                    vertical=True, position_x=0.85, position_y=0.15, height=0.7))
    if "vM" in scal:
        p.add_mesh(pv.Sphere(radius=2.5, center=m["vm_metric_xyz"]), color="magenta")
        p.add_text(f"Métrica = {m['vm_metric']:.0f} MPa (esfera magenta)   bruto = {m['vm_max_raw']:.0f} MPa", font_size=14)
    p.camera_position = [(180, -260, 160), (15, -73, 20), (0, 0, 1)]
    p.add_axes()
    p.screenshot(os.path.join(FIG, name))
    p.close()
print("figuras en", FIG)
