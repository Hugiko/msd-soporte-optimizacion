# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 21:26 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 15 | 0 | - | en marcha |
| Refuerzo + vaciado | 14 | 0 | - | en marcha |
| Diseno desde cero | 14 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 14 descartados en la pasada rapida, 4 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 28 % | Refuerzo + vaciado: aun aprendiendo | Diseno desde cero: error tipico 8 %

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 43 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 015 | 2.420 | 289.4 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212633_vaciado_015_NO_VALIDO_2.420kg.jpg) |
| Diseno desde cero | 014 | 1.994 | 564.1 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212533_cero_014_NO_VALIDO_1.994kg.jpg) |
| Refuerzo + vaciado | 014 | 2.544 | 179.4 | cerca_del_limite | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212451_refuerzo_014_CASI_2.544kg.jpg) |
| Vaciado del original | 014 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212441_vaciado_014_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 013 | 1.921 | 537.2 | descartado | [rama C1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) de | [ver](runs/opt_37800N/galeria/20261122_212433_cero_013_NO_VALIDO_1.921kg.jpg) |
| Refuerzo + vaciado | 013 | 2.544 | 179.4 | cerca_del_limite | [rama R1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) de | [ver](runs/opt_37800N/galeria/20261122_212252_refuerzo_013_CASI_2.544kg.jpg) |
| Vaciado del original | 013 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) de | [ver](runs/opt_37800N/galeria/20261122_211322_vaciado_013_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 012 | 1.636 | 1656.4 | descartado | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210741_cero_012_NO_VALIDO_1.636kg.jpg) |
| Refuerzo + vaciado | 012 | 2.059 | 1173.3 | descartado | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210704_refuerzo_012_NO_VALIDO_2.059kg.jpg) |
| Vaciado del original | 012 | 2.229 | 612.6 | descartado | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](runs/opt_37800N/galeria/20261122_210542_vaciado_012_NO_VALIDO_2.229kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
