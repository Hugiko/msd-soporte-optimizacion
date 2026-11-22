# Optimizacion del soporte - panel en directo

> **Ultima actualizacion:** 22/11/2026 21:44 &nbsp;|&nbsp; **Estado:** EN MARCHA &nbsp;|&nbsp; carga 37800 N &nbsp;|&nbsp; limites: 187 MPa (coef. seguridad >= 1.15 sobre sy = 215 MPa) y 0.25 mm &nbsp;|&nbsp; acero S235

| Familia | disenos calculados | cumplen | mejor masa | estado |
|---|---|---|---|---|
| Vaciado del original | 22 | 0 | - | en marcha |
| Refuerzo + vaciado | 22 | 0 | - | en marcha |
| Diseno desde cero | 21 | 0 | - | en marcha |

**Calculos ahorrados:** 0 descartados por el modelo sin ANSYS, 21 descartados en la pasada rapida, 10 piezas repetidas reutilizadas. **Fiabilidad del modelo de tension:** Vaciado del original: error tipico 17 % | Refuerzo + vaciado: error tipico 0 % | Diseno desde cero: error tipico 3 %

## Mejor diseno actual

Aun ningun diseno cumple el limite.

## Evolucion en el tiempo

![evolucion](runs/opt_37800N/evolucion_global.png)

Grafico interactivo (hora y datos de cada punto al pasar el raton): [evolucion_interactiva.html](runs/opt_37800N/evolucion_interactiva.html) - descargar y abrir con el navegador (en el PC: doble clic en `runs/opt_37800N/evolucion_interactiva.html`).

**[Galeria: TODOS los disenos (validos y no validos) en orden cronologico](runs/opt_37800N/GALERIA.md)** - 65 fichas.

## Arbol genealogico de la busqueda

![arbol](runs/opt_37800N/arbol.png)

Detalle de cada rama: [ARBOL.md](runs/opt_37800N/ARBOL.md)

## Ultimos disenos calculados

| familia | # | masa | tension | resultado | motivo | ficha |
|---|---|---|---|---|---|---|
| Refuerzo + vaciado | 022 | 2.565 | 183.8 | cerca_del_limite | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_214457_refuerzo_022_CASI_2.565kg.jpg) |
| Vaciado del original | 022 | 2.412 | 327.5 | descartado | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_214317_vaciado_022_NO_VALIDO_2.412kg.jpg) |
| Diseno desde cero | 021 | 2.467 | 444.0 | descartado | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_214213_cero_021_NO_VALIDO_2.467kg.jpg) |
| Refuerzo + vaciado | 021 | 2.556 | 178.2 | cerca_del_limite | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_214133_refuerzo_021_CASI_2.556kg.jpg) |
| Vaciado del original | 021 | 2.422 | 200.5 | cerca_del_limite | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en es | [ver](runs/opt_37800N/galeria/20261122_213953_vaciado_021_CASI_2.422kg.jpg) |
| Diseno desde cero | 020 | 2.473 | 445.9 | descartado | [rama C1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_213902_cero_020_NO_VALIDO_2.473kg.jpg) |
| Refuerzo + vaciado | 020 | 2.552 | 178.1 | cerca_del_limite | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_213822_refuerzo_020_CASI_2.552kg.jpg) |
| Vaciado del original | 020 | 2.422 | 212.8 | descartado | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas  | [ver](runs/opt_37800N/galeria/20261122_213642_vaciado_020_NO_VALIDO_2.422kg.jpg) |
| Diseno desde cero | 019 | 2.380 | 456.2 | descartado | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_213552_cero_019_NO_VALIDO_2.380kg.jpg) |
| Refuerzo + vaciado | 019 | 2.548 | 178.1 | cerca_del_limite | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor | [ver](runs/opt_37800N/galeria/20261122_213513_refuerzo_019_CASI_2.548kg.jpg) |

---

**Como funciona:** el programa prueba dos familias de piezas (vaciado del original y diseno desde cero). Tras un reparto inicial, aprende con modelos sustitutos (procesos gaussianos) y propone pequenos cambios alrededor del mejor diseno: si mejora, sigue por esa linea y alarga el paso; si no, lo acorta. Cada diseno se calcula en ANSYS MAPDL (SOLID187, pernos empotrados, carga por RBE3). Cada nuevo mejor genera un proyecto de Workbench listo para abrir.

**Abrir un proyecto:** descargar el `.wbpz` > Workbench > File > Restore Archive. Todo el detalle esta en `bitacora.md`; cada diseno en `runs/`.
