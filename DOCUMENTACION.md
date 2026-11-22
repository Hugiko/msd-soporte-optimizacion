# Documentación del proyecto: optimización automática del soporte

**Mecánica de Sólidos Deformables, curso 2026-27. Grupo 831_MSD_13_B. Proyecto 2 «Diseño de un soporte», Soporte 6 (carga 2, acero S235).**

Este documento resume todo lo hecho hasta el 22/11/2026: el problema, las decisiones tomadas y su motivo, cómo funciona el programa, qué produce, cómo se usa y qué queda pendiente. El detalle cronológico de cada decisión está en `bitacora.md` y el estado de las tareas en `ESTADO.md`.

---

## 1. Resumen en una frase

Hemos construido un programa que **genera piezas automáticamente, las calcula en ANSYS, aprende de cada resultado y se va acercando al soporte con el mejor compromiso entre masa y seguridad** que cumple los límites (σ ≤ 215 MPa y desplazamiento ≤ 0,25 mm), sin mover nunca los 4 agujeros de los pernos ni los 2 del bulón. Funciona solo durante horas y lo publica todo en GitHub y en Discord.

---

## 2. El problema

### 2.1 Lo que pide el enunciado
- Partir del soporte `0.stp` (derivado del GE Jet Engine Bracket Challenge, GrabCAD 2013).
- **Solo se conservan** las posiciones de los 4 agujeros de anclaje (pernos de Ø10,31 mm) y de los 2 orificios del bulón (Ø19,05 mm). Todo lo demás se puede modificar.
- Objetivo: (i) que nunca se supere la tensión admisible y (ii) minimizar el material.
- Material: acero S235, con E = 210 GPa, σy = 215 MPa, ν = 0,30 y ρ = 7850 kg/m³.
- Informe con portada, índice, objetivo, descripción, modelo de EF, resultados, conclusiones y bibliografía. Defensa oral de unos 10 minutos.

### 2.2 Decisiones sobre el planteamiento

| Tema | Decisión | Motivo |
|---|---|---|
| **Carga** | **37 800 N** (caso «Horizontal» de la Fig. 2), configurable a 42 258 N (Tabla 2) | La Tabla 2 da 42 258 N para la carga 2, que coincide con el módulo del caso diagonal: errata probable. Decisión del grupo |
| **Dirección** | Horizontal, perpendicular al bulón, en **−X** del STEP | En 0.stp, Z es vertical, Y es el eje del bulón y X la horizontal perpendicular. Con el reparto RBE3, el sentido no cambia la tensión de von Mises |
| **Apoyo** | Empotramiento de las **superficies cilíndricas de los 4 agujeros de los pernos** | Son las «fixed support interfaces» de la Fig. 3. Empotrar toda la base sería pegarla al suelo y daría tensiones irrealmente bajas |
| **Aplicación de la carga** | RBE3 desde un nodo piloto, en el punto medio entre orejetas, a las superficies de los 2 agujeros del bulón | Mismo esquema que SimJEB; sin cargas puntuales |
| **Tensión admisible** | **215 MPa** (σadm = σy, sin margen) | El enunciado no da otra. El 0,9 que se usó al principio venía del prompt, no del enunciado |
| **Desplazamiento** | **≤ 0,25 mm** (≈ 2 × el original, 0,129 mm) | No lo exige el enunciado. Se añade para evitar piezas ligeras pero blandas |
| **Impresión 3D** | Reglas de fabricación aditiva **activadas** | El enunciado no la exige para nosotros (esa frase se refiere al concurso de 2013), pero el original está pensado para ella. Decisión de diseño propia |
| **Cuándo una pieza es «mejor»** | Menor **puntuación = masa × aprovechamiento^0,5** | Compromiso entre masa y coeficiente de seguridad, pedido por el grupo (ver §6.4) |

---

## 3. Entorno técnico

- **ANSYS Student 2026 R1** (v261), instalado en `C:\Program Files\ANSYS Inc\ANSYS Student\v261`. Funciona desde una terminal normal, sin el Cloudpaging Player.
- **Licencia**: Student local. MAPDL se lanza con `MAPDL.exe -b -p ansys` (sin `-p ansys` pide productos que no existen).
  - **Límite: 128 000 nodos** (comprobado: MAPDL da error al superarlo).
  - **Solo una sesión de ANSYS a la vez**: con Workbench abierto, el optimizador no puede calcular.
- **Python 3.12** con entorno propio (`.venv`): cadquery (geometría), gmsh (malla), BoTorch y PyTorch (procesos gaussianos), numpy/scipy, pyvista (imágenes), matplotlib y plotly (gráficas), shapely (perfiles 2D), requests (Discord).
- **Workbench** se controla por script (`RunWB2 -B -R`) para generar proyectos `.wbpj` y `.wbpz`.
- **Prueba de validación** (viga en voladizo, SOLID187): flecha 1,9052 mm frente a 1,9048 mm analítica (0,02 %), reacción exacta y σx = 300,13 frente a 300 MPa (0,04 %).

---

## 4. Modelo de elementos finitos

### 4.1 Geometría fija (extraída de 0.stp)
- **Pernos** (eje Z, superficie de z = 0,63 a 7,85 mm): (0; 0) con R = 5,334; (52,047; 1,580), (0; −148,125) y (38,083; −146,968) con R = 5,156 mm.
- **Bulón**: R = 9,557 mm, eje (−0,0304; 0,9995; 0), centros (−21,357; −60,417; 44,725) y (−20,490; −88,979; 44,725). Separación entre orejetas: 28,58 mm.
- **Original**: 307 191 mm³, es decir, **2,4115 kg** (CAD) o 2,4234 kg (volumen de la malla de 4 mm). No es macizo: tiene cavidades interiores con agujeros de evacuación de polvo en la base.

### 4.2 Malla y cálculo
- Tetraedros de 2.º orden **SOLID187** con aristas rectas (los curvos daban elementos distorsionados), mallados con gmsh. Orden de nodos y signo del volumen verificados en cada malla.
- **Malla de optimización**: h = 4 mm, hmin = 1 mm (unos 60 000–90 000 nodos, 30–60 s por cálculo).
- **Malla de verificación**: h = 3,5 mm.
- **Pasada rápida** (solo familia «desde cero»): h = 6 mm.
- Equilibrio comprobado en cada cálculo: la suma de reacciones coincide con la carga (error < 0,1 %).

### 4.3 Métrica de tensión
- El máximo bruto de von Mises **no sirve**: está en el borde del agujero empotrado, que es una singularidad. Crece sin límite al refinar la malla: 474 → 888 → 973 → 975 MPa.
- **Métrica usada**: máximo de von Mises excluyendo **5 mm alrededor de cada agujero de perno** (zona de apoyo de la cabeza del tornillo) y **2 mm alrededor del bulón** (esquinas del RBE3).
- **Convergencia** (original, 42 258 N): 204,0 → 210,4 → 218,2 → 215,7 MPa con 45k a 103k nodos. Las dos mallas más finas difieren un 1,2 %.
- En cada diseño se guarda también la tensión sin exclusión y con exclusiones de 3, 5 y 8 mm (sensibilidad para el informe).

### 4.4 Resultados de referencia del original (37 800 N)

| Magnitud | Malla de 4 mm (APDL) | Malla fina 3,5 mm | Workbench (68 849 nodos) |
|---|---|---|---|
| Tensión métrica | 212,9–213,3 MPa | 195,2 MPa | — |
| von Mises bruta (singular) | 793 MPa | — | 631,6 MPa |
| Desplazamiento máximo | 0,129 mm | 0,133 mm | 0,132 mm |
| Coeficiente de seguridad (215/métrica) | 1,01 | 1,10 | — |

El original está **prácticamente en el límite** del S235 con esta carga: se diseñó para titanio (σy = 903 MPa).

---

## 5. Familias de piezas (cómo se construye cada diseño)

Una **familia** es una forma de construir la pieza con unas variables. El programa busca los mejores valores de esas variables. En **todas** se comprueba en cada diseño que los 6 agujeros están exactamente en su sitio (área de cada superficie cilíndrica dividida por la de referencia = 1,000 ± 1 %).

### 5.1 «Vaciado del original» (11 variables)
Al 0.stp le quita material donde casi no trabaja:
- **hueco interior** (posición, longitud, anchura, suelo y techo), con al menos 3 mm de pared por encima según el mapa de alturas del original;
- **recorte inclinado** del bloque por el lado alejado de las orejetas (inicio, altura, inclinación y anchura);
- **remodelado de los alojamientos** de los tornillos (radio entre 10,54 y 12 mm).

Todas las herramientas de corte tienen sus aristas redondeadas. Se usan booleanas «difusas» (tolerancia 10⁻⁴), porque sin ellas OCC falla en silencio con la geometría del original. Hallazgo: agrandar el alojamiento a R = 14 mm dispara la tensión a 800 MPa, porque adelgaza la pared frente a las cavidades interiores.

### 5.2 «Refuerzo + vaciado» (14 variables) — la más prometedora
- Añade un **collar cilíndrico** alrededor de cada alojamiento de tornillo (espesor delantero, espesor trasero y altura), justo donde está el punto crítico del original.
- **Prueba en ANSYS**: con un collar de 6 mm, el pico baja de **212,9 a 181,2 MPa** (+159 g) y el punto crítico pasa a la orejeta.
- Con ese margen aplica las mismas operaciones de vaciado. En la prueba corta dio piezas válidas de 168–177 MPa.
- La versión 1 (rellenar las cavidades por capas) se retiró porque no se podía mallar.

### 5.3 «Diseño desde cero» (12 variables)
Soporte nuevo:
- cajón de torsión entre las dos filas de pernos, opcionalmente hueco con almas bajo las orejetas;
- 2 orejetas (envolvente del círculo y el pie, con acuerdo de pie 2,5 veces mayor);
- franja plana en los pernos y paredes extremas inclinadas.

Variables: alojamiento, ancho de barras, inclinación de paredes, altura, anchos superior e inferior, desplazamiento del cajón, posición del pie de pared, espesor de pared, material y espesor de las orejetas, y radio de acuerdos.

Todos los acuerdos entrantes se generan en 2D con un cierre morfológico (sin esquinas vivas). En las pruebas todavía **no ha encontrado ninguna pieza válida**, aunque baja la tensión de rama en rama (≈ 2 000 → 450–750 MPa).

### 5.4 Reglas de impresión 3D (todas las familias)
- **Techos interiores autoportantes**: pendiente de 45° (`angulo_voladizo_deg`) y techo a cuatro aguas.
- **Agujero de evacuación de polvo** de Ø5 mm en cada cámara.
- **Ninguna cavidad cerrada**: si queda alguna al combinar operaciones, se rellena.
- Espesores mínimos: 3 mm de pared sobre los huecos y 5 mm de suelo.

Fuentes en `docs/fabricacion_aditiva.md` (ISO/ASTM 52911-1:2019, NASA, Cambridge, Diegel et al., TUHH, Assembly Magazine). Matiz para la defensa: el S235 no es un acero habitual en impresión 3D.

---

## 6. Cómo funciona el optimizador

### 6.1 El ciclo de cada pieza
1. **Propuesta** de unos valores de las variables (§6.2).
2. **Comprobaciones antes de ANSYS:**
   - **pieza repetida**: si su volumen coincide con una ya calculada, se reutiliza el resultado;
   - **filtro por predicción**: si el modelo es fiable (error típico < 10 %) y la probabilidad de cumplir es < 5 %, no se calcula; 1 de cada 10 se calcula igualmente como control;
   - **pasada rápida** (familia «desde cero»): malla gruesa; si incumple más de 1,5 veces el límite, se descarta ahí.
3. **Geometría → malla → ANSYS → resultados.** La malla tiene un tiempo máximo de 60 s por intento (gmsh se cuelga a veces de forma aleatoria) y 6 estrategias de reintento.
4. **Clasificación**: válida, casi (hasta un 10 % por encima del límite), no válida, fallida o filtrada.
5. **Si es candidata a nuevo mejor**: verificación con malla fina. Si ahí no cumple, no se acepta.
6. **Ficha, galería, registro, árbol, panel, Discord y GitHub.**

### 6.2 Cómo decide qué probar (cómo aprende)
1. **Reparto inicial**: 12 diseños por familia (secuencia de Sobol) repartidos por todo el espacio.
2. **Modelos sustitutos**: procesos gaussianos (BoTorch) que predicen **masa, tensión y desplazamiento** de cualquier pieza, con su incertidumbre, a partir de todo lo calculado. Para la masa se usan además 48 geometrías construidas sin ANSYS por familia.
3. **Elección del candidato**: entre unos 4 500 candidatos al azar alrededor del mejor diseño de la rama (cambios de todas las variables, cambios de 1–3 variables y continuaciones de la dirección que funcionó), se elige el de mayor **mejora esperada de la puntuación × probabilidad de cumplir**. Se penalizan las zonas donde hubo fallos.
4. **Ramas (árbol genealógico)**:
   - Una rama hace 30 pruebas alrededor de su mejor diseño. Si mejora, sigue en esa línea y alarga el paso; si falla 4 veces, lo acorta.
   - Al terminar, su mejor diseño crea ramas hijas:
     - **fina** (paso 0,10; solo mueve las variables que más influyen según los modelos);
     - **amplia** (paso 0,35);
     - **cruce** (mezcla al azar con el mejor diseño de otra rama).
   - **Cada 3 ramas terminadas nace una rama exploradora**, que parte de un punto al azar alejado de todo lo probado para no quedarse atrapada en una zona. ≈ 25 % del tiempo es exploración.
   - Siempre se trabaja en la rama activa cuyo origen es mejor. Todas comparten los mismos modelos.
5. **Reparto entre familias**: se alternan. Una familia sin ninguna pieza válida tras 30 intentos solo calcula 1 de cada 3 turnos.
6. **Parada**: 300 diseños por familia, o 8 fallos seguidos en una familia.

### 6.3 Mientras no hay piezas válidas
El objetivo pasa a ser **reducir el incumplimiento** (el mayor de tensión/límite y desplazamiento/límite) hasta conseguir una pieza válida. Después, mejorar la puntuación.

### 6.4 Cuándo una pieza es «mejor»
**Puntuación = masa × aprovechamiento^p** (menor = mejor):
- **aprovechamiento** = max(σ / 215 MPa; u / 0,25 mm) = 1 / coeficiente de seguridad;
- **p = 0,5** (`peso_seguridad`): un 1 % menos de masa vale lo mismo que un 2 % menos de tensión. Con p = 0 se vuelve al criterio literal del enunciado (solo masa).
- Los límites son **obligatorios**: la puntuación solo ordena las piezas válidas.

| Pieza (pruebas) | Masa | Coef. seguridad | Puntuación |
|---|---|---|---|
| Original | 2,423 kg | 1,01 | 2,411 |
| Vaciado n.º 4 | 2,420 kg | 1,01 | 2,408 |
| Refuerzo n.º 5 | 2,543 kg | 1,21 | **2,307** |

---

## 7. Qué produce

### 7.1 En cada nuevo mejor diseño
- **Proyecto de Workbench** listo para abrir: geometría, acero S235, selecciones con nombre, Fixed Support, Remote Force deformable, malla y resultados.
  - `.wbpj` **resuelto** en el PC;
  - `.wbpz` **montado** en GitHub (abrir con *File → Restore Archive* y pulsar *Solve*).
- Entrada en el **historial** (ficha, STEP, modelo APDL, datos), **fotograma del vídeo timelapse** y **mensaje de Discord actualizado**.

### 7.2 En GitHub (repositorio privado `Hugiko/msd-soporte-optimizacion`)
- **`README.md` = panel en directo**, actualizado en cada pieza:
  - estado por familia;
  - cálculos ahorrados y fiabilidad del modelo;
  - mejor diseño con su ficha, coeficiente de seguridad, puntuación y verificación;
  - gráfica de la evolución en el tiempo;
  - **árbol en imagen**;
  - historial de todas las mejoras;
  - últimos diseños.
- **`GALERIA.md`**: todas las piezas (válidas y no válidas) en orden cronológico, con fichas `AAAAMMDD_HHMMSS_familia_n_VEREDICTO_masa.jpg`.
- **`ARBOL.md`**: árbol de ramas dibujado con Mermaid.
- **`evolucion_interactiva.html`**: gráfico en el que, al pasar el ratón, se ven la hora y los datos de cada punto. Se descarga y se abre en el navegador.
- Registros CSV, clasificación por familia y gráficas de evolución e importancia de las variables.

### 7.3 La ficha de cada pieza (`resumen.png`)
4 vistas: **geometría 3D | tensión de von Mises | deformada amplificada | radiografía del interior** (cavidades visibles y las cerradas en rojo).

### 7.4 En Discord (3 canales)
- **Mejor versión**: UN mensaje que se **edita** con cada mejora (y cada 15 diseños como señal de vida). Incluye masa y reducción, tensión, desplazamiento, coeficiente de seguridad, puntuación, origen, verificación y enlace al `.wbpz`.
- **Árbol**: imagen nueva cada vez que cambia la estructura.
- **Todo lo generado**: ficha de cada pieza y avisos (errores, familia terminada, disco lleno, fin).

---

## 8. Robustez y mantenimiento
- **Reanudación**: guarda tras cada pieza. Si se cierra o se apaga el PC, al relanzar continúa donde iba y repite la pieza que quedó a medias.
- **Licencia ocupada**: si Workbench está abierto, avisa y reintenta cada minuto sin penalizar el diseño. Los proyectos de Workbench que no se puedan crear quedan pendientes y se reintentan.
- **Mallado colgado**: tiempo máximo de 60 s por intento (30 s en la pasada rápida), en un proceso aparte.
- **Errores inesperados**: se registran en `errores.log`, se avisa por Discord y se sigue; con 5 seguidos se detiene. `optimizar.bat` lo **reinicia solo** al minuto.
- **Disco**: limpieza inmediata si quedan menos de 5 GB y pausa si queda menos de 1 GB.
- **Limpieza automática** (cada 10 diseños):
  - se borran los archivos pesados de los diseños antiguos ya superados;
  - **nunca** se borran los datos de los que aprende ni las fichas;
  - se conservan los 5 mejores y los 20 últimos completos, los 3 últimos `.wbpj` resueltos en el PC y los 10 últimos `.wbpz` en GitHub.
- **Versión de la geometría**: si cambia la forma de construir las piezas, los resultados antiguos se archivan en `runs/archivo/` y se empieza limpio.
- **Seguridad**: los enlaces de Discord están en `discord_webhooks.json`, que **no se sube a GitHub**.

---

## 9. Cómo se usa

1. **Cerrad Workbench** (licencia de una sola sesión).
2. Doble clic en **`optimizar.bat`**. Se puede cerrar la ventana en cualquier momento.
3. Opcional: **`instalar_autoarranque.bat`** (una vez) para que arranque al iniciar sesión. Se quita con `desinstalar_autoarranque.bat`.
4. Seguimiento: la consola, el README de GitHub y Discord.
5. `probar_optimizador.bat`: prueba corta en una carpeta aparte (`runs/prueba_*`).

### 9.1 Ajustes principales (`config.json`)

| Ajuste | Valor | Para qué |
|---|---|---|
| `carga_N` | 37800 | 42258 para la Tabla 2 (resultados en carpeta propia) |
| `sigma_y_MPa` / `margen_optimizacion` | 215 / 1,00 | Límite de tensión |
| `desplazamiento_max_mm` | 0,25 | 0 = sin límite |
| `peso_seguridad` | 0,5 | Compromiso masa-seguridad (0 = solo masa) |
| `familias` | vaciado, refuerzo, cero | Familias activas |
| `presupuesto_por_familia` | 300 | Diseños máximos por familia |
| `pruebas_por_rama` / `rama_exploradora_cada` | 30 / 3 | Árbol de ramas |
| `reglas_impresion_3d` / `angulo_voladizo_deg` | true / 45 | Fabricación aditiva |
| `cribado_rapido` / `cribado_rapido_familias` | 1,5 / cero | Pasada rápida |
| `filtro_prob_minima` / `filtro_error_max` | 0,05 / 0,10 | Filtro por predicción |
| `verificar_mejores` / `verificacion_h_mm` | true / 3,5 | Verificación con malla fina |
| `crear_workbench_en_cada_mejora` / `mejora_minima_para_nuevo_mejor` | true / 0,0001 | Proyectos de Workbench |
| `limpieza_*`, `mantener_*`, `disco_minimo_gb` | 10, 20, 5, 3, 10, 5 | Limpieza y disco |
| `discord` / `subir_a_github` | true / true | Publicación |

---

## 10. Estructura de archivos

```
Trabajo/
├── optimizar.bat, probar_optimizador.bat, (des)instalar_autoarranque.bat
├── config.json                 ajustes
├── discord_webhooks.json       enlaces de Discord (NO se sube a GitHub)
├── README.md                   panel en directo (lo reescribe el programa)
├── DOCUMENTACION.md            este documento
├── ESTADO.md, bitacora.md      estado y decisiones
├── 0.stp.txt                   archivo original del enunciado (no se modifica)
├── cad/                        0.stp, agujeros_fijos.json, mapa de alturas, referencia del original
├── docs/                       parte1.md (SimJEB), fabricacion_aditiva.md
├── figuras/                    figuras de la Fase 2 (convergencia, von Mises y desplazamiento del original)
├── scripts/
│   ├── optimizer.py            optimizador (familias, ramas, panel, Discord, GitHub)
│   ├── evaluate.py             evaluación de una pieza (geometría → malla → ANSYS → métricas → imágenes)
│   ├── fem.py, run_mapdl.py    modelo de EF, entrada de MAPDL y lanzador
│   ├── geometry.py             familia «desde cero» y utilidades comunes
│   ├── geometry_vaciado.py     familia «vaciado»
│   ├── geometry_refuerzo.py    familia «refuerzo» (collares)
│   ├── exportar_workbench.py   proyectos de Workbench
│   ├── render.py, report.py    imágenes, fichas y gráficas
│   ├── discord_notify.py       avisos a Discord
│   └── fase2_*.py, find_holes.py, exportar_original_ansys.py   fases 0–2
└── runs/opt_37800N/            resultados (se crea al arrancar): familias, historial, galería, árbol, timelapse...
```

---

## 11. Hallazgos importantes hasta ahora
1. **El original está en el límite** con la carga de 37,8 kN: 212,9 MPa con la malla de optimización (195,2 MPa con malla fina), coeficiente de seguridad ≈ 1,0–1,1.
2. **Su punto crítico** está en el fondo del alojamiento del tornillo delantero. Ahí manda la combinación del alojamiento con las cavidades interiores.
3. **Vaciar sin reforzar apenas da margen** (−0,35 % de masa): casi cualquier corte grande supera el límite.
4. **Reforzar ese punto con un collar** baja el pico a 181 MPa y abre margen para vaciar el resto.
5. **La malla de optimización es ligeramente conservadora** en el punto crítico: la malla fina da tensiones un ~8 % menores.
6. **El máximo bruto** (630–975 MPa según la malla) es una singularidad del empotramiento, no una tensión real.
7. **La familia «desde cero»** aprende, pero todavía no llega a piezas válidas.

---

## 12. Limitaciones y pendientes
- **Fase 5 (pendiente)**:
  - verificación del diseño final con malla fina y estudio de convergencia;
  - modelo de tornillo realista (apoyo de la cabeza y contacto con el suelo, sin empotrar el agujero), que eliminaría la singularidad;
  - desplazamientos X/Y/Z, deformaciones y coeficiente de seguridad;
  - comparación entre el original y el final;
  - informe y guion de defensa.
- **La exclusión de 5 mm alrededor de los pernos** está justificada con el estudio de convergencia, pero hay que explicarla bien en la defensa.
- **Familia «refuerzo» v1 retirada**: el relleno escalonado de cavidades no se podía mallar.
- **No implementado (decisión)**:
  - preparar la siguiente pieza mientras ANSYS calcula (riesgo alto);
  - pulido final con CMA-ES (las ramas finas ya afinan);
  - mapa topológico tipo BESO (posible análisis para el informe).
- **Parte 1 (SimJEB)**: borrador en `docs/parte1.md`. Faltan los diseños concretos destacados, porque la web los carga con JavaScript.

---

## 13. Referencias
- Enunciado: *Trabajo MSD 26-27* (Proyecto 2) e *Instrucciones generales*, EINA, Universidad de Zaragoza.
- Whalen, E., Beyene, A., Mueller, C. (2021). *SimJEB: Simulated Jet Engine Bracket Dataset*. Computer Graphics Forum 40(5). doi:10.1111/cgf.14353 · arXiv:2105.03534.
- ISO/ASTM 52911-1:2019 y resto de fuentes de fabricación aditiva: `docs/fabricacion_aditiva.md`.
- Herramientas: ANSYS Student 2026 R1 (MAPDL y Workbench), gmsh, cadquery/OpenCascade, BoTorch/GPyTorch, PyVista, Plotly.
