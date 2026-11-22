# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 20:48 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 5 | 0 | - | en marcha |
| Refuerzo + vaciado | 4 | 0 | - | en marcha |
| Diseno desde cero | 4 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 4 descartados en la pasada rapida, 0 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: aun aprendiendo | Refuerzo + vaciado: aun aprendiendo | Diseno desde cero: aun aprendiendo

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 13 fichas.

## Arbol genealogico de la busqueda



Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 005 | 2.300 | - | fallido | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204848_vaciado_005_FALLO_2.300kg.jpg) |
| Diseno desde cero | 004 | 1.233 | 2493.1 | descartado | reparto inicial (Sobol 4/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204757_cero_004_NO_VALIDO_1.233kg.jpg) |
| Refuerzo + vaciado | 004 | 0.000 | - | fallido | reparto inicial (Sobol 4/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204723_refuerzo_004_FALLO_0.000kg.jpg) |
| Vaciado del original | 004 | 2.161 | - | fallido | reparto inicial (Sobol 4/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204711_vaciado_004_FALLO_2.161kg.jpg) |
| Diseno desde cero | 003 | 1.384 | 902.6 | descartado | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204622_cero_003_NO_VALIDO_1.384kg.jpg) |
| Refuerzo + vaciado | 003 | 1.565 | 779.7 | descartado | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204542_refuerzo_003_NO_VALIDO_1.565kg.jpg) |
| Vaciado del original | 003 | 2.413 | 315.5 | descartado | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204443_vaciado_003_NO_VALIDO_2.413kg.jpg) |
| Diseno desde cero | 002 | 1.607 | 1664.8 | descartado | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204344_cero_002_NO_VALIDO_1.607kg.jpg) |
| Refuerzo + vaciado | 002 | 2.547 | - | fallido | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204308_refuerzo_002_FALLO_2.547kg.jpg) |
| Vaciado del original | 002 | 2.401 | 294.3 | descartado | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204212_vaciado_002_NO_VALIDO_2.401kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
