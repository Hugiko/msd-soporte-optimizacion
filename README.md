# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 20:56 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 8 | 0 | - | en marcha |
| Refuerzo + vaciado | 7 | 0 | - | en marcha |
| Diseno desde cero | 7 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 7 descartados en la pasada rapida, 0 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: aun aprendiendo | Refuerzo + vaciado: aun aprendiendo | Diseno desde cero: aun aprendiendo

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 22 fichas.

## Arbol genealogico de la busqueda



Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 008 | 2.002 | 2392.5 | descartado | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205624_vaciado_008_NO_VALIDO_2.002kg.jpg) |
| Diseno desde cero | 007 | 0.972 | 1853.1 | descartado | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205540_cero_007_NO_VALIDO_0.972kg.jpg) |
| Refuerzo + vaciado | 007 | 1.971 | 331.5 | descartado | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205506_refuerzo_007_NO_VALIDO_1.971kg.jpg) |
| Vaciado del original | 007 | 1.845 | 635.7 | descartado | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205407_vaciado_007_NO_VALIDO_1.845kg.jpg) |
| Diseno desde cero | 006 | 1.490 | 1384.6 | descartado | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205316_cero_006_NO_VALIDO_1.490kg.jpg) |
| Refuerzo + vaciado | 006 | 2.409 | 302.8 | descartado | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205236_refuerzo_006_NO_VALIDO_2.409kg.jpg) |
| Vaciado del original | 006 | 2.404 | 310.6 | descartado | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205130_vaciado_006_NO_VALIDO_2.404kg.jpg) |
| Diseno desde cero | 005 | 1.415 | 1642.8 | descartado | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205031_cero_005_NO_VALIDO_1.415kg.jpg) |
| Refuerzo + vaciado | 005 | 2.195 | 618.0 | descartado | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204949_refuerzo_005_NO_VALIDO_2.195kg.jpg) |
| Vaciado del original | 005 | 2.300 | - | fallido | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204848_vaciado_005_FALLO_2.300kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
