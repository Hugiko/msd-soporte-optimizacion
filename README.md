# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 14:07 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 35 | 12 | 1 | 14 | 6 | 45 |

## Mejor diseno

**2.2571 kg** (-6.9 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **202.1 MPa** &nbsp;|&nbsp; coef. seguridad **1.06** &nbsp;|&nbsp; desplazamiento **0.146 mm** &nbsp;|&nbsp; iteracion 29 &nbsp;|&nbsp; **malla fina: 213.8 MPa**

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm
3. rebaje desde arriba hasta z = 9 mm en x 42..62, y -80..-68 mm (esquinas R3) (y su simetrico)
4. aligeramiento pasante vertical D16 mm en (49, -56) (y su simetrico)
5. aligeramiento pasante vertical D12 mm en (4, -74) (y su simetrico)
6. aligeramiento pasante vertical D16 mm en (-26, -29) (y su simetrico)
7. aligeramiento pasante vertical D10 mm en (28, -74) (y su simetrico)
8. aligeramiento pasante vertical D10 mm en (19, -74) (y su simetrico)
9. aligeramiento pasante vertical D8 mm en (43, -44) (y su simetrico)
10. bolsillo desde la cara de apoyo 8 x 16 mm, hasta z = 12 mm (techo a 45 grados) en (14, -44) (y su simetrico)
11. bolsillo desde la cara de apoyo 28 x 24 mm, hasta z = 10 mm (techo a 45 grados) en (16, -100) (y su simetrico)
12. bolsillo desde la cara de apoyo 36 x 20 mm, hasta z = 7 mm (techo a 45 grados) en (20, -110) (y su simetrico)

Ultimo hito verificado (2.257 kg, iteracion 29): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/09_it029_2.257kg/workbench/soporte_it029.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/09_it029_2.257kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_131413_it029_REEVALUADA_2.257kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 35 | ACEPTADA | R1 | aligeramiento pasante vertical D8 mm en (37, -62) (y su simetrico) | 2.277 kg, 194 MPa | cumple y recupera parte de la inversion de la iteracion 33 (masa 2.3089 -> 2.2770 kg; el m |
| 34 | RECHAZADA | R14 | bolsillo desde la cara de apoyo 32 x 32 mm, hasta z = 14 mm (techo a 4 | 2.282 kg, 203 MPa | cumple pero no mejora al mejor (puntuacion 2.2822 frente a 2.2571) |
| 33 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |
| 32 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |
| 31 | INVERSION | R12 | acampanar la raiz de los collares (30 grados hasta z = 16 mm) | 2.309 kg, 191 MPa | refuerzo eficiente: compra 5.6 % de margen de tension con +52 g (2.3 % de masa); ese marge |
| 30 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 29 | REEVALUADA | - | pieza actual reconstruida | 2.257 kg, 202 MPa | cumple: se sigue optimizando con las reglas nuevas |
| 28 | RECHAZADA | R14 | bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 4 | 2.204 kg, 203 MPa | no cumple: 203.0 MPa con la malla normal, que corregidos a malla fina (x1.069) son 217.1 M |
| 27 | RECHAZADA | R13 | ventana pasante en x 6..38, y -80..-68 mm (esquinas R3) (y su simetric | 2.192 kg, 203 MPa | no cumple: 202.5 MPa con la malla normal, que corregidos a malla fina (x1.069) son 216.6 M |
| 26 | RECHAZADA | R2 | rebaje desde arriba hasta z = 5 mm en x -26..14, y -80..-68 mm (esquin | 2.202 kg, 203 MPa | no cumple: 202.6 MPa con la malla normal, que corregidos a malla fina (x1.069) son 216.7 M |
| 25 | RECHAZADA | R1 | aligeramiento pasante vertical D12 mm en (4, -32) (y su simetrico) | 2.183 kg, 208 MPa | no cumple: 207.9 MPa con la malla normal, que corregidos a malla fina (x1.069) son 222.3 M |
| 24 | RECHAZADA | R1 | aligeramiento pasante vertical D12 mm en (7, -116) (y su simetrico) | 2.183 kg, 205 MPa | no cumple: 205.3 MPa con la malla normal, que corregidos a malla fina (x1.069) son 219.6 M |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
