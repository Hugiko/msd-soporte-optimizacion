# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 23/11/2026 07:12 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 67 | 0 | - | en marcha |
| Refuerzo + vaciado | 143 | 36 | 2.372 kg (CS 1.16) | en marcha |
| Diseno desde cero | 67 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 67 descartados en la pasada rapida, 32 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 4 % | Refuerzo + vaciado: error tipico 0 % | Diseno desde cero: error tipico 2 %

## Mejor diseno actual

**2.3720 kg** (-2.12 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **185.4 MPa** &nbsp;|&nbsp; desplazamiento **0.130 mm** &nbsp;|&nbsp; coef. seguridad **1.16** &nbsp;|&nbsp; puntuacion **2.3690** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 142 &nbsp;|&nbsp; calculado 2026-11-23 07:07 &nbsp;|&nbsp; **verificado con malla fina: 185.8 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/18_refuerzo_142_2.372kg/workbench/soporte_refuerzo_142.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/18_refuerzo_142_2.372kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/18_refuerzo_142_2.372kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261123_070858_refuerzo_142_VALIDO_2.372kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 277 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 19 | 23/11 07:08 | 2.3720 kg | -0.26 % (punt.) | 185.4 MPa | 0.130 mm | Refuerzo + vaciado 142 | [Workbench](runs/opt_37800N/historial/18_refuerzo_142_2.372kg/workbench/soporte_refuerzo_142.wbpz) | <img src="runs/opt_37800N/galeria/20261123_070858_refuerzo_142_VALIDO_2.372kg.jpg" width="320"> |
| 18 | 23/11 07:02 | 2.3777 kg | -0.55 % (punt.) | 185.6 MPa | 0.129 mm | Refuerzo + vaciado 140 | [Workbench](runs/opt_37800N/historial/17_refuerzo_140_2.378kg/workbench/soporte_refuerzo_140.wbpz) | <img src="runs/opt_37800N/galeria/20261123_070352_refuerzo_140_VALIDO_2.378kg.jpg" width="320"> |
| 17 | 23/11 06:48 | 2.3920 kg | -0.78 % (punt.) | 185.0 MPa | 0.129 mm | Refuerzo + vaciado 132 | [Workbench](runs/opt_37800N/historial/16_refuerzo_132_2.392kg/workbench/soporte_refuerzo_132.wbpz) | <img src="runs/opt_37800N/galeria/20261123_064945_refuerzo_132_VALIDO_2.392kg.jpg" width="320"> |
| 16 | 23/11 06:35 | 2.4121 kg | -0.33 % (punt.) | 184.3 MPa | 0.128 mm | Refuerzo + vaciado 127 | [Workbench](runs/opt_37800N/historial/15_refuerzo_127_2.412kg/workbench/soporte_refuerzo_127.wbpz) | <img src="runs/opt_37800N/galeria/20261123_063617_refuerzo_127_VALIDO_2.412kg.jpg" width="320"> |
| 15 | 23/11 06:14 | 2.4224 kg | -0.25 % (punt.) | 183.1 MPa | 0.128 mm | Refuerzo + vaciado 119 | [Workbench](runs/opt_37800N/historial/14_refuerzo_119_2.422kg/workbench/soporte_refuerzo_119.wbpz) | <img src="runs/opt_37800N/galeria/20261123_061509_refuerzo_119_VALIDO_2.422kg.jpg" width="320"> |
| 14 | 23/11 00:18 | 2.4278 kg | -0.26 % (punt.) | 183.5 MPa | 0.128 mm | Refuerzo + vaciado 085 | [Workbench](runs/opt_37800N/historial/13_refuerzo_085_2.428kg/workbench/soporte_refuerzo_085.wbpz) | <img src="runs/opt_37800N/galeria/20261123_001901_refuerzo_085_VALIDO_2.428kg.jpg" width="320"> |
| 13 | 22/11 23:51 | 2.4356 kg | -0.28 % (punt.) | 182.7 MPa | 0.128 mm | Refuerzo + vaciado 071 | [Workbench](runs/opt_37800N/historial/12_refuerzo_071_2.436kg/workbench/soporte_refuerzo_071.wbpz) | <img src="runs/opt_37800N/galeria/20261122_235224_refuerzo_071_VALIDO_2.436kg.jpg" width="320"> |
| 12 | 22/11 23:48 | 2.4427 kg | -0.42 % (punt.) | 182.6 MPa | 0.127 mm | Refuerzo + vaciado 070 | [Workbench](runs/opt_37800N/historial/11_refuerzo_070_2.443kg/workbench/soporte_refuerzo_070.wbpz) | <img src="runs/opt_37800N/galeria/20261122_234856_refuerzo_070_VALIDO_2.443kg.jpg" width="320"> |
| 11 | 22/11 23:37 | 2.4587 kg | -0.10 % (punt.) | 179.8 MPa | 0.127 mm | Refuerzo + vaciado 066 | [Workbench](runs/opt_37800N/historial/10_refuerzo_066_2.459kg/workbench/soporte_refuerzo_066.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233830_refuerzo_066_VALIDO_2.459kg.jpg" width="320"> |
| 10 | 22/11 23:34 | 2.4605 kg | -0.13 % (punt.) | 180.2 MPa | 0.127 mm | Refuerzo + vaciado 065 | [Workbench](runs/opt_37800N/historial/09_refuerzo_065_2.460kg/workbench/soporte_refuerzo_065.wbpz) | <img src="runs/opt_37800N/galeria/20261122_233451_refuerzo_065_VALIDO_2.460kg.jpg" width="320"> |
| 9 | 22/11 23:29 | 2.4635 kg | -0.98 % (punt.) | 180.3 MPa | 0.127 mm | Refuerzo + vaciado 063 | [Workbench](runs/opt_37800N/historial/08_refuerzo_063_2.463kg/workbench/soporte_refuerzo_063.wbpz) | <img src="runs/opt_37800N/galeria/20261122_232949_refuerzo_063_VALIDO_2.463kg.jpg" width="320"> |
| 8 | 22/11 23:10 | 2.4879 kg | -0.03 % (punt.) | 180.3 MPa | 0.126 mm | Refuerzo + vaciado 054 | [Workbench](runs/opt_37800N/historial/07_refuerzo_054_2.488kg/workbench/soporte_refuerzo_054.wbpz) | <img src="runs/opt_37800N/galeria/20261122_231112_refuerzo_054_VALIDO_2.488kg.jpg" width="320"> |
| 7 | 22/11 22:56 | 2.4885 kg | -0.17 % (punt.) | 180.4 MPa | 0.126 mm | Refuerzo + vaciado 049 | registrado | <img src="runs/opt_37800N/galeria/20261122_225746_refuerzo_049_VALIDO_2.488kg.jpg" width="320"> |
| 6 | 22/11 22:40 | 2.4937 kg | -0.20 % (punt.) | 179.8 MPa | 0.126 mm | Refuerzo + vaciado 043 | registrado | <img src="runs/opt_37800N/galeria/20261122_224143_refuerzo_043_VALIDO_2.494kg.jpg" width="320"> |
| 5 | 22/11 22:30 | 2.4929 kg | -0.27 % (punt.) | 182.6 MPa | 0.126 mm | Refuerzo + vaciado 039 | registrado | <img src="runs/opt_37800N/galeria/20261122_223109_refuerzo_039_VALIDO_2.493kg.jpg" width="320"> |
| 4 | 22/11 22:23 | 2.5048 kg | -0.36 % (punt.) | 180.0 MPa | 0.125 mm | Refuerzo + vaciado 037 | registrado | <img src="runs/opt_37800N/galeria/20261122_222449_refuerzo_037_VALIDO_2.505kg.jpg" width="320"> |
| 3 | 22/11 22:07 | 2.5104 kg | -0.00 % (punt.) | 181.7 MPa | 0.125 mm | Refuerzo + vaciado 029 | - | <img src="runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg" width="320"> |
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | registrado | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | registrado | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Refuerzo + vaciado | 143 | 2.357 | 186.8 | cerca_del_limite | [rama R1.1.1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.05 | [ver](runs/opt_37800N/galeria/20261123_071251_refuerzo_143_CASI_2.357kg.jpg) |
| Refuerzo + vaciado | 142 | 2.372 | 185.4 | valido | [rama R1.1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso  | [ver](runs/opt_37800N/galeria/20261123_070858_refuerzo_142_VALIDO_2.372kg.jpg) |
| Diseno desde cero | 067 | 2.264 | 380.6 | descartado | [rama C1.2] [aun sin disenos validos] pequeno cambio alrededor del mej | [ver](runs/opt_37800N/galeria/20261123_070711_cero_067_NO_VALIDO_2.264kg.jpg) |
| Refuerzo + vaciado | 141 | 2.379 | 185.9 | valido | [rama R1.1.1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.05 | [ver](runs/opt_37800N/galeria/20261123_070703_refuerzo_141_VALIDO_2.379kg.jpg) |
| Vaciado del original | 067 | 2.423 | 212.9 | descartado | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso ma | [ver](runs/opt_37800N/galeria/20261123_070600_vaciado_067_NO_VALIDO_2.423kg.jpg) |
| Refuerzo + vaciado | 140 | 2.378 | 185.6 | valido | [rama R1.1.1.1.1] varios pasos sin mejora: paso mas corto (0.05); camb | [ver](runs/opt_37800N/galeria/20261123_070352_refuerzo_140_VALIDO_2.378kg.jpg) |
| Refuerzo + vaciado | 139 | 2.404 | 183.9 | valido | [rama R1.1.1.1.1] varios pasos sin mejora: paso mas corto (0.05); camb | [ver](runs/opt_37800N/galeria/20261123_070159_refuerzo_139_VALIDO_2.404kg.jpg) |
| Diseno desde cero | 066 | 2.264 | 380.6 | descartado | [rama C1.2] [aun sin disenos validos] varios pasos sin mejora: paso ma | [ver](runs/opt_37800N/galeria/20261123_070057_cero_066_NO_VALIDO_2.264kg.jpg) |
| Refuerzo + vaciado | 138 | 2.383 | 185.1 | cerca_del_limite | [rama R1.1.1.1.1] pequeno cambio alrededor del mejor de la rama (paso  | [ver](runs/opt_37800N/galeria/20261123_070048_refuerzo_138_CASI_2.383kg.jpg) |
| Vaciado del original | 066 | 2.413 | 194.0 | cerca_del_limite | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mej | [ver](runs/opt_37800N/galeria/20261123_065851_vaciado_066_CASI_2.413kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
