"""Imagenes de geometria (STEP) y de resultados con camara fija (para comparar y para el timelapse)."""
import os
import warnings
import numpy as np
import pyvista as pv
warnings.filterwarnings("ignore", category=FutureWarning)

pv.OFF_SCREEN = True
CAM = [(190, -300, 170), (12, -74, 22), (0, 0, 1)]   # camara fija para todas las imagenes


def step_to_polydata(step_path, tol=0.15):
    import cadquery as cq
    shp = cq.importers.importStep(step_path).val()
    verts, tris = shp.tessellate(tol, 0.3)
    pts = np.array([(v.x, v.y, v.z) for v in verts])
    faces = np.hstack([np.full((len(tris), 1), 3), np.array(tris)]).ravel()
    return pv.PolyData(pts, faces)


def geometry_png(step_path, png, title="", color="#9db4c8"):
    mesh = step_to_polydata(step_path)
    p = pv.Plotter(off_screen=True, window_size=(1280, 900))
    p.set_background("white")
    p.add_mesh(mesh, color=color, smooth_shading=True, specular=0.3)
    if title:
        p.add_text(title, font_size=13, color="black")
    p.camera_position = CAM
    p.add_axes()
    p.screenshot(png)
    p.close()


def panel4(wd, title, info_lines, clim=(0, 250)):
    """Ficha 2x2: geometria | von Mises | desplazamiento (deformada) | datos. Lee campos.npz de wd."""
    d = np.load(os.path.join(wd, "campos.npz"))
    nodes, tris, vm, u = d["nodes"], d["tris"] - 1, d["vm"], d["u"]
    faces = np.hstack([np.full((len(tris), 1), 3), tris[:, :3]]).ravel()
    mesh = pv.PolyData(np.asarray(nodes, float), faces)
    mesh["von Mises (MPa)"] = vm
    umag = np.linalg.norm(u, axis=1)
    scale = 15.0 / max(umag.max(), 1e-9)               # deformada visible (~15 mm el maximo)
    dmesh = pv.PolyData(np.asarray(nodes + scale * u, float), faces)
    dmesh["desplazamiento (mm)"] = umag
    p = pv.Plotter(off_screen=True, shape=(2, 2), window_size=(1800, 1350), border=True)
    p.set_background("white")
    sb = dict(title_font_size=20, label_font_size=17, n_labels=5, vertical=True, position_x=0.84,
              position_y=0.1, height=0.75, color="black")
    p.subplot(0, 0)
    p.add_mesh(mesh, color="#9db4c8", smooth_shading=True, specular=0.3)
    head = title + ("\n" + info_lines[0] if info_lines else "")
    p.add_text("Geometria 3D  |  " + head, font_size=11, color="black"); p.camera_position = CAM
    extra = [ln for ln in info_lines[1:] if ln.strip() and not ln.startswith("   ux") and not ln.startswith(("Tension bruta", "Malla"))][:18]
    if extra:      # datos y operaciones aplicadas al original (abajo a la izquierda)
        p.add_text("\n".join(extra), position="lower_left", font_size=10, color="#1a1a1a", font="courier")
    p.subplot(0, 1)
    p.add_mesh(mesh, scalars="von Mises (MPa)", cmap="turbo", clim=clim, scalar_bar_args=dict(fmt="%.0f", **sb))
    p.add_text("Tension de von Mises (MPa)", font_size=12, color="black"); p.camera_position = CAM
    p.subplot(1, 0)
    p.add_mesh(dmesh, scalars="desplazamiento (mm)", cmap="viridis", scalar_bar_args=dict(fmt="%.3f", **sb))
    p.add_mesh(mesh, style="wireframe", color="#bfbfbf", opacity=0.08)
    p.add_text(f"Desplazamiento total (mm) - deformada x{scale:.0f}", font_size=12, color="black"); p.camera_position = CAM
    p.subplot(1, 1)
    # RADIOGRAFIA: piel exterior semitransparente + cavidades interiores cerradas en rojo
    surf = pv.PolyData(np.asarray(nodes, float), faces).clean()
    n_cav = 0
    try:
        conn = surf.connectivity(extraction_mode="all")
        rid = np.asarray(conn.cell_data["RegionId"])
        regs = [conn.extract_cells(np.flatnonzero(rid == k)).extract_surface() for k in np.unique(rid)]
        diag = [rg.length for rg in regs]
        outer = int(np.argmax(diag))
        p.add_mesh(regs[outer], color="#8fa3b5", opacity=0.22, smooth_shading=True)
        p.add_mesh(regs[outer].extract_feature_edges(feature_angle=35, boundary_edges=False, manifold_edges=False),
                   color="#2b3a4a", line_width=1.2)
        for k, rg in enumerate(regs):
            if k != outer:
                p.add_mesh(rg, color="#d7301f", opacity=0.85, smooth_shading=True); n_cav += 1
    except Exception:
        p.add_mesh(surf, color="#8fa3b5", opacity=0.22)
    try:
        p.enable_depth_peeling(10)
    except Exception:
        pass
    p.add_text("Radiografia: interior visible" + (f"  |  {n_cav} cavidad(es) cerrada(s) en rojo" if n_cav else
               "  (sin cavidades cerradas)"), font_size=12, color="black")
    p.camera_position = CAM
    out = os.path.join(wd, "resumen.png")
    p.screenshot(out)
    p.close()
    return out


def results_png(nodes, tris, scal, png, title="", label="von Mises (MPa)", clim=(0, 250), cmap="turbo", marker=None):
    t = np.asarray(tris) - 1
    faces = np.hstack([np.full((len(t), 1), 3), t[:, :3]]).ravel()
    mesh = pv.PolyData(np.asarray(nodes), faces)
    mesh[label] = np.asarray(scal)
    p = pv.Plotter(off_screen=True, window_size=(1280, 900))
    p.set_background("white")
    p.add_mesh(mesh, scalars=label, cmap=cmap, clim=clim,
               scalar_bar_args=dict(title=label, title_font_size=26, label_font_size=22, n_labels=6,
                                    fmt="%.0f", vertical=True, position_x=0.86, position_y=0.12,
                                    height=0.72, color="black"))
    if marker is not None:
        p.add_mesh(pv.Sphere(radius=2.5, center=marker), color="magenta")
    if title:
        p.add_text(title, font_size=13, color="black")
    p.camera_position = CAM
    p.add_axes()
    p.screenshot(png)
    p.close()
