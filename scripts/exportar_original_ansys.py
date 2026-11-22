"""Genera el paquete para abrir en ANSYS el soporte ORIGINAL (0.stp) con las condiciones del proyecto,
lo resuelve aqui para conocer los resultados de referencia y escribe un LEEME con los pasos."""
import os, sys, json, shutil, zipfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fem, render
from run_mapdl import run

F = float(sys.argv[1]) if len(sys.argv) > 1 else 37800.0
OUT = os.path.join(fem.ROOT, "entregas", "modelo_original_ansys")
os.makedirs(OUT, exist_ok=True)
LOG = os.path.join(OUT, "progreso.log")
step = os.path.join(fem.ROOT, "cad", "0.stp")
fem.log(f"Malla del original (h=4 mm, tet10) y modelo de ANSYS con F = {F:.0f} N", LOG)
nodes, tets, tris = fem.mesh_step(step, 4.0, hmin=1.5, logfile=LOG)
info = fem.write_inp(os.path.join(OUT, "model.inp"), nodes, tets, tris, force=F)
gui = f"""! =====================================================================
! SOPORTE ORIGINAL (0.stp) - acero S235 - carga {F:.0f} N en -X (horizontal, perpendicular al bulon)
! Mechanical APDL 2026 R1:
!   1. File > Change Directory...  -> esta carpeta
!   2. File > Read Input from...   -> abrir_en_ansys.inp
! Hace: malla SOLID187 ({info['n_nodes']} nodos), E=210 GPa, nu=0,3, empotramiento (UX=UY=UZ=0)
! en las superficies de los 4 agujeros de pernos, carga repartida por RBE3 desde un nodo
! piloto (centro entre orejetas) a las superficies de los 2 agujeros del bulon. Resuelve.
! Para cambiar la carga: editar *SET,FUERZA en model.inp
! =====================================================================
/INPUT,model,inp
/POST1
SET,LAST
/EFACET,1
/SHOW,WIN32C
/VIEW,1,1,-1.5,1
/ANG,1
/AUTO,1
/PLOPTS,INFO,3
CMSEL,S,FIJO
FSUM            ! suma de reacciones en los pernos (debe ser igual a la carga)
ALLSEL
PRRSOL,F
PLNSOL,S,EQV    ! tension de von Mises (MPa)
"""
open(os.path.join(OUT, "abrir_en_ansys.inp"), "w").write(gui)
shutil.copy(step, os.path.join(OUT, "0.stp"))

fem.log("Resolviendo aqui para obtener los valores de referencia...", LOG)
r = run(OUT, "model.inp", timeout=1800, np_=4, job="file", logfile=LOG)
m, s, u = fem.read_results(OUT, nodes, force=F, excl=(), pin_half=None)
json.dump(m, open(os.path.join(OUT, "resultados_referencia.json"), "w"), indent=1)
render.results_png(nodes, tris, s, os.path.join(OUT, "vonmises_original.png"),
                   f"Original | F = {F:.0f} N | metrica {m['vm_metric']:.0f} MPa | bruto {m['vm_max_raw']:.0f} MPa",
                   marker=m["vm_metric_xyz"])
d = fem.load_dir(); pilot = info["pilot"]
leeme = f"""SOPORTE ORIGINAL (0.stp) - MODELO DE ANSYS CON LAS CONDICIONES DEL PROYECTO
================================================================================
Grupo 831_MSD_13_B - Soporte 6 - acero S235 - carga {F:.0f} N

A) MECHANICAL APDL (reproduce EXACTAMENTE mis resultados, misma malla)
   1. Abrir "Mechanical APDL 2026 R1".
   2. File > Change Directory... -> esta carpeta.
   3. File > Read Input from... -> abrir_en_ansys.inp   (tarda ~1 min)
   4. Sale el mapa de von Mises. En la ventana de salida, FSUM muestra las reacciones.

B) WORKBENCH / MECHANICAL (para montarlo vosotros "a mano")
   1. Static Structural. Geometry -> importar 0.stp (unidades mm).
   2. Material: E = 210000 MPa, nu = 0,3, densidad 7850 kg/m3 (S235).
   3. Malla: tetraedros de 2.o orden (Element Order: Quadratic), tamano 4 mm.
   4. Fixed Support: las caras cilindricas de los 4 agujeros de pernos (diametro 10,31 / 10,67 mm,
      desde z = 0,63 hasta z = 7,85 mm). SOLO el cilindro del agujero (lo azul de la Fig. 3).
   5. Remote Force sobre las caras cilindricas de los 2 agujeros del bulon (diametro 19,11 mm):
        - Location (punto piloto): X = {pilot[0]:.3f}  Y = {pilot[1]:.3f}  Z = {pilot[2]:.3f} mm
        - Componentes: Fx = {F*d[0]:.1f} N   Fy = {F*d[1]:.1f} N   Fz = 0 N
        - Behavior: Deformable  (equivale al RBE3 que uso)
   6. Resolver: Equivalent Stress, Total Deformation, Directional Deformation X/Y/Z,
      Force Reaction en el Fixed Support.

RESULTADOS DE REFERENCIA (mi calculo, malla de {info['n_nodes']} nodos / {info['n_elems']} elementos)
   Masa (volumen de la malla x 7850)           : {m['mass_kg']:.4f} kg
   Reaccion total en pernos                     : ({m['reaction'][0]:.1f}, {m['reaction'][1]:.1f}, {m['reaction'][2]:.1f}) N  (error {m['reaction_err_pct']:.4f} %)
   Tension von Mises MAXIMA BRUTA               : {m['vm_max_raw']:.1f} MPa  en {np.round(m['vm_max_raw_xyz'],1).tolist()}
       -> esta en el borde de un agujero de perno EMPOTRADO: es una singularidad
          (crece sin limite al refinar la malla), no una tension real.
   Tension metrica (excluye 5 mm alrededor de los pernos y 2 mm del bulon): {m['vm_metric']:.1f} MPa
                                                 en {np.round(m['vm_metric_xyz'],1).tolist()}
   Coeficiente de seguridad 215 / metrica       : {215/m['vm_metric']:.2f}
   Desplazamiento maximo |u|                    : {m['u_max']:.4f} mm  (ux {m['ux_max']:.4f}, uy {m['uy_max']:.4f}, uz {m['uz_max']:.4f})

   En Workbench la malla sera distinta: la tension bruta maxima (singular) puede salir muy diferente;
   compare la tension lejos de los bordes de los agujeros de los pernos, las reacciones y los desplazamientos.
"""
open(os.path.join(OUT, "LEEME.txt"), "w", encoding="utf-8").write(leeme)
for f in os.listdir(OUT):
    if f.split(".")[-1] in ("rst", "full", "esav", "emat", "osav", "page", "mntr", "ldhi", "lock", "db", "dbb", "err"):
        try:
            os.remove(os.path.join(OUT, f))
        except OSError:
            pass
with zipfile.ZipFile(os.path.join(fem.ROOT, "entregas", "modelo_original_ansys.zip"), "w", zipfile.ZIP_DEFLATED) as z:
    for f in ("model.inp", "abrir_en_ansys.inp", "0.stp", "LEEME.txt", "vonmises_original.png", "resultados_referencia.json"):
        z.write(os.path.join(OUT, f), f)
print(leeme)
