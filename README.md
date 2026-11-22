# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 20:42 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 2 | 0 | - | en marcha |
| Refuerzo + vaciado | 1 | 0 | - | en marcha |
| Diseno desde cero | 1 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 1 descartados en la pasada rapida, 0 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: aun aprendiendo | Refuerzo + vaciado: aun aprendiendo | Diseno desde cero: aun aprendiendo

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 4 fichas.

## Arbol genealogico de la busqueda



Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 002 | 2.401 | 294.3 | descartado | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204212_vaciado_002_NO_VALIDO_2.401kg.jpg) |
| Diseno desde cero | 001 | 1.510 | 1933.7 | descartado | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204110_cero_001_NO_VALIDO_1.510kg.jpg) |
| Refuerzo + vaciado | 001 | 2.544 | 179.4 | cerca_del_limite | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_204033_refuerzo_001_CASI_2.544kg.jpg) |
| Vaciado del original | 001 | 2.423 | 212.9 | descartado | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_203856_vaciado_001_NO_VALIDO_2.423kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
