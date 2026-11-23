# Documentación del proyecto: optimización del soporte guiada por reglas

**Mecánica de Sólidos Deformables, curso 2026-27. Grupo 831_MSD_13_B. Proyecto 2 «Diseño de un soporte», Soporte 6 (carga 2, acero S235).**

Este documento recoge, a fecha 23/11/2026, el problema, las decisiones y su motivo, cómo funciona el programa, qué produce, cómo se usa y qué queda pendiente. El detalle cronológico está en `bitacora.md` y el estado de las tareas en `ESTADO.md`.

> **Cambio de enfoque (23/11/2026).** Hasta el 23/11 el programa exploraba varias «familias» de piezas con un optimizador bayesiano. Ninguna convergía de forma clara y descartar una mala costaba mucho. Ahora:
> 1. las soluciones publicadas se calculan con nuestras condiciones y de ellas se sacan **reglas de diseño con datos**;
> 2. la pieza del enunciado se **modifica paso a paso** aplicando esas reglas, cada cambio con su porqué;
> 3. los cambios que no mejoran se **revierten**.
>
> Además: **carga de 42 258 N** (confirmada por el profesor) y **coeficiente de seguridad ≥ 1,0** (215 MPa) obligatorio. Los resultados anteriores se conservan en el PC (`runs/archivo/`, ya no en GitHub) y los datos que usan las reglas, en `estudio/calculos_anteriores.csv`.

---

## 1. Resumen en una frase

Un **creador de piezas**: se le dan las premisas (carga, límites de tensión y desplazamiento, agujeros fijos) y busca la pieza de **mínima masa**. Parte del soporte del enunciado y lo va modificando con sentido: añade material donde está el pico de tensión, lo quita donde no trabaja y **crea formas nuevas** (nervios) en la trayectoria de la carga. Cada cambio sale de una **regla de diseño respaldada por datos**, se calcula en ANSYS y se acepta o se revierte según el resultado. El objetivo es el soporte más ligero con **coeficiente de seguridad ≥ 1** (σ ≤ 215 MPa) y desplazamiento ≤ 0,25 mm, sin mover nunca los 4 agujeros de los pernos ni los 2 del bulón.

---

## 2. El problema

### 2.1 Lo que pide el enunciado
- Partir del soporte `0.stp` (derivado del GE Jet Engine Bracket Challenge, GrabCAD 2013).
- **Solo se conservan** las posiciones de los 4 agujeros de anclaje (pernos de Ø10,31 mm) y de los 2 orificios del bulón (Ø19,05 mm).
- Objetivo: (i) no superar nunca la tensión admisible y (ii) minimizar el material.
- Material: acero S235 con E = 210 GPa, σy = 215 MPa, ν = 0,30 y ρ = 7850 kg/m³.
- Informe (portada, índice, objetivo, descripción, modelo de EF, resultados, conclusiones y bibliografía) y defensa oral de unos 10 minutos.

### 2.2 Decisiones sobre el planteamiento

| Tema | Decisión | Motivo |
|---|---|---|
| **Carga** | **42 258 N** (Tabla 2, carga 2) | Confirmado por el profesor el 23/11/2026. Hasta entonces se usaban 37 800 N (Fig. 2) |
| **Dirección** | Horizontal, perpendicular al bulón, en **−X** del STEP | En 0.stp, Z es vertical, Y es el eje del bulón y X la horizontal perpendicular. Con el reparto RBE3 el sentido no cambia la tensión de von Mises |
| **Apoyo** | Empotramiento de las **superficies cilíndricas de los 4 agujeros de los pernos** | Son las «fixed support interfaces» de la Fig. 3 |
| **Aplicación de la carga** | RBE3 desde un nodo piloto (punto medio entre orejetas) a los 2 agujeros del bulón | Mismo esquema que SimJEB; sin cargas puntuales |
| **Tensión admisible** | **Coeficiente de seguridad ≥ 1,0**, es decir, **σ ≤ 215 MPa**, obligatorio | Límite del enunciado. Ninguna pieza que lo supere cuenta como válida |
| **Desplazamiento** | **≤ 0,25 mm** | No lo exige el enunciado; evita piezas ligeras pero blandas |
| **Impresión 3D** | Reglas de fabricación aditiva activadas | Decisión de diseño propia: techos a 45°, evacuación de polvo, sin cavidades cerradas |
| **Objetivo** | **Mínima masa**; tensión y desplazamiento son límites obligatorios | Lo que pide el grupo (23/11): el parámetro es la masa. La seguridad sobrante no puntúa (`peso_seguridad` = 0) |

---

## 3. Entorno técnico

- **ANSYS Student 2026 R1** (v261). MAPDL se lanza con `MAPDL.exe -b -p ansys`.
  - **Límite: 128 000 nodos**.
  - **Solo una sesión de ANSYS a la vez**: con Workbench abierto, el programa espera.
- **Python 3.12** (`.venv`): cadquery (geometría), gmsh (malla), numpy/scipy, pyvista (imágenes), matplotlib y plotly (gráficas), shapely, requests (Discord).
- **Workbench** por script (`RunWB2 -B -R`) para los proyectos `.wbpj` y `.wbpz`.
- **Validación** (viga en voladizo, SOLID187): flecha con un 0,02 % de error, reacción exacta y σx con un 0,04 %.

---

## 4. Modelo de elementos finitos

### 4.1 Geometría fija (extraída de 0.stp)
- **Pernos** (eje Z, superficie de z = 0,63 a 7,85 mm): (0; 0) con R = 5,334; (52,047; 1,580), (0; −148,125) y (38,083; −146,968) con R = 5,156 mm.
- **Bulón**: R = 9,557 mm, eje (−0,0304; 0,9995; 0), centros (−21,357; −60,417; 44,725) y (−20,490; −88,979; 44,725).
- **Original**: 2,4115 kg (CAD) o 2,4234 kg (volumen de la malla de 4 mm).

### 4.2 Malla y cálculo
- Tetraedros de 2.º orden **SOLID187** (gmsh) con orden de nodos y signo del volumen verificados.
- Mallas:
  - **completa**: h = 4 mm, unos 80 000 nodos, unos 45 s por cálculo;
  - **rápida**: h = 6 mm, unos 25 s, para el descarte temprano;
  - **fina**: h = 3,5 mm, para verificar los hitos.
- Equilibrio comprobado en cada cálculo (error de reacción < 0,1 %).
- **El modelo es lineal**: tensiones y desplazamientos son proporcionales a la carga. Comprobado al cambiar de 37 800 a 42 258 N: SimJEB n.º 373 pasa de 3 883 a 4 341 MPa, es decir, ×1,118 = 42 258/37 800.

### 4.3 Métrica de tensión
- El máximo bruto de von Mises está en el borde del agujero empotrado: es una **singularidad** y crece sin límite al refinar.
- **Métrica**: máximo de von Mises excluyendo **5 mm alrededor de cada perno** (apoyo de la cabeza del tornillo) y **2 mm alrededor del bulón** (esquinas del RBE3). Justificación con el estudio de convergencia de la Fase 2 (`bitacora.md`).

### 4.4 El original con la carga de 42 258 N
- Calculado con 37 800 N: 212,9 MPa (malla de 4 mm), 195,2 MPa (malla fina) y 0,129 mm.
- Con 42 258 N (factor lineal ×1,118): **≈ 238 MPa** con la malla de 4 mm y ≈ 218 MPa con la fina, es decir, **coeficiente de seguridad ≈ 0,90**.
- **El original NO cumple** con la carga del enunciado. El pico está en el fondo del alojamiento de la cabeza del perno 1, en (3,6; −9,9; 10,4).
- El primer paso del programa es, por tanto, **reforzar**.

---

## 5. Paso 1: estudio de las soluciones publicadas (`scripts/estudio_simjeb.py`)

- **SimJEB** (Whalen et al., 2021; Harvard Dataverse doi:10.7910/DVN/XFUWJG) recoge los **381 diseños** del GE Jet Engine Bracket Challenge en el mismo sistema de coordenadas que nuestro `0.stp`, que es su diseño n.º 0.
- **Cada diseño se calcula con NUESTRO modelo**: 42 258 N en −X, pernos empotrados, la misma métrica y los mismos límites.
  1. Primero, una pasada rápida (h = 6 mm). Si supera 1,5 veces el límite, se descarta ahí.
  2. Si es prometedor, se calcula con la malla completa.
  3. Los diseños sin los agujeros del enunciado (bulón macizo, agujeros de otro tamaño) quedan como «incompatibles».
- Se guarda el **campo de tensiones** de cada diseño. Con él, `scripts/campo.py` mide:
  - material ocioso (por debajo del 15 % del límite);
  - reparto de masa y tensión por zonas (pernos delanteros y traseros, orejetas, placa base, cuerpo);
  - dónde está el pico y si es una concentración local;
  - ligamento de material delante del bulón.
- Resultados: `estudio/estudio_simjeb.json` (un registro por diseño) y `estudio/caracteristicas.json`.
- Tarda unas 3–4 h. Se hace una vez y se puede interrumpir.

## 6. Paso 2: reglas de diseño (`scripts/reglas.py` → `DESIGN_RULES.md`)

Cada regla tiene **si** (condición medida en el mapa de tensiones), **hago** (operación), **porque** (mecánica), **evidencia** (datos) y su **historial de aplicación**.

| Regla | Si… | Hago… | Porque… |
|---|---|---|---|
| R1 | toda una columna vertical trabaja < umbral | aligeramiento pasante vertical | no está en el camino de carga; con Kt ≈ 3 (Kirsch) el borde del agujero queda < 3 × umbral |
| R2 | todo lo que hay por encima de una cota trabaja < umbral | rebaje desde arriba | material que ni el momento de vuelco ni el cortante usan |
| R3 | el núcleo de un bloque trabaja < umbral | hueco interior (techo a 45° + evacuación) | a flexión y torsión trabajan las pieles (σ = M·y/I) |
| R4 | el pico está junto al alojamiento de un perno | collar en ese perno y en su simétrico | más sección frente al momento de vuelco F·h |
| R5 | el pico está en el acuerdo del fondo del alojamiento | alojamiento más ancho con acuerdo mayor | Peterson… **pero los datos la contradicen** (ver abajo) |
| R6 | el pico es una entalla fuera de los alojamientos | redondeo de las aristas | Kt baja con el radio del acuerdo |
| R7 | el pico está en las orejetas | engrosar el anillo de las orejetas | aplastamiento y cortadura ∝ 1/ligamento |
| R8 | el pico está en el borde de un corte anterior | reducir o deshacer ese corte | ese material sí trabajaba |
| R9 | un corte fue rechazado | en esa zona, cortes ≤ 0,6 × el rechazado | búsqueda por bisección del tamaño |
| R10 | no queda material ocioso donde cortar | subir el umbral 15 % → 25 % → 35 % | primero lo más seguro |
| **R11** | un bloque trabaja algo (< 45–60 % del límite) o quitarlo entero se rechazó | **forma nueva**: se quita el bloque y se crean **nervios**, uno por cada familia de la carga (tracción y compresión) que lleve ≥ 25 % de ella, en su dirección principal, dimensionados para trabajar al 50 % del límite y con acuerdo de 3 mm en la raíz | Michell (1904): la estructura mínima lleva cada familia por su trayectoria, con un volumen ∫\|σ\| dV / σ_trabajo |

**Datos de las reglas**
- **Las reglas se juzgan con datos.** Una regla que contradicen los datos de un cambio **directo** (mismo diseño, cambiando solo eso) **se desactiva**. Las comparaciones con SimJEB (diseños distintos) pueden respaldarla o ser «no concluyentes», pero no la desactivan. Una regla que se prueba 8 veces en el optimizador sin que ninguna se acepte **se suspende**. Ejemplo real: R5 parecía lógica (agrandar el radio del acuerdo baja Kt), pero en los 294 diseños calculados antes, agrandar el alojamiento **sube** la tensión (Spearman +0,76: mediana de 360 MPa con R > 11 mm frente a 206 MPa con el del original). Pesa más la sección que se pierde que el acuerdo que se gana, así que está desactivada.
- **R4 está respaldada** por una prueba directa: collares de 6 mm bajan el pico del original un 15 % (de 238 a 203 MPa con 42 258 N) con +159 g.
- **R1–R3 y R7** se completan con el estudio de SimJEB: material ocioso, zonas y ligamentos de los diseños válidos frente al original.

## 7. Paso 3: el optimizador guiado por reglas (`scripts/optimizer.py`)

### 7.1 Una iteración
1. **Mapa de tensiones** de la pieza actual (`campo.py`): material ocioso, pico, concentración y **direcciones principales** (trayectorias de carga). Se calculan con el tensor completo que exporta ANSYS; el von Mises reconstruido coincide con el de ANSYS (error 1e-7).
2. **Propuestas** (`reglas.py`): hasta 3 modificaciones, cada una con su regla, su porqué con números de la pieza actual y lo que se espera.
   - Si la pieza **no cumple** o está a menos de un 3 % del límite, primero refuerzos (R4, R6, R7, R8).
   - Si hay margen, aligeramientos (R1–R3) y sustituciones de bloques por nervios (R11), al menos una de cada regla disponible.
3. **Evaluación rápida** (malla gruesa) de cada propuesta, **comparada con la pieza actual en la misma malla gruesa**: así se cancela el error de la malla gruesa. Se descarta si la tensión prevista supera el límite en más de un 3 % o si no mejora la pieza.
4. **Evaluación completa** (malla de 4 mm) solo de la más prometedora.
5. **Decisión**:
   - **ACEPTADA** si cumple y mejora al mejor, o si la pieza aún no cumplía y se acerca al límite;
   - **INVERSIÓN** si es un refuerzo eficiente (−% de tensión ≥ 2 × % de masa) cuando no queda margen: se acepta para gastar ese margen aligerando y, si en 3 iteraciones no hay mejora, se deshace;
   - **RECHAZADA** si no cumple o no mejora: se revierte, se registra el motivo y la zona queda marcada (R9).
6. **Hito** (mejora de masa ≥ 1 % desde el anterior, y al final): verificación con **malla fina** y **proyecto Workbench**. Si la malla fina no confirma, se vuelve al último diseño verificado.
7. **Fin**: cuando ninguna regla encuentra modificaciones o tras 8 iteraciones seguidas sin mejorar.

### 7.2 Operaciones (`scripts/operaciones.py`)
La pieza es siempre **0.stp + una lista de operaciones** y se puede reconstruir desde cero.
- **Quitan material**: agujero vertical pasante, rebaje desde arriba, hueco interior.
- **Añaden o reforman**: collar en un perno, alojamiento, redondeo, anillo de orejetas y **nervio**. El nervio es una pared vertical con el borde superior inclinado (también hace de cartela) en la dirección de la carga; nace de la base, así que se imprime sin soportes.
- Lo que se añade nunca invade el paso de los tornillos y sus cabezas, el del bulón ni el hueco entre orejetas, y no sale de la caja que ocupa el soporte original (volumen de diseño).
- **Ninguna forma se pone «a ver si funciona»**: cada una sale del campo de tensiones (dónde, en qué dirección y de qué tamaño) y se comprueba en ANSYS.

Las que quitan nunca entran en las zonas protegidas: alojamiento + 3 mm alrededor de cada perno y radio del bulón + 6 mm en las orejetas. **Los 6 agujeros se verifican en cada pieza.**

### 7.3 Velocidad (frente al enfoque anterior)
- **Una sola línea de trabajo**, sin familias ni ramas.
- **Descarte temprano**: unos 25 s por propuesta en la malla rápida; solo una por iteración pasa a la malla completa (unos 45 s).
- Unos 2–3 min por iteración. Antes, la familia «desde cero» tardaba 4 min por diseño sin ningún válido en 101.

---

## 8. Qué produce

**Trazabilidad**
- **`ITERACIONES.md`** (en `runs/opt_42258N/`): cada iteración con regla, porqué, lo esperado, resultado antes/después (masa, tensión, CS), decisión y motivo, y las propuestas descartadas en la evaluación rápida.
- **GitHub**: un **commit por iteración** con mensaje descriptivo. Ejemplo: `Iteracion 3 [ACEPTADA] R1: aligeramiento... | masa 2.52->2.45 kg, tension 212->213 MPa`. El cuerpo del commit lleva el porqué y el motivo.
- **Discord**:
  - canal «todo»: un mensaje por iteración;
  - canal «árbol»: **camino de la pieza** en imagen cada vez que cambia;
  - canal «top»: el mejor diseño, en un mensaje que se edita.

**Paneles y archivos**
- **`README.md` = panel en directo**: estado, mejor diseño con sus operaciones, camino de la pieza, últimas iteraciones y enlaces.
- **`DESIGN_RULES.md`**: reglas, evidencia y estadísticas de aplicación, actualizado en cada iteración.
- **Galería** (`GALERIA.md`), **hitos** (`HISTORIAL.md`, con STEP, operaciones y proyecto Workbench) y **gráfico interactivo** (`evolucion_interactiva.html`).
- **Ficha de cada pieza**: geometría | von Mises | deformada | radiografía, con la lista de operaciones aplicadas al original.

## 9. Robustez
- **Reanudación**: guarda tras cada iteración. La pieza actual se guarda en `pieza_actual.step` y siempre se puede reconstruir desde el 0.stp.
- **Licencia ocupada**: espera y reintenta cada minuto.
- **Estudio y optimizador nunca a la vez**: si el estudio está en marcha en otra ventana, `optimizar.bat` espera a que termine y sigue solo.
- **Errores inesperados**: se registran, se avisa por Discord y se sigue; con 5 seguidos se detiene y `optimizar.bat` lo reinicia.
- **Limpieza** cada 10 iteraciones (archivos pesados de iteraciones antiguas; nunca los datos ni las fichas).
- **Seguridad**: los enlaces de Discord están en `discord_webhooks.json`, que **no se sube a GitHub**.

## 10. Cómo se usa
1. **Cerrad Workbench** (licencia de una sola sesión).
2. Doble clic en **`optimizar.bat`**:
   - primero completa el estudio de SimJEB si falta;
   - después escribe las reglas;
   - por último, optimiza.
   Se puede cerrar en cualquier momento.
3. Seguimiento: la consola, el README de GitHub y Discord.
4. `probar_optimizador.bat`: prueba corta (2 iteraciones) en `runs/prueba_*`, sin GitHub ni Discord.

### 10.1 Ajustes (`config.json`)

| Ajuste | Valor | Para qué |
|---|---|---|
| `carga_N` | 42258 | Carga del enunciado (Tabla 2) |
| `sigma_y_MPa` / `margen_optimizacion` | 215 / 1,0 | Límite = 215 MPa (CS ≥ 1, obligatorio) |
| `desplazamiento_max_mm` | 0,25 | 0 = sin límite |
| `peso_seguridad` | 0 | 0 = objetivo solo masa; > 0 = la seguridad sobrante desempata |
| `estudio_simjeb` | true | Estudio de las soluciones publicadas antes de optimizar |
| `candidatos_por_iteracion` | 3 | Propuestas que se prueban en la evaluación rápida |
| `umbrales_ocioso` | 0,15 / 0,25 / 0,35 | Umbral de material ocioso (R10) |
| `descarte_rapido_tolerancia` | 0,03 | Margen sobre el límite en la evaluación rápida |
| `max_iteraciones_sin_mejora` / `max_inversiones_seguidas` | 8 / 2 | Parada e inversiones |
| `verificar_mejores` / `verificacion_h_mm` | true / 3,5 | Verificación con malla fina en cada hito |
| `crear_workbench_en_cada_mejora` / `workbench_mejora_minima_pct` | true / 1,0 | Proyecto Workbench cada ≥ 1 % de mejora de masa y al final |
| `reglas_impresion_3d` / `angulo_voladizo_deg` | true / 45 | Fabricación aditiva |
| `discord` / `subir_a_github` | true / true | Publicación |

## 11. Estructura de archivos

```
Trabajo/
├── optimizar.bat, probar_optimizador.bat, (des)instalar_autoarranque.bat
├── config.json, discord_webhooks.json (NO se sube)
├── README.md (panel), DESIGN_RULES.md (reglas), DOCUMENTACION.md, ESTADO.md, bitacora.md
├── cad/            0.stp, agujeros_fijos.json, referencia del original
├── estudio/        estudio de SimJEB (estudio_simjeb.json, caracteristicas.json, evidencia.json, img/) y calculos_anteriores.csv
├── scripts/
│   ├── optimizer.py         optimizador guiado por reglas + panel, Discord, GitHub, Workbench
│   ├── reglas.py            reglas, evidencia, propuestas y DESIGN_RULES.md
│   ├── campo.py             análisis del campo de tensiones (ocioso, pico, zonas, candidatos)
│   ├── operaciones.py       operaciones sobre la pieza (quitar / añadir) y zonas protegidas
│   ├── estudio_simjeb.py    cálculo de las soluciones publicadas con nuestras condiciones
│   ├── evaluate.py          geometría → malla → ANSYS → métricas → imágenes
│   ├── fem.py, run_mapdl.py, geometry.py (agujeros fijos), render.py, exportar_workbench.py, discord_notify.py
│   └── fase2_*.py, find_holes.py, exportar_original_ansys.py   (fases 0–2)
├── datos_simjeb/   381 STEP + metadata (NO se sube) y campos de tensión del estudio
└── runs/opt_42258N/  iteraciones, galería, historial, ITERACIONES.md, registro.csv, estado.json
    runs/archivo/     resultados del enfoque anterior (familias, 37 800 N); solo en el PC
```

**Eliminado el 23/11** (enfoque anterior):
- familias «vaciado», «refuerzo», «desde cero» y «SimJEB modificado»;
- procesos gaussianos (BoTorch), árbol de ramas, torneo y anti-estancamiento;
- `report.py`.

Sus operaciones útiles (collar, hueco con techo a 45°, aligeramientos, booleanas robustas, zonas protegidas) se han reutilizado en `operaciones.py`.

## 12. Limitaciones y pendientes
- **Fase 5**:
  - verificación final con malla fina y convergencia;
  - modelo de tornillo realista (sin empotrar el agujero);
  - comparación del original con el final;
  - informe y guion de defensa.
- La exclusión de 5 mm alrededor de los pernos hay que explicarla bien en la defensa.
- Las correlaciones de los cálculos anteriores son observacionales: en cada diseño cambiaban varias variables a la vez. Por eso cada regla se comprueba otra vez en el optimizador, que hace un solo cambio cada vez.

## 13. Referencias
- Enunciado: *Trabajo MSD 26-27* (Proyecto 2) e *Instrucciones generales*, EINA, Universidad de Zaragoza.
- Whalen, E., Beyene, A., Mueller, C. (2021). *SimJEB: Simulated Jet Engine Bracket Dataset*. Computer Graphics Forum 40(5). doi:10.1111/cgf.14353. Datos: Harvard Dataverse, doi:10.7910/DVN/XFUWJG.
- Concentración de tensiones: Kirsch (placa con agujero circular, Kt = 3); Pilkey & Pilkey, *Peterson's Stress Concentration Factors*.
- ISO/ASTM 52911-1:2019 y resto de fuentes de fabricación aditiva: `docs/fabricacion_aditiva.md`.
- Herramientas: ANSYS Student 2026 R1 (MAPDL y Workbench), gmsh, cadquery/OpenCascade, PyVista, Plotly.
