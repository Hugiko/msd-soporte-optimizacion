# Registro de iteraciones (changelog de la pieza)

Carga 42258 N | limite 215 MPa (coef. de seguridad >= 1.00) y 0.25 mm | reglas: [DESIGN_RULES.md](../../DESIGN_RULES.md) | la mas reciente arriba

## Iteracion 1 - ACEPTADA: R4 collar de 6 mm en los pernos 1 y 3

*2026-11-23 19:40*

- **Pieza de partida:** 2.4234 kg | 238.0 MPa | CS 0.90 | 0.144 mm
- **Por que (regla R4):** El pico (238 MPa, 111 % del limite) esta junto al alojamiento del perno 1 (concentracion local x2.4). El momento de vuelco de la carga (F x 44,7 mm) llega a los pernos por una seccion pequena alrededor del alojamiento: un collar de 6 mm aumenta esa seccion. El perno 3 es su simetrico respecto al plano medio de las orejetas y trabaja igual. Evidencia: prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de 238 a 203 MPa (-15 %) con +159 g (escalado lineal a 42258 N); en 228 disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman -0.25, p = 0.00014); material junto a los pernos delanteros: original 25 cm3, mediana del grupo de referencia 37 cm3; en 104 de 297 disenos publicados calculados el pico esta junto a un perno.
- **Se esperaba:** del orden de -15 % (collares anteriores: -15 % con 6 mm) (prevision rapida: 2.5045 kg | 221.9 MPa | CS 0.97 | 0.139 mm)
- **Resultado (malla completa):** 2.5044 kg | 201.9 MPa | CS 1.06 | 0.139 mm (tension -15.2 %, masa +81 g)
- **Decision:** ACEPTADA - primera pieza que CUMPLE
- Descartada en la evaluacion rapida: [R4] collar de 4 mm en los pernos 1 y 3 -> pasa la evaluacion rapida (2.4652 kg | 232.7 MPa | CS 0.92 | 0.142 mm) pero otra es mas prometedora; se podra proponer de nuevo
- Nota: R5 (Alojamiento de la cabeza mas ancho con acuerdo de fondo mayor) desactivada: los datos la contradicen

<img src="galeria/20261123_194312_it001_ACEPTADA_2.504kg.jpg" width="520">

## Iteracion 0 - INICIO

*2026-11-23 19:40*

- **Resultado (malla completa):** 2.4234 kg | 238.0 MPa | CS 0.90 | 0.144 mm
- **Decision:** INICIO - NO cumple (238 MPa > 215): primero hay que reforzar donde esta el pico

<img src="galeria/20261123_194027_it000_INICIO_2.423kg.jpg" width="520">

