# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 09:23 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 5 | 4 | 0 | 1 | 0 | 9 |

## Mejor diseno

**2.3827 kg** (-1.7 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **197.2 MPa** &nbsp;|&nbsp; coef. seguridad **1.09** &nbsp;|&nbsp; desplazamiento **0.142 mm** &nbsp;|&nbsp; iteracion 5

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm
3. rebaje desde arriba hasta z = 9 mm en x 42..62, y -80..-68 mm (esquinas R3) (y su simetrico)
4. aligeramiento pasante vertical D16 mm en (49, -56) (y su simetrico)
5. aligeramiento pasante vertical D12 mm en (4, -74) (y su simetrico)
6. aligeramiento pasante vertical D16 mm en (64, -32) (y su simetrico)

Ultimo hito verificado (2.399 kg, iteracion 4): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/02_it004_2.399kg/workbench/soporte_it004.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/02_it004_2.399kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_092340_it005_ACEPTADA_2.383kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 5 | ACEPTADA | R1 | aligeramiento pasante vertical D16 mm en (64, -32) (y su simetrico) | 2.383 kg, 197 MPa | cumple y mejora al mejor (puntuacion 2.3989 -> 2.3827; masa 2.3989 -> 2.3827 kg) |
| 4 | ACEPTADA | R1 | aligeramiento pasante vertical D12 mm en (4, -74) (y su simetrico) | 2.399 kg, 206 MPa | cumple y mejora al mejor (puntuacion 2.4281 -> 2.3989; masa 2.4281 -> 2.3989 kg) |
| 3 | ACEPTADA | R1 | aligeramiento pasante vertical D16 mm en (49, -56) (y su simetrico) | 2.428 kg, 206 MPa | cumple y mejora al mejor (puntuacion 2.4822 -> 2.4281; masa 2.4822 -> 2.4281 kg) |
| 2 | ACEPTADA | R2 | rebaje desde arriba hasta z = 9 mm en x 42..62, y -80..-68 mm (esquina | 2.482 kg, 201 MPa | cumple y mejora al mejor (puntuacion 2.5044 -> 2.4822; masa 2.5044 -> 2.4822 kg) |
| 1 | RECHAZADA | R1 | aligeramiento pasante vertical D12 mm en (40, -71) (y su simetrico) | 2.460 kg, 208 MPa | no cumple: 207.8 MPa con la malla normal, que corregidos a malla fina (x1.041) son 216.3 M |
| 0 | INICIO | - | pieza SIMETRICA de partida: original + collares de 6 mm en los pernos  | 2.504 kg, 202 MPa | cumple: se sigue quitando material donde no trabaja |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
