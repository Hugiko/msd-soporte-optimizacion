# Optimizacion del soporte guiada por reglas - panel en directo

> **Ultima actualizacion:** 23/11/2026 19:52 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga **42258 N** &nbsp;|&nbsp; limite **215 MPa** (coef. de seguridad >= 1.00, obligatorio) y 0.25 mm &nbsp;|&nbsp; acero S235

La pieza parte del **0.stp del enunciado** y se modifica paso a paso: en cada iteracion una **regla de diseno** (sacada del estudio de las soluciones publicadas y de nuestros calculos, ver [DESIGN_RULES.md](DESIGN_RULES.md)) propone anadir material donde esta el pico, quitarlo donde no trabaja o **crear formas nuevas** (nervios en la direccion principal de tension, dimensionados con la carga que llevan), siempre **con su porque**; se prueba en ANSYS y se acepta o se revierte. Objetivo: **minima masa** con la tension y el desplazamiento como limites obligatorios. Cada cambio esta en [ITERACIONES.md](runs/opt_42258N/ITERACIONES.md).

| iteraciones | aceptadas | inversiones | rechazadas | sin cambio | descartadas en la evaluacion rapida |
|---|---|---|---|---|---|
| 1 | 1 | 0 | 0 | 0 | 1 |

## Mejor diseno

**2.5044 kg** (+3.3 % frente al original, 2.423 kg) &nbsp;|&nbsp; tension **201.9 MPa** &nbsp;|&nbsp; coef. seguridad **1.06** &nbsp;|&nbsp; desplazamiento **0.139 mm** &nbsp;|&nbsp; iteracion 1 &nbsp;|&nbsp; **malla fina: 212.5 MPa**

Operaciones sobre el original:

1. collar de 6.0 mm alrededor del perno 1 hasta z = 22 mm
2. collar de 6.0 mm alrededor del perno 3 hasta z = 22 mm

Ultimo hito verificado (2.504 kg, iteracion 1): [Proyecto Workbench (.wbpz)](runs/opt_42258N/historial/01_it001_2.504kg/workbench/soporte_it001.wbpz) &nbsp;|&nbsp; [Geometria STEP](runs/opt_42258N/historial/01_it001_2.504kg/geometria.step)

![mejor diseno](runs/opt_42258N/galeria/20261123_194312_it001_ACEPTADA_2.504kg.jpg)

## Camino de la pieza

![camino](runs/opt_42258N/camino.png)

Grafico interactivo: [evolucion_interactiva.html](runs/opt_42258N/evolucion_interactiva.html) &nbsp;|&nbsp; [Galeria de todas las piezas](runs/opt_42258N/GALERIA.md) &nbsp;|&nbsp; [Hitos con proyecto Workbench](runs/opt_42258N/HISTORIAL.md)

## Ultimas iteraciones

| iteracion | decision | regla | modificacion | resultado | motivo |
|---|---|---|---|---|---|
| 1 | ACEPTADA | R4 | collar de 6 mm en los pernos 1 y 3 | 2.504 kg, 202 MPa | primera pieza que CUMPLE |
| 0 | INICIO | - | pieza del enunciado (0.stp) | 2.423 kg, 238 MPa | NO cumple (238 MPa > 215): primero hay que reforzar donde esta el pico |

---

**Como funciona:** estudio de las 381 soluciones publicadas (SimJEB) con nuestra carga -> reglas de diseno con datos -> el 0.stp se modifica paso a paso (cada cambio justificado por una regla) -> evaluacion rapida (malla gruesa) para descartar pronto -> evaluacion completa en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3) -> se acepta o se revierte. Hitos verificados con malla fina y con proyecto de Workbench (`.wbpz`: Workbench > File > Restore Archive).

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas estan en `estudio/calculos_anteriores.csv`.
