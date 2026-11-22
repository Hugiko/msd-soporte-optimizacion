# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 21:55 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 25 | 0 | - | en marcha |
| Refuerzo + vaciado | 25 | 2 | 2.528 kg (CS 1.20) | en marcha |
| Diseno desde cero | 25 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 25 descartados en la pasada rapida, 11 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 9 % | Refuerzo + vaciado: error tipico 1 % | Diseno desde cero: error tipico 3 %

## Mejor diseno actual

**2.5278 kg** (+4.31 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **179.6 MPa** &nbsp;|&nbsp; desplazamiento **0.124 mm** &nbsp;|&nbsp; coef. seguridad **1.20** &nbsp;|&nbsp; puntuacion **2.5126** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 023 &nbsp;|&nbsp; calculado 2026-11-22 21:46 &nbsp;|&nbsp; **verificado con malla fina: 186.9 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 75 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | [Workbench](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Diseno desde cero | 025 | 2.273 | 389.6 | descartado | [rama C1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_215555_cero_025_NO_VALIDO_2.273kg.jpg) |
| Refuerzo + vaciado | 025 | 2.528 | 179.6 | valido | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); c | [ver](runs/opt_37800N/galeria/20261122_215515_refuerzo_025_VALIDO_2.528kg.jpg) |
| Vaciado del original | 025 | 2.423 | 213.2 | descartado | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_215505_vaciado_025_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 024 | 2.326 | 447.6 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_215413_cero_024_NO_VALIDO_2.326kg.jpg) |
| Refuerzo + vaciado | 024 | 2.499 | 185.9 | cerca_del_limite | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambi | [ver](runs/opt_37800N/galeria/20261122_215333_refuerzo_024_CASI_2.499kg.jpg) |
| Vaciado del original | 024 | 2.422 | 200.5 | cerca_del_limite | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_215154_vaciado_024_CASI_2.422kg.jpg) |
| Diseno desde cero | 023 | 2.467 | 595.9 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_215101_cero_023_NO_VALIDO_2.467kg.jpg) |
| Refuerzo + vaciado | 023 | 2.528 | 179.6 | valido | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg) |
| Vaciado del original | 023 | 2.423 | 213.1 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_214629_vaciado_023_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 022 | 2.459 | 433.7 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_214539_cero_022_NO_VALIDO_2.459kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
