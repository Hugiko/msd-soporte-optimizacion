# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 22:02 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 27 | 0 | - | en marcha |
| Refuerzo + vaciado | 27 | 3 | 2.515 kg (CS 1.20) | en marcha |
| Diseno desde cero | 27 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 27 descartados en la pasada rapida, 13 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 9 % | Refuerzo + vaciado: error tipico 1 % | Diseno desde cero: error tipico 3 %

## Mejor diseno actual

**2.5153 kg** (+3.79 % de masa frente al original, 2.423 kg con el mismo modelo) &nbsp;|&nbsp; tension **179.4 MPa** &nbsp;|&nbsp; desplazamiento **0.125 mm** &nbsp;|&nbsp; coef. seguridad **1.20** &nbsp;|&nbsp; puntuacion **2.4998** &nbsp;|&nbsp; Refuerzo + vaciado, diseno 027 &nbsp;|&nbsp; calculado 2026-11-22 21:57 &nbsp;|&nbsp; **verificado con malla fina: 186.7 MPa**

[Proyecto Workbench (.wbpz)](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) &nbsp;|&nbsp; [Modelo APDL](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/modelo_apdl.zip) &nbsp;|&nbsp; [Geometria STEP](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/geometria.step)

![mejor diseno](runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg)

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 81 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Historial de mejoras (todas; la mas reciente arriba)

| n | hora | masa | mejora | tension | desplaz. | familia / diseno | proyecto | ficha |
|---|---|---|---|---|---|---|---|---|
| 2 | 22/11 21:58 | 2.5153 kg | -0.51 % (punt.) | 179.4 MPa | 0.125 mm | Refuerzo + vaciado 027 | [Workbench](runs/opt_37800N/historial/02_refuerzo_027_2.515kg/workbench/soporte_refuerzo_027.wbpz) | <img src="runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg" width="320"> |
| 1 | 22/11 21:47 | 2.5278 kg | - | 179.6 MPa | 0.124 mm | Refuerzo + vaciado 023 | [Workbench](runs/opt_37800N/historial/01_refuerzo_023_2.528kg/workbench/soporte_refuerzo_023.wbpz) | <img src="runs/opt_37800N/galeria/20261122_214808_refuerzo_023_VALIDO_2.528kg.jpg" width="320"> |

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Diseno desde cero | 027 | 2.248 | 391.8 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_220208_cero_027_NO_VALIDO_2.248kg.jpg) |
| Refuerzo + vaciado | 027 | 2.515 | 179.4 | valido | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_ | [ver](runs/opt_37800N/galeria/20261122_215923_refuerzo_027_VALIDO_2.515kg.jpg) |
| Vaciado del original | 027 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_215744_vaciado_027_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 026 | 2.330 | 434.9 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_215735_cero_026_NO_VALIDO_2.330kg.jpg) |
| Refuerzo + vaciado | 026 | 2.492 | - | fallido | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia t_col | [ver](runs/opt_37800N/galeria/20261122_215654_refuerzo_026_FALLO_2.492kg.jpg) |
| Vaciado del original | 026 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_215607_vaciado_026_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 025 | 2.273 | 389.6 | descartado | [rama C1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_215555_cero_025_NO_VALIDO_2.273kg.jpg) |
| Refuerzo + vaciado | 025 | 2.528 | 179.6 | valido | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); c | [ver](runs/opt_37800N/galeria/20261122_215515_refuerzo_025_VALIDO_2.528kg.jpg) |
| Vaciado del original | 025 | 2.423 | 213.2 | descartado | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_215505_vaciado_025_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 024 | 2.326 | 447.6 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_215413_cero_024_NO_VALIDO_2.326kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
