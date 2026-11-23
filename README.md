# Optimización del soporte guiada por reglas - panel en directo

> **Estado (23/11/2026):** cambio de enfoque. Se está calculando el **estudio de las 381 soluciones publicadas (SimJEB)** con la carga del enunciado (**42 258 N**) y el límite de **215 MPa (coeficiente de seguridad ≥ 1, obligatorio)**. Después empieza la optimización y este panel se actualizará en cada iteración.

**Cómo funciona ahora**
1. Las soluciones publicadas se calculan con **nuestra** carga y **nuestro** límite.
2. De ellas, y de nuestros cálculos anteriores, salen **reglas de diseño con datos**: [DESIGN_RULES.md](DESIGN_RULES.md).
3. La pieza del enunciado (`0.stp`) se modifica **paso a paso**. Cada cambio sale de una regla, con su porqué: añadir material donde está el pico o quitarlo donde no trabaja.
4. Cada cambio pasa por una **evaluación rápida** (malla gruesa) y, si promete, por la **completa** en ANSYS. Se **acepta** si mejora y se **revierte** si no, quedando registrado el motivo.
5. Cada iteración queda en `runs/opt_42258N/ITERACIONES.md`, en un commit propio y en un mensaje de Discord.

Documentación completa: [DOCUMENTACION.md](DOCUMENTACION.md) · Estado: [ESTADO.md](ESTADO.md) · Bitácora: [bitacora.md](bitacora.md)

Enfoque anterior (familias de piezas, 37 800 N, hasta el 23/11/2026): resultados solo en el PC (`runs/archivo/`); los datos que usan las reglas están en `estudio/calculos_anteriores.csv`.
