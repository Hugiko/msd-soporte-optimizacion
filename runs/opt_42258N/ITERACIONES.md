# Registro de iteraciones (changelog de la pieza)

Carga 42258 N | limite 215 MPa (coef. de seguridad >= 1.00) y 0.25 mm | reglas: [DESIGN_RULES.md](../../DESIGN_RULES.md) | la mas reciente arriba

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

