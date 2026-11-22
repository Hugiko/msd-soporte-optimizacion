# Reglas de fabricación aditiva (impresión 3D metálica) aplicadas por el optimizador

Proceso supuesto: fusión láser de lecho de polvo metálico (PBF-LB/M), como en el GE Jet Engine Bracket Challenge
(el enunciado indica que los diseños «debían poder fabricarse mediante fabricación aditiva»). El propio 0.stp tiene
cavidades interiores con agujeros de evacuación de polvo en la base: es un diseño pensado para impresión 3D.
Orientación de impresión supuesta: cara inferior (la de apoyo) sobre la plataforma.

| Regla | Valor usado | Dónde se aplica | Justificación |
|---|---|---|---|
| Ángulo mínimo de superficies interiores que miran hacia abajo (sin soportes) | 45° respecto a la horizontal (`angulo_voladizo_deg` en config.json) | Techo de todos los huecos interiores: a cuatro aguas con esa pendiente | Valor de referencia habitual; los soportes interiores no se pueden retirar. El ángulo mínimo real depende de máquina y material [2, 3, 4] |
| Parte plana máxima en el vértice del techo | 3 mm | Huecos de la familia «vaciado» | Los puentes cortos se imprimen sin soporte [5] |
| Agujero de evacuación de polvo | Ø5 mm, uno por cámara, del suelo a la cara inferior | Todos los huecos interiores | ≥ 3 mm recomendado; ≥ 5 mm para conductos largos [6] |
| Pared mínima sobre los huecos | 3 mm | Ambas familias | Muy conservador (en metal se imprimen paredes de ~1 mm) |
| Agujeros del bulón (Ø19,1 horizontales) y de los pernos | Fijos por el enunciado | — | Necesitan soporte exterior o mecanizado posterior (escariado); los soportes exteriores sí se retiran |

## Fuentes
1. ISO/ASTM 52911-1:2019, *Additive manufacturing — Design — Part 1: Laser-based powder bed fusion of metals* (apartado de voladizos). Vista previa: https://webstore.ansi.org/preview-pages/ISO/preview_ISO+ASTM+52911-1-2019.pdf
2. NASA TM-20250010927, *Metal LPBF Filleting*: https://ntrs.nasa.gov/api/citations/20250010927/downloads/Metal%20LPBF%20Filleting%20TM%204.pdf
3. *Support-free metal additive manufacturing: a structured review on the state of the art in academia and industry*, Cambridge University Press: https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3969D4E6D526FCCB38B78AC0990EA2DF/S2732527X21005423a.pdf
4. Diegel, O. et al., *Design for Additive Manufacturing* (capítulo de reglas de diseño; los límites dependen de la máquina), Springer: https://dx.doi.org/10.1007/978-981-13-8281-9_10
5. Guía de diseño LPBF en Inconel 718 (voladizos de 25–80°, puentes hasta 5 mm, agujeros horizontales de 1–12 mm), TUHH: https://tore.tuhh.de/bitstreams/8dd86972-e3f7-4f29-b1f3-0bdbea96897a/download
6. *Design for Additive Manufacturing, Part 3*, Assembly Magazine (agujeros de evacuación ≥ 3 mm; ≥ 5 mm para conductos largos): https://www.assemblymag.com/articles/97510-design-for-additive-manufacturing-part-3

Nota: el S235 no es un acero habitual en impresión 3D (lo son 316L o 17-4PH). El cálculo usa las propiedades del S235
que fija el enunciado; la geometría se diseña con las reglas del proceso aditivo del concurso original.
