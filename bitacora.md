# Bitácora – Proyecto 2 "Diseño de un soporte" (831_MSD_13_B, Soporte 6: carga 2, acero S235)

## Reglas de trabajo
- Toda ejecución (MAPDL, optimizador, instalaciones) muestra su progreso en una **consola visible** y lo guarda también en un log en disco (petición del grupo, 2026-11-22).
- Los PDF y el `0.stp` original no se modifican. Se trabaja sobre la copia `cad/0.stp` (el original es `0.stp.txt`).

## 2026-11-22 – Fase 0 (entorno)
- **ANSYS**: Student 2026 R1 (v261), en `C:\Program Files\ANSYS Inc\ANSYS Student\v261`. Hay un Cloudpaging Player (Numecent) instalado, pero los binarios de MAPDL son accesibles desde una terminal normal, sin abrir el reproductor.
- **Licencia**: Student local (FlexNet ansyslmd en 127.0.0.1), no necesita VPN. Con la llamada por defecto MAPDL pide MECH_1/MEBA, que no existen ("No such feature"). **Solución: lanzar con `-p ansys`.** Límite Student: 128 000 nodos/elementos en estructural (pendiente de comprobar el valor exacto en un modelo grande).
- **Vía elegida**: MAPDL en batch (`MAPDL.exe -b -p ansys -np 2 -smp -i x.inp -o x.out`) mediante `scripts/run_mapdl.py`, con timeout que mata solo su propio árbol de procesos (`taskkill /T /PID`) y progreso en consola. Se descartan Workbench/PyMAPDL: hay más piezas que pueden fallar y no aportan nada al bucle.
- **Prueba de la viga en voladizo** (`tests/cantilever`), tet10 SOLID187, 6650 nodos, 27 s:
  flecha 1,9052 mm frente a 1,9048 mm analítico (0,02 %); reacción 1000,0 N; σx(x = 50) 300,13 MPa frente a 300 MPa (0,04 %). → **Modo AUTOMÁTICO viable.**
- **Python**: 3.12 en el venv `.venv`, con numpy, scipy, pandas, matplotlib, pyvista, gmsh, cadquery 2.8, optuna, cma y scikit-learn. torch/botorch en instalación (si fallan, se usa Optuna).
- **Pipeline geométrico previsto**: cadquery (geometría paramétrica) → gmsh (malla tet10) → `.inp` con NBLOCK/EBLOCK y componentes de las superficies de pernos y bulón → MAPDL. Así se evita la importación de CAD en MAPDL, que necesita licencias de importación.
- Procesos ANSYS huérfanos (PID 2784 y 6524) de la primera prueba fallida, sin licencia: no se mataron porque el sistema de permisos lo denegó. Están parados esperando y se pueden cerrar desde el Administrador de tareas.

## Geometría de 0.stp (scripts/find_holes.py → cad/agujeros.json)
- Volumen 307 191 mm³, es decir, **masa en acero 2,411 kg**. Caja envolvente x[−39,8; 67,5] y[−163,4; 16,9] z[−1,3; 63,2] mm.
- Pernos (eje Z, placa z = 0,63–7,85): (0; 0) R5,334 · (52,047; 1,580) · (0; −148,125) · (38,083; −146,968), los tres últimos con R5,156.
- Bulón: R9,557 (Ø19,11), eje (−0,0304; 0,9995; 0), centros (−21,357; −60,417; 44,725) y (−20,490; −88,979; 44,725). Separación entre orejetas 28,58 mm.

## PUNTO ABIERTO – dirección de la carga 2 (pendiente de decisión del grupo/tutor)
- En 0.stp **Z es la vertical** (normal a la placa base).
- La Tabla 2 parece usar el sistema de SimJEB/GE, **con Y vertical**:
  - caso 1 = Fy 35 586 N, que coincide con el caso «Vertical 35,6 kN» de la Fig. 2;
  - caso 3: (Fy, Fz) = (31 404; 28 276) tiene módulo 42 258 N, que coincide con «Diagonal 42,3 kN»;
  - caso 4: ±19 766,4 N × 28,58 mm = 565 kN·mm, que coincide con «Torsional 565 kN·mm» (pares opuestos en las dos orejetas, horizontales).
  → En la Tabla 2, Z sería **horizontal y perpendicular al eje del bulón**, es decir, ≈ X del STEP.
- El caso 2 de la Tabla (Fz = 42 258 N) correspondería entonces a «Horizontal», que en la Fig. 2 vale 37,8 kN (8500 lbf). 42 258 es el módulo del caso diagonal → errata probable en la magnitud.
- Por eso hay dos interpretaciones: (A) 42 258 N en Z del STEP (tirón vertical, lo que dice la Tabla tomada literalmente con los ejes del STEP); (B) carga horizontal en X del STEP (lo que indican la Fig. 2 y la coherencia de la Tabla), con 42 258 N (Tabla) o 37,8 kN (Fig. 2).
- SimJEB (Whalen et al., 2021, CGF 40(5), doi:10.1111/cgf.14353) aplica las cargas con RBE3 sobre la superficie del agujero de interfaz y los pernos con RBE2 + SPC. El texto accesible no da los vectores de carga.

## 2026-11-22 – Dirección de la carga (RESUELTO con el grupo)
- Sistema del enunciado: Y vertical (eje de los pernos), X a lo largo del bulón, Z horizontal perpendicular al bulón (aclarado por el grupo con la Fig. 3).
- Carga 2 = Fz = 42 258 N → en el STEP, dirección horizontal perpendicular al bulón: d = (0,9995; 0,0303; 0).
- Se mantiene 42 258 N (Tabla 2, la más desfavorable). La posible errata frente a los 37,8 kN de la Fig. 2 queda para consultarla con el tutor; la carga está parametrizada (`force` en fem.write_inp).
- Con un RBE3 sobre la superficie completa, el problema es lineal en F: el signo de la carga no cambia σvM.

## 2026-11-22 – Fase 2 (modelo base)
- **Límite Student confirmado: 128 000 nodos** (error de MAPDL al superarlo). El código de salida 8 es «terminado con avisos» y se trata como correcto.
- Malla: gmsh, tet10 (SOLID187) con **aristas rectas**. Con los nodos intermedios curvos, 299 elementos fallaban la comprobación de forma de MAPDL por distorsión. El orden de los nodos gmsh→SOLID187 y el signo del volumen se verifican en cada malla (`check_tet10`).
- Superficies de pernos y bulón: se seleccionan los triángulos de superficie con los 3 vértices sobre el cilindro (tolerancia 0,05 mm) y se comprueba que estén los 4 pernos y las 2 orejetas.
- Condiciones de contorno: empotramiento (UX = UY = UZ = 0) en los 4 cilindros de los pernos. Carga mediante RBE3 desde un nodo piloto (MASS21) situado en el punto medio entre las dos orejetas hasta toda la superficie de ambos agujeros. No hay cargas puntuales.
- Equilibrio: R = (42 238,5; 1 282,5; 0) N = F·d, **error 0,0000 %**.
- **Métrica de tensión** (`fem.stress_metric`): máximo de σvM nodal promediado excluyendo (a) un cilindro de r = R + 5 mm alrededor de cada perno (zona de arandela/cabeza M10 y singularidad del empotramiento) y (b) una banda de 2 mm alrededor de la superficie del bulón (esquinas del RBE3).
  Elección de la zona, con mallas de 45k a 103k nodos:
  - exclusión de 2–3 mm en los pernos: el valor crece al refinar (218 → 298 MPa) → singular;
  - 5 mm: 204 → 210 → 218 → 216 MPa → estable (1,2 % entre las dos mallas más finas);
  - en el bulón, pasar de 1 a 5 mm no cambia el resultado.
- **Resultados del original** (malla de 103k nodos, h = 3,5 mm): masa 2,421 kg (CAD 2,4115 kg; +0,4 % por discretización), métrica 215,7 MPa, σvM bruto 975 MPa (singular), umax 0,149 mm (ux 0,122 · uy 0,021 · uz 0,103), **FS = 215/215,7 = 1,00**. El original en acero está justo en el límite de σy.
  Con σ_obj = 0,9·215 = 193,5 MPa el original NO cumple. Con FS 1,5 (143 MPa) tampoco.
- Pendiente: uy máx. salta de 0,012 a 0,021 mm en la malla más fina (efecto local por revisar). La malla de gmsh con 4 hilos no es determinista (diferencias de ~3 % en la métrica entre repeticiones) → el optimizador usará 1 hilo.
- Figuras: `figuras/fase2_convergencia.png`, `figuras/fase2_vonmises_original.png`, `figuras/fase2_desplazamiento_original.png`. Datos en `runs/base/*/metrics.json` y `runs/base/convergencia.csv`.

## 2026-11-22 – Fase 3 (en curso)
- Ejes y carga (acordado con el grupo): en las imágenes, Z arriba, Y = eje del bulón, X perpendicular. **Carga en −X**, aplicada en los agujeros del bulón (RBE3). Con un modelo lineal y RBE3, σvM no depende del sentido.
- Apoyo: empotramiento en las superficies de los 4 agujeros de pernos (las «fixed support interfaces» azules de la Fig. 3), no en toda la cara inferior. Fijar toda la base equivaldría a pegarla al suelo y subestimaría las tensiones, porque con esta carga un lado de la base tiende a levantarse.
- Geometría paramétrica (`scripts/geometry.py`): 12 variables. Todos los acuerdos se generan con cierres morfológicos 2D (sin depender del fillet 3D de OCC). Los 6 agujeros se verifican en cada diseño (área cilíndrica / referencia = 1,000 ± 1 %).
- Evaluación (`scripts/evaluate.py`): reintentos automáticos de malla (HXT → Delaunay → h × 0,9 → Frontal) si gmsh falla o ANSYS rechaza elementos; limpieza de perfiles 2D y ShapeFix; eliminación registrada de virutas sueltas < 0,1 % del volumen.
- **Validación de extremos (v3): 6/6 evaluados sin fallos** (`runs/extremos/resumen.json`). Ninguno cumple: el mejor da 539 MPa con 2,80 kg.
- **Hallazgo**: con la familia «cajón», el pico está en el fondo del alojamiento circular de los pernos (a 12–13 mm del eje): 539–599 MPa. En el original, la tensión cerca de los pernos es de 208–218 MPa y casi no depende del radio de exclusión (5 → 20 mm). Diferencia geométrica: el original tiene los pernos en una franja rebajada en cada extremo, con la pared inclinada detrás, sin alojamientos circulares. → Hay que reparametrizar los extremos antes del bucle largo.
- Repositorio de GitHub (privado): https://github.com/Hugiko/msd-soporte-optimizacion. El optimizador sube cada iteración en segundo plano; si falla la red, no se detiene.

## 2026-11-22 – Fase 3: carga por defecto y geometría v5
- **Carga por defecto: 37 800 N** (caso Horizontal de la Fig. 2), decidido por el grupo. Se cambia en `config.json` (`carga_N`: 37800 o 42258). Cada carga guarda sus resultados en `runs/opt_<carga>N`.
- Referencia: el modelo es lineal, así que el original con 37,8 kN da 216 × 37 800 / 42 258 ≈ **193 MPa**, justo en σ_obj = 193,5 MPa.
- Geometría v5: pernos en franja plana (asiento a la cota del original), cajón con paredes extremas inclinadas (`phi_end`) que pueden llegar hasta la línea de pernos (`g_end` < 0 → bloque con pozos tallados, como el original), radio del pozo variable (`R_pocket`). Medido en 0.stp: asiento plano hasta r = 8,0 mm, acuerdo de 2,54 mm y pozo de r = 10,54 mm.
- Cámaras del hueco: todas sus aristas redondeadas con el fillet 3D de OCC (fiable en sólidos convexos); si falla, la cámara se deja maciza y se registra. La reparación automática de gmsh queda solo como último recurso, porque al coser caras puede borrar el volumen.
- Validación de extremos v5: **6/6 evaluados sin fallos**. Mejor diseño de prueba a mano: 520 MPa con 2,72 kg (pico en el acuerdo del pozo del perno trasero; 296 MPa en el pie de la orejeta). **Aún lejos del original (193 MPa).**
- `shell()` de OCC sobre el original (para vaciarlo con espesor constante) falla («BRep_API: command not done»).
- PENDIENTE DE DECISIÓN: familia «desde cero» (v5) frente a familia «vaciado del original».

## 2026-11-22 – Fase 3: programa definitivo
- Límite: **215 MPa** (σ_adm = σy; el enunciado no da ningún margen; el 0,9 venía del prompt). Configurable (`margen_optimizacion`).
- Exclusión de la singularidad: 5 mm alrededor de cada agujero de perno (zona de la cabeza del tornillo) y 2 mm alrededor del bulón. Se justifica con el estudio de convergencia (el pico bruto diverge: 474 → 975 MPa) y en cada diseño se guarda la sensibilidad (exclusión 0 / 3 / 5 / 8 mm). El diseño final se verificará con un modelo de tornillo realista.
- **Dos familias** que se alternan: «vaciado del original» (10 parámetros: hueco interior redondeado y recorte inclinado del lado alejado) y «desde cero» (12 parámetros). En el original, los cortes necesitan booleanas difusas (tol = 1e-4): sin ellas OCC falla en silencio. El original NO es macizo: tiene cavidades interiores (suelo a 2,54 mm) y agujeros de evacuación de polvo.
- **Algoritmo**: DOE Sobol (12) → procesos gaussianos (BoTorch) para masa y tensión → región de confianza (tipo TuRBO): pequeños cambios alrededor del mejor; si mejora, sigue la dirección y alarga el paso; si falla 4 veces, lo acorta; si el paso es < 0,02, reinicia en otra zona; tras 3 reinicios sin mejora, la familia termina. Adquisición = mejora esperada de masa × probabilidad de cumplir.
- Cada **nuevo mejor diseño global**: proyecto de Workbench (.wbpj resuelto en el PC + .wbpz montado para GitHub; Fixed Support, Remote Force deformable, malla cuadrática de 4 mm), entrada en `historial/`, fotograma del timelapse, ficha `resumen.png` (geometría | von Mises | deformada | datos) y subida a GitHub. El `README.md` del repositorio es un panel que se actualiza en cada iteración.
- Licencia Student = **1 sesión de ANSYS a la vez**. Si Workbench está abierto, el programa detecta «licencia ocupada», avisa y reintenta cada minuto (no penaliza el diseño). Los proyectos de Workbench que no se puedan crear quedan pendientes y se reintentan.
- Limpieza automática cada 10 diseños: borra los ficheros pesados de diseños antiguos ya superados (conserva datos, fichas, los 5 mejores y los 20 últimos) y los proyectos de Workbench resueltos salvo los 3 últimos mejores.
- Uso: `optimizar.bat` (doble clic), `instalar_autoarranque.bat` (arranca solo al iniciar sesión), `probar_optimizador.bat` (prueba corta en carpeta aparte), `config.json` (ajustes).

- Familia «vaciado»: nuevo parámetro `R_pocket` (remodelar el alojamiento de la cabeza del tornillo, acuerdo de fondo R − 8). Prueba sobre el casi-original: con R = 10,54 da 212,9 MPa; con R = 14 da **800 MPa** (al agrandar el pozo se adelgaza la pared que lo separa de las cavidades interiores del original). Rango limitado a 10,54–12 mm.
- La familia «desde cero» es la que puede añadir material en cualquier zona (solo respeta los 6 agujeros); el optimizador alterna ambas.
- Prueba completa del programa (5 diseños por familia): sin errores; 2 proyectos de Workbench creados y resueltos; historial, timelapse, gráficas, panel y limpieza (440 → 198 MB) correctos.

- Segunda condición: **desplazamiento máximo ≤ 0,25 mm** (≈ 2 × el original, 0,129 mm con 37,8 kN; configurable, 0 = sin límite). El enunciado no lo exige; se añade para evitar piezas ligeras pero demasiado flexibles. Hay un tercer proceso gaussiano para log(u_max) y la probabilidad de cumplir es el producto de las dos. Sin diseños válidos, el criterio es el incumplimiento máximo (σ/σlím, u/ulím).
- Un nuevo mejor diseño exige una mejora de masa ≥ 0,5 % (`mejora_minima_para_nuevo_mejor`): evita crear proyectos de Workbench por mejoras insignificantes.
- Reparto del tiempo: una familia sin ningún diseño válido tras 30 intentos solo calcula 1 de cada 3 turnos.
- Se silencian los avisos de obsolescencia de torch (no son errores).
- Prueba corta repetida con el límite de desplazamiento: sin errores.

- Región de confianza: **cualquier mejora real cuenta como éxito** (umbral 0,01 %; antes 0,5 %, que trataba como fracasos mejoras del 0,1–0,2 % y encogía el paso justo cuando iba bien). El 0,5 % se mantiene solo para crear un proyecto de Workbench.
- Detección de geometrías repetidas: antes de ANSYS se compara el volumen con todos los diseños calculados; si coincide (< 0,5 mm³), se reutiliza el resultado (se habían calculado varias veces piezas idénticas: 013–015 = 001, 016–018).
- Panel: el mejor diseño real se muestra siempre; el historial lista TODAS las mejoras (las que tienen proyecto de Workbench lo indican); gráfica con la hora real en el eje; gráfico interactivo `evolucion_interactiva.html` (plotly). La referencia de masa pasa a ser el original con el mismo modelo de EF (2,423 kg), no la del CAD.
- Subidas a GitHub: git por ruta completa (con doble clic desde el Explorador no se encontraba git y no se subía nada).

## 2026-11-22 – Fabricabilidad (fabricación aditiva)
- Proceso supuesto: **fabricación aditiva metálica** (LPBF), como exigía el GE Jet Engine Bracket Challenge. El propio 0.stp tiene cavidades interiores con agujeros de evacuación de polvo en la base (diseño pensado para AM). Matiz para la defensa: el S235 no es un acero habitual en AM (lo son 316L y 17-4PH); se analiza la geometría con las propiedades que fija el enunciado.
- Reglas implantadas en ambas familias:
  1. **Techo autoportante**: cada hueco interior es el mayor sólido con techo a cuatro aguas de 45° que cabe (en «vaciado», caja ∩ dos tiendas a 45°, con parte plana superior ≤ 3 mm; en «desde cero», `tent45()` en las dos secciones). Imprimible sin soportes interiores.
  2. **Evacuación de polvo**: agujero de Ø5 mm desde el suelo de cada cámara hasta la cara inferior.
  3. Pared mínima de 3 mm sobre los huecos y suelo mínimo de 5 mm (vaciado) / 7,22 mm (desde cero).
- Comprobado en los extremos de ambas familias: todas las geometrías se construyen, con los 6 agujeros intactos.
- Versionado de la geometría (`VERSION` en cada familia): al arrancar, si los resultados guardados son de otra versión, se **archivan** en `runs/archivo/` y se empieza limpio (la ejecución anterior, sin reglas de fabricación, queda archivada).

- **Galería cronológica**: cada diseño calculado (válido, casi, no válido o fallido) deja su ficha comprimida (JPG) en `runs/opt_<carga>N/galeria/AAAAMMDD_HHMMSS_familia_n_VEREDICTO_masa.jpg`; los fallos dejan una tarjeta con el error. `GALERIA.md` las muestra todas, de la más reciente a la más antigua, y se enlaza desde el README. Las copias PNG de cada carpeta ya no se suben (no se duplican).

- **Árbol genealógico de ramas**: una rama es una línea de búsqueda que parte de un diseño semilla y prueba cambios alrededor de su mejor diseño (región de confianza). Al terminar (30 pruebas, configurable en `pruebas_por_rama`, o paso diminuto), su mejor diseño crea dos ramas hijas: «fina» (paso inicial 0,10) y «amplia» (0,35). Siempre se trabaja en la rama activa cuyo origen es mejor (empates: la más antigua). Todas las ramas comparten los procesos gaussianos (lo que aprende una lo aprovechan las demás). Cada diseño registra su rama. `ARBOL.md` dibuja el árbol con Mermaid (GitHub lo muestra como diagrama): azul = activa, gris = terminada, verde = rama donde se encontró el mejor diseño. Presupuesto por familia: 300.
- Prueba corta (ramas de 2 diseños): ramas V1 → V1.1/V1.2 → V1.1.1/V1.1.2 creadas correctamente; en «desde cero» la tensión baja de rama en rama (906 → 865 → 794 → 670 MPa).
