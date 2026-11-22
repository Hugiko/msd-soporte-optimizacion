# Estado del proyecto y plan pendiente

Última actualización: 22/11/2026. Detalle de cada decisión en `bitacora.md`.

## Objetivo
Un programa autónomo (`optimizar.bat`) que genera piezas, las calcula en ANSYS, aprende de cada resultado y converge al
soporte de **mínima masa** que cumple **σ ≤ 215 MPa** (fuera de la singularidad de los pernos) y **u ≤ 0,25 mm**,
manteniendo fijos los 4 agujeros de los pernos y los 2 del bulón. Carga: 37 800 N en −X (configurable a 42 258 N).

## Hecho
- **Fases 0–2**: ANSYS Student 2026 R1 por script (licencia `-p ansys`, límite de 128 000 nodos, una sola sesión a la vez).
  Modelo base validado (reacciones exactas, convergencia de malla, métrica con exclusión de 5 mm alrededor de los pernos).
  Figuras en `figuras/`; resultados de referencia del original en `cad/referencia_original/`.
- **Pipeline de evaluación** (`scripts/evaluate.py`): geometría → malla tet10 (gmsh) → MAPDL → métricas → imágenes;
  reintentos de malla, **tiempo máximo de mallado** (proceso aparte, 300 s), espera si la licencia está ocupada y ficha
  `resumen.png` (geometría | von Mises | deformada | radiografía).
- **Familias de geometría activas**: `vaciado` (original menos hueco/recorte/alojamientos), `refuerzo` (v2: collares junto a los tornillos + vaciado; baja el pico del original de 212,9 a 181,2 MPa) y `cero` (diseño nuevo).
  Los 6 agujeros se verifican en cada diseño.
- **Reglas de impresión 3D** (activadas, `reglas_impresion_3d` en `config.json`): techos interiores a 45°, agujero de evacuación de
  Ø5 por cámara y ninguna cavidad cerrada. Fuentes en `docs/fabricacion_aditiva.md`. El enunciado no lo exige
  (la frase se refiere al concurso de GE de 2013); es una decisión de diseño propia.
- **Optimizador** (`scripts/optimizer.py`): DOE → procesos gaussianos (BoTorch) para masa, tensión y desplazamiento → **ramas**
  (árbol genealógico: fina / amplia / cruce / exploradora al azar cada 3 ramas, congelado de parámetros en las finas) → «cualquier mejora cuenta».
  Detección de piezas repetidas, **filtro por predicción** (si el modelo es fiable) y **pasada rápida** con malla gruesa.
- **Salidas**: proyecto Workbench `.wbpj` (resuelto, en el PC) + `.wbpz` (en GitHub) en cada nueva mejora; historial; galería
  cronológica de todos los diseños; gráfica en el tiempo + gráfica interactiva html; árbol (`ARBOL.md` + `arbol.png`);
  panel `README.md`; limpieza automática; subida a GitHub en segundo plano; reanudación tras apagar el PC.
- **Limpieza total y reinicio del repositorio de GitHub** (historial limpio, un solo commit).

## En curso / pendiente
1. [hecho] Tiempo máximo de mallado: un gmsh colgado ya no bloquea el programa (comprobado: 6 estrategias fallidas en 72 s).
2. [hecho] Relleno de la familia `refuerzo` simplificado (capas de 4 mm, contornos suavizados).
3. [comprobado] Familia `refuerzo`: **no es fiable**. La unión del relleno escalonado con el interior del original deja superficies que
   se cortan («PLC Error: a segment and a facet intersect») y gmsh no puede mallarlas. **Retirada de las familias activas**
   (el código sigue en `scripts/geometry_refuerzo.py`). Idea pendiente: un refuerzo con primitivas simples y redondeadas
   (anillos o nervios alrededor de los alojamientos) en lugar de rellenar cavidades.
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
10. Más adelante (fase 5): verificación del mejor diseño con malla fina y modelo de tornillo realista; informe y defensa.




