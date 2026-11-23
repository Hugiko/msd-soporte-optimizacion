# Reglas de diseno del soporte (DESIGN_RULES)

Actualizado: 23/11/2026 22:41. Generado por `scripts/reglas.py` a partir de:

1. **Estudio de las soluciones publicadas** (SimJEB: los 381 disenos del GE Jet Engine Bracket Challenge, Whalen et al. 2021, doi:10.7910/DVN/XFUWJG) calculados con **nuestra** carga (42258 N en -X por el bulon, pernos empotrados) y **nuestro** limite (215 MPa, coef. de seguridad >= 1; desplazamiento <= 0.25 mm). Resultados: `estudio/estudio_simjeb.json`.
2. **Nuestros calculos anteriores** (familias vaciado y refuerzo, 294 disenos con 37 800 N; el modelo es lineal y se escalan x1.118). Datos: `estudio/calculos_anteriores.csv`.
3. **Lo que pasa al aplicarlas** en el optimizador (cada aplicacion: tension y masa antes/despues). Una regla que los datos de un cambio DIRECTO contradicen se DESACTIVA (las comparaciones con SimJEB, entre disenos distintos, pueden respaldarla o ser no concluyentes, pero no la desactivan); una que falla 8 veces sin ninguna mejora en el optimizador se SUSPENDE.

## Estudio de las soluciones publicadas

381 disenos calculados: **16 cumplen**, 281 no cumplen, 50 no tienen los agujeros del enunciado (bulon macizo o agujeros de otro tamano), 34 fallaron (malla). Los que superaban 1,5 veces el limite en la pasada rapida (malla gruesa) se descartaron sin calculo fino.

Los mas ligeros que cumplen (son la referencia de lo que se puede conseguir; NO se copian: la pieza final sale del original modificado paso a paso):

| SimJEB | masa | tension | desplaz. | tipo | material ocioso | pico en |
|---|---|---|---|---|---|---|
| 237 (Bol) | 1.975 kg | 183 MPa | 0.140 mm | block | 24 % | orejetas del bulon |
| 474 (Kiran Kumar A) | 2.236 kg | 197 MPa | 0.126 mm | block | 30 % | orejetas del bulon |
| 475 (Kiran Kumar A) | 2.241 kg | 212 MPa | 0.130 mm | block | 33 % | cuerpo, lado trasero (x >= 15 mm) |
| 527 (NIKHIL KHOBRAGADE) | 2.272 kg | 195 MPa | 0.128 mm | block | 34 % | orejetas del bulon |
| 476 (Kiran Kumar A) | 2.412 kg | 197 MPa | 0.122 mm | block | 37 % | orejetas del bulon |
| 538 (A0I0A) | 2.433 kg | 172 MPa | 0.134 mm | block | 34 % | orejetas del bulon |
| 537 (A0I0A) | 2.434 kg | 175 MPa | 0.133 mm | block | 34 % | orejetas del bulon |
| 86 (riyosketch) | 2.464 kg | 170 MPa | 0.132 mm | block | 32 % | orejetas del bulon |
| 211 (Michael Waugh) | 2.542 kg | 198 MPa | 0.155 mm | block | 35 % | alrededor de los pernos traseros |
| 180 (Tomek F.) | 2.570 kg | 195 MPa | 0.148 mm | block | 30 % | orejetas del bulon |
| 403 (Rafael) | 2.593 kg | 175 MPa | 0.119 mm | block | 42 % | orejetas del bulon |
| 233 (Farandy Angesti Liong) | 2.801 kg | 174 MPa | 0.138 mm | block | 43 % | alrededor de los pernos traseros |

<img src="estudio/img/simjeb_237.png" width="260" title="SimJEB 237"> <img src="estudio/img/simjeb_474.png" width="260" title="SimJEB 474"> <img src="estudio/img/simjeb_475.png" width="260" title="SimJEB 475"> <img src="estudio/img/simjeb_527.png" width="260" title="SimJEB 527"> <img src="estudio/img/simjeb_476.png" width="260" title="SimJEB 476"> <img src="estudio/img/simjeb_538.png" width="260" title="SimJEB 538">

## Reglas

### R1. Aligeramiento pasante donde toda la columna de material esta ociosa  (ACTIVA)

- **Si:** toda la columna vertical (radio del agujero + 3 mm de margen) trabaja por debajo del umbral de material ocioso.
- **Hago:** agujero vertical pasante; paredes verticales (imprimible sin soportes); nunca en las zonas protegidas.
- **Porque:** ese material no esta en el camino de la carga (bulon -> orejetas -> cuerpo -> pernos). Un agujero en una zona a tension s multiplica la tension en su borde por Kt ~ 3 (placa con agujero circular, Kirsch): si todo alrededor esta por debajo del umbral u, el borde queda por debajo de ~3u del limite y el pico no cambia.
- **Espero:** baja la masa; la tension maxima casi no cambia.
- **Evidencia (respaldada por los datos):** en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Aplicada en el optimizador:** 61 veces (5 descartadas en la evaluacion rapida, 28 aceptadas, 2 rechazadas); tension +1.1 % (mediana), masa -16 g (mediana).
  - calibracion de la evaluacion rapida (malla gruesa): cambio de tension previsto -0.1 % frente a +1.1 % real (mediana de 30)
  - iteracion 34: aceptada: aligeramiento pasante vertical D10 mm en (34, -83) (tension +1.9 %, masa -14 g)
  - iteracion 35: aceptada: aligeramiento pasante vertical D10 mm en (43, -98) (tension +0.6 %, masa -17 g)
  - iteracion 36: aceptada: aligeramiento pasante vertical D10 mm en (34, -83) (tension +1.9 %, masa -14 g)
  - iteracion 37: aceptada: aligeramiento pasante vertical D10 mm en (43, -98) (tension +0.6 %, masa -17 g)

Referencia: los 16 disenos publicados VALIDOS.

| | material ocioso (< 15 % de su propio pico) | masa |
|---|---|---|
| pieza original (SimJEB n.o 0) | 51 % | 2.423 kg |
| mediana del grupo de referencia (16) | 31 % | 2.503 kg |
| mediana de su mitad mas ligera (8) | 25 % | 2.342 kg |

Donde esta el material (cm3) - original frente a la mitad mas ligera del grupo de referencia:

| zona | original | referencia ligera (mediana) | exceso del original |
|---|---|---|---|
| alrededor de los pernos delanteros | 25 | 37 | -12 |
| alrededor de los pernos traseros | 24 | 37 | -12 |
| orejetas del bulon | 20 | 21 | -1 |
| placa base (z < 10 mm) | 67 | 45 | +21 |
| cuerpo, lado de las orejetas (x < 15 mm) | 70 | 56 | +14 |
| cuerpo, lado trasero (x >= 15 mm) | 103 | 96 | +6 |

### R2. Rebaje desde arriba de la capa ociosa  (ACTIVA)

- **Si:** todo el material por encima de una cota zc, en un rectangulo (con 4 mm de margen), esta por debajo del umbral.
- **Hago:** rebaje desde arriba hasta zc (suelo horizontal: imprimible) con esquinas redondeadas de radio = 20 % de su lado menor (3-8 mm); deja >= 5 mm de suelo y nunca una pared de menos de 5 mm al borde.
- **Porque:** material que no transmite carga: su tension es baja porque ni el momento de vuelco ni el cortante pasan por ahi. Quitarlo desde arriba no deja voladizos y no corta el camino de carga.
- **Espero:** baja la masa; la tension maxima casi no cambia.
- **Evidencia (respaldada por los datos):** en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55).
- **Aplicada en el optimizador:** 10 veces (3 descartadas en la evaluacion rapida, 4 aceptadas, 1 rechazadas); tension +0.1 % (mediana), masa -34 g (mediana).
  - calibracion de la evaluacion rapida (malla gruesa): cambio de tension previsto -0.1 % frente a +0.1 % real (mediana de 5)
  - iteracion 4: aceptada: rebaje desde arriba hasta z = 9 mm en x 42..54, y -100..-52  (tension -6.0 %, masa -47 g)
  - iteracion 5: rechazada: rebaje desde arriba hasta z = 5 mm en x -30..-18, y -40..-8  (tension +0.0 %, masa +0 g)
  - iteracion 13: aceptada: rebaje desde arriba hasta z = 5 mm en x 38..50, y -60..-44 m (tension +1.3 %, masa -34 g)
  - iteracion 14: aceptada: rebaje desde arriba hasta z = 7 mm en x -26..-10, y -124..-1 (tension -0.9 %, masa -27 g)

Referencia: los 16 disenos publicados VALIDOS.

| | material ocioso (< 15 % de su propio pico) | masa |
|---|---|---|
| pieza original (SimJEB n.o 0) | 51 % | 2.423 kg |
| mediana del grupo de referencia (16) | 31 % | 2.503 kg |
| mediana de su mitad mas ligera (8) | 25 % | 2.342 kg |

Donde esta el material (cm3) - original frente a la mitad mas ligera del grupo de referencia:

| zona | original | referencia ligera (mediana) | exceso del original |
|---|---|---|---|
| alrededor de los pernos delanteros | 25 | 37 | -12 |
| alrededor de los pernos traseros | 24 | 37 | -12 |
| orejetas del bulon | 20 | 21 | -1 |
| placa base (z < 10 mm) | 67 | 45 | +21 |
| cuerpo, lado de las orejetas (x < 15 mm) | 70 | 56 | +14 |
| cuerpo, lado trasero (x >= 15 mm) | 103 | 96 | +6 |

### R3. Hueco interior en el nucleo ocioso (conservando las pieles)  (ACTIVA)

- **Si:** un bloque interior, a >= 4 mm de cualquier superficie, trabaja por debajo del umbral.
- **Hago:** hueco con techo a 45 grados y agujero de evacuacion D5 (impresion 3D).
- **Porque:** a flexion y torsion la tension crece con la distancia a la fibra neutra (s = M y / I, t = T r / J): el nucleo apenas trabaja y la rigidez la dan las pieles. Por eso las vigas son en I o en cajon.
- **Espero:** baja la masa; la tension sube poco (las pieles siguen).
- **Evidencia (respaldada por los datos):** en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Huecos interiores cerrados en ese grupo: 1 de 16 (en el concurso no se podian dejar cavidades cerradas; aqui se dejan con evacuacion).
- **Aplicada en el optimizador:** 24 veces (1 descartadas en la evaluacion rapida, 1 aceptadas, 0 rechazadas); tension +1.5 % (mediana), masa -5 g (mediana).
  - calibracion de la evaluacion rapida (malla gruesa): cambio de tension previsto +0.3 % frente a +1.5 % real (mediana de 1)
  - iteracion 15: aceptada: hueco interior 12 x 16 x 8 mm (techo a 45 grados + evacuacio (tension +1.5 %, masa -5 g)

Referencia: los 16 disenos publicados VALIDOS.

| | material ocioso (< 15 % de su propio pico) | masa |
|---|---|---|
| pieza original (SimJEB n.o 0) | 51 % | 2.423 kg |
| mediana del grupo de referencia (16) | 31 % | 2.503 kg |
| mediana de su mitad mas ligera (8) | 25 % | 2.342 kg |

Donde esta el material (cm3) - original frente a la mitad mas ligera del grupo de referencia:

| zona | original | referencia ligera (mediana) | exceso del original |
|---|---|---|---|
| alrededor de los pernos delanteros | 25 | 37 | -12 |
| alrededor de los pernos traseros | 24 | 37 | -12 |
| orejetas del bulon | 20 | 21 | -1 |
| placa base (z < 10 mm) | 67 | 45 | +21 |
| cuerpo, lado de las orejetas (x < 15 mm) | 70 | 56 | +14 |
| cuerpo, lado trasero (x >= 15 mm) | 103 | 96 | +6 |

### R4. Collar de refuerzo en el perno donde esta el pico (y en su simetrico)  (ACTIVA)

- **Si:** el pico de tension esta junto al alojamiento de la cabeza de un perno.
- **Hago:** anillo de material alrededor del alojamiento (y del perno simetrico respecto al plano medio de las orejetas).
- **Porque:** la carga horizontal aplicada a 44,7 mm de altura crea un momento de vuelco (F x h ~ 1,9 kN m con 42 258 N) que la pieza lleva a los pernos; alrededor del alojamiento la seccion es pequena. Mas seccion -> menos tension (s ~ M / W). El soporte es simetrico respecto al plano medio de las orejetas (y ~ -75 mm): el perno simetrico trabaja igual.
- **Espero:** baja la tension maxima; sube un poco la masa.
- **Evidencia (respaldada por los datos):** prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de 238 a 203 MPa (-15 %) con +159 g (escalado lineal a 42258 N); en 228 disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman -0.25, p = 0.00014); material junto a los pernos delanteros: original 25 cm3, mediana del grupo de referencia 37 cm3; en 104 de 297 disenos publicados calculados el pico esta junto a un perno.
- **Aplicada en el optimizador:** 2 veces (0 descartadas en la evaluacion rapida, 1 aceptadas, 0 rechazadas); tension -15.2 % (mediana), masa +81 g (mediana).
  - calibracion de la evaluacion rapida (malla gruesa): cambio de tension previsto -6.8 % frente a -15.2 % real (mediana de 1)
  - iteracion 1: aceptada: collar de 6 mm en los pernos 1 y 3 (tension -15.2 %, masa +81 g)

### R5. Alojamiento de la cabeza mas ancho con acuerdo de fondo mayor  (DESACTIVADA: LOS DATOS LA CONTRADICEN)

- **Si:** el pico esta en el acuerdo del fondo del alojamiento de un perno (entalla).
- **Hago:** alojamiento de radio mayor con acuerdo de fondo R - 8 mm.
- **Porque:** hipotesis de partida: el factor de concentracion Kt baja al crecer el radio del acuerdo (Peterson). PERO agrandar el alojamiento tambien quita seccion justo donde esta el pico.
- **Espero:** segun la teoria del acuerdo, baja la tension; segun la seccion, la sube: deciden los datos.
- **Evidencia (CONTRADICHA por los datos):** en 294 disenos anteriores, alojamiento mas ancho -> MAS tension (Spearman +0.76, p = 8.7e-56; mediana 360 MPa con R > 11 mm frente a 206 MPa con el del original): pesa mas la seccion que se pierde que el acuerdo que se gana. Regla DESACTIVADA por los datos..

### R6. Redondear las aristas entrantes junto al pico  (ACTIVA)

- **Si:** el pico es una concentracion local (pico >= 1,8 veces la tension media a 12 mm) fuera de los alojamientos.
- **Hago:** acuerdo (redondeo) de las aristas a menos de 6 mm del pico (nunca las de los 6 agujeros fijos).
- **Porque:** una arista viva entrante es una entalla: Kt crece al bajar el radio (Peterson). Un acuerdo reparte la tension en mas material.
- **Espero:** baja la tension maxima con muy poca masa.
- **Evidencia (basada en la teoria / en sus resultados):** no se puede medir en las mallas publicadas (radios de acuerdo); regla basada en la teoria (Peterson) y en los resultados del propio optimizador.

### R7. Engrosar el anillo de las orejetas  (ACTIVA)

- **Si:** el pico esta en las orejetas del bulon.
- **Hago:** anillo de material alrededor del bulon en las dos orejetas (mismo espesor).
- **Porque:** el bulon empuja la orejeta en la direccion de la carga; el ligamento delante del agujero trabaja a cortadura y aplastamiento (s ~ F / (2 t e)). Mas ligamento e -> menos tension.
- **Espero:** baja la tension en la orejeta; sube un poco la masa.
- **Evidencia (respaldada por los datos):** ligamento delante del bulon: original 7.5 mm, mediana de los 16 disenos publicados VALIDOS: 7.6 mm, y 7.5 mm en los 25 disenos cuyo pico esta en la orejeta.
- **Aplicada en el optimizador:** 1 veces (1 descartadas en la evaluacion rapida, 0 aceptadas, 0 rechazadas).

### R8. Reponer material donde un corte anterior ha creado el pico  (ACTIVA)

- **Si:** el pico esta a menos de 4 mm de un corte hecho antes.
- **Hago:** se reduce ese corte (x0,6 de su tamano; si queda muy pequeno, se deshace).
- **Porque:** si el pico aparece en el borde de un corte, ese material SI estaba en el camino de carga: se devuelve solo ese material en vez de reforzar en otro sitio.
- **Espero:** baja la tension maxima; sube un poco la masa.
- **Evidencia (basada en la teoria / en sus resultados):** regla de procedimiento: se juzga por sus resultados en el optimizador.

### R9. Cortar menos donde ya se rechazo un corte  (ACTIVA)

- **Si:** un corte se rechazo (tension por encima del limite o pieza peor).
- **Hago:** en esa zona solo se proponen cortes de como maximo 0,6 veces el tamano rechazado.
- **Porque:** el rechazo dice que ahi hay material que trabaja; un corte menor puede ser aceptable (busqueda por biseccion del tamano).
- **Espero:** evita repetir errores y aprovecha lo que si se pueda quitar.
- **Evidencia (basada en la teoria / en sus resultados):** regla de procedimiento: se juzga por sus resultados en el optimizador.

### R10. Subir el umbral de material ocioso cuando ya no queda donde quitar  (ACTIVA)

- **Si:** no hay ninguna zona por debajo del umbral actual donde quepa un corte.
- **Hago:** se pasa al siguiente umbral (15 %, 25 %, 35 % del limite).
- **Porque:** se empieza por lo mas seguro (con Kt ~ 3, el borde de un corte en material al 15 % queda al ~45 %) y solo despues se aprovecha material que trabaja algo mas.
- **Espero:** permite seguir aligerando con un riesgo controlado.
- **Evidencia (basada en la teoria / en sus resultados):** regla de procedimiento: se juzga por sus resultados en el optimizador.

### R11. Sustituir un bloque que trabaja poco por un nervio en la trayectoria de la carga (FORMA NUEVA)  (SUSPENDIDA: 9 INTENTOS SIN NINGUNA MEJORA)

- **Si:** un bloque trabaja por debajo del 45-60 % del limite (no es ocioso: lleva algo de carga) o un rebaje se rechazo porque ese material si trabajaba.
- **Hago:** se quita el bloque y se crean NERVIOS (paredes verticales, imprimibles, con acuerdo de 3 mm en la raiz): uno por cada familia de la carga (traccion y compresion) en su direccion principal, dimensionado para llevarla al 50 % del limite.
- **Porque:** Michell (1904): la estructura de volumen minimo que lleva una carga sigue las trayectorias de las tensiones principales, y su volumen es la integral de |s| dV dividida por la tension de trabajo. En un bloque macizo casi todo el material trabaja muy por debajo del limite; un nervio en la direccion de la carga lleva lo mismo (traccion/compresion, que aprovecha toda la seccion) con mucho menos material.
- **Espero:** baja la masa (bloque menos nervio); la tension sube algo, pero el nervio trabaja por debajo del limite.
- **Evidencia (basada en la teoria / en sus resultados):** NO CONCLUYENTE: entre los disenos publicados calculados con malla completa, los de nervios / arcos / vigas (9) tienen de mediana un 35 % de material ocioso y 1.048 kg, frente al 32 % y 2.119 kg de los tipo bloque (38). Teoria: Michell (1904), estructuras de volumen minimo.
- **Aplicada en el optimizador:** 9 veces (9 descartadas en la evaluacion rapida, 0 aceptadas, 0 rechazadas).

---
Las reglas R9 y R10 son de procedimiento (como aplicar las demas). La lista completa de iteraciones, con el antes y el despues de cada cambio, esta en `runs/opt_<carga>N/ITERACIONES.md`.
