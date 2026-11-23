# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 24/11/2026 00:06 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 58 | 55 | 0 | 3 | 0 | 112 |

## Mejor diseno

**2.1608 kg** (-10.8 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **203.1 MPa** &nbsp;|&nbsp; coef. seguridad **1.06** &nbsp;|&nbsp; desplazamiento **0.155 mm** &nbsp;|&nbsp; iteracion 14 &nbsp;|&nbsp; **malla fina: 214.0 MPa**

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm
3. aligeramiento pasante vertical D12 mm en (40, -71)
4. rebaje desde arriba hasta z = 7 mm en x 54..66, y -124..-28 mm (esquinas R3)
5. rebaje desde arriba hasta z = 9 mm en x 42..54, y -100..-52 mm (esquinas R3)
6. aligeramiento pasante vertical D16 mm en (-20, -26)
7. aligeramiento pasante vertical D12 mm en (4, -74)
8. aligeramiento pasante vertical D10 mm en (40, -86)
9. aligeramiento pasante vertical D10 mm en (22, -71)
10. aligeramiento pasante vertical D8 mm en (40, -62)
11. aligeramiento pasante vertical D16 mm en (34, -74)
12. rebaje desde arriba hasta z = 5 mm en x 38..50, y -60..-44 mm (esquinas R3)
13. rebaje desde arriba hasta z = 7 mm en x -26..-10, y -124..-104 mm (esquinas R3.2)

Ultimo hito verificado (2.161 kg, iteracion 14): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/11_it014_2.161kg/workbench/soporte_it014.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/11_it014_2.161kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261123_210749_it014_ACEPTADA_2.161kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 58 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 57 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |
| 56 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 55 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |
| 54 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 53 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |
| 52 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 51 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |
| 50 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 49 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |
| 48 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (34, -83) | 2.131 kg, 208 MPa | cumple y mejora al mejor (puntuacion 2.1443 -> 2.1307; masa 2.1443 -> 2.1307 kg) |
| 47 | ACEPTADA | R1 | aligeramiento pasante vertical D10 mm en (43, -98) | 2.144 kg, 204 MPa | cumple y mejora al mejor (puntuacion 2.1608 -> 2.1443; masa 2.1608 -> 2.1443 kg) |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
