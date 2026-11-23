# Reglas de diseno del soporte (DESIGN_RULES)

Actualizado: 23/11/2026 15:16. Generado por `scripts/reglas.py` a partir de:

1. **Estudio de las soluciones publicadas** (SimJEB: los 381 disenos del GE Jet Engine Bracket Challenge, Whalen et al. 2021, doi:10.7910/DVN/XFUWJG) calculados con **nuestra** carga (42258 N en -X por el bulon, pernos empotrados) y **nuestro** limite (215 MPa, coef. de seguridad >= 1; desplazamiento <= 0.25 mm). Resultados: `estudio/estudio_simjeb.json`.
2. **Nuestros calculos anteriores** (familias vaciado y refuerzo, 294 disenos con 37 800 N; el modelo es lineal y se escalan x1.118). Archivo: `runs/archivo/`.
3. **Lo que pasa al aplicarlas** en el optimizador (cada aplicacion: tension y masa antes/despues). Una regla que los datos de un cambio DIRECTO contradicen se DESACTIVA (las comparaciones con SimJEB, entre disenos distintos, pueden respaldarla o ser no concluyentes, pero no la desactivan); una que falla 8 veces sin ninguna mejora en el optimizador se SUSPENDE.

## Estudio de las soluciones publicadas

31 disenos calculados: **0 cumplen**, 25 no cumplen, 2 no tienen los agujeros del enunciado (bulon macizo o agujeros de otro tamano), 4 fallaron (malla). Los que superaban 1,5 veces el limite en la pasada rapida (malla gruesa) se descartaron sin calculo fino.

## Reglas

### R1. Aligeramiento pasante donde toda la columna de material esta ociosa  (ACTIVA)

- **Si:** toda la columna vertical (radio del agujero + 3 mm de margen) trabaja por debajo del umbral de material ocioso.
- **Hago:** agujero vertical pasante; paredes verticales (imprimible sin soportes); nunca en las zonas protegidas.
- **Porque:** ese material no esta en el camino de la carga (bulon -> orejetas -> cuerpo -> pernos). Un agujero en una zona a tension s multiplica la tension en su borde por Kt ~ 3 (placa con agujero circular, Kirsch): si todo alrededor esta por debajo del umbral u, el borde queda por debajo de ~3u del limite y el pico no cambia.
- **Espero:** baja la masa; la tension maxima casi no cambia.
- **Evidencia (basada en la teoria / en sus resultados):** estudio de SimJEB aun incompleto: regla basada en la mecanica (Kirsch, flexion).

### R2. Rebaje desde arriba de la capa ociosa  (ACTIVA)

- **Si:** todo el material por encima de una cota zc, en un rectangulo (con 4 mm de margen), esta por debajo del umbral.
- **Hago:** rebaje desde arriba hasta zc con acuerdos redondeados (suelo horizontal: imprimible); deja >= 5 mm de suelo.
- **Porque:** material que no transmite carga: su tension es baja porque ni el momento de vuelco ni el cortante pasan por ahi. Quitarlo desde arriba no deja voladizos y no corta el camino de carga.
- **Espero:** baja la masa; la tension maxima casi no cambia.
- **Evidencia (basada en la teoria / en sus resultados):** estudio de SimJEB aun incompleto: regla basada en la mecanica (Kirsch, flexion).

### R3. Hueco interior en el nucleo ocioso (conservando las pieles)  (ACTIVA)

- **Si:** un bloque interior, a >= 4 mm de cualquier superficie, trabaja por debajo del umbral.
- **Hago:** hueco con techo a 45 grados y agujero de evacuacion D5 (impresion 3D).
- **Porque:** a flexion y torsion la tension crece con la distancia a la fibra neutra (s = M y / I, t = T r / J): el nucleo apenas trabaja y la rigidez la dan las pieles. Por eso las vigas son en I o en cajon.
- **Espero:** baja la masa; la tension sube poco (las pieles siguen).
- **Evidencia (basada en la teoria / en sus resultados):** estudio de SimJEB aun incompleto: regla basada en la mecanica (Kirsch, flexion).

### R4. Collar de refuerzo en el perno donde esta el pico (y en su simetrico)  (ACTIVA)

- **Si:** el pico de tension esta junto al alojamiento de la cabeza de un perno.
- **Hago:** anillo de material alrededor del alojamiento (y del perno simetrico respecto al plano medio de las orejetas).
- **Porque:** la carga horizontal aplicada a 44,7 mm de altura crea un momento de vuelco (F x h ~ 1,9 kN m con 42 258 N) que la pieza lleva a los pernos; alrededor del alojamiento la seccion es pequena. Mas seccion -> menos tension (s ~ M / W). El soporte es simetrico respecto al plano medio de las orejetas (y ~ -75 mm): el perno simetrico trabaja igual.
- **Espero:** baja la tension maxima; sube un poco la masa.
- **Evidencia (respaldada por los datos):** prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de 238 a 203 MPa (-15 %) con +159 g (escalado lineal a 42258 N); en 228 disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman -0.25, p = 0.00014).

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
- **Evidencia (basada en la teoria / en sus resultados):** estudio aun incompleto: regla basada en la mecanica (aplastamiento/cortadura).

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

---
Las reglas R9 y R10 son de procedimiento (como aplicar las demas). La lista completa de iteraciones, con el antes y el despues de cada cambio, esta en `runs/opt_<carga>N/ITERACIONES.md`.
