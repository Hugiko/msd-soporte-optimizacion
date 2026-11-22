# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 21:02 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 10 | 0 | - | en marcha |
| Refuerzo + vaciado | 10 | 0 | - | en marcha |
| Diseno desde cero | 10 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 10 descartados en la pasada rapida, 0 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: aun aprendiendo | Refuerzo + vaciado: aun aprendiendo | Diseno desde cero: aun aprendiendo

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 30 fichas.

## Arbol genealogico de la busqueda



Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Diseno desde cero | 010 | 1.297 | 1583.2 | descartado | reparto inicial (Sobol 10/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210235_cero_010_NO_VALIDO_1.297kg.jpg) |
| Refuerzo + vaciado | 010 | 2.357 | 911.5 | descartado | reparto inicial (Sobol 10/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210202_refuerzo_010_NO_VALIDO_2.357kg.jpg) |
| Vaciado del original | 010 | 0.000 | - | fallido | reparto inicial (Sobol 10/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210058_vaciado_010_FALLO_0.000kg.jpg) |
| Diseno desde cero | 009 | 1.765 | 612.1 | descartado | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210049_cero_009_NO_VALIDO_1.765kg.jpg) |
| Refuerzo + vaciado | 009 | 2.140 | 355.2 | descartado | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205941_refuerzo_009_NO_VALIDO_2.140kg.jpg) |
| Vaciado del original | 009 | 1.968 | 496.8 | descartado | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205841_vaciado_009_NO_VALIDO_1.968kg.jpg) |
| Diseno desde cero | 008 | 2.063 | 1174.5 | descartado | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205748_cero_008_NO_VALIDO_2.063kg.jpg) |
| Refuerzo + vaciado | 008 | 2.212 | 639.1 | descartado | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205715_refuerzo_008_NO_VALIDO_2.212kg.jpg) |
| Vaciado del original | 008 | 2.002 | 2392.5 | descartado | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205624_vaciado_008_NO_VALIDO_2.002kg.jpg) |
| Diseno desde cero | 007 | 0.972 | 1853.1 | descartado | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_205540_cero_007_NO_VALIDO_0.972kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
