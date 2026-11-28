# Prompt: estudio exhaustivo de la pieza final del Soporte 6 (MSD 2026-27)

> Copia todo lo que hay debajo de la línea en el agente que vaya a hacer el estudio. Está escrito para un agente con acceso a los archivos de este PC y a ANSYS Student.

---

## 0. Tu papel y lo que te pido

Eres un ingeniero mecánico especialista en análisis por elementos finitos. Trabajas para un grupo de estudiantes de Ingeniería de Tecnologías Industriales (Universidad de Zaragoza, EINA). Han diseñado y optimizado un soporte de acero y necesitan un **estudio muy exhaustivo de la pieza final**, que después será la base del informe de la asignatura y de su defensa oral.

Tienes que:

1. **Entender** por qué la pieza es como es. Abajo te doy el trasfondo completo: qué pide el enunciado, qué decisiones se tomaron y por qué, y el porqué de cada hueco, bolsillo y refuerzo.
2. **Analizarla a fondo** con ANSYS y con cálculos a mano:
   - cómo carga y por dónde va la carga;
   - reacciones en cada perno;
   - tensiones, deformaciones unitarias y desplazamientos;
   - convergencia de malla y sensibilidad a las hipótesis del modelo;
   - efecto de la temperatura;
   - comportamiento dinámico.
   Más adelante tienes la lista completa.
3. **Explicar con números** por qué se quitó material en cada sitio y por qué se añadió en otros. También qué se intentó y no funcionó, porque eso demuestra dónde está el camino de la carga.
4. **Redactar** el estudio en español, con figuras y tablas numeradas, preparado para integrarse en el informe.

Trabaja en español. **No inventes datos, resultados ni referencias.** Cada número sale de un cálculo tuyo, de un archivo que te indico o de una fuente que cites. Si algo es una hipótesis tuya, dilo explícitamente.

---

## 1. Contexto académico

- **Asignatura:** Mecánica de Sólidos Deformables (MSD), Grado en Ingeniería de Tecnologías Industriales, curso 2026-27.
- **Grupo:** 831_MSD_13_B. **Proyecto 2 «Diseño de un soporte», Soporte 6: caso de carga 2, acero S235.**
- **Enunciado:** `C:\Users\hugof\Downloads\Trabajo MSD 26-27.pdf` (Proyecto 2, págs. 9-12). **Instrucciones:** `C:\Users\hugof\Downloads\Instrucciones generales.pdf`. **Léelos** (no los modifiques).
- **Origen:** el soporte del «GE Jet Engine Bracket Challenge» (GrabCAD, 2013). Era un soporte de elevación de un motor a reacción, en Ti-6Al-4V, con 4 casos de carga y fabricación aditiva.
- **Lo que pide el enunciado:**
  - Partir de `0.stp`.
  - Conservar **solo** la posición de los 4 agujeros de anclaje (pernos de 10,31 mm) y de los 2 orificios del bulón (19,05 mm). Todo lo demás se puede cambiar.
  - Objetivo: (i) no superar nunca la tensión admisible y (ii) minimizar el material.
- **Partes del trabajo:**
  - Parte 1: información de https://simjeb.github.io y análisis de los diseños más atractivos.
  - Parte 2: análisis por EF e informe con resultados y conclusiones.
- **Estructura obligatoria del informe:** portada, índice, objetivo, descripción del problema, modelo de EF (malla, condiciones de contorno, cargas…), resultados, conclusiones y bibliografía.
  - Figuras y tablas numeradas y citadas en el texto.
  - **Leyendas con unidades.** Se recomienda agrandar la leyenda de ANSYS.
  - Defensa oral de unos 10 minutos más preguntas.
- **Práctica 5:** según las instrucciones, en ella se tratan **problemas termoelásticos y dinámicos**. Por eso el estudio debe incluir temperatura y dinámica.

### 1.1 Datos del problema (Soporte 6)

| Dato | Valor | Fuente / comentario |
|---|---|---|
| Material | Acero S235: E = 210 GPa, σy = 215 MPa, ν = 0,30, ρ = 7850 kg/m³ | Tabla 1 del enunciado (usa estos valores, aunque la norma dé 235 MPa) |
| Carga | **42 258 N** | Tabla 2, caso 2. **Confirmado por el profesor el 23/11/2026** |
| Dirección | Horizontal y perpendicular al eje del bulón: **−X** en el sistema de `0.stp` | Ver la nota de abajo |
| Apoyo | Superficies cilíndricas de los 4 agujeros de los pernos, **empotradas** | «Fixed support interface», Fig. 3 del enunciado |
| Aplicación de la carga | RBE3 desde un nodo piloto, en el punto medio entre las orejetas, a las superficies de los 2 agujeros del bulón | Mismo esquema que SimJEB |
| Criterio | **CS ≥ 1,0 obligatorio**: σ von Mises ≤ 215 MPa | Decisión del grupo, con el límite del enunciado |
| Desplazamiento | ≤ 0,25 mm | Límite propio del grupo (no lo pide el enunciado) para evitar piezas blandas |

**Nota sobre la carga (explícala en el informe).** Hay una incoherencia en el enunciado:
- La Tabla 2 da para el caso 2 `Fx = 0, Fy = 0, Fz = 42 258 N`.
- La Fig. 2 dice «Horizontal 37,8 kN».
- 42 258 N es el módulo del caso diagonal (√(31 403,89² + 28 276,19²) = 42 258 N).

Se usó 37 800 N hasta que el profesor confirmó 42 258 N (23/11/2026). En el sistema de la Tabla 2, «Y» es la vertical (el caso 1, vertical, es Fy), así que Fz es horizontal. En `0.stp`, Z es vertical, Y es casi el eje del bulón y X es la horizontal perpendicular al bulón. **El modelo es lineal**: tensiones y desplazamientos escalan con la carga (comprobado: ×1,118 = 42 258/37 800).

### 1.2 Geometría fija (de `cad/agujeros_fijos.json`, en mm, sistema de `0.stp`)

**Pernos** (eje Z; superficie cilíndrica de z = 0,63 a 7,85; cara de apoyo en z ≈ 0):

| Perno | Centro (x, y) | Radio |
|---|---|---|
| 1 | (0; 0) | 5,334 |
| 2 | (52,047; 1,580) | 5,156 |
| 3 | (0; −148,125) | 5,156 |
| 4 | (38,083; −146,968) | 5,156 |

**Bulón:**
- R = 9,557; eje (−0,0304; 0,9995; 0).
- Centros (−21,357; −60,417; 44,725) y (−20,490; −88,979; 44,725).
- Nodo piloto del RBE3 en (−20,92; −74,70; 44,725).
- Fuerza = 42 258 N · (−0,99954; −0,03035; 0).
- Brazo de la carga respecto a la cara de apoyo ≈ 44,7 mm, así que el **momento de vuelco** es ≈ 42 258 × 44,7 ≈ 1,89 kN·m.

**Simetría:** el plano medio de las orejetas (normal = eje del bulón, por el nodo piloto) es plano de simetría de la pieza final.
- Los pernos 1 y 3 son simétricos entre sí.
- **Los pernos 2 y 4 no**: están desfasados en el enunciado, así que la pieza es simétrica salvo allí. El original es simétrico en ~90 % de su volumen.

---

## 2. Cómo se llegó a la pieza (lo que tienes que poder explicar)

### 2.1 El original no cumple
El soporte del enunciado (`cad/0.stp`), calculado con 42 258 N (malla tet10 de 4 mm, escalando linealmente el cálculo de 37 800 N):

| Magnitud | Valor |
|---|---|
| Masa | 2,4115 kg (CAD) / 2,4234 kg (volumen de la malla) |
| Tensión (métrica, malla de 4 mm) | **238 MPa** (CS ≈ 0,90): NO cumple |
| Tensión con malla fina | ≈ 218 MPa |
| Desplazamiento máximo | ≈ 0,145 mm |
| Pico | Fondo del alojamiento de la cabeza del perno 1, en (3,6; −9,9; 10,4) |

Por tanto, el primer paso fue **reforzar**, y después aligerar.

### 2.2 Método

**(a) Estudio de las soluciones publicadas (SimJEB).**
- SimJEB (Whalen, Beyene y Mueller, 2021; Harvard Dataverse doi:10.7910/DVN/XFUWJG) reúne los 381 diseños del concurso, en el mismo sistema de coordenadas que `0.stp`.
- Se calcularon **todos con nuestro modelo**: acero S235, 42 258 N en −X, pernos empotrados y la misma métrica.
- De ahí salieron reglas de diseño respaldadas por datos (`DESIGN_RULES.md`).
- Resultado (figura `figuras/comparativa_simjeb.png`, datos en `estudio/comparativa_simjeb.csv`):

| Resultado | Diseños |
|---|---|
| Cumplen (σ ≤ 215 MPa y u ≤ 0,25 mm) | **16** |
| No cumplen | 281 (227 descartados en una pasada rápida con malla de 6 mm al superar 1,5 veces el límite); ninguno falla solo por desplazamiento |
| Incompatibles (sin los agujeros del enunciado) | 50 |
| Geometría no mallable | 34 |

- **Nuestra pieza es la 2.ª más ligera de las 17 que cumplen.** El diseño publicado más ligero que cumple es el **n.º 237** (categoría *block*, autor «Bol»): **1,975 kg, 183,5 MPa, 0,140 mm** (imagen en `estudio/img/simjeb_237.png`).
  - Su topología es distinta: base en **arco** abierto por debajo entre los pares de pernos, y una sola placa-cartela de las orejetas a la base.
  - Analiza por qué es más ligero y qué nos impide llegar ahí partiendo del original con operaciones de quitar/añadir.
- Siguientes en masa: n.º 474 (2,236 kg, 197,3 MPa), n.º 475 (2,241 kg, 211,9 MPa) y n.º 527 (2,272 kg, 194,9 MPa).
- Ojo: los diseños SimJEB se hicieron para titanio y 4 casos de carga; aquí se evalúan en acero y solo con el caso 2.

**(b) Optimizador guiado por reglas** (`scripts/optimizer.py`, `scripts/reglas.py`, `scripts/operaciones.py`, `scripts/campo.py`).
- Parte del original y lo modifica **paso a paso**. La pieza es siempre «0.stp + lista de operaciones».
- En cada iteración:
  1. lee el campo de tensiones: material ocioso, pico, direcciones principales;
  2. propone cambios, cada uno con su regla y su porqué;
  3. los evalúa en ANSYS;
  4. **acepta** si cumple y baja la masa; si no, **revierte** y anota el motivo.
- Objetivo: **solo la masa**; la tensión y el desplazamiento son límites obligatorios.
- **Reglas principales:**
  - R1: aligeramiento pasante donde toda la columna trabaja por debajo de un umbral.
  - R2: rebaje desde arriba.
  - R3: hueco interior.
  - R4: collar en un perno.
  - R7: anillo de las orejetas.
  - R8: reducir un corte que tocaba el pico.
  - R12: acampanar los collares.
  - R14: bolsillo desde la cara de apoyo con techo a 45°.
  - R18: agrandar una forma pura existente.
- El umbral de «material ocioso» sube por pasos: 15 → 25 → 35 → 45 % del límite.
- **Restricciones de las operaciones:**
  - Nunca entran en las zonas protegidas: alojamiento del perno + 3 mm, y radio del bulón + 6 mm en las orejetas.
  - No salen del volumen del original.
  - Techos a 45° y sin cavidades cerradas (fabricación aditiva).
  - **Simetría obligatoria**: cada operación se aplica también en su simétrica.
- **Verificación:** cada mejora ≥ 1 % se recalcula con **malla fina** (3,5 mm). Para aceptar una pieza se exige σ(malla 4 mm) × k ≤ 215 MPa, donde k es el cociente fina/normal medido (~1,04-1,08).
- **Formas puras (24/11/2026):** al final, el vaciado irregular de la mejor pieza (23 operaciones, 2,0776 kg, 195,2 MPa) se sustituyó por **formas geométricas puras inscritas** en lo ya vaciado: círculos, ranuras y bolsillos en ranura, sin paredes de menos de 4 mm. El objetivo era facilitar la fabricación. Eso costó +110 g; la R18 recuperó 32 g agrandando esas formas (it. 72, 74 y 77).

### 2.3 La pieza final: iteración 77 (verificada con malla fina)

| Magnitud | Malla 4 mm (96 353 nodos) | Malla fina 3,5 mm (120 608 nodos) |
|---|---|---|
| Masa | 2,1556 kg (volumen de la malla); **2,1381 kg (CAD)** | ídem |
| σ von Mises (métrica) | 193,7 MPa en (−0,20; −58,50; 57,14) | **209,4 MPa** en (−0,18; −87,09; 57,38) |
| CS = 215/σ | 1,110 | **1,027** |
| u máx | 0,159 mm (ux 0,134; uy 0,014; uz 0,112) | 0,166 mm |
| Error de equilibrio de reacciones | < 10⁻⁶ % | — |

- Reducción de masa respecto al original: **−11,3 %** (CAD: 2,4115 → 2,1381 kg) o −11,1 % (malla: 2,4234 → 2,1556 kg).
- **Historia de esta pieza:**
  - El optimizador aceptó la it. 77 el 24/11, pero no la comprobó con malla fina porque bajaba la masa menos de un 1 %.
  - La siguiente (it. 78, 2,1263 kg) no pasó la malla fina por 0,1 MPa (215,1 MPa). Al deshacerla se volvió al último hito verificado, la it. 72 (2,1614 kg, 209,2 MPa con malla fina), y se perdieron también las it. 74 y 77.
  - El 28/11 se reconstruyó la 77 y se comprobó aparte: con malla normal reproduce exactamente 2,1556 kg y 193,7 MPa, y con malla fina da 209,4 MPa. **Cumple**, así que es el hito 17.
  - Los archivos de la it. 72 siguen en `historial/16_it072_2.161kg/` por si se quieren comparar.
- El pico está en **la unión de la orejeta con el cuerpo** (z ≈ 57), en una orejeta o en su simétrica según la malla.
  - Es **flexión** (concentración de tensiones ×1,6).
  - Refinar el acuerdo no lo resolvía; necesita más canto.
- Workbench (proyecto ya resuelto, malla por defecto, 78 156 nodos): u máx 0,1621 mm; σ máx bruta 605 MPa, que es la singularidad del borde del perno empotrado (ver §2.5).

**Las 14 operaciones sobre el original y su porqué:**
- «(y su simétrica)» = también se aplica en el lado simétrico respecto al plano de las orejetas.
- «it.» = iteración del optimizador; el detalle está en `runs/opt_42258N/ITERACIONES.md`.
- Las formas 5 a 14 son las formas puras que sustituyeron a los cortes de las iteraciones indicadas.

| # | Operación | Por qué (regla, mecánica y datos) |
|---|---|---|
| 1-2 | **Collar de 6 mm** alrededor de los pernos 1 y 3, hasta z = 22 mm, **acampanado a 30°** hasta z = 16 mm | **Refuerzo** (R4 + R12).<br>• El pico del original estaba en el fondo del alojamiento del perno 1: el momento de vuelco F·h se transmite por la sección que rodea a los pernos delanteros.<br>• Prueba directa: collares de 6 mm bajan el pico de 238 a 203 MPa (−15 %) con +159 g.<br>• Pieza simétrica de partida (original + collares): 2,5044 kg, 201,9 MPa.<br>• El cilindro dejaba una esquina viva en su unión con el cuerpo. Acampanarlo a 30° (it. 31/37) bajó el pico de 202,1 a 190,7 MPa (−5,6 %) con +52 g. Ese margen se «gastó» después aligerando.<br>• Collares de 8-9 mm (it. 9, 15) no mejoran (9 mm: sube a 207 MPa).<br>• Collares en los pernos 2 y 4 (it. 60, 61, 75, 76): cumplen pero pesan más sin hacer falta. |
| 3 | **Rebaje desde arriba** hasta z = 9 mm en x 40…64, y −82…−66 (esquinas R3) (y su simétrica) | R2 (it. 2, en x 42…62, y −80…−68).<br>• Todo el material por encima de z = 9 en esa zona trabajaba por debajo del 15 % del límite: ni el momento de vuelco ni el cortante pasan por ahí.<br>• 2,5044 → 2,4822 kg; 201,9 → 200,9 MPa.<br>R18 (it. 77): ampliado 2 mm por cada lado; el borde que se quitaba trabajaba como máximo al 69 % del límite.<br>• 2,1581 → 2,1556 kg; 198,0 → 193,7 MPa. |
| 4 | **Anillo de las orejetas** hasta radio 20,1 mm (ligamento de 10,5 mm delante del bulón) | **Refuerzo** (R7, it. 39).<br>• El pico pasó a la orejeta. Había 7,5 mm de ligamento, igual que la mediana de los 16 diseños SimJEB válidos (7,6 mm). La tensión de aplastamiento y cortadura va como ~1/e.<br>• +15 g; 202,2 → 193,8 MPa (−4,2 %).<br>• Seguir creciendo a 23,1 mm **empeora** (it. 58 y 73: 208 y 204 MPa). Explícalo: rigidiza la orejeta y lleva más carga a la unión orejeta-cuerpo, que trabaja a flexión. |
| 5 | **Ranura** de (42; −79) a (42; −67), r = 11,5 (y su simétrica) | Sustituye al grupo central de aligeramientos R1 de las it. 3, 35, 41, 55, 57 y 59: D16 en (49; −56) y (37; −62), D20 en (43; −68), D12 en (34; −77).<br>• Cada columna trabajaba por debajo del 25-45 % del límite: no está en el camino de la carga, y con Kt ≈ 3 (Kirsch) el borde queda bajo el límite.<br>• En la it. 55 se **redujo** (R8) el D16 de (49; −56) porque el pico estaba en su borde: ese material sí trabajaba. |
| 6 | **Ranura** de (26; −72) a (18; −76), r = 4 (y su simétrica) | Sustituye a D10 en (28; −74) y D10 en (19; −74) (it. 7 y 8): columnas por debajo del 25 % del límite. |
| 7 | **Agujero pasante D16** en (−26; −29) (y su simétrico) | R1 (it. 6).<br>• Columna por debajo del 25 % del límite; el pico estaba a 121 mm.<br>• 2,3827 → 2,3552 kg. |
| 8 | **Agujero pasante D13** en (4; −74), sobre el plano de simetría | R1 (it. 4).<br>• Columna por debajo del 23 %; pico a 82 mm.<br>• Era D12; la conversión a formas puras lo dejó en D13. |
| 9 | **Agujero pasante D13** en (4; −110) (y su simétrico) | R1 (it. 66, D10): columna por debajo del 41 % del límite.<br>R18 (it. 72): el material que se quitaba al agrandarlo trabajaba como máximo al 62 % del límite.<br>• 2,1876 → 2,1614 kg; 193,7 → 196,7 MPa. |
| 10 | **Agujero pasante D8** en (43; −44) (y su simétrico) | R1 (it. 11): columna por debajo del 34 %. |
| 11 | **Bolsillo en ranura desde la cara de apoyo**, 21 mm de ancho, de (13; −54) a (7; −35), hasta z = 11, techo a 45° (y su simétrico) | Sustituye a los bolsillos R14 de las it. 18 y 47 y al hueco interior R3 de la it. 43.<br>• **El soporte solo se sujeta por los pernos**: la placa base bajo el cuerpo no lleva carga aunque el cuerpo de encima sí.<br>• Placa base del original (z < 10 mm): 67 cm³ con un 77 % de material ocioso. En la mitad más ligera de los SimJEB válidos: mediana de 45 cm³. |
| 12 | **Bolsillo en ranura**, 15 mm de ancho, de (23; −27) a (56; −28), hasta z = 6 (y su simétrico) | Sustituye al bolsillo R14 de 56 × 16 mm de la it. 52 (material por debajo del 45 % del límite). |
| 13 | **Bolsillo en ranura**, 8 mm de ancho, de (23; −38) a (29; −61), hasta z = 6 (y su simétrico) | Sustituye a los bolsillos R14 de las it. 19, 20, 38 y 42 y a sus simétricos. Misma razón que el 11. |
| 14 | **Bolsillo en ranura**, 30 mm de ancho, de (−31; −94) a (−33; −57), hasta z = 12 (y su simétrico) | R14 (it. 68): material bajo las orejetas, del lado de la carga, por debajo del 45 % del límite. En formas puras quedó de 27 mm.<br>R18 (it. 74): ensanchado a 30 mm; el borde que se quitaba trabajaba como máximo al 40 % del límite.<br>• 2,1614 → 2,1581 kg; 196,7 → 198,0 MPa. |

Las coordenadas exactas (incluidos radios) están en `runs/opt_42258N/historial/17_it077_2.156kg/operaciones.json`.

**¿Y los nervios?** La regla R11 crea nervios en la dirección de las tensiones principales (Michell): se quita un bloque que trabaja poco y se ponen nervios. Se probó **9 veces y ninguna mejoró** la pieza, así que la regla quedó suspendida. **La pieza final no tiene nervios nuevos.** Los refuerzos son collares, acampanado y anillo. Explica por qué tiene sentido: la pieza original ya tiene una cartela y almas en la dirección de la carga, y lo que sobraba era placa base y material fuera de ese camino.

### 2.4 Lo que se intentó y se rechazó (demuestra dónde va la carga)

| It. | Cambio | Resultado | Lectura |
|---|---|---|---|
| 36, 56 | Agujero D12 en (−17; −74), entre las orejetas | **600 MPa** / 220 MPa | Es el alma que une las orejetas con la base: camino principal de la carga |
| 45 | Agujero D24 en (4; −32) | **594 MPa** | Corta la cartela que va de la orejeta al perno 1 |
| 62, 64 | Rebaje hasta z = 9 / z = 5 en x −9…11, y −44…−24 | **331 / 333 MPa** | Misma cartela diagonal orejeta → perno 1 (y su simétrica → perno 3) |
| 63 | Rebaje hasta z = 5 en x −1…15, y −120…−104 | 294 MPa | Cartela hacia el perno 3 |
| 46 | Agujero D20 en (7; −116) | 292 MPa | Ídem |
| 51 | Agujero D10 en (37; −86) | 249 MPa | Material junto al camino hacia los pernos traseros |
| 1, 12, 13, 14, 21, 24-28, 48, 49, 53, 54, 65 | Aligeramientos pequeños | 202-210 MPa con malla de 4 mm; tras corregir a malla fina, 216-226 MPa | Al límite: no cumplen por poco tras la corrección a malla fina |
| 78 | Agrandar la ranura n.º 5 (R18) | 2,1263 kg, 198,5 MPa con malla de 4 mm, pero **215,1 MPa con malla fina** | Rechazada por 0,1 MPa: la ranura central ya está en su tamaño máximo. (La it. 77, anterior, se recuperó después; ver §2.3) |
| 73 | Anillo de las orejetas a radio 23,1 mm | 204,4 MPa (sube) | Más anillo rigidiza la orejeta y lleva más carga a la unión orejeta-cuerpo |

### 2.5 Decisiones de modelo que debes discutir en el informe

- **Métrica de tensión** (`scripts/fem.py`, `stress_metric`): máximo de von Mises excluyendo los nodos a menos de **5 mm** de cada agujero de perno (en el tramo z del agujero ± 5 mm) y a menos de **2 mm** de la superficie del bulón (esquinas del RBE3).
  - Motivo: el borde del agujero empotrado es una **singularidad**: su tensión no converge al refinar (bruto 920 MPa con malla de 4 mm y 895 MPa con la fina; el máximo bruto salta de un nodo a otro según la malla).
  - Hipótesis física: 5 mm ≈ zona de apoyo de una arandela de M10 (diámetro exterior 20 mm según ISO 7089; **verifícalo**).
  - **Sensibilidad (pieza final; malla 4 mm / malla fina):**

| Exclusión | Malla 4 mm | Malla fina |
|---|---|---|
| Sin exclusión | 920 MPa | 895 MPa |
| Pernos 3 mm, bulón 0 mm | 317 MPa | 302 MPa |
| Pernos 3 mm, bulón 2 mm | **253 MPa** | **271 MPa** |
| Pernos 5 mm, bulón 2 mm (la usada) | 193,7 MPa | 209,4 MPa |

  - **Es el punto débil del modelo:** entre 3 y 5 mm de los pernos hay hasta 271 MPa. Hay que estudiarlo con un modelo de tornillo realista: contacto bajo cabeza o arandela, precarga, apoyo solo a compresión en la cara inferior. Así se ve si esa tensión es real o un artefacto del empotramiento.
  - Lo mismo con el bulón: modelo de contacto bulón-orejeta en vez de RBE3.
- **Malla:** tetraedros de 2.º orden SOLID187 generados con gmsh.
  - Rápida h = 6 mm, normal h = 4 mm, fina h = 3,5 mm.
  - El cociente fina/normal en el pico ha sido de 1,04-1,08; para la pieza final, 209,4/193,7 = **1,081**.
  - **No hay convergencia demostrada.** Con CS = 1,027 en la malla fina, el margen es pequeño.
  - Validación del montaje con una viga en voladizo: flecha con un 0,02 % de error.
- **Simetría impuesta, fabricación aditiva y formas puras:** son decisiones de diseño del grupo, no exigencias del enunciado.

---

## 3. Archivos (raíz: `C:\Users\hugof\Desktop\Universidad\MSD\Trabajo`)

| Qué | Dónde |
|---|---|
| **Pieza final** (STEP, operaciones, métricas, imágenes, modelo APDL completo) | `runs/opt_42258N/historial/17_it077_2.156kg/`<br>`geometria.step`, `operaciones.json`, `metrics.json`, `resumen.png`, `vonmises.png`, `modelo_apdl.zip` (`model.inp` con malla, RBE3, empotramiento y carga; el parámetro `FUERZA` está al final) |
| **Proyecto Workbench** de la pieza final (ya resuelto) | `runs/opt_42258N/historial/17_it077_2.156kg/workbench/soporte_it077.wbpj` (y `.wbpz`) |
| Campos de resultados (nodos, tets, von Mises, desplazamientos y tensor completo SX…SXZ) | `runs/opt_42258N/iteraciones/077/reverificada/completa/` (`campos.npz`, `res_nod.txt`, `res_comp.txt`, `model.inp`) y malla fina en `.../077/reverificada/verificacion/`<br>Resumen: `.../077/reverificada/verificacion_resultado.json` |
| Pieza anterior (it. 72), por si se compara | `runs/opt_42258N/historial/16_it072_2.161kg/` |
| Original | `cad/0.stp` (**no modificar**); resultados de referencia (37 800 N) en `cad/referencia_original/` |
| Geometría fija | `cad/agujeros_fijos.json` |
| Historia completa, iteración a iteración (regla, porqué, previsión, antes/después, decisión) | `runs/opt_42258N/ITERACIONES.md`, `runs/opt_42258N/registro.csv`, `runs/opt_42258N/estado.json` (solo lectura) |
| Hitos verificados con malla fina y Workbench | `runs/opt_42258N/historial/` y `HISTORIAL.md` |
| Galería de fichas de cada iteración | `runs/opt_42258N/galeria/` |
| Reglas de diseño con evidencia y estadísticas | `DESIGN_RULES.md` |
| Documentación y bitácora | `DOCUMENTACION.md`, `bitacora.md`, `ESTADO.md`, `docs/parte1.md` (SimJEB), `docs/fabricacion_aditiva.md` |
| Estudio SimJEB | `estudio/estudio_simjeb.json` / `.csv`, `estudio/comparativa_simjeb.csv`, `estudio/caracteristicas.json`, `estudio/img/` |
| Figura de la comparativa | `figuras/comparativa_simjeb.png` (generada con `scripts/grafica_simjeb.py`) |
| Convergencia del original (fase 2) | `figuras/fase2_*.png` y `bitacora.md` |
| **STEP de los 381 diseños publicados** y sus metadatos | `datos_simjeb/stp/<id>.stp` (p. ej. `237.stp`), `datos_simjeb/metadata.tab`, `datos_simjeb/README.txt` (no se sube a GitHub) |
| Nuestro cálculo de cada diseño publicado (campos, métricas, imagen) | `datos_simjeb/estudio/<id>/` (`campos.npz`, `metrics.json`, `vonmises.png`) |
| Pieza con el vaciado irregular (it. 68, antes de las formas puras) | `runs/opt_42258N/historial/14_it068_2.078kg/` |
| Enfoques anteriores, solo como historia (37 800 N por familias; 42 258 N sin simetría) | `runs/archivo/` (**no** sirven para la pieza final) |

### 3.1 Cómo está organizado

```
Trabajo/
├── cad/                 0.stp (original, NO tocar), agujeros_fijos.json, referencia_original/
├── config.json          carga, límites, mallas, simetría, formas puras (lo lee todo el código)
├── scripts/             código (ver abajo)
├── estudio/             estudio SimJEB: tablas, características, evidencia de las reglas, img/
├── datos_simjeb/        381 STEP de SimJEB + nuestro cálculo de cada uno (estudio/<id>/)
├── figuras/             figuras generales (comparativa SimJEB, convergencia del original)
├── docs/                parte 1 (SimJEB), fabricación aditiva, este prompt
├── runs/opt_42258N/     el optimizador actual (carga 42 258 N)
│   ├── estado.json        estado completo (mejor, actual, rechazos, historia): SOLO LECTURA
│   ├── ITERACIONES.md     cada iteración explicada; registro.csv (una fila por iteración)
│   ├── historial/         HITOS verificados con malla fina: NN_itXXX_masa/ con STEP, operaciones, métricas, fichas, modelo APDL y workbench/
│   ├── iteraciones/NNN/   cada iteración: completa/ (cálculo con malla de 4 mm), candK_rapida/ y actual_rapida/ (malla de 6 mm)
│   ├── galeria/, fotos/   fichas de cada cálculo (geometría | von Mises | deformada | radiografía)
│   └── MEJOR_GLOBAL.json  resumen del mejor diseño
└── estudio_final/       (lo creas tú) tu trabajo
```

- **Limpieza de iteraciones:** en las iteraciones antiguas el optimizador borra los archivos pesados (`campos.npz`, `res_*.txt`, `model.inp`). Los cálculos completos de la pieza final están en `iteraciones/077/reverificada/`; para cualquier otra, reconstrúyela desde su lista de operaciones.
- **Contenido de `campos.npz`** (numpy), mm y MPa:
  - `nodes` (N × 3);
  - `tets4` (vértices de cada tetraedro, índices desde 0);
  - `tris` (triángulos de superficie de 6 nodos, índices desde 1);
  - `vm` (von Mises nodal; los nodos intermedios de SOLID187 valen 0);
  - `u` (desplazamientos, N × 3);
  - `sig6` (SX, SY, SZ, SXY, SYZ, SXZ por nodo).
- **Contenido de `metrics.json`:**
  - masa CAD y de la malla;
  - reacciones y error de equilibrio;
  - `vm_metric` y su posición;
  - máximo bruto;
  - sensibilidad a la exclusión (`vm_ex_bX_pY`: X mm alrededor de los pernos, Y mm alrededor del bulón);
  - `u_max` y sus componentes;
  - nodos, elementos y tiempos.
- **Scripts útiles:**

| Script | Para qué |
|---|---|
| `operaciones.py` | Construye una pieza desde el 0.stp y una lista de operaciones; `describe(op)` la explica en texto. |
| `evaluate.py` | Geometría → malla gmsh → MAPDL → métricas e imágenes. |
| `fem.py` | Escribe el `model.inp` (SOLID187, RBE3, empotramiento, carga) y define la métrica (`stress_metric`). |
| `campo.py` | Análisis del campo: material ocioso, zonas, pico, direcciones principales y camino de la carga. |
| `verificar_diseno.py ops.json carpeta` | Calcula un diseño con malla normal y fina. |
| `exportar_workbench.py` | Crea un proyecto de Workbench desde un STEP. |
| `estudio_simjeb.py` | Calcula diseños de SimJEB con nuestras condiciones. |
| `grafica_simjeb.py` | La figura comparativa. |
| `render.py` | Las fichas de cada pieza. |

**Herramientas:**
- **ANSYS Student 2026 R1:**
  - MAPDL: `"C:\Program Files\ANSYS Inc\ANSYS Student\v261\ansys\bin\winx64\MAPDL.exe" -b -p ansys -i model.inp -o salida.out`. **Sin `-p ansys` falla la licencia.**
  - Workbench: `RunWB2.exe` en `...\v261\Framework\bin\Win64\`.
  - **Límite de 128 000 nodos. Solo una sesión de ANSYS a la vez**: cierra Workbench antes de lanzar MAPDL.
- **Python:** `.venv` del proyecto (cadquery, gmsh, numpy, scipy, pyvista, matplotlib, shapely).
  - `operaciones.build(ops)` reconstruye la pieza desde `0.stp` y la lista de operaciones.
  - `evaluate.evaluate(...)` malla, calcula en MAPDL y saca métricas e imágenes.
  - En Windows, ejecútalos **desde un archivo .py**, no por stdin, porque usan multiprocessing.

---

## 4. El estudio que tienes que hacer

Haz todo lo que puedas de esta lista, en este orden de prioridad. Para cada apartado: qué se calcula, cómo (modelo, malla, condiciones), resultados con figuras y tablas, e **interpretación física**.

### A. Comprobación del modelo y convergencia (lo primero: de esto depende el «cumple»)
1. Reproduce el resultado de la pieza final (193,7 / 209,4 MPa; 0,159 / 0,166 mm) con el `model.inp` y con Workbench, y explica las diferencias.
2. **Estudio de convergencia de malla** en el pico (unión orejeta-cuerpo, z ≈ 57).
   - Refinamiento local (sizing de cara o arista en el acuerdo de la unión, el fondo de los alojamientos y el borde de los aligeramientos) dentro del límite de 128 000 nodos.
   - Si hace falta, **submodelo**.
   - Representa σ frente a tamaño de elemento o número de nodos y extrapola (Richardson).
   - **Concluye si el pico convergido es ≤ 215 MPa.** Si no lo es, dilo claramente y cuantifica cuánto material o qué cambio haría falta.
3. **Sensibilidad a la exclusión de la métrica** (tabla de §2.5) y **singularidades**: explica por qué el valor en el borde del empotramiento no es físico (Saint-Venant, singularidad de la condición de contorno). Muestra con 3-4 mallas que diverge.
4. **Modelo de apoyo realista.**
   - Pernos M10 con contacto bajo cabeza o arandela, cara inferior apoyada solo a compresión y precarga razonable (justificada y citada).
   - Bulón con contacto en lugar de RBE3.
   - Compara tensiones, desplazamientos y reacciones con el modelo empotrado. Esto decide si los 253-271 MPa a 3-5 mm de los pernos son reales.

### B. Cómo carga la pieza (análisis estático detallado, caso 2)
1. **Cálculo a mano:**
   - cortante de 42 258 N y momento de vuelco ≈ 1,89 kN·m;
   - reparto entre pernos delanteros (1, 3) y traseros (2, 4): tracción/compresión y cortante;
   - orejeta según la teoría clásica de orejetas: tracción en la sección neta, desgarro (*shear-out*), aplastamiento con e/D y espesor.
   Compáralo con el MEF.
2. **Reacciones en cada perno** desde el MEF (FSUM por grupo de nodos de cada agujero: Fx, Fy, Fz y momentos). ¿Qué perno trabaja más y por qué? Comprueba la capacidad de un M10 (clase supuesta y justificada).
3. **Mapas** (con leyendas grandes y unidades) de:
   - von Mises;
   - tensiones principales σ1 y σ3: **zonas a tracción y a compresión**;
   - **vectores de tensiones principales**: camino de la carga;
   - deformación unitaria equivalente;
   - desplazamientos total y por componentes, con la deformada amplificada.
4. **Recorrido de la carga:** de las orejetas por la cartela y las almas a los pernos. Usa los vectores principales y relaciónalo con §2.4 (los cortes rechazados por 300-600 MPa son justo ese camino). Explica por qué la placa base bajo el cuerpo apenas trabaja y por eso se vació.
5. **Material ocioso:** histograma de volumen por nivel de tensión (% del límite), original frente a final. Cuánto material queda por debajo del 15 %, 25 %… y dónde está.
6. **Para cada uno de los 14 rasgos de la tabla de §2.3:** tensión que soporta hoy el material de su borde y cuánto margen queda. Así se justifica con el resultado final, además de con la historia.
7. **Comparación original ↔ final** con la misma malla y la misma carga: masa, pico, ubicación del pico, rigidez (u y F/u) y distribución de tensiones.

### C. Temperatura (termoelasticidad: práctica 5)
Define y **justifica** un rango de temperaturas de servicio. Por ejemplo, de −40 °C (exterior en vuelo o en invierno) a la temperatura cercana a un motor que consideres razonable. Es una hipótesis: dilo. Estudia:
1. **Propiedades del S235 con la temperatura.**
   - E(T), límite de proporcionalidad y límite elástico.
   - Fuente recomendada: EN 1993-1-2, tabla 3.1 (factores k_E,θ, k_p,θ, k_y,θ). Cítala y explica que es una norma de cálculo frente a incendio.
   - α = 12·10⁻⁶ K⁻¹ (EN 1993-1-1, §3.2.6; verifícalo).
   - Recalcula **CS(T)** y u(T). Con cargas impuestas y apoyos fijos, las tensiones apenas dependen de E (solo de ν) y los desplazamientos van como 1/E. Demuéstralo numéricamente.
2. **Dilatación libre uniforme:** sin tensiones. Compruébalo en ANSYS como validación.
3. **Dilatación impedida:** la base (el motor) y el soporte a distinta temperatura, con los pernos fijos. Calcula las tensiones térmicas (orden de magnitud: E·α·ΔT ≈ 2,5 MPa/K) y su **combinación con la carga mecánica**. ¿A partir de qué ΔT deja de cumplir?
4. **Gradiente térmico:** análisis térmico estacionario (por ejemplo, base caliente y orejetas a temperatura ambiente) acoplado al estructural (Workbench: Steady-State Thermal → Static Structural). Tensiones y deformada resultantes.
5. **Baja temperatura:** fragilidad del S235 (grados JR/J0/J2 y temperatura del ensayo Charpy). Recomendación de grado si la pieza trabaja en frío.

### D. Dinámica (práctica 5)
1. **Análisis modal libre y con los pernos fijos:** primeras 6-10 frecuencias y formas modales, original frente a final. ¿Ha bajado la frecuencia fundamental al aligerar?
2. Comenta el riesgo de resonancia con las frecuencias de excitación de un motor o de la elevación (hipótesis justificada) y, si te da tiempo, un **armónico** o un **impulso** (carga aplicada de golpe: factor dinámico ≈ 2 en un sistema de 1 GDL).

### E. Otros (si te da tiempo; márcalos como complementarios)
1. **Pandeo lineal** de las almas y paredes finas bajo la carga del caso 2 (factor de carga crítico).
2. **Fatiga:** si la carga se repite (ciclos de elevación), Goodman o Soderberg con un Se estimado (Shigley) en la zona del pico. Indica que no es un requisito del enunciado.
3. **Los otros 3 casos de carga** del enunciado (vertical, diagonal y torsión) aplicados a la pieza final, solo como información. **La pieza se diseñó solo para el caso 2**; no la penalices por los demás, pero di qué pasaría.
4. **Fabricación:** formas puras (círculos, ranuras, bolsillos en ranura), techos a 45°, sin cavidades cerradas y paredes ≥ 4 mm. Discute la fabricación aditiva frente al mecanizado con estas formas.
5. **SimJEB n.º 237:** calcúlalo con malla fina y analiza su topología frente a la nuestra. ¿Qué aprendemos para una siguiente versión?

---

## 5. Advertencias (cosas que ya sabemos)

- La pieza final cumple con **CS = 1,027 en malla fina**, un margen pequeño. Sin un estudio de convergencia, el «cumple» no está demostrado (§A.2).
- La métrica depende de la exclusión de 5 mm alrededor de los pernos; con 3 mm, la pieza **no cumpliría** (253-271 MPa) (§A.3-A.4).
- La masa «de malla» (2,1556 kg) es ~0,8 % mayor que la del CAD (2,1381 kg). En el informe, usa la del CAD para la pieza y explica que la gráfica SimJEB usa la de malla para todos (comparación homogénea).
- La incoherencia de la carga del enunciado (§1.1).
- Los pernos 2 y 4 no son simétricos: la pieza es simétrica salvo allí.
- En `runs/opt_42258N/` existe un `EN_EJECUCION.lock` antiguo: el optimizador **no** está en marcha. Aun así, no lances ANSYS si ves un `python.exe` del optimizador corriendo.

## 6. Normas de trabajo

- **No modifiques** `cad/0.stp`, los PDF del enunciado ni nada de `runs/` (son datos). Trabaja en una carpeta nueva: `Trabajo/estudio_final/`, con subcarpetas `modelos/`, `resultados/`, `figuras/` y `scripts/`.
- **No inventes nada.** Cada valor sale de un cálculo reproducible (guarda los scripts y los `.inp`) o de una referencia citada (autor, título, año, norma y apartado). Separa claramente resultado, hipótesis y opinión.
- Las ejecuciones largas, en una **consola visible** con el progreso y con log en disco.
- Una sola sesión de ANSYS a la vez y respeta el límite de 128 000 nodos.
- `discord_webhooks.json` contiene secretos: no lo leas, no lo imprimas, no lo subas. No envíes datos personales a servicios externos.
- Si subes algo al repositorio Git del proyecto (privado), que sea solo `estudio_final/`. Nunca `datos_simjeb/` ni `discord_webhooks.json`.

## 7. Entregables

1. **`estudio_final/ESTUDIO_PIEZA_FINAL.md`**, y su versión **.docx**, con esta estructura:
   1. Resumen ejecutivo (1 página: qué es la pieza, cuánto pesa, si cumple y con qué margen, y las 5 conclusiones clave).
   2. Objetivo y descripción del problema (datos de §1, incluida la nota de la carga).
   3. Antecedentes: el original no cumple; estudio SimJEB y figura comparativa; método de optimización por reglas.
   4. Modelo de EF: geometría, material, malla, condiciones de contorno, carga y métrica. Validación y convergencia.
   5. Resultados del caso 2: mapas, reacciones, camino de la carga, material ocioso y cálculo a mano.
   6. **Justificación de la geometría:** cada rasgo de la tabla de §2.3 con su porqué (historia y comprobación con el resultado final) y lo que se rechazó (§2.4).
   7. Sensibilidad: apoyos realistas, exclusión de la métrica, malla.
   8. Temperatura.
   9. Dinámica.
   10. Complementarios (pandeo, fatiga, otros casos, fabricación, SimJEB 237).
   11. Conclusiones y propuestas de mejora (con números).
   12. Bibliografía.
2. Figuras numeradas en `estudio_final/figuras/` (PNG ≥ 150 ppp, leyendas con unidades y legibles).
3. Tablas de datos (CSV) y scripts y modelos reproducibles.
4. Una **lista de 8-10 preguntas probables de la defensa** con su respuesta corta y basada en los resultados.

Antes de empezar los cálculos, presenta un **plan breve**: qué análisis harás, con qué herramienta y en qué orden. Después ejecútalo y ve informando de los resultados parciales.
