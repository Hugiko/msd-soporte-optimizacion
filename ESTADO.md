# Estado del proyecto y plan pendiente

Última actualización: 23/11/2026. Detalle de cada decisión en `bitacora.md`; funcionamiento completo en `DOCUMENTACION.md`.

## Objetivo
Partir del soporte del enunciado (`0.stp`) y modificarlo paso a paso, con un porqué para cada cambio (reglas de diseño respaldadas por datos), hasta el soporte de **mínima masa** que cumple **coeficiente de seguridad ≥ 1,0 (σ ≤ 215 MPa, obligatorio)** y **u ≤ 0,25 mm**, sin mover los 4 agujeros de los pernos ni los 2 del bulón.
- **Carga: 42 258 N** en −X (Tabla 2), confirmada por el profesor el 23/11/2026.
- Con esta carga el original **no cumple**: ≈ 238 MPa, CS ≈ 0,90.

## Hecho
- **Fases 0–2**: ANSYS Student 2026 R1 por script (`-p ansys`, 128 000 nodos, una sesión), modelo base validado, métrica con exclusión de 5 mm alrededor de los pernos y figuras en `figuras/`.
- **Pipeline de evaluación** (`scripts/evaluate.py`): geometría → malla tet10 → MAPDL → métricas → imágenes y ficha; además guarda el campo de tensiones con los tetraedros para analizarlo.
- **Enfoque anterior** (familias + optimizador bayesiano, 22–23/11): 624 diseños con 37 800 N, sin convergencia clara. Archivado en `runs/archivo/opt_37800N_familias_hasta_20261123/`; sus datos se usan como evidencia de las reglas.
- **Nuevo enfoque (23/11)**:
  1. [hecho] `estudio_simjeb.py`: las 381 soluciones publicadas con nuestras condiciones (pasada rápida + completa, reanudable).
     **En marcha** desde las 14:55 del 23/11 (unas 3–4 h).
  2. [hecho] `campo.py`: análisis del campo (material ocioso, pico y concentración, zonas, ligamentos, dónde caben cortes).
  3. [hecho] `reglas.py` + `DESIGN_RULES.md`: 10 reglas con condición, operación, porqué, evidencia y estadísticas.
     - R5 (alojamiento más ancho) ya está **desactivada por los datos**.
     - R4 (collar) está **respaldada** por una prueba directa.
  4. [hecho] `operaciones.py`: 7 operaciones (3 quitan, 4 añaden o reforman) con zonas protegidas y verificación de los 6 agujeros.
  5. [hecho] `optimizer.py` nuevo:
     - iteraciones con evaluación rápida comparada en la misma malla y evaluación completa solo de la mejor;
     - aceptar, revertir o invertir;
     - hitos con malla fina y Workbench.
  6. [hecho] Trazabilidad: `ITERACIONES.md`, un commit por iteración y un mensaje de Discord por iteración.
  7. [hecho] Limpieza: eliminadas las familias, BoTorch, el árbol de ramas y `report.py`; configuración nueva.

## Pendiente
1. **En marcha (23/11, 15:19)**: `optimizar.bat` lanzado. Espera a que termine el estudio (unas 4 h), escribe las reglas y empieza a optimizar solo.
2. Cuando termine el estudio: revisar `DESIGN_RULES.md` con todos los datos (R1–R3 y R7 se completan con SimJEB).
3. Prueba corta ya hecha (2 iteraciones): collar de 6 mm en los pernos 1 y 3 → 238 → 201,9 MPa (cumple; malla fina 212,5); después, rebaje de material ocioso: −35 g, +0,9 % de tensión.
3. Fase 5:
   - verificación final con malla fina y convergencia;
   - modelo de tornillo realista;
   - comparación del original con el final;
   - informe y guion de defensa.
