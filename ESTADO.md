# Estado del proyecto y plan pendiente

Última actualización: 23/11/2026. Detalle de cada decisión en `bitacora.md`.

## Objetivo
Un programa autónomo (`optimizar.bat`) que genera piezas, las calcula en ANSYS, aprende de cada resultado y converge al
soporte de **mínima masa** que cumple un **coeficiente de seguridad ≥ 1,15 (σ ≤ 187 MPa)** (fuera de la singularidad de los pernos) y **u ≤ 0,25 mm**,
manteniendo fijos los 4 agujeros de los pernos y los 2 del bulón. Carga: 37 800 N en −X (configurable a 42 258 N).

## Hecho
- **Fases 0–2**: ANSYS Student 2026 R1 por script (licencia `-p ansys`, límite de 128 000 nodos, una sola sesión a la vez).
  Modelo base validado (reacciones exactas, convergencia de malla, métrica con exclusión de 5 mm alrededor de los pernos).
  Figuras en `figuras/`; resultados de referencia del original en `cad/referencia_original/`.
- **Pipeline de evaluación** (`scripts/evaluate.py`): geometría → malla tet10 (gmsh) → MAPDL → métricas → imágenes;
  reintentos de malla, **tiempo máximo de mallado** (proceso aparte, 300 s), espera si la licencia está ocupada y ficha
  `resumen.png` (geometría | von Mises | deformada | radiografía).
- **Familias de geometría activas**: `simjeb` (NUEVA, 23/11: diseños del concurso GE/SimJEB modificados), `refuerzo` (v2: collares junto a
  los tornillos + vaciado; baja el pico del original de 212,9 a 181,2 MPa) y `cero` (diseño nuevo). `vaciado` queda **retirada**
  (62 diseños sin ninguno válido; sus resultados se conservan). Los 6 agujeros se verifican en cada diseño.
- **Reglas de impresión 3D** (activadas, `reglas_impresion_3d` en `config.json`): techos interiores a 45°, agujero de evacuación de
  Ø5 por cámara y ninguna cavidad cerrada. Fuentes en `docs/fabricacion_aditiva.md`. El enunciado no lo exige
  (la frase se refiere al concurso de GE de 2013); es una decisión de diseño propia.
- **Optimizador** (`scripts/optimizer.py`): DOE → procesos gaussianos (BoTorch) para masa, tensión y desplazamiento → **ramas**
  (árbol genealógico: fina / amplia / cruce por turnos, exploradora al azar cada 2 ramas, congelado de parámetros en las finas) → «cualquier mejora cuenta».
  **Anti-estancamiento** (23/11): ramas de 12 pruebas, paso mínimo 0,05, mutaciones grandes, distancia mínima 0,03 a todo lo probado,
  25 % de turnos en una rama al azar y, si una familia lleva 25 diseños sin mejorar un 0,3 %, 2 exploradoras nuevas.
  Detección de piezas repetidas, **filtro por predicción** (si el modelo es fiable) y **pasada rápida** con malla gruesa.
- **Salidas**: proyecto Workbench `.wbpj` (resuelto, en el PC) + `.wbpz` (en GitHub) en cada nueva mejora; historial; galería
  cronológica de todos los diseños; gráfica en el tiempo + gráfica interactiva html; árbol (`ARBOL.md` + `arbol.png`);
  panel `README.md`; limpieza automática; subida a GitHub en segundo plano; reanudación tras apagar el PC.
- **Limpieza total y reinicio del repositorio de GitHub** (historial limpio, un solo commit).

## En curso / pendiente
1. [hecho] Tiempo máximo de mallado: un gmsh colgado ya no bloquea el programa (comprobado: 6 estrategias fallidas en 72 s).
2. [hecho] Relleno de la familia `refuerzo` simplificado (capas de 4 mm, contornos suavizados).
3. [hecho] Familia `refuerzo` v1 (relleno escalonado) no se podía mallar → sustituida por la v2 (collares cilíndricos), que funciona.
4. [hecho] Malla colgada en la pasada rapida (gmsh con malla gruesa sobre geometrias del original): limite de 60 s por intento,
   deteccion de cierre del proceso, pasada rapida opcional (si falla -> malla normal) y solo en la familia `cero`.
5. [hecho] **Discord**: canal del mejor diseno (un mensaje que se edita), canal del arbol (imagen al cambiar) y canal de todo lo
   generado; enlaces en `discord_webhooks.json` (NO se sube a GitHub). Proteccion ante errores inesperados (se avisa y se sigue),
   `optimizar.bat` se reinicia solo si el programa cae, control de espacio en disco.
6. [hecho] Prueba completa (`--prueba`, 2 familias): sin errores. Ramas (V1 -> V1.1/V1.2 -> V1.1.1/V1.1.2/V1.1.3 cruce), pasada
   rapida (descarta disenos de `cero` en ~40 s), piezas repetidas reutilizadas, galeria, arbol en imagen, panel y Discord (3 canales).
7. [hecho] Limpieza automatica: wbpz solo de los 10 ultimos mejores en GitHub; wbpj resueltos solo 3 en el PC; datos y fichas siempre.
8. [hecho] Pruebas borradas (PC y Discord), programa subido a GitHub y listo: doble clic en `optimizar.bat`.
9. [hecho] Verificación automática con malla fina de cada candidato a nuevo mejor; geometría construida una sola vez por pieza.
10. [hecho] Criterio aeronáutico: coeficiente de seguridad ≥ 1,15 (σ ≤ 187 MPa) obligatorio y, entre piezas válidas, menor puntuación masa × aprovechamiento^0,15. Discord activo siempre.
11. [hecho, 23/11] **La búsqueda se estancaba** (cambios diminutos en la misma rama toda la noche). Cambios:
    - Familia **`simjeb`** (`scripts/geometry_simjeb.py`): SimJEB (Whalen et al., 2021; Harvard Dataverse, doi:10.7910/DVN/XFUWJG)
      recoge los ~380 diseños del GE Jet Engine Bracket Challenge en el MISMO sistema de coordenadas que nuestro `0.stp` (que es su
      diseño n.º 0). Se toman los más ligeros que el original con tensión horizontal estimada ≤ 260 MPa, se descartan los que no
      tienen los agujeros del enunciado (comprobación previa en `datos_simjeb/compatibilidad.json`), se calculan los 40 más
      prometedores **tal cual** (torneo) y después se **modifican**: collares junto a los pernos (añaden) y 2 aligeramientos
      pasantes verticales (quitan; nunca tocan pernos ni orejetas; imprimibles). Los agujeros se detectan en la malla.
    - Optimizador: ramas por turnos entre hermanas, anti-estancamiento, exploradoras más frecuentes, mutaciones grandes.
    - Proyecto Workbench válido también para diseños SimJEB (caras de pernos/bulón según lo detectado en la malla).
    - **Sin perder el progreso**: el archivado es ahora por familia (añadir una familia no archiva nada); `runs/opt_37800N` sigue igual.
12. Más adelante (fase 5): verificación del mejor diseño con malla fina y modelo de tornillo realista; informe y defensa.
