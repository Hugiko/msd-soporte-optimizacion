# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 18:30 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 43 | 16 | 3 | 15 | 7 | 60 |

## Mejor diseno

**2.2362 kg** (-7.7 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **200.9 MPa** &nbsp;|&nbsp; coef. seguridad **1.07** &nbsp;|&nbsp; desplazamiento **0.149 mm** &nbsp;|&nbsp; iteracion 43

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
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
13. bolsillo desde la cara de apoyo 32 x 28 mm, hasta z = 12 mm (techo a 45 grados) en (18, -94) (y su simetrico)
14. anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm)
15. aligeramiento pasante vertical D12 mm en (34, -77) (y su simetrico)
16. bolsillo desde la cara de apoyo 24 x 32 mm, hasta z = 10 mm (techo a 45 grados) en (11, -104) (y su simetrico)
17. hueco interior 12 x 16 x 8 mm (techo a 45 grados + evacuacion D5) en (9, -44) (y su simetrico)

Ultimo hito verificado (2.257 kg, iteracion 29): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/09_it029_2.257kg/workbench/soporte_it029.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/09_it029_2.257kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_183013_it043_ACEPTADA_2.236kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 43 | ACEPTADA | R3 | hueco interior 12 x 16 x 8 mm (techo a 45 grados + evacuacion D5) en ( | 2.236 kg, 201 MPa | cumple y mejora al mejor (puntuacion 2.2433 -> 2.2362; masa 2.2433 -> 2.2362 kg) |
| 42 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 24 x 32 mm, hasta z = 10 mm (techo a 4 | 2.243 kg, 200 MPa | cumple y mejora al mejor (puntuacion 2.2514 -> 2.2433; masa 2.2514 -> 2.2433 kg) |
| 41 | ACEPTADA | R1 | aligeramiento pasante vertical D12 mm en (34, -77) (y su simetrico) | 2.251 kg, 200 MPa | cumple y mejora al mejor (puntuacion 2.2571 -> 2.2514; masa 2.2571 -> 2.2514 kg) |
| 40 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 39 | INVERSION | R7 | anillo de las orejetas hasta radio 20.1 mm (ligamento 10.5 mm) | 2.302 kg, 194 MPa | refuerzo eficiente: compra 4.2 % de margen de tension con +15 g (0.7 % de masa); ese marge |
| 38 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 32 x 28 mm, hasta z = 12 mm (techo a 4 | 2.287 kg, 202 MPa | cumple y recupera parte de la inversion de la iteracion 37 (masa 2.3089 -> 2.2868 kg; el m |
| 37 | INVERSION | R12 | acampanar la raiz de los collares (30 grados hasta z = 16 mm) | 2.309 kg, 191 MPa | refuerzo eficiente: compra 5.6 % de margen de tension con +52 g (2.3 % de masa); ese marge |
| 36 | RECHAZADA | R1 | aligeramiento pasante vertical D12 mm en (-17, -74) (y su simetrico) | 2.257 kg, 600 MPa | no cumple: 600.3 MPa con la malla normal, que corregidos a malla fina (x1.058) son 635.0 M |
| 35 | ACEPTADA | R1 | aligeramiento pasante vertical D8 mm en (37, -62) (y su simetrico) | 2.277 kg, 194 MPa | cumple y recupera parte de la inversion de la iteracion 33 (masa 2.3089 -> 2.2770 kg; el m |
| 34 | RECHAZADA | R14 | bolsillo desde la cara de apoyo 32 x 32 mm, hasta z = 14 mm (techo a 4 | 2.282 kg, 203 MPa | cumple pero no mejora al mejor (puntuacion 2.2822 frente a 2.2571) |
| 33 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |
| 32 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
