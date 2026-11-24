# Registro de iteraciones (changelog de la pieza)

Carga 42258 N | limite 215 MPa (coef. de seguridad >= 1.00) y 0.25 mm | reglas: [DESIGN_RULES.md](../../DESIGN_RULES.md) | la mas reciente arriba

## Iteracion 0 - INICIO

*2026-11-24 09:00*

- **Por que (regla None):** La pieza tiene que ser simetrica respecto al plano medio de las orejetas. La pieza anterior (2,144 kg, 14 operaciones) no lo era: sus aligeramientos estaban donde sobraba material solo en un lado. Repetidos en el lado simetrico no cumplen (14 operaciones: 316 MPa; 8 operaciones: 252 MPa; 5 operaciones: 242 MPa; 3 operaciones: 208 MPa; 2 operaciones: 202 MPa; limite 215 MPa con la correccion a malla fina x1,041), porque los pernos 2 y 4 del enunciado no son simetricos y ese lado trabaja mas. Se parte de la ultima pieza simetrica que cumple (los dos collares, ya simetricos) y las reglas siguen en modo simetrico, conservando lo aprendido (estadistica de cada regla y calibracion de malla).
- **Resultado (malla completa):** 2.5044 kg | 201.9 MPa | CS 1.06 | 0.139 mm
- **Decision:** INICIO - cumple: se sigue quitando material donde no trabaja

<img src="galeria/20261124_090049_it000_INICIO_2.504kg.jpg" width="520">

