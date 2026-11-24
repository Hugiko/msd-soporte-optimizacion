# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 19:06 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 51 | 17 | 3 | 21 | 8 | 75 |

## Mejor diseno

**2.2207 kg** (-8.4 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **201.1 MPa** &nbsp;|&nbsp; coef. seguridad **1.07** &nbsp;|&nbsp; desplazamiento **0.150 mm** &nbsp;|&nbsp; iteracion 47 &nbsp;|&nbsp; **malla fina: 211.9 MPa**

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
18. bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 45 grados) en (9, -40) (y su simetrico)

Ultimo hito verificado (2.221 kg, iteracion 47): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/10_it047_2.221kg/workbench/soporte_it047.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/10_it047_2.221kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_184402_it047_ACEPTADA_2.221kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 51 | RECHAZADA | R1 | aligeramiento pasante vertical D10 mm en (37, -86) (y su simetrico) | 2.172 kg, 249 MPa | no cumple: 249.4 MPa con la malla normal, que corregidos a malla fina (x1.058) son 263.8 M |
| 50 | RECHAZADA | R2 | rebaje desde arriba hasta z = 5 mm en x -1..11, y -124..-112 mm (esqui | 2.162 kg, 215 MPa | no cumple: 215.3 MPa con la malla normal, que corregidos a malla fina (x1.058) son 227.8 M |
| 49 | RECHAZADA | R14 | bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 4 | 2.194 kg, 207 MPa | no cumple: 206.8 MPa con la malla normal, que corregidos a malla fina (x1.058) son 218.8 M |
| 48 | RECHAZADA | R14 | bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 4 | 2.199 kg, 207 MPa | no cumple: 207.3 MPa con la malla normal, que corregidos a malla fina (x1.058) son 219.3 M |
| 47 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 28 x 32 mm, hasta z = 12 mm (techo a 4 | 2.221 kg, 201 MPa | cumple y mejora al mejor (puntuacion 2.2362 -> 2.2207; masa 2.2362 -> 2.2207 kg) |
| 46 | RECHAZADA | R1 | aligeramiento pasante vertical D20 mm en (7, -116) (y su simetrico) | 2.081 kg, 292 MPa | no cumple: 292.4 MPa con la malla normal, que corregidos a malla fina (x1.058) son 309.3 M |
| 45 | RECHAZADA | R1 | aligeramiento pasante vertical D24 mm en (4, -32) (y su simetrico) | 2.024 kg, 594 MPa | no cumple: 594.1 MPa con la malla normal, que corregidos a malla fina (x1.058) son 628.4 M |
| 44 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 43 | ACEPTADA | R3 | hueco interior 12 x 16 x 8 mm (techo a 45 grados + evacuacion D5) en ( | 2.236 kg, 201 MPa | cumple y mejora al mejor (puntuacion 2.2433 -> 2.2362; masa 2.2433 -> 2.2362 kg) |
| 42 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 24 x 32 mm, hasta z = 10 mm (techo a 4 | 2.243 kg, 200 MPa | cumple y mejora al mejor (puntuacion 2.2514 -> 2.2433; masa 2.2514 -> 2.2433 kg) |
| 41 | ACEPTADA | R1 | aligeramiento pasante vertical D12 mm en (34, -77) (y su simetrico) | 2.251 kg, 200 MPa | cumple y mejora al mejor (puntuacion 2.2571 -> 2.2514; masa 2.2571 -> 2.2514 kg) |
| 40 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
