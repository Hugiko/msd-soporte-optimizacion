# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 23/11/2026 06:18 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 59 | 0 | - | en marcha |
| Refuerzo + vaciado | 119 | 23 | 2.422 kg (CS 1.17) | en marcha |
| Diseno desde cero | 59 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 59 descartados en la pasada rapida, 27 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 4 % | Refuerzo + vaciado: error tipico 18 % | Diseno desde cero: error tipico 2 %

## Mejor diseno actual

**2.4224 kg** (-0.04 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **183.1 MPa** &nbsp;|&nbsp; desplazamiento **0.128 mm** &nbsp;|&nbsp; coef. seguridad **1.17** &nbsp;|&nbsp; puntuacion **2.4148** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 119 &nbsp;|&nbsp; calculado 2026-11-23 06:13 &nbsp;|&nbsp; **verificado con malla fina: 183.3 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/14_refuerzo_119_2.422kg/workbench/soporte_refuerzo_119.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/14_refuerzo_119_2.422kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/14_refuerzo_119_2.422kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261123_061509_refuerzo_119_VALIDO_2.422kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 237 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 15 | 23/11 06:14 | 2.4224 kg | -0.25 % (punt.) | 183.1 MPa | 0.128 mm | Refuerzo + vaciado 119 | [Workbench](runs/opt_37800N/historial/14_refuerzo_119_2.422kg/workbench/soporte_refuerzo_119.wbpz) | <img src="runs/opt_37800N/galeria/20261123_061509_refuerzo_119_VALIDO_2.422kg.jpg" width="320"> |
| 14 | 23/11 00:18 | 2.4278 kg | -0.26 % (punt.) | 183.5 MPa | 0.128 mm | Refuerzo + vaciado 085 | [Workbench](runs/opt_37800N/historial/13_refuerzo_085_2.428kg/workbench/soporte_refuerzo_085.wbpz) | <img src="runs/opt_37800N/galeria/20261123_001901_refuerzo_085_VALIDO_2.428kg.jpg" width="320"> |
| 13 | 22/11 23:51 | 2.4356 kg | -0.28 % (punt.) | 182.7 MPa | 0.128 mm | Refuerzo + vaciado 071 | [Workbench](runs/opt_37800N/historial/12_refuerzo_071_2.436kg/workbench/soporte_refuerzo_071.wbpz) | <img src="runs/opt_37800N/galeria/20261122_235224_refuerzo_071_VALIDO_2.436kg.jpg" width="320"> |
| 12 | 22/11 23:48 | 2.4427 kg | -0.42 % (punt.) | 182.6 MPa | 0.127 mm | Refuerzo + vaciado 070 | [Workbench](runs/opt_37800N/historial/11_refuerzo_070_2.443kg/workbench/soporte_refuerzo_070.wbpz) | <img src="runs/opt_37800N/galeria/20261122_234856_refuerzo_070_VALIDO_2.443kg.jpg" width="320"> |
| 11 | 22/11 23:37 | 2.4587 kg | -0.10 % (punt.) | 179.8 MPa | 0.127 mm | Refuerzo + vaciado 066 | [Workbench](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/workbench/soporte_refuerzo_066.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233830_refuerzo_066_VALIDO_2.459kg.jpg" width="320"> |
| 10 | 22/11 23:34 | 2.4605 kg | -0.13 % (punt.) | 180.2 MPa | 0.127 mm | Refuerzo + vaciado 065 | [Workbench](runs/opt_37800N/historial/09_refuerzo_065_2.460kg/workbench/soporte_refuerzo_065.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233451_refuerzo_065_VALIDO_2.460kg.jpg" width="320"> |
| 9 | 22/11 23:29 | 2.4635 kg | -0.98 % (punt.) | 180.3 MPa | 0.127 mm | Refuerzo + vaciado 063 | [Workbench](runs/opt_37800N/historial/08_refuerzo_063_2.463kg/workbench/soporte_refuerzo_063.wbpz) | <img src="runs/opt_37800N/galeria/20261122_232949_refuerzo_063_VALIDO_2.463kg.jpg" width="320"> |
| 8 | 22/11 23:10 | 2.4879 kg | -0.03 % (punt.) | 180.3 MPa | 0.126 mm | Refuerzo + vaciado 054 | [Workbench](runs/opt_37800N/historial/07_refuerzo_054_2.488kg/workbench/soporte_refuerzo_054.wbpz) | <img src="runs/opt_37800N/galeria/20261122_231112_refuerzo_054_VALIDO_2.488kg.jpg" width="320"> |
| 7 | 22/11 22:56 | 2.4885 kg | -0.17 % (punt.) | 180.4 MPa | 0.126 mm | Refuerzo + vaciado 049 | [Workbench](runs/opt_37800N/historial/06_refuerzo_049_2.488kg/workbench/soporte_refuerzo_049.wbpz) | <img src="runs/opt_37800N/galeria/20261122_225746_refuerzo_049_VALIDO_2.488kg.jpg" width="320"> |
| 6 | 22/11 22:40 | 2.4937 kg | -0.20 % (punt.) | 179.8 MPa | 0.126 mm | Refuerzo + vaciado 043 | [Workbench](runs/opt_37800N/historial/05_refuerzo_043_2.494kg/workbench/soporte_refuerzo_043.wbpz) | <img src="runs/opt_37800N/galeria/20261122_224143_refuerzo_043_VALIDO_2.494kg.jpg" width="320"> |
| 5 | 22/11 22:30 | 2.4929 kg | -0.27 % (punt.) | 182.6 MPa | 0.126 mm | Refuerzo + vaciado 039 | [Workbench](runs/opt_37800N/historial/04_refuerzo_039_2.493kg/workbench/soporte_refuerzo_039.wbpz) | <img src="runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg" width="320"> |
| 4 | 22/11 22:23 | 2.5048 kg | -0.36 % (punt.) | 180.0 MPa | 0.125 mm | Refuerzo + vaciado 037 | registrado | <img src="runs/opt_37800N/galeria/20261122_222449_refuerzo_037_VALIDO_2.505kg.jpg" width="320"> |
| 3 | 22/11 22:07 | 2.5104 kg | -0.00 % (punt.) | 181.7 MPa | 0.125 mm | Refuerzo + vaciado 029 | - | <img src="runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg" width="320"> |
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | registrado | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | registrado | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Refuerzo + vaciado | 119 | 2.422 | 183.1 | valido | [rama R1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0. | [ver](runs/opt_37800N/galeria/20261123_061509_refuerzo_119_VALIDO_2.422kg.jpg) |
| Refuerzo + vaciado | 118 | 2.450 | 182.4 | valido | [rama R1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0. | [ver](runs/opt_37800N/galeria/20261123_061316_refuerzo_118_VALIDO_2.450kg.jpg) |
| Diseno desde cero | 059 | 2.264 | 380.6 | descartado | [rama C1.2] [aun sin disenos validos] el ultimo paso mejoro: sigue en  | [ver](runs/opt_37800N/galeria/20261123_061215_cero_059_NO_VALIDO_2.264kg.jpg) |
| Refuerzo + vaciado | 117 | 2.393 | 184.8 | cerca_del_limite | [rama R1.1.1.1] varios pasos sin mejora: paso mas corto (0.10); cambia | [ver](runs/opt_37800N/galeria/20261123_061206_refuerzo_117_CASI_2.393kg.jpg) |
| Vaciado del original | 059 | 2.400 | 200.8 | cerca_del_limite | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso ma | [ver](runs/opt_37800N/galeria/20261123_061031_vaciado_059_CASI_2.400kg.jpg) |
| Refuerzo + vaciado | 116 | 2.401 | 184.5 | cerca_del_limite | [rama R1.1.1.1] varios pasos sin mejora: paso mas corto (0.10); cambia | [ver](runs/opt_37800N/galeria/20261123_060917_refuerzo_116_CASI_2.401kg.jpg) |
| Refuerzo + vaciado | 115 | 2.409 | 188.7 | cerca_del_limite | [rama R1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0. | [ver](runs/opt_37800N/galeria/20261123_060739_refuerzo_115_CASI_2.409kg.jpg) |
| Diseno desde cero | 058 | 2.264 | 380.6 | descartado | [rama C1.2] [aun sin disenos validos] pequeno cambio alrededor del mej | [ver](runs/opt_37800N/galeria/20261123_060642_cero_058_NO_VALIDO_2.264kg.jpg) |
| Refuerzo + vaciado | 114 | 2.409 | 446.3 | descartado | [rama R1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0. | [ver](runs/opt_37800N/galeria/20261123_060603_refuerzo_114_NO_VALIDO_2.409kg.jpg) |
| Vaciado del original | 058 | 2.360 | 208.9 | descartado | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mej | [ver](runs/opt_37800N/galeria/20261123_060509_vaciado_058_NO_VALIDO_2.360kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
