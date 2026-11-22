# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 23:46 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 43 | 0 | - | en marcha |
| Refuerzo + vaciado | 69 | 16 | 2.459 kg (CS 1.20) | en marcha |
| Diseno desde cero | 42 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 42 descartados en la pasada rapida, 19 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 5 % | Refuerzo + vaciado: error tipico 2 % | Diseno desde cero: error tipico 2 %

## Mejor diseno actual

**2.4587 kg** (+1.46 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **179.8 MPa** &nbsp;|&nbsp; desplazamiento **0.127 mm** &nbsp;|&nbsp; coef. seguridad **1.20** &nbsp;|&nbsp; puntuacion **2.4443** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 066 &nbsp;|&nbsp; calculado 2026-11-22 23:36 &nbsp;|&nbsp; **verificado con malla fina: 185.0 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/workbench/soporte_refuerzo_066.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261122_233830_refuerzo_066_VALIDO_2.459kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 154 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 11 | 22/11 23:37 | 2.4587 kg | -0.10 % (punt.) | 179.8 MPa | 0.127 mm | Refuerzo + vaciado 066 | [Workbench](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/workbench/soporte_refuerzo_066.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233830_refuerzo_066_VALIDO_2.459kg.jpg" width="320"> |
| 10 | 22/11 23:34 | 2.4605 kg | -0.13 % (punt.) | 180.2 MPa | 0.127 mm | Refuerzo + vaciado 065 | [Workbench](runs/opt_37800N/historial/09_refuerzo_065_2.460kg/workbench/soporte_refuerzo_065.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233451_refuerzo_065_VALIDO_2.460kg.jpg" width="320"> |
| 9 | 22/11 23:29 | 2.4635 kg | -0.98 % (punt.) | 180.3 MPa | 0.127 mm | Refuerzo + vaciado 063 | [Workbench](runs/opt_37800N/historial/08_refuerzo_063_2.463kg/workbench/soporte_refuerzo_063.wbpz) | <img src="runs/opt_37800N/galeria/20261122_232949_refuerzo_063_VALIDO_2.463kg.jpg" width="320"> |
| 8 | 22/11 23:10 | 2.4879 kg | -0.03 % (punt.) | 180.3 MPa | 0.126 mm | Refuerzo + vaciado 054 | [Workbench](runs/opt_37800N/historial/07_refuerzo_054_2.488kg/workbench/soporte_refuerzo_054.wbpz) | <img src="runs/opt_37800N/galeria/20261122_231112_refuerzo_054_VALIDO_2.488kg.jpg" width="320"> |
| 7 | 22/11 22:56 | 2.4885 kg | -0.17 % (punt.) | 180.4 MPa | 0.126 mm | Refuerzo + vaciado 049 | [Workbench](runs/opt_37800N/historial/06_refuerzo_049_2.488kg/workbench/soporte_refuerzo_049.wbpz) | <img src="runs/opt_37800N/galeria/20261122_225746_refuerzo_049_VALIDO_2.488kg.jpg" width="320"> |
| 6 | 22/11 22:40 | 2.4937 kg | -0.20 % (punt.) | 179.8 MPa | 0.126 mm | Refuerzo + vaciado 043 | [Workbench](runs/opt_37800N/historial/05_refuerzo_043_2.494kg/workbench/soporte_refuerzo_043.wbpz) | <img src="runs/opt_37800N/galeria/20261122_224143_refuerzo_043_VALIDO_2.494kg.jpg" width="320"> |
| 5 | 22/11 22:30 | 2.4929 kg | -0.27 % (punt.) | 182.6 MPa | 0.126 mm | Refuerzo + vaciado 039 | [Workbench](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/workbench/soporte_refuerzo_039.wbpz) | <img src="runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg" width="320"> |
| 4 | 22/11 22:23 | 2.5048 kg | -0.36 % (punt.) | 180.0 MPa | 0.125 mm | Refuerzo + vaciado 037 | [Workbench](runs/opt_37800N/historial/03_refuerzo_037_2.505kg/workbench/soporte_refuerzo_037.wbpz) | <img src="runs/opt_37800N/galeria/20261122_222449_refuerzo_037_VALIDO_2.505kg.jpg" width="320"> |
| 3 | 22/11 22:07 | 2.5104 kg | -0.00 % (punt.) | 181.7 MPa | 0.125 mm | Refuerzo + vaciado 029 | - | <img src="runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg" width="320"> |
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | [Workbench](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | [Workbench](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Refuerzo + vaciado | 069 | 2.444 | 182.8 | cerca_del_limite | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.20); cambia t | [ver](runs/opt_37800N/galeria/20261122_234638_refuerzo_069_CASI_2.444kg.jpg) |
| Vaciado del original | 043 | 2.408 | 197.9 | cerca_del_limite | [rama V1.1] [aun sin disenos validos] rama nueva (fina, paso 0.10) des | [ver](runs/opt_37800N/galeria/20261122_234501_vaciado_043_CASI_2.408kg.jpg) |
| Refuerzo + vaciado | 068 | 2.440 | 182.0 | cerca_del_limite | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20 | [ver](runs/opt_37800N/galeria/20261122_234411_refuerzo_068_CASI_2.440kg.jpg) |
| Refuerzo + vaciado | 067 | 2.452 | 179.6 | cerca_del_limite | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20 | [ver](runs/opt_37800N/galeria/20261122_234238_refuerzo_067_CASI_2.452kg.jpg) |
| Diseno desde cero | 042 | 2.256 | 415.9 | descartado | [rama C1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_234103_cero_042_NO_VALIDO_2.256kg.jpg) |
| Refuerzo + vaciado | 066 | 2.459 | 179.8 | valido | [rama R1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.10); c | [ver](runs/opt_37800N/galeria/20261122_233830_refuerzo_066_VALIDO_2.459kg.jpg) |
| Vaciado del original | 042 | 2.414 | 193.8 | cerca_del_limite | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_233654_vaciado_042_CASI_2.414kg.jpg) |
| Refuerzo + vaciado | 065 | 2.460 | 180.2 | valido | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10 | [ver](runs/opt_37800N/galeria/20261122_233451_refuerzo_065_VALIDO_2.460kg.jpg) |
| Refuerzo + vaciado | 064 | 2.456 | 185.7 | valido | [rama R1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.10); c | [ver](runs/opt_37800N/galeria/20261122_233316_refuerzo_064_VALIDO_2.456kg.jpg) |
| Diseno desde cero | 041 | 2.250 | 393.0 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_233223_cero_041_NO_VALIDO_2.250kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
