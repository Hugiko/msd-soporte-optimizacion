# Registro de iteraciones (changelog de la pieza)

Carga 42258 N | limite 215 MPa (coef. de seguridad >= 1.00) y 0.25 mm | reglas: [DESIGN_RULES.md](../../DESIGN_RULES.md) | la mas reciente arriba

## Iteracion 30 - SIN CAMBIO

*2026-11-24 13:17*

- **Pieza de partida:** 2.2571 kg | 202.1 MPa | CS 1.06 | 0.146 mm
- **Decision:** SIN CAMBIO - todas las modificaciones propuestas se descartaron en la evaluacion rapida
- Descartada en la evaluacion rapida: [R12] acampanar la raiz de los collares (30 grados hasta z = 16 mm) -> tension prevista 237 MPa: supera el limite (215 MPa)
- Nota: R10: ya no queda material por debajo del 15 % del limite donde quepa un corte -> se pasa al umbral del 25 %
- Nota: 1 propuestas descartadas por SIMETRIA: quitarian distinto material en un lado que en su simetrico (el contorno del original no es simetrico en esa zona)

## Iteracion 29 - REEVALUADA

*2026-11-24 13:14*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla None):** la pieza tiene que ser simetrica: se quita el aligeramiento D16 en (64, -32), que solo quitaba material en un lado (2,07 cm3 a su alrededor frente a 0,20 en el simetrico: alli el contorno del original es mas estrecho); desde ahora cada corte debe quitar parecido material en los dos lados. Nueva regla R12 (collar acampanado)
- **Resultado (malla completa):** 2.2571 kg | 202.1 MPa | CS 1.06 | 0.146 mm | simetria 89.9 % del volumen (92.7 % lejos de los pernos)
- **Decision:** REEVALUADA - cumple: se sigue optimizando con las reglas nuevas

<img src="galeria/20261124_131413_it029_REEVALUADA_2.257kg.jpg" width="520">

## Iteracion 28 - RECHAZADA: R14 bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 45 grados) en (28, -92) (y su simetrico)

*2026-11-24 12:25*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R14):** Todo el material por debajo de z = 12 mm en esa zona (y 4 mm alrededor y encima) trabaja por debajo del 45 % del limite: la placa base bajo el cuerpo no lleva carga (el soporte solo se sujeta por los pernos). Se vacia desde la cara de apoyo con techo a 45 grados (imprimible), sin tocar el cuerpo de encima; el pico (199 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** mediana de las 4 veces que se ha aplicado: +0.1 % (prevision rapida: 2.2058 kg | 199.5 MPa | CS 1.08 | 0.147 mm)
- **Resultado (malla completa):** 2.2039 kg | 203.0 MPa | CS 1.06 | 0.147 mm (tension +1.8 %, masa -37 g)
- **Decision:** RECHAZADA - no cumple: 203.0 MPa con la malla normal, que corregidos a malla fina (x1.069) son 217.1 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R13] ventana pasante en x -26..-2, y -80..-68 mm (esquinas R3) (y su simetrico) -> tension prevista 1382 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x -26..-2, y -80..-68 mm (esquinas R3) (y su simetrico) -> tension prevista 210 MPa: supera el limite (215 MPa)

<img src="galeria/20261124_122817_it028_RECHAZADA_2.204kg.jpg" width="520">

## Iteracion 27 - RECHAZADA: R13 ventana pasante en x 6..38, y -80..-68 mm (esquinas R3) (y su simetrico)

*2026-11-24 12:22*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R13):** Todo el material de esa zona, desde la cara de apoyo hasta arriba (y 4 mm alrededor), trabaja por debajo del 45 % del limite: la carga baja por el cuerpo hasta los pernos y esa parte de la placa no esta en el camino. Se abre una ventana pasante (esquinas R3); el pico (199 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** la tension maxima casi no cambia (prevision rapida: 2.1906 kg | 199.3 MPa | CS 1.08 | 0.149 mm)
- **Resultado (malla completa):** 2.1922 kg | 202.5 MPa | CS 1.06 | 0.148 mm (tension +1.6 %, masa -49 g)
- **Decision:** RECHAZADA - no cumple: 202.5 MPa con la malla normal, que corregidos a malla fina (x1.069) son 216.6 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R14] bolsillo desde la cara de apoyo 36 x 28 mm, hasta z = 12 mm (techo a 45 grados) en (24, -90) (y su simetrico) -> la malla o el calculo han fallado (RuntimeError: todas las estrategias de malla/solucion fallaron: malla alg10 h6.00: Exception: HXT 3D mesh failed | malla)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x 6..38, y -80..-68 mm (esquinas R3) (y su simetrico) -> pasa la evaluacion rapida (2.1971 kg | 199.4 MPa | CS 1.08 | 0.149 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_122515_it027_RECHAZADA_2.192kg.jpg" width="520">

## Iteracion 26 - RECHAZADA: R2 rebaje desde arriba hasta z = 5 mm en x -26..14, y -80..-68 mm (esquinas R3) (y su simetrico)

*2026-11-24 12:19*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R2):** Todo el material por encima de z = 5 mm en esa zona (y 4 mm alrededor) trabaja por debajo del 45 % del limite: ni el momento de vuelco ni el cortante pasan por ahi. El rebaje deja un suelo horizontal (imprimible) y acuerdos redondeados. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55).
- **Se esperaba:** mediana de las 6 veces que se ha aplicado: -0.2 % (prevision rapida: 2.2009 kg | 198.0 MPa | CS 1.09 | 0.148 mm)
- **Resultado (malla completa):** 2.2020 kg | 202.6 MPa | CS 1.06 | 0.147 mm (tension +1.7 %, masa -39 g)
- **Decision:** RECHAZADA - no cumple: 202.6 MPa con la malla normal, que corregidos a malla fina (x1.069) son 216.7 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R13] ventana pasante en x -26..14, y -80..-68 mm (esquinas R3) (y su simetrico) -> tension prevista 380 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R1] aligeramiento pasante vertical D12 mm en (52, -23) (y su simetrico) -> tension prevista 271 MPa: supera el limite (215 MPa)

<img src="galeria/20261124_122236_it026_RECHAZADA_2.202kg.jpg" width="520">

## Iteracion 25 - RECHAZADA: R1 aligeramiento pasante vertical D12 mm en (4, -32) (y su simetrico)

*2026-11-24 12:16*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R1):** Toda la columna en (4, -32) hasta 9 mm de radio trabaja como maximo al 40 % del limite (umbral de material ocioso: 45 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~100 %; el pico (199 MPa, en alrededor de los pernos traseros) esta a 110 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 191 veces que se ha aplicado: +1.1 % (prevision rapida: 2.1863 kg | 199.3 MPa | CS 1.08 | 0.152 mm)
- **Resultado (malla completa):** 2.1835 kg | 207.9 MPa | CS 1.03 | 0.152 mm (tension +4.3 %, masa -58 g)
- **Decision:** RECHAZADA - no cumple: 207.9 MPa con la malla normal, que corregidos a malla fina (x1.069) son 222.3 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R13] ventana pasante en x -2..14, y -40..-28 mm (esquinas R3) (y su simetrico) -> tension prevista 250 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x 2..14, y -44..-28 mm (esquinas R3) (y su simetrico) -> tension prevista 240 MPa: supera el limite (215 MPa)

<img src="galeria/20261124_121938_it025_RECHAZADA_2.183kg.jpg" width="520">

## Iteracion 24 - RECHAZADA: R1 aligeramiento pasante vertical D12 mm en (7, -116) (y su simetrico)

*2026-11-24 12:13*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R1):** Toda la columna en (7, -116) hasta 9 mm de radio trabaja como maximo al 40 % del limite (umbral de material ocioso: 45 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~100 %; el pico (199 MPa, en alrededor de los pernos traseros) esta a 28 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 190 veces que se ha aplicado: +1.0 % (prevision rapida: 2.1868 kg | 200.2 MPa | CS 1.07 | 0.152 mm)
- **Resultado (malla completa):** 2.1834 kg | 205.3 MPa | CS 1.05 | 0.152 mm (tension +3.0 %, masa -58 g)
- **Decision:** RECHAZADA - no cumple: 205.3 MPa con la malla normal, que corregidos a malla fina (x1.069) son 219.6 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R13] ventana pasante en x 2..14, y -120..-104 mm (esquinas R3) (y su simetrico) -> tension prevista 226 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x 2..18, y -116..-104 mm (esquinas R3) (y su simetrico) -> tension prevista 258 MPa: supera el limite (215 MPa)

<img src="galeria/20261124_121641_it024_RECHAZADA_2.183kg.jpg" width="520">

## Iteracion 23 - SIN CAMBIO

*2026-11-24 12:11*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Decision:** SIN CAMBIO - todas las modificaciones propuestas se descartaron en la evaluacion rapida
- Descartada en la evaluacion rapida: [R1] aligeramiento pasante vertical D20 mm en (7, -35) (y su simetrico) -> tension prevista 253 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R13] ventana pasante en x -30..38, y -80..-68 mm (esquinas R3) (y su simetrico) -> tension prevista 211 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x -6..14, y -44..-28 mm (esquinas R3.2) (y su simetrico) -> tension prevista 304 MPa: supera el limite (215 MPa)

## Iteracion 22 - SIN CAMBIO

*2026-11-24 12:09*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Decision:** SIN CAMBIO - todas las modificaciones propuestas se descartaron en la evaluacion rapida
- Descartada en la evaluacion rapida: [R1] aligeramiento pasante vertical D24 mm en (7, -113) (y su simetrico) -> tension prevista 314 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R13] ventana pasante en x -2..18, y -120..-104 mm (esquinas R3.2) (y su simetrico) -> tension prevista 356 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 9 mm en x -10..14, y -124..-104 mm (esquinas R4) (y su simetrico) -> tension prevista 324 MPa: supera el limite (215 MPa)
- Nota: R10: ya no queda material por debajo del 35 % del limite donde quepa un corte -> se pasa al umbral del 45 %

## Iteracion 21 - RECHAZADA: R14 bolsillo desde la cara de apoyo 24 x 24 mm, hasta z = 10 mm (techo a 45 grados) en (14, -108) (y su simetrico)

*2026-11-24 12:06*

- **Pieza de partida:** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R14):** Todo el material por debajo de z = 10 mm en esa zona (y 4 mm alrededor y encima) trabaja por debajo del 35 % del limite: la placa base bajo el cuerpo no lleva carga (el soporte solo se sujeta por los pernos). Se vacia desde la cara de apoyo con techo a 45 grados (imprimible), sin tocar el cuerpo de encima; el pico (199 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** mediana de las 3 veces que se ha aplicado: -0.1 % (prevision rapida: 2.2390 kg | 198.7 MPa | CS 1.08 | 0.146 mm)
- **Resultado (malla completa):** 2.2391 kg | 204.0 MPa | CS 1.05 | 0.146 mm (tension +2.4 %, masa -2 g)
- **Decision:** RECHAZADA - no cumple: 204.0 MPa con la malla normal, que corregidos a malla fina (x1.069) son 218.2 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R14] bolsillo desde la cara de apoyo 20 x 24 mm, hasta z = 8 mm (techo a 45 grados) en (40, -72) (y su simetrico) -> tension prevista 211 MPa: supera el limite (215 MPa)
- Nota: R10: ya no queda material por debajo del 25 % del limite donde quepa un corte -> se pasa al umbral del 35 %

<img src="galeria/20261124_120923_it021_RECHAZADA_2.239kg.jpg" width="520">

## Iteracion 20 - ACEPTADA: R14 bolsillo desde la cara de apoyo 36 x 20 mm, hasta z = 7 mm (techo a 45 grados) en (20, -110) (y su simetrico)

*2026-11-24 12:04*

- **Pieza de partida:** 2.2593 kg | 199.6 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R14):** Todo el material por debajo de z = 7 mm en esa zona (y 4 mm alrededor y encima) trabaja por debajo del 25 % del limite: la placa base bajo el cuerpo no lleva carga (el soporte solo se sujeta por los pernos). Se vacia desde la cara de apoyo con techo a 45 grados (imprimible), sin tocar el cuerpo de encima; el pico (200 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** mediana de las 2 veces que se ha aplicado: +0.1 % (prevision rapida: 2.2411 kg | 200.0 MPa | CS 1.07 | 0.146 mm)
- **Resultado (malla completa):** 2.2410 kg | 199.3 MPa | CS 1.08 | 0.146 mm (tension -0.1 %, masa -18 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.2593 -> 2.2410; masa 2.2593 -> 2.2410 kg)

<img src="galeria/20261124_120623_it020_ACEPTADA_2.241kg.jpg" width="520">

## Iteracion 19 - ACEPTADA: R14 bolsillo desde la cara de apoyo 28 x 24 mm, hasta z = 10 mm (techo a 45 grados) en (16, -100) (y su simetrico)

*2026-11-24 11:58*

- **Pieza de partida:** 2.2914 kg | 199.0 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R14):** Todo el material por debajo de z = 10 mm en esa zona (y 4 mm alrededor y encima) trabaja por debajo del 25 % del limite: la placa base bajo el cuerpo no lleva carga (el soporte solo se sujeta por los pernos). Se vacia desde la cara de apoyo con techo a 45 grados (imprimible), sin tocar el cuerpo de encima; el pico (199 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** la tension maxima casi no cambia (prevision rapida: 2.2591 kg | 199.6 MPa | CS 1.08 | 0.146 mm)
- **Resultado (malla completa):** 2.2593 kg | 199.6 MPa | CS 1.08 | 0.146 mm (tension +0.3 %, masa -32 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.2914 -> 2.2593; masa 2.2914 -> 2.2593 kg)
- Descartada en la evaluacion rapida: [R14] bolsillo desde la cara de apoyo 16 x 48 mm, hasta z = 6 mm (techo a 45 grados) en (26, -44) (y su simetrico) -> pasa la evaluacion rapida (2.2684 kg | 199.4 MPa | CS 1.08 | 0.146 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Nota: R10: ya no queda material por debajo del 15 % del limite donde quepa un corte -> se pasa al umbral del 25 %

<img src="galeria/20261124_120139_it019_ACEPTADA_2.259kg.jpg" width="520">

## Iteracion 18 - ACEPTADA: R14 bolsillo desde la cara de apoyo 8 x 16 mm, hasta z = 12 mm (techo a 45 grados) en (14, -44) (y su simetrico)

*2026-11-24 11:54*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R14):** Todo el material por debajo de z = 12 mm en esa zona (y 4 mm alrededor y encima) trabaja por debajo del 15 % del limite: la placa base bajo el cuerpo no lleva carga (el soporte solo se sujeta por los pernos). Se vacia desde la cara de apoyo con techo a 45 grados (imprimible), sin tocar el cuerpo de encima; el pico (199 MPa, en alrededor de los pernos traseros) esta lejos. Evidencia: placa base (z < 10 mm): original 67 cm3 con un 77 % de material ocioso; mediana de la mitad mas ligera de los 16 disenos publicados VALIDOS: 45 cm3.
- **Se esperaba:** la tension maxima casi no cambia (prevision rapida: 2.2916 kg | 198.9 MPa | CS 1.08 | 0.146 mm)
- **Resultado (malla completa):** 2.2914 kg | 199.0 MPa | CS 1.08 | 0.146 mm (tension -0.1 %, masa -1 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.2925 -> 2.2914; masa 2.2925 -> 2.2914 kg)
- Descartada en la evaluacion rapida: [R14] bolsillo desde la cara de apoyo 8 x 12 mm, hasta z = 13 mm (techo a 45 grados) en (14, -102) (y su simetrico) -> pasa la evaluacion rapida (2.2918 kg | 198.8 MPa | CS 1.08 | 0.146 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_115705_it018_ACEPTADA_2.291kg.jpg" width="520">

## Iteracion 17 - REEVALUADA

*2026-11-24 11:49*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla None):** la pieza tiene que ser simetrica: las zonas protegidas de los pernos se reflejan tambien, para que cada corte y su simetrico sean identicos; ademas hay reglas nuevas (R13 ventanas pasantes, R14 bolsillos desde la cara de apoyo, umbral hasta el 45 %)
- **Resultado (malla completa):** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm | simetria 90.6 % del volumen (93.7 % lejos de los pernos)
- **Decision:** REEVALUADA - cumple: se sigue optimizando con las reglas nuevas

<img src="galeria/20261124_114901_it017_REEVALUADA_2.293kg.jpg" width="520">

## Iteracion 16 - SIN CAMBIO

*2026-11-24 11:26*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Decision:** SIN CAMBIO - ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa un corte y el pico no admite refuerzo)

## Iteracion 15 - RECHAZADA: R4 collar de 9 mm en los pernos 3 y 1

*2026-11-24 11:24*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R4):** El pico (199 MPa, 100 % del limite) esta junto al alojamiento del perno 3 (concentracion local x2.6). El momento de vuelco de la carga (F x 44,7 mm) llega a los pernos por una seccion pequena alrededor del alojamiento: un collar de 9 mm aumenta esa seccion. El perno 1 es su simetrico respecto al plano medio de las orejetas y trabaja igual. Evidencia: prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de 238 a 203 MPa (-15 %) con +159 g (escalado lineal a 42258 N); en 228 disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman -0.25, p = 0.00014); material junto a los pernos delanteros: original 25 cm3, mediana del grupo de referencia 37 cm3; en 104 de 297 disenos publicados calculados el pico esta junto a un perno.
- **Se esperaba:** mediana de las 2 veces que se ha aplicado: -9.2 % (prevision rapida: 2.3627 kg | 199.1 MPa | CS 1.08 | 0.143 mm)
- **Resultado (malla completa):** 2.3640 kg | 207.4 MPa | CS 1.04 | 0.142 mm (tension +4.1 %, masa +71 g)
- **Decision:** RECHAZADA - no cumple: 207.4 MPa con la malla normal, que corregidos a malla fina (x1.077) son 223.4 MPa > 215 MPa

<img src="galeria/20261124_112653_it015_RECHAZADA_2.364kg.jpg" width="520">

## Iteracion 14 - RECHAZADA: R3 hueco interior 12 x 20 x 8 mm (techo a 45 grados + evacuacion D5) en (12, -42) (y su simetrico)

*2026-11-24 11:22*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R3):** El nucleo de esa zona (a mas de 4 mm de cualquier superficie) trabaja por debajo del 35 % del limite: en flexion la tension crece con la distancia a la fibra neutra, asi que vaciarlo conserva las pieles, que son las que trabajan. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Huecos interiores cerrados en ese grupo: 1 de 16 (en el concurso no se podian dejar cavidades cerradas; aqui se dejan con evacuacion).
- **Se esperaba:** la tension sube poco (prevision rapida: 2.2830 kg | 196.2 MPa | CS 1.10 | 0.146 mm)
- **Resultado (malla completa):** 2.2818 kg | 202.3 MPa | CS 1.06 | 0.146 mm (tension +1.5 %, masa -11 g)
- **Decision:** RECHAZADA - no cumple: 202.3 MPa con la malla normal, que corregidos a malla fina (x1.077) son 217.9 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3627 kg | 199.1 MPa | CS 1.08 | 0.143 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_112447_it014_RECHAZADA_2.282kg.jpg" width="520">

## Iteracion 13 - RECHAZADA: R1 aligeramiento pasante vertical D8 mm en (40, -59) (y su simetrico)

*2026-11-24 11:18*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R1):** Toda la columna en (40, -59) hasta 7 mm de radio trabaja como maximo al 30 % del limite (umbral de material ocioso: 35 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~89 %; el pico (199 MPa, en alrededor de los pernos traseros) esta a 86 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 189 veces que se ha aplicado: +0.9 % (prevision rapida: 2.2700 kg | 199.4 MPa | CS 1.08 | 0.146 mm)
- **Resultado (malla completa):** 2.2682 kg | 209.4 MPa | CS 1.03 | 0.146 mm (tension +5.1 %, masa -24 g)
- **Decision:** RECHAZADA - no cumple: 209.4 MPa con la malla normal, que corregidos a malla fina (x1.077) son 225.5 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3627 kg | 199.1 MPa | CS 1.08 | 0.143 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Descartada en la evaluacion rapida: [R3] hueco interior 12 x 20 x 8 mm (techo a 45 grados + evacuacion D5) en (12, -42) (y su simetrico) -> pasa la evaluacion rapida (2.2830 kg | 196.2 MPa | CS 1.10 | 0.146 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_112155_it013_RECHAZADA_2.268kg.jpg" width="520">

## Iteracion 12 - RECHAZADA: R1 aligeramiento pasante vertical D12 mm en (-5, -74) (y su simetrico)

*2026-11-24 11:12*

- **Pieza de partida:** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm
- **Por que (regla R1):** Toda la columna en (-5, -74) hasta 9 mm de radio trabaja como maximo al 34 % del limite (umbral de material ocioso: 35 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~100 %; el pico (199 MPa, en alrededor de los pernos traseros) esta a 71 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 188 veces que se ha aplicado: +0.9 % (prevision rapida: 2.2773 kg | 198.7 MPa | CS 1.08 | 0.146 mm)
- **Resultado (malla completa):** 2.2777 kg | 202.6 MPa | CS 1.06 | 0.146 mm (tension +1.6 %, masa -15 g)
- **Decision:** RECHAZADA - no cumple: 202.6 MPa con la malla normal, que corregidos a malla fina (x1.077) son 218.1 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3627 kg | 199.1 MPa | CS 1.08 | 0.143 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Descartada en la evaluacion rapida: [R3] hueco interior 12 x 20 x 8 mm (techo a 45 grados + evacuacion D5) en (12, -42) (y su simetrico) -> pasa la evaluacion rapida (2.2830 kg | 196.2 MPa | CS 1.10 | 0.146 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_111823_it012_RECHAZADA_2.278kg.jpg" width="520">

## Iteracion 11 - ACEPTADA: R1 aligeramiento pasante vertical D8 mm en (43, -44) (y su simetrico)

*2026-11-24 09:41*

- **Pieza de partida:** 2.3201 kg | 198.0 MPa | CS 1.09 | 0.144 mm
- **Por que (regla R1):** Toda la columna en (43, -44) hasta 7 mm de radio trabaja como maximo al 34 % del limite (umbral de material ocioso: 35 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~100 %; el pico (198 MPa, en alrededor de los pernos traseros) esta a 101 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 187 veces que se ha aplicado: +0.9 % (prevision rapida: 2.2948 kg | 202.1 MPa | CS 1.06 | 0.145 mm)
- **Resultado (malla completa):** 2.2925 kg | 199.3 MPa | CS 1.08 | 0.146 mm (tension +0.6 %, masa -28 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.3201 -> 2.2925; masa 2.3201 -> 2.2925 kg)
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3901 kg | 201.4 MPa | CS 1.07 | 0.141 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Descartada en la evaluacion rapida: [R3] hueco interior 12 x 20 x 8 mm (techo a 45 grados + evacuacion D5) en (12, -42) (y su simetrico) -> pasa la evaluacion rapida (2.3103 kg | 205.1 MPa | CS 1.05 | 0.145 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_094448_it011_ACEPTADA_2.293kg.jpg" width="520">

## Iteracion 10 - RECHAZADA: R1 aligeramiento pasante vertical D8 mm en (37, -83) (y su simetrico)

*2026-11-24 09:39*

- **Pieza de partida:** 2.3201 kg | 198.0 MPa | CS 1.09 | 0.144 mm
- **Por que (regla R1):** Toda la columna en (37, -83) hasta 7 mm de radio trabaja como maximo al 34 % del limite (umbral de material ocioso: 35 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~100 %; el pico (198 MPa, en alrededor de los pernos traseros) esta a 62 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 186 veces que se ha aplicado: +0.9 % (prevision rapida: 2.2908 kg | 201.4 MPa | CS 1.07 | 0.145 mm)
- **Resultado (malla completa):** 2.2879 kg | 200.3 MPa | CS 1.07 | 0.145 mm (tension +1.1 %, masa -32 g)
- **Decision:** RECHAZADA - no cumple: 200.3 MPa con la malla normal, que corregidos a malla fina (x1.077) son 215.7 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R6] redondeo R3.0 de las aristas junto a (17, -142, 13) (y su simetrico) -> la geometria no se puede construir (operacion 10 (redondeo): el redondeo no se puede hacer en esas aristas (StdFail_NotDone))
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3901 kg | 201.4 MPa | CS 1.07 | 0.141 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_094131_it010_RECHAZADA_2.288kg.jpg" width="520">

## Iteracion 9 - RECHAZADA: R4 collar de 8 mm en los pernos 3 y 1

*2026-11-24 09:34*

- **Pieza de partida:** 2.3201 kg | 198.0 MPa | CS 1.09 | 0.144 mm
- **Por que (regla R4):** El pico (198 MPa, 99 % del limite) esta junto al alojamiento del perno 3 (concentracion local x2.6). El momento de vuelco de la carga (F x 44,7 mm) llega a los pernos por una seccion pequena alrededor del alojamiento: un collar de 8 mm aumenta esa seccion. El perno 1 es su simetrico respecto al plano medio de las orejetas y trabaja igual. Evidencia: prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de 238 a 203 MPa (-15 %) con +159 g (escalado lineal a 42258 N); en 228 disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman -0.25, p = 0.00014); material junto a los pernos delanteros: original 25 cm3, mediana del grupo de referencia 37 cm3; en 104 de 297 disenos publicados calculados el pico esta junto a un perno.
- **Se esperaba:** del orden de -20 % (collares anteriores: -15 % con 6 mm) (prevision rapida: 2.3654 kg | 201.4 MPa | CS 1.07 | 0.142 mm)
- **Resultado (malla completa):** 2.3665 kg | 191.6 MPa | CS 1.12 | 0.142 mm (tension -3.3 %, masa +46 g)
- **Decision:** RECHAZADA - cumple pero no mejora al mejor (puntuacion 2.3665 frente a 2.3201)
- Descartada en la evaluacion rapida: [R1] aligeramiento pasante vertical D12 mm en (-17, -74) (y su simetrico) -> tension prevista 412 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R4] collar de 9 mm en los pernos 3 y 1 -> pasa la evaluacion rapida (2.3901 kg | 201.4 MPa | CS 1.07 | 0.141 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Nota: R10: ya no queda material por debajo del 25 % del limite donde quepa un corte -> se pasa al umbral del 35 %

<img src="galeria/20261124_093855_it009_RECHAZADA_2.366kg.jpg" width="520">

## Iteracion 8 - ACEPTADA: R1 aligeramiento pasante vertical D10 mm en (19, -74) (y su simetrico)

*2026-11-24 09:30*

- **Pieza de partida:** 2.3349 kg | 196.2 MPa | CS 1.10 | 0.144 mm
- **Por que (regla R1):** Toda la columna en (19, -74) hasta 8 mm de radio trabaja como maximo al 25 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~75 %; el pico (196 MPa, en alrededor de los pernos traseros) esta a 68 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 185 veces que se ha aplicado: +0.9 % (prevision rapida: 2.3209 kg | 192.2 MPa | CS 1.12 | 0.145 mm)
- **Resultado (malla completa):** 2.3201 kg | 198.0 MPa | CS 1.09 | 0.144 mm (tension +0.9 %, masa -15 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.3349 -> 2.3201; masa 2.3349 -> 2.3201 kg)

<img src="galeria/20261124_093222_it008_ACEPTADA_2.320kg.jpg" width="520">

## Iteracion 7 - ACEPTADA: R1 aligeramiento pasante vertical D10 mm en (28, -74) (y su simetrico)

*2026-11-24 09:28*

- **Pieza de partida:** 2.3552 kg | 196.6 MPa | CS 1.09 | 0.143 mm
- **Por que (regla R1):** Toda la columna en (28, -74) hasta 8 mm de radio trabaja como maximo al 25 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~75 %; el pico (197 MPa, en alrededor de los pernos traseros) esta a 69 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 184 veces que se ha aplicado: +1.1 % (prevision rapida: 2.3357 kg | 198.8 MPa | CS 1.08 | 0.144 mm)
- **Resultado (malla completa):** 2.3349 kg | 196.2 MPa | CS 1.10 | 0.144 mm (tension -0.2 %, masa -20 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.3552 -> 2.3349; masa 2.3552 -> 2.3349 kg)

<img src="galeria/20261124_093025_it007_ACEPTADA_2.335kg.jpg" width="520">

## Iteracion 6 - ACEPTADA: R1 aligeramiento pasante vertical D16 mm en (-26, -29) (y su simetrico)

*2026-11-24 09:23*

- **Pieza de partida:** 2.3827 kg | 197.2 MPa | CS 1.09 | 0.142 mm
- **Por que (regla R1):** Toda la columna en (-26, -29) hasta 11 mm de radio trabaja como maximo al 25 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~74 %; el pico (197 MPa, en alrededor de los pernos traseros) esta a 121 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 183 veces que se ha aplicado: +1.3 % (prevision rapida: 2.3560 kg | 198.2 MPa | CS 1.08 | 0.144 mm)
- **Resultado (malla completa):** 2.3552 kg | 196.6 MPa | CS 1.09 | 0.143 mm (tension -0.3 %, masa -28 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.3827 -> 2.3552; masa 2.3827 -> 2.3552 kg)
- Descartada en la evaluacion rapida: [R1] aligeramiento pasante vertical D16 mm en (-23, -119) (y su simetrico) -> tension prevista 439 MPa: supera el limite (215 MPa)

<img src="galeria/20261124_092617_it006_ACEPTADA_2.355kg.jpg" width="520">

## Iteracion 5 - ACEPTADA: R1 aligeramiento pasante vertical D16 mm en (64, -32) (y su simetrico)

*2026-11-24 09:19*

- **Pieza de partida:** 2.3989 kg | 205.6 MPa | CS 1.05 | 0.141 mm
- **Por que (regla R1):** Toda la columna en (64, -32) hasta 11 mm de radio trabaja como maximo al 25 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~74 %; el pico (206 MPa, en alrededor de los pernos delanteros) esta a 26 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 182 veces que se ha aplicado: +1.6 % (prevision rapida: 2.3833 kg | 204.9 MPa | CS 1.05 | 0.142 mm)
- **Resultado (malla completa):** 2.3827 kg | 197.2 MPa | CS 1.09 | 0.142 mm (tension -4.1 %, masa -16 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.3989 -> 2.3827; masa 2.3989 -> 2.3827 kg)
- Descartada en la evaluacion rapida: [R4] collar de 4 mm en los pernos 2 y 4 -> pasa la evaluacion rapida (2.4403 kg | 206.5 MPa | CS 1.04 | 0.140 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Descartada en la evaluacion rapida: [R4] collar de 6 mm en los pernos 2 y 4 -> pasa la evaluacion rapida (2.4754 kg | 205.5 MPa | CS 1.05 | 0.138 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_092340_it005_ACEPTADA_2.383kg.jpg" width="520">

## Iteracion 4 - ACEPTADA: R1 aligeramiento pasante vertical D12 mm en (4, -74) (y su simetrico)

*2026-11-24 09:13*

- **Pieza de partida:** 2.4281 kg | 206.0 MPa | CS 1.04 | 0.141 mm
- **Por que (regla R1):** Toda la columna en (4, -74) hasta 9 mm de radio trabaja como maximo al 23 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~70 %; el pico (206 MPa, en alrededor de los pernos delanteros) esta a 82 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 181 veces que se ha aplicado: +1.9 % (prevision rapida: 2.3997 kg | 205.7 MPa | CS 1.05 | 0.141 mm)
- **Resultado (malla completa):** 2.3989 kg | 205.6 MPa | CS 1.05 | 0.141 mm (tension -0.2 %, masa -29 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.4281 -> 2.3989; masa 2.4281 -> 2.3989 kg)
- Descartada en la evaluacion rapida: [R4] collar de 4 mm en los pernos 2 y 4 -> pasa la evaluacion rapida (2.4690 kg | 203.1 MPa | CS 1.06 | 0.139 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Descartada en la evaluacion rapida: [R4] collar de 6 mm en los pernos 2 y 4 -> pasa la evaluacion rapida (2.5041 kg | 206.3 MPa | CS 1.04 | 0.138 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Nota: R5 (Alojamiento de la cabeza mas ancho con acuerdo de fondo mayor) desactivada: los datos la contradicen

<img src="galeria/20261124_091728_it004_ACEPTADA_2.399kg.jpg" width="520">

## Iteracion 3 - ACEPTADA: R1 aligeramiento pasante vertical D16 mm en (49, -56) (y su simetrico)

*2026-11-24 09:07*

- **Pieza de partida:** 2.4822 kg | 200.9 MPa | CS 1.07 | 0.140 mm
- **Por que (regla R1):** Toda la columna en (49, -56) hasta 11 mm de radio trabaja como maximo al 25 % del limite (umbral de material ocioso: 25 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~74 %; el pico (201 MPa, en orejetas del bulon) esta a 54 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 180 veces que se ha aplicado: +1.6 % (prevision rapida: 2.4309 kg | 203.8 MPa | CS 1.05 | 0.141 mm)
- **Resultado (malla completa):** 2.4281 kg | 206.0 MPa | CS 1.04 | 0.141 mm (tension +2.5 %, masa -54 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.4822 -> 2.4281; masa 2.4822 -> 2.4281 kg)
- Descartada en la evaluacion rapida: [R7] anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm) -> tension prevista 213 MPa: supera el limite (215 MPa)
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 5 mm en x 38..50, y -80..-64 mm (esquinas R3) (y su simetrico) -> la malla o el calculo han fallado (RuntimeError: todas las estrategias de malla/solucion fallaron: malla alg10 h6.00: Exception: HXT 3D mesh failed | malla)
- Nota: R10: ya no queda material por debajo del 15 % del limite donde quepa un corte -> se pasa al umbral del 25 %

<img src="galeria/20261124_091035_it003_ACEPTADA_2.428kg.jpg" width="520">

## Iteracion 2 - ACEPTADA: R2 rebaje desde arriba hasta z = 9 mm en x 42..62, y -80..-68 mm (esquinas R3) (y su simetrico)

*2026-11-24 09:05*

- **Pieza de partida:** 2.5044 kg | 201.9 MPa | CS 1.06 | 0.139 mm
- **Por que (regla R2):** Todo el material por encima de z = 9 mm en esa zona (y 4 mm alrededor) trabaja por debajo del 15 % del limite: ni el momento de vuelco ni el cortante pasan por ahi. El rebaje deja un suelo horizontal (imprimible) y acuerdos redondeados. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55).
- **Se esperaba:** mediana de las 5 veces que se ha aplicado: +0.1 % (prevision rapida: 2.4817 kg | 201.1 MPa | CS 1.07 | 0.139 mm)
- **Resultado (malla completa):** 2.4822 kg | 200.9 MPa | CS 1.07 | 0.140 mm (tension -0.5 %, masa -22 g)
- **Decision:** ACEPTADA - cumple y mejora al mejor (puntuacion 2.5044 -> 2.4822; masa 2.5044 -> 2.4822 kg)
- Descartada en la evaluacion rapida: [R7] anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm) -> pasa la evaluacion rapida (2.5200 kg | 210.5 MPa | CS 1.02 | 0.141 mm) pero otra es mas prometedora; se podra proponer de nuevo

<img src="galeria/20261124_090732_it002_ACEPTADA_2.482kg.jpg" width="520">

## Iteracion 1 - RECHAZADA: R1 aligeramiento pasante vertical D12 mm en (40, -71) (y su simetrico)

*2026-11-24 09:01*

- **Pieza de partida:** 2.5044 kg | 201.9 MPa | CS 1.06 | 0.139 mm
- **Por que (regla R1):** Toda la columna en (40, -71) hasta 9 mm de radio trabaja como maximo al 14 % del limite (umbral de material ocioso: 15 %): no esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del ~41 %; el pico (202 MPa, en orejetas del bulon) esta a 46 mm. Evidencia: en los 16 disenos publicados VALIDOS, la mitad mas ligera tiene un 25 % de material ocioso (por debajo del 15 % de su pico) frente al 51 % del original; en ese grupo, a mas material ocioso mas masa (Spearman +0.55). Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) menos masa (Spearman -0.11, p = 0.69).
- **Se esperaba:** mediana de las 179 veces que se ha aplicado: +1.3 % (prevision rapida: 2.4601 kg | 204.1 MPa | CS 1.05 | 0.140 mm)
- **Resultado (malla completa):** 2.4599 kg | 207.8 MPa | CS 1.03 | 0.140 mm (tension +2.9 %, masa -44 g)
- **Decision:** RECHAZADA - no cumple: 207.8 MPa con la malla normal, que corregidos a malla fina (x1.041) son 216.3 MPa > 215 MPa
- Descartada en la evaluacion rapida: [R2] rebaje desde arriba hasta z = 11 mm en x 42..62, y -80..-64 mm (esquinas R3.2) (y su simetrico) -> la malla o el calculo han fallado (RuntimeError: todas las estrategias de malla/solucion fallaron: malla alg10 h6.00: Exception: HXT 3D mesh failed | malla)
- Descartada en la evaluacion rapida: [R7] anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm) -> pasa la evaluacion rapida (2.5199 kg | 210.4 MPa | CS 1.02 | 0.141 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Nota: R11 (Sustituir un bloque que trabaja poco por un nervio en la trayectoria de la carga (FORMA NUEVA)) suspendida: 9 intentos sin ninguna mejora

<img src="galeria/20261124_090436_it001_RECHAZADA_2.460kg.jpg" width="520">

## Iteracion 0 - INICIO

*2026-11-24 09:00*

- **Por que (regla None):** La pieza tiene que ser simetrica respecto al plano medio de las orejetas. La pieza anterior (2,144 kg, 14 operaciones) no lo era: sus aligeramientos estaban donde sobraba material solo en un lado. Repetidos en el lado simetrico no cumplen (14 operaciones: 316 MPa; 8 operaciones: 252 MPa; 5 operaciones: 242 MPa; 3 operaciones: 208 MPa; 2 operaciones: 202 MPa; limite 215 MPa con la correccion a malla fina x1,041), porque los pernos 2 y 4 del enunciado no son simetricos y ese lado trabaja mas. Se parte de la ultima pieza simetrica que cumple (los dos collares, ya simetricos) y las reglas siguen en modo simetrico, conservando lo aprendido (estadistica de cada regla y calibracion de malla).
- **Resultado (malla completa):** 2.5044 kg | 201.9 MPa | CS 1.06 | 0.139 mm
- **Decision:** INICIO - cumple: se sigue quitando material donde no trabaja

<img src="galeria/20261124_090049_it000_INICIO_2.504kg.jpg" width="520">

