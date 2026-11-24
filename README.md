# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 20:33 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 70 | 22 | 4 | 31 | 11 | 111 |

## Mejor diseno

**2.0776 kg** (-14.3 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **195.2 MPa** &nbsp;|&nbsp; coef. seguridad **1.10** &nbsp;|&nbsp; desplazamiento **0.159 mm** &nbsp;|&nbsp; iteracion 68

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm, acampanado a 30 grados hasta z = 16 mm
3. rebaje desde arriba hasta z = 9 mm en x 42..62, y -80..-68 mm (esquinas R3) (y su simetrico)
4. aligeramiento pasante vertical D10 mm en (49, -56) (y su simetrico)
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
19. bolsillo desde la cara de apoyo 56 x 16 mm, hasta z = 6 mm (techo a 45 grados) en (35, -28) (y su simetrico)
20. aligeramiento pasante vertical D20 mm en (43, -68) (y su simetrico)
21. aligeramiento pasante vertical D16 mm en (37, -62) (y su simetrico)
22. aligeramiento pasante vertical D10 mm en (4, -110) (y su simetrico)
23. bolsillo desde la cara de apoyo 28 x 64 mm, hasta z = 12 mm (techo a 45 grados) en (-31, -76) (y su simetrico)

Ultimo hito verificado (2.086 kg, iteracion 66): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/13_it066_2.086kg/workbench/soporte_it066.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/13_it066_2.086kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261124_203221_it068_ACEPTADA_2.078kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 70 | SIN CAMBIO | - | - | - | ninguna regla encuentra ya una modificacion posible (no queda material ocioso donde quepa  |
| 69 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 68 | ACEPTADA | R14 | bolsillo desde la cara de apoyo 28 x 64 mm, hasta z = 12 mm (techo a 4 | 2.078 kg, 195 MPa | cumple y mejora al mejor (puntuacion 2.0858 -> 2.0776; masa 2.0858 -> 2.0776 kg) |
| 67 | SIN CAMBIO | - | - | - | todas las modificaciones propuestas se descartaron en la evaluacion rapida |
| 66 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (4, -110) (y su simetrico) | 2.086 kg, 197 MPa | cumple y mejora al mejor (puntuacion 2.1213 -> 2.0858; masa 2.1213 -> 2.0858 kg) |
| 65 | RECHAZADA | R1 | aligeramiento pasante vertical D10 mm en (1, -41) (y su simetrico) | 2.087 kg, 206 MPa | no cumple: 206.0 MPa con la malla normal, que corregidos a malla fina (x1.054) son 217.1 M |
| 64 | RECHAZADA | R2 | rebaje desde arriba hasta z = 5 mm en x -5..7, y -44..-24 mm (esquinas | 2.024 kg, 333 MPa | no cumple: 333.4 MPa con la malla normal, que corregidos a malla fina (x1.054) son 351.2 M |
| 63 | RECHAZADA | R2 | rebaje desde arriba hasta z = 5 mm en x -1..15, y -120..-104 mm (esqui | 2.015 kg, 293 MPa | no cumple: 293.5 MPa con la malla normal, que corregidos a malla fina (x1.054) son 309.2 M |
| 62 | RECHAZADA | R2 | rebaje desde arriba hasta z = 9 mm en x -9..11, y -44..-24 mm (esquina | 1.988 kg, 331 MPa | no cumple: 331.3 MPa con la malla normal, que corregidos a malla fina (x1.054) son 349.0 M |
| 61 | RECHAZADA | R4 | collar de 6 mm en los pernos 4 y 2 | 2.198 kg, 195 MPa | cumple pero no mejora al mejor (puntuacion 2.1984 frente a 2.1213) |
| 60 | RECHAZADA | R4 | collar de 4 mm en los pernos 4 y 2 | 2.163 kg, 197 MPa | cumple pero no mejora al mejor (puntuacion 2.1630 frente a 2.1213) |
| 59 | ACEPTADA | R1 | aligeramiento pasante vertical D16 mm en (37, -62) (y su simetrico) | 2.121 kg, 203 MPa | cumple y mejora al mejor (puntuacion 2.1806 -> 2.1213; masa 2.1806 -> 2.1213 kg) |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
