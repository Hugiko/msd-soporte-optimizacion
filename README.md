# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 22:37 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 34 | 0 | - | en marcha |
| Refuerzo + vaciado | 41 | 6 | 2.493 kg (CS 1.18) | en marcha |
| Diseno desde cero | 33 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 33 descartados en la pasada rapida, 16 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 7 % | Refuerzo + vaciado: error tipico 1 % | Diseno desde cero: error tipico 3 %

## Mejor diseno actual

**2.4929 kg** (+2.87 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **182.6 MPa** &nbsp;|&nbsp; desplazamiento **0.126 mm** &nbsp;|&nbsp; coef. seguridad **1.18** &nbsp;|&nbsp; puntuacion **2.4841** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 039 &nbsp;|&nbsp; calculado 2026-11-22 22:29 &nbsp;|&nbsp; **verificado con malla fina: 182.3 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/workbench/soporte_refuerzo_039.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 108 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 5 | 22/11 22:30 | 2.4929 kg | -0.27 % (punt.) | 182.6 MPa | 0.126 mm | Refuerzo + vaciado 039 | [Workbench](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/workbench/soporte_refuerzo_039.wbpz) | <img src="runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg" width="320"> |
| 4 | 22/11 22:23 | 2.5048 kg | -0.36 % (punt.) | 180.0 MPa | 0.125 mm | Refuerzo + vaciado 037 | [Workbench](runs/opt_37800N/historial/03_refuerzo_037_2.505kg/workbench/soporte_refuerzo_037.wbpz) | <img src="runs/opt_37800N/galeria/20261122_222449_refuerzo_037_VALIDO_2.505kg.jpg" width="320"> |
| 3 | 22/11 22:07 | 2.5104 kg | -0.00 % (punt.) | 181.7 MPa | 0.125 mm | Refuerzo + vaciado 029 | - | <img src="runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg" width="320"> |
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | [Workbench](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | [Workbench](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 034 | 2.409 | 302.8 | descartado | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_223734_vaciado_034_NO_VALIDO_2.409kg.jpg) |
| Refuerzo + vaciado | 041 | 2.484 | 186.5 | cerca_del_limite | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); c | [ver](runs/opt_37800N/galeria/20261122_223618_refuerzo_041_CASI_2.484kg.jpg) |
| Refuerzo + vaciado | 040 | 0.000 | - | fallido | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.04); cambi | [ver](runs/opt_37800N/galeria/20261122_223425_refuerzo_040_FALLO_0.000kg.jpg) |
| Diseno desde cero | 033 | 2.260 | 403.8 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_223412_cero_033_NO_VALIDO_2.260kg.jpg) |
| Refuerzo + vaciado | 039 | 2.493 | 182.6 | valido | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); c | [ver](runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg) |
| Vaciado del original | 033 | 2.414 | 212.2 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_222908_vaciado_033_NO_VALIDO_2.414kg.jpg) |
| Refuerzo + vaciado | 038 | 2.384 | 414.3 | descartado | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.04); cambi | [ver](runs/opt_37800N/galeria/20261122_222810_refuerzo_038_NO_VALIDO_2.384kg.jpg) |
| Refuerzo + vaciado | 037 | 2.505 | 180.0 | valido | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); c | [ver](runs/opt_37800N/galeria/20261122_222449_refuerzo_037_VALIDO_2.505kg.jpg) |
| Diseno desde cero | 032 | 2.255 | 393.2 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_222255_cero_032_NO_VALIDO_2.255kg.jpg) |
| Refuerzo + vaciado | 036 | 2.505 | 181.3 | cerca_del_limite | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); c | [ver](runs/opt_37800N/galeria/20261122_222209_refuerzo_036_CASI_2.505kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
