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

## 2026-11-22 – Mejoras para funcionamiento desatendido
- **Discord** (`scripts/discord_notify.py`, enlaces en `discord_webhooks.json`, excluido de GitHub): canal «top» con UN mensaje que se edita (mejor diseño y estadísticas, actualizado al mejorar y cada 15 diseños como señal de vida), canal «árbol» (imagen nueva al cambiar la estructura o el mejor de una rama) y canal «todo» (ficha de cada diseño y avisos). Envío en segundo plano con reintentos y respetando los límites de Discord.
- **Robustez**: tiempo máximo de mallado de 60 s por intento (proceso aparte; gmsh se colgaba de forma aleatoria con malla gruesa en geometrías del original); pasada rápida opcional y solo en la familia «desde cero»; un error inesperado en un diseño se registra (`errores.log`), se avisa y se sigue (5 seguidos → parada); `optimizar.bat` reinicia el programa al minuto si cae; control de espacio en disco (limpieza si quedan < 5 GB, pausa si queda < 1 GB).
- Familia `refuerzo` retirada (geometrías no mallables). Filtro por predicción, ramas de cruce y congelado de parámetros en las ramas finas.
- Prueba completa: sin errores.

- **Ramas exploradoras**: todas las ramas nacían del mejor diseño de su madre, así que la búsqueda podía quedarse atrapada en un «valle» (le pasó a «vaciado», pegado al original). Ahora, cada 3 ramas terminadas (`rama_exploradora_cada`), nace una rama que parte de un punto al azar de entre los 20 más alejados de todo lo probado (de 2048 candidatos Sobol aleatorios) y hace allí sus pruebas; si encuentra algo mejor, sus hijas toman el relevo. Con 30 pruebas por rama, ≈ 25 % del tiempo es exploración. Comprobado con una simulación del árbol (resultados ficticios): las exploradoras nacen, se ejecutan y, cuando mejoran, la búsqueda continúa desde ellas.

## 2026-11-22 – Familia «refuerzo» v2 y verificación con malla fina
- **Refuerzo v2 (collares)**: un collar cilíndrico alrededor de cada alojamiento de tornillo (espesor delantero, trasero y altura como variables) + las operaciones de vaciado. Prueba en ANSYS sobre el original: con 6 mm, el pico baja de **212,9 a 181,2 MPa** (+159 g) y el punto crítico pasa a la orejeta. Malla sin problemas (formas cilíndricas simples). En la prueba corta, piezas válidas de 168–177 MPa.
- Cavidades cerradas que aparecen al combinar operaciones: se rellenan (en impresión 3D el polvo quedaría atrapado) en lugar de descartar la pieza.
- **Verificación automática con malla fina** (h = 3,5 mm) de cada candidato a nuevo mejor: si no cumple con la malla fina, se clasifica como «casi» y no se acepta. Resultado en la prueba: original 212,9 MPa (malla normal) → 195,2 MPa (malla fina); diseño 4: 195,1 MPa. Confirma la Fase 2: la malla normal es ligeramente conservadora en el punto crítico.
- Rapidez: la geometría de cada pieza se construye una sola vez (antes, dos: comprobación de repetidas + cálculo).
- En el modo de prueba no se envía nada a Discord salvo que se pida (`--discord`).
- No implementado (decisión): cálculo en paralelo geometría/ANSYS (riesgo alto, ganancia ~1,5×), pulido final con CMA-ES (las ramas «finas» ya afinan), mapa topológico tipo BESO (queda como posible análisis para el informe).

## 2026-11-22 – Criterio de «mejor diseño»: compromiso masa-seguridad
- Petición del grupo: que «mejor» no sea solo «más ligero», sino un consenso entre masa y coeficiente de seguridad.
- **Puntuación = masa × aprovechamiento^p** (menor = mejor), con aprovechamiento = max(σ/215 MPa, u/0,25 mm) = 1/CS. `peso_seguridad` p = 0,5 por defecto: 1 % menos de masa equivale a 2 % menos de tensión. p = 0 recupera el criterio literal del enunciado (solo masa). Los límites siguen siendo obligatorios; la puntuación solo ordena las piezas válidas.
- Se aplica en todo: nuevo mejor (y su verificación con malla fina), mejor de cada rama (región de confianza, cruces), adquisición (mejora esperada de log masa + p·log aprovechamiento, con varianza combinada), panel, Discord, árbol, clasificación y limpieza.
- Ejemplos (p = 0,5): original 2,423 kg / 212,9 MPa → 2,411; vaciado n.º 4 2,420 kg → 2,408; refuerzo n.º 5 2,543 kg / 177 MPa (CS 1,21) → 2,307 (mejor).
- Discord activo siempre, también en las pruebas.

## 2026-11-22 – Criterio aeronáutico: coeficiente de seguridad mínimo 1,15 y p = 0,15
- Revisión del criterio de «mejor» para una pieza de avión: en aeronáutica la seguridad se EXIGE (factor fijo) y, por encima, manda la masa (cada gramo vuela). p = 0,5 premiaba demasiado la seguridad (una pieza 120 g más pesada ganaba al original).
- **Requisito**: coeficiente de seguridad ≥ 1,15 sobre σy (factor de herraje de CS/FAR 25.625, aplicable a orejetas y uniones atornilladas) → σ ≤ 187 MPa (`margen_optimizacion` = 1/1,15). Cubre además la incertidumbre de malla (~8 %). **El original no cumple** (CS 1,01); la familia «refuerzo» sí (CS 1,21–1,27).
- **Desempate**: puntuación = masa × aprovechamiento^0,15 (1 % de masa ≈ 7 % de tensión).
- El coeficiente de seguridad que se muestra (panel, Discord, fichas) es siempre 215 MPa / σ.

## 2026-11-23 – Estancamiento: familia «SimJEB modificado» y anti-estancamiento
- **Diagnóstico de la noche del 22 al 23/11**: la familia «refuerzo» seguía mejorando a pasos diminutos (rama fina de 30 pruebas con paso 0,025 alrededor del mismo diseño, elección de rama siempre «la de mejor origen», así que las hermanas amplia/cruce no llegaban a ejecutarse); «vaciado» (62 diseños) y «desde cero» (62) sin ninguna pieza válida con σ ≤ 187 MPa.
- **SimJEB**: se descargan de Harvard Dataverse (doi:10.7910/DVN/XFUWJG) la tabla, el README y los 382 STEP (carpeta `datos_simjeb/`, no se sube a GitHub). Comprobado: nuestro `0.stp` es el diseño n.º 0 de SimJEB (mismo archivo, 1 950 338 bytes) → mismo sistema de coordenadas y mismos agujeros. Su columna `max_hor_stress` es el caso horizontal de 37,8 kN (el nuestro); factor de escala a nuestra métrica medido en el original: 212,9 / 414,3.
- **Nueva familia `simjeb`** (`scripts/geometry_simjeb.py`): candidatos más ligeros que el original con tensión estimada ≤ 260 MPa; comprobación previa de agujeros (se excluyen los que tienen el bulón macizo, el agujero del bulón más pequeño o los de perno agrandados); torneo de los 40 más prometedores tal cual; después collares (añaden) y 2 aligeramientos verticales pasantes (quitan; zonas protegidas alrededor de pernos y orejetas; se rechaza si parten la pieza). Agujeros detectados en la malla (`fem.detect_interfaces`), con error específico que no reintenta la malla si no se reconocen.
- **Optimizador**: ramas de 12 pruebas; paso mínimo 0,05; ramas hermanas por turnos; 25 % de turnos en una rama al azar; mutaciones grandes (2–5 variables) fuera de las ramas finas; distancia mínima 0,03 a todo lo probado; exploradora cada 2 ramas; **anti-estancamiento** (25 diseños sin mejorar un 0,3 % → 2 exploradoras y cierre de finas estancadas, aviso a Discord); variable categórica «semilla»; 3 ramas iniciales desde las 3 mejores semillas distintas; simjeb 2 diseños por ronda; presupuesto 600 por familia.
- **Sin perder el progreso**: el archivado por cambio de versión es ahora **por familia** (antes archivaba toda la carpeta); añadir la familia `simjeb` no archiva nada. Comprobado sobre una copia de `runs/opt_37800N`: no se archiva nada y las ramas de «refuerzo» continúan. `vaciado` se retira (`familias_retiradas`) conservando sus resultados.
- **Workbench**: el proyecto se monta también para diseños SimJEB (caras de pernos y bulón según lo detectado en la malla; tolerancia 0,25 mm y sin exigir superficies cilíndricas exactas).
- **Comprobación de compatibilidad** (`python scripts/geometry_simjeb.py --comprobar`): 74 candidatos → 62 compatibles, 10 excluidos (bulón macizo o de otro radio, agujeros de perno de otro tamaño o inexistentes), 2 con malla dudosa que se mantienen. La detección del bulón agrupa ahora los nodos por huecos > 6 mm (con malla de 4 mm y superficies B-spline los nodos del agujero quedaban a > 2 mm).
- **Booleanas sobre diseños SimJEB**: muchas superficies son B-spline tipo malla y la unión collar a collar fallaba (p. ej. n.º 321). Ahora se unen todos los collares a la vez y se repite con tolerancia difusa creciente (10⁻⁴ → 0,05 mm); igual para los aligeramientos. 31/32 modificaciones aleatorias se construyen bien.
- **Prueba completa en ANSYS** (n.º 321 tal cual): 1,301 kg, 284,6 MPa (estimación desde la tabla de SimJEB: 176 MPa; la estimación solo sirve para ordenar), 0,17 mm, error de reacciones 2·10⁻⁶ %. Con collares + un aligeramiento colocado a mano sobre el brazo: 466 MPa en el borde del aligeramiento (cortaba un brazo que trabaja): resultado físico que el optimizador debe aprender a evitar.
- **Petición del grupo: la pieza tiene que ser NUEVA.** Los diseños SimJEB sin modificar (o con cambios < 0,2 % del volumen) son solo **referencias**: se calculan para elegir puntos de partida, pero nunca cuentan como mejor diseño. Torneo reducido a 30 para empezar antes a modificar.

## 2026-11-23 – Cambio de enfoque: reglas de diseño con datos y carga de 42 258 N

- **Petición del grupo**: las familias no convergían y descartar una mala costaba mucho.
  1. Coeficiente de seguridad ≥ 1,0 (215 MPa) obligatorio.
  2. Aprender de las soluciones publicadas: evaluarlas con nuestras condiciones y sacar reglas con datos.
  3. Algoritmo nuevo que parta del original y lo modifique aplicando reglas (añadir y quitar material), cada cambio con su porqué, revirtiendo lo que no mejora.
  4. Trazabilidad en GitHub y Discord.
  5. Mucho más rápido.
  6. Limpieza.
- **Carga**: el profesor confirma **42 258 N** (Tabla 2). El modelo es lineal: SimJEB 373 pasa de 3 883 a 4 341 MPa (×1,118 = 42 258/37 800). El original pasa a ≈ 238 MPa (CS ≈ 0,90): **no cumple**, y el primer paso es reforzar.
- **Archivado** el enfoque anterior en `runs/archivo/opt_37800N_familias_hasta_20261123/` (624 diseños). **Eliminados**:
  - módulos de familias (`geometry_vaciado/refuerzo/simjeb.py`, la familia «desde cero» de `geometry.py`);
  - procesos gaussianos, ramas, torneo y anti-estancamiento;
  - `report.py`;
  - `cad_stp.zip` (ya descomprimido) y los ficheros de comprobación antiguos de SimJEB.
- **Nuevos módulos**:
  - `estudio_simjeb.py`: las 381 soluciones con nuestra carga; pasada rápida (h = 6) y completa solo si es prometedor; unos 30 s por diseño descartado;
  - `campo.py`: análisis del campo de tensiones;
  - `operaciones.py`: 7 operaciones con zonas protegidas;
  - `reglas.py` y `DESIGN_RULES.md`;
  - `optimizer.py` reescrito.
- **Datos ya visibles**:
  - En el original, **el 51 % del material trabaja a menos del 15 % del límite** (el 85 % en la placa base). El pico está en el fondo del alojamiento del perno 1, con una concentración local ×2,4.
  - **R5 desactivada por los datos**: agrandar el alojamiento (radio del acuerdo mayor, Peterson) SUBE la tensión en los 294 diseños anteriores (Spearman +0,76; mediana de 360 frente a 206 MPa). Domina la sección que se pierde.
  - **R4 (collar) respaldada**: prueba directa de −15 % con 6 mm (+159 g); en la familia refuerzo, más collar delantero → menos tensión (Spearman −0,25).
- **Redondeo junto al pico**: la primera prueba fallaba porque tocaba el borde del agujero del perno, y la verificación de agujeros lo detectó. Ahora las aristas de los 6 agujeros fijos se excluyen siempre.

## 2026-11-23 – Formas nuevas con fundamento y objetivo «solo masa»

- **Petición del grupo**:
  - que sea un «creador de piezas»: con unas premisas, la mínima masa con la tensión y el desplazamiento como límites;
  - que pueda **añadir formas nuevas** si mejoran la pieza, pero nunca «pegotes a ver si funcionan».
- **Objetivo**: `peso_seguridad` = 0, es decir, solo masa. La seguridad sobrante ya no puntúa.
- **Direcciones principales**: MAPDL exporta ahora el tensor completo (SX, SY, SZ, SXY, SYZ, SXZ) en cada nodo. `campo.py` calcula las tensiones y direcciones principales de cada elemento y la **dirección dominante** de una zona (tensor de orientación ponderado por |σ|·V). Comprobación: el von Mises reconstruido coincide con el de ANSYS (error relativo 1e-7).
- **Operación `nervio`**:
  - pared vertical de espesor t con el borde superior inclinado (también hace de cartela), que nace de la base y es imprimible;
  - nunca invade los tornillos, sus cabezas, el bulón ni el hueco entre orejetas;
  - no sale de la caja del original.
- **Regla R11 (sustituir un bloque por un nervio)**:
  - **Cuándo**: un bloque que trabaja algo (< 45–60 % del límite), o un rebaje que se rechazó por tensión.
  - **Dirección del nervio**: la principal dominante del material quitado.
  - **Tamaño (Michell 1904)**: el volumen mínimo que lleva la carga es ∫|σ| dV / σ_trabajo, con el nervio al 60 % del límite.
  - **Ejemplo sobre el original** (carga escalada a una pieza que cumple): bloque trasero de 64 cm³ (máx. 41 % del límite) → nervio de 4 mm a 60° en la dirección (+0,46; +0,81; −0,36), de las orejetas hacia el perno 2. Son 8,9 cm³ en lugar de 64 (−430 g previstos). La geometría se construye y conserva los 6 agujeros.
- **GitHub**: fuera `runs/archivo/` (4 413 ficheros del enfoque anterior; quedan en el PC). Los datos que usan las reglas pasan a `estudio/calculos_anteriores.csv`.
- **Primeras pruebas de R11 en ANSYS** (pieza de 2,450 kg y 201,9 MPa; bloque trasero de 31 cm³ que trabaja al 43 % como máximo):
  - 1 nervio en la dirección dominante → 515 MPa. El pico estaba en el propio nervio: un bloque a flexión lleva tracción Y compresión y un solo nervio no equilibra.
  - Mejoras con fundamento:
    - **dos familias** (Michell: un nervio por cada familia que lleve ≥ 25 % de la carga);
    - nervios dimensionados al 50 % del límite;
    - **acuerdo de 3 mm en la raíz** del nervio;
    - **no dejar paredes < 5 mm** al borde de un rebaje (se abre hasta el borde);
    - **radio de las esquinas** del vaciado = 20 % de su lado menor (3–8 mm).
  - Resultado tras las mejoras: 515 → 404 → 362 MPa. Ese bloque sigue sin poder sustituirse entero, porque está en el camino de la carga hacia el perno 2.
  - El optimizador lo rechazará y, por R9, en esa zona solo probará sustituciones menores. Si R11 falla 8 veces sin acierto, se suspende y queda reflejado en DESIGN_RULES.md.
- Booleanas: algunos cortes daban sólidos que OCC marca como no válidos; ida y vuelta por STEP los repara (comprobado). La malla rápida prueba ahora la reparación de geometría de gmsh en su 3.er intento.
- Los cortes que atraviesan la zona de cartelas y alojamientos pueden dejar caras diminutas que gmsh no malla. Esas propuestas se descartan solas y quedan anotadas.

## 2026-11-24 – Bucle de verificación (malla fina) corregido

- **Síntoma:** desde la noche del 23 al 24 el optimizador repetía el mismo ciclo (84 veces, unas 11 h).
  1. Desde la pieza verificada de 2,161 kg aceptaba dos aligeramientos (2,144 kg y 2,131 kg, 208,3 MPa con la malla de 4 mm).
  2. En el hito, la **malla fina** daba 216,8 MPa (> 215): no se confirmaba y volvía a 2,161 kg.
  3. Nada recordaba el motivo, así que volvía a proponer los mismos cambios.
- **Causa de fondo:** en esta pieza la malla de 4 mm da el pico entre un 2 y un 7 % más bajo que la malla fina (12 verificaciones distintas: cociente fina/normal 1,02–1,07). Las piezas aceptadas al 97 % del límite podían superarlo.
- **Corrección** (con los datos del propio programa):
  1. **Calibración malla normal → malla fina:** cada verificación guarda el cociente fina/normal (tensión y desplazamiento). Para aceptar una pieza se exige `σ_normal × k ≤ 215 MPa`, con k = mediana de las 3 últimas verificaciones (ahora 1,041, es decir ≤ 206,5 MPa con la malla normal). Las reglas analizan el campo con ese límite corregido.
  2. **Si la malla fina no confirma un hito**, los cambios hechos desde el último diseño verificado se anotan como rechazados. Por la regla R9, en esa zona solo se probarán cambios menores, así que el mismo camino no puede repetirse.
- La calibración se sembró con las 12 verificaciones del registro. Progreso conservado: pieza actual 2,144 kg; último hito verificado 2,161 kg (frente a 2,423 kg del original, que además no cumplía).

## 2026-11-24 – Pieza simétrica (obligatorio)

- **Petición del grupo:** «sobre todo la pieza tiene que ser simétrica».
- **Plano de simetría:** el plano medio de las orejetas (perpendicular al bulón por su centro, donde se aplica la carga). El original es simétrico en un 90 % de su volumen; la asimetría viene de los agujeros de los pernos del enunciado (pernos 2 y 4 desfasados 18,5 mm; 1 y 3, 4,5 mm). La pieza será simétrica salvo donde lo impiden esos agujeros fijos.
- **Implementación:**
  - cada operación (aligeramiento, rebaje, hueco, nervio, redondeo) se aplica también en su simétrico; los collares van por parejas simétricas y las orejetas ya lo son;
  - en el análisis del campo, un material solo es «ocioso» si también lo es en el lado simétrico.
- **Intento de conservar la pieza asimétrica** (2,144 kg, 14 operaciones) aplicando sus operaciones en simétrico, en ANSYS con la corrección a malla fina (×1,041):

  | Operaciones | Masa | Tensión normal | Corregida | Resultado |
  |---|---|---|---|---|
  | 14 | 2,061 kg | 316 MPa | 329 MPa | no cumple |
  | 8 | — | 252 MPa | 262 MPa | no cumple |
  | 5 | — | 242 MPa | 252 MPa | no cumple |
  | 3 | — | 208 MPa | 216 MPa | no cumple |
  | 2 (solo collares) | 2,504 kg | 202 MPa | 210 MPa | cumple |

  Sus aligeramientos estaban donde sobraba material solo en un lado.
- **Nuevo punto de partida:** la pieza asimétrica se archiva en el PC (`runs/archivo/opt_42258N_asimetrico_hasta_20261124`) y el optimizador sigue en modo simétrico desde el original con los dos collares (2,504 kg, 201,9 MPa). Conserva la estadística de cada regla y la calibración de malla.
- **Corregido también:** el motivo de rechazo ahora muestra la tensión corregida a malla fina (antes decía «desplazamiento» por error cuando la causa era la tensión corregida).

## 2026-11-24 – Primera optimización simétrica terminada y reglas nuevas

- **Resultado de la primera pasada simétrica:** 2,293 kg; 199,3 MPa con malla normal y **213,8 MPa con malla fina** (límite 215), desplazamiento 0,146 mm. Terminó porque ninguna regla encontraba nada más.
- **Diagnóstico:**
  - El pico está en la **unión del collar del perno 3 con el cuerpo** (arista viva, concentración ×2,6). Detrás, casi igual de cargada, está la parte alta de las **orejetas**.
  - OCC no consigue redondear esa unión (superficies B-spline): de 27 aristas, solo 9 admiten el acuerdo por separado.
  - Un collar troncocónico a 30° elimina ese pico, pero entonces manda la orejeta (201 MPa) y añade 114 g. No compensa.
  - La **placa base sigue ociosa al 73 %** (60 cm³, frente a 37,5 cm³ del diseño publicado válido más ligero, SimJEB 237 con 1,975 kg). No se podía quitar: los cortes desde arriba dejaban un suelo de 5 mm y los agujeros redondos exigían que toda la columna estuviera ociosa (el cuerpo de encima trabaja).
- **Simetría:** 90,6 % del volumen tiene material en su simétrico, igual que el original. La asimetría restante viene del original (paredes interiores) y de la posición de los pernos.
- **Mejoras nuevas:**
  - **R13, ventanas pasantes:** donde toda la columna está ociosa.
  - **R14, bolsillos desde la cara de apoyo:** con techo a 45°, imprimibles, en la placa base bajo el cuerpo. En la pieza actual salen bolsillos de 28 × 24 mm hasta z = 19–21 mm al umbral del 25 %.
  - **Umbral de material ocioso hasta el 45 %.**
  - **Protecciones de los pernos también reflejadas:** cada corte coincide exactamente con su simétrico. Por eso la pieza actual se reconstruye y se recalcula antes de seguir.
  - **Collar con acuerdo en la raíz:** opción añadida, aunque OCC no siempre puede aplicarla.
  - Evidencia de R13 y R14: la placa base del original tiene 67 cm³ (77 % ociosa); la mitad más ligera de los 16 diseños publicados válidos, 45 cm³.

## 2026-11-24 – Simetría efectiva y collar acampanado (R12)

- **Asimetría detectada por el grupo:** el aligeramiento D16 en (64, −32) se aplicaba también en su simétrico, (66, −112), pero allí **no hay material**: el contorno del original es más estrecho en esa zona. Resultado: un agujero en un extremo y nada en el otro. Material a su alrededor: 2,07 frente a 0,20 cm³.
- **Corrección:**
  - Se quita ese aligeramiento de la pieza.
  - **Simetría efectiva:** cada corte propuesto debe quitar parecido material en los dos lados (diferencia ≤ 25 %, medida en la malla); si no, se descarta.
- **Primera pasada con R13/R14** (antes de corregirlo): 2,293 → 2,241 kg gracias a los bolsillos desde la cara de apoyo. Después se paró: los cortes de 37–58 g pasaban del límite por un 1–3 %.
- **Pruebas en ANSYS para bajar los picos** (pieza simétrica sin ese agujero: 2,257 kg y 202,1 MPa en la parte alta de la orejeta; corregido a malla fina son 216 MPa, un poco por encima):
  - collares acampanados (30° hasta z = 16 mm): **190,7 MPa (−5,6 %) con +52 g** → nueva regla **R12**, que el optimizador acepta como inversión;
  - collar cónico entero a 15°: no se puede mallar (superficie periódica);
  - engrosar las orejetas por fuera: la operación de prueba apenas añadió material (sin efecto); pendiente de rehacer.
- Corregida también la condición de «inversión»: usaba la tensión sin la corrección a malla fina.
