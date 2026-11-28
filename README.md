# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 28/11/2026 17:10 &nbsp;|&nbsp; **Estado:** DETENIDO (al relanzar optimizar.bat continua) &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 78 | 26 | 4 | 34 | 11 | 124 |

## Mejor diseno

**2.1556 kg** (-11.1 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **193.7 MPa** &nbsp;|&nbsp; coef. seguridad **1.11** &nbsp;|&nbsp; desplazamiento **0.159 mm** &nbsp;|&nbsp; iteracion 77 &nbsp;|&nbsp; **malla fina: 209.4 MPa**

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
3. rebaje desde arriba hasta z = 9 mm en x 40..64, y -82..-66 mm (esquinas R3) (y su simetrico)
4. anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm)
5. ranura que une los aligeramientos de (42, -79) y (42, -67) (quita la pared fina entre ellos) (y su simetrico)
6. ranura que une los aligeramientos de (26, -72) y (18, -76) (quita la pared fina entre ellos) (y su simetrico)
7. aligeramiento pasante vertical D16 mm en (-26, -29) (y su simetrico)
8. aligeramiento pasante vertical D13 mm en (4, -74) (y su simetrico)
9. aligeramiento pasante vertical D13 mm en (4, -110) (y su simetrico)
10. aligeramiento pasante vertical D8 mm en (43, -44) (y su simetrico)
11. bolsillo en ranura desde la cara de apoyo, 21 mm de ancho, de (13, -54) a (7, -35), hasta z = 11 mm (techo a 45 grados) (y su simetrico)
12. bolsillo en ranura desde la cara de apoyo, 15 mm de ancho, de (23, -27) a (56, -28), hasta z = 6 mm (techo a 45 grados) (y su simetrico)
13. bolsillo en ranura desde la cara de apoyo, 8 mm de ancho, de (23, -38) a (29, -61), hasta z = 6 mm (techo a 45 grados) (y su simetrico)
14. bolsillo en ranura desde la cara de apoyo, 30 mm de ancho, de (-31, -94) a (-33, -57), hasta z = 12 mm (techo a 45 grados) (y su simetrico)

Ultimo hito verificado (2.156 kg, iteracion 77): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/17_it077_2.156kg/workbench/soporte_it077.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/17_it077_2.156kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_215434_it077_ACEPTADA_2.156kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 78 | ACEPTADA | R18 | agrandar: ranura que une los aligeramientos de (42, -79) y (42, -67) ( | 2.126 kg, 198 MPa | cumple y mejora al mejor (puntuacion 2.1556 -> 2.1263; masa 2.1556 -> 2.1263 kg) |
| 77 | ACEPTADA | R18 | agrandar: rebaje desde arriba hasta z = 9 mm en x 40..64, y -82..-66 m | 2.156 kg, 194 MPa | cumple y mejora al mejor (puntuacion 2.1581 -> 2.1556; masa 2.1581 -> 2.1556 kg) |
| 76 | RECHAZADA | R4 | collar de 6 mm en los pernos 4 y 2 | 2.235 kg, 193 MPa | cumple pero no mejora al mejor (puntuacion 2.2353 frente a 2.1581) |
| 75 | RECHAZADA | R4 | collar de 4 mm en los pernos 4 y 2 | 2.200 kg, 193 MPa | cumple pero no mejora al mejor (puntuacion 2.1999 frente a 2.1581) |
| 74 | ACEPTADA | R18 | agrandar: bolsillo en ranura desde la cara de apoyo, 30 mm de ancho, d | 2.158 kg, 198 MPa | cumple y mejora al mejor (puntuacion 2.1614 -> 2.1581; masa 2.1614 -> 2.1581 kg) |
| 73 | RECHAZADA | R7 | anillo de las orejetas hasta radio 23.1 mm (ligamento 13.5 mm) | 2.185 kg, 204 MPa | no cumple: 204.4 MPa con la malla normal, que corregidos a malla fina (x1.076) son 219.9 M |
| 72 | ACEPTADA | R18 | agrandar: aligeramiento pasante vertical D13 mm en (4, -110) (y su sim | 2.161 kg, 197 MPa | cumple y mejora al mejor (puntuacion 2.1876 -> 2.1614; masa 2.1876 -> 2.1614 kg) |
| 71 | REEVALUADA | - | pieza actual reconstruida | 2.188 kg, 194 MPa | cumple: se sigue optimizando con las reglas nuevas |
| 70 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |
| 69 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 68 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 28 x 64 mm, hasta z = 12 mm (techo a 4 | 2.078 kg, 195 MPa | cumple y mejora al mejor (puntuacion 2.0858 -> 2.0776; masa 2.0858 -> 2.0776 kg) |
| 67 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
