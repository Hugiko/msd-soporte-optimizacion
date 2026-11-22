# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 21:32 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 18 | 0 | - | en marcha |
| Refuerzo + vaciado | 17 | 0 | - | en marcha |
| Diseno desde cero | 17 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 17 descartados en la pasada rapida, 8 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 28 % | Refuerzo + vaciado: error tipico 1 % | Diseno desde cero: error tipico 7 %

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 52 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Vaciado del original | 018 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_213237_vaciado_018_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 017 | 2.477 | 447.2 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_213228_cero_017_NO_VALIDO_2.477kg.jpg) |
| Refuerzo + vaciado | 017 | 2.546 | 177.6 | cerca_del_limite | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_213148_refuerzo_017_CASI_2.546kg.jpg) |
| Vaciado del original | 017 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_213006_vaciado_017_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 016 | 2.232 | 468.4 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_212958_cero_016_NO_VALIDO_2.232kg.jpg) |
| Refuerzo + vaciado | 016 | 2.544 | 179.4 | cerca_del_limite | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_212915_refuerzo_016_CASI_2.544kg.jpg) |
| Vaciado del original | 016 | 2.423 | 212.9 | descartado | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_212904_vaciado_016_NO_VALIDO_2.423kg.jpg) |
| Diseno desde cero | 015 | 2.056 | 498.0 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212856_cero_015_NO_VALIDO_2.056kg.jpg) |
| Refuerzo + vaciado | 015 | 2.541 | 179.7 | cerca_del_limite | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212815_refuerzo_015_CASI_2.541kg.jpg) |
| Vaciado del original | 015 | 2.420 | 289.4 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_212633_vaciado_015_NO_VALIDO_2.420kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
