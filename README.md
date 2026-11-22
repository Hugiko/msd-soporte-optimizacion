# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 22:22 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 32 | 0 | - | en marcha |
| Refuerzo + vaciado | 36 | 4 | 2.510 kg (CS 1.18) | en marcha |
| Diseno desde cero | 32 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 32 descartados en la pasada rapida, 16 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 7 % | Refuerzo + vaciado: error tipico 1 % | Diseno desde cero: error tipico 3 %

## Mejor diseno actual

**2.5104 kg** (+3.59 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **181.7 MPa** &nbsp;|&nbsp; desplazamiento **0.125 mm** &nbsp;|&nbsp; coef. seguridad **1.18** &nbsp;|&nbsp; puntuacion **2.4997** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 029 &nbsp;|&nbsp; calculado 2026-11-22 22:06

> Mejora pequena (0.20 % sobre el ultimo registrado, 2.5153 kg): aun sin proyecto propio. El proyecto de Workbench y la entrada del historial se crean cuando la mejora acumulada llega al 0.01 %. Proyectos del ultimo registrado:

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 100 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 3 | 22/11 22:07 | 2.5104 kg | -0.00 % (punt.) | 181.7 MPa | 0.125 mm | Refuerzo + vaciado 029 | - | <img src="runs/opt_37800N/galeria/20261122_220734_refuerzo_029_VALIDO_2.510kg.jpg" width="320"> |
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | [Workbench](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | [Workbench](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Diseno desde cero | 032 | 2.255 | 393.2 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_222255_cero_032_NO_VALIDO_2.255kg.jpg) |
| Refuerzo + vaciado | 036 | 2.505 | 181.3 | cerca_del_limite | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); c | [ver](runs/opt_37800N/galeria/20261122_222209_refuerzo_036_CASI_2.505kg.jpg) |
| Vaciado del original | 032 | 2.406 | 211.9 | descartado | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_222009_vaciado_032_NO_VALIDO_2.406kg.jpg) |
| Refuerzo + vaciado | 035 | 0.000 | - | fallido | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut | [ver](runs/opt_37800N/galeria/20261122_221908_refuerzo_035_FALLO_0.000kg.jpg) |
| Refuerzo + vaciado | 034 | 0.000 | - | fallido | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut | [ver](runs/opt_37800N/galeria/20261122_221856_refuerzo_034_FALLO_0.000kg.jpg) |
| Diseno desde cero | 031 | 2.243 | 388.3 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_221842_cero_031_NO_VALIDO_2.243kg.jpg) |
| Refuerzo + vaciado | 033 | 2.487 | 183.1 | cerca_del_limite | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); c | [ver](runs/opt_37800N/galeria/20261122_221753_refuerzo_033_CASI_2.487kg.jpg) |
| Vaciado del original | 031 | 2.414 | 193.8 | cerca_del_limite | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_221552_vaciado_031_CASI_2.414kg.jpg) |
| Refuerzo + vaciado | 032 | 2.498 | 183.6 | cerca_del_limite | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); c | [ver](runs/opt_37800N/galeria/20261122_221453_refuerzo_032_CASI_2.498kg.jpg) |
| Refuerzo + vaciado | 031 | 2.490 | 183.2 | cerca_del_limite | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_ | [ver](runs/opt_37800N/galeria/20261122_221253_refuerzo_031_CASI_2.490kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
