# Refuerzo + vaciado: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 21:59

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (3)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 027 **MEJOR** | 2.515 | 179.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, t_col_tra | [ver](027/vonmises.png) |
| 023 | 2.528 | 179.6 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | [ver](023/vonmises.png) |
| 025 | 2.528 | 179.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_s0, r_cut | [ver](025/vonmises.png) |

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (12)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.544 | 179.4 | reparto inicial (Sobol 1/12): explorar todo el espacio | - |
| 013 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 001; cambia  | [ver](013/vonmises.png) |
| 014 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | [ver](014/vonmises.png) |
| 015 | 2.541 | 179.7 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | [ver](015/vonmises.png) |
| 016 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | [ver](016/vonmises.png) |
| 017 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | [ver](017/vonmises.png) |
| 018 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia  | [ver](018/vonmises.png) |
| 019 | 2.548 | 178.1 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | [ver](019/vonmises.png) |
| 020 | 2.552 | 178.1 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | [ver](020/vonmises.png) |
| 021 | 2.556 | 178.2 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | [ver](021/vonmises.png) |
| 022 | 2.565 | 183.8 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | [ver](022/vonmises.png) |
| 024 | 2.499 | 185.9 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia t_col_del | [ver](024/vonmises.png) |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (9)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 003 | 1.565 | 779.7 | reparto inicial (Sobol 3/12): explorar todo el espacio | - |
| 005 | 2.195 | 618.0 | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](005/vonmises.png) |
| 006 | 2.409 | 302.8 | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](006/vonmises.png) |
| 007 | 1.971 | 331.5 | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](007/vonmises.png) |
| 008 | 2.212 | 639.1 | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](008/vonmises.png) |
| 009 | 2.140 | 355.2 | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](009/vonmises.png) |
| 010 | 2.357 | 911.5 | reparto inicial (Sobol 10/12): explorar todo el espacio | [ver](010/vonmises.png) |
| 011 | 2.404 | 612.7 | reparto inicial (Sobol 11/12): explorar todo el espacio | [ver](011/vonmises.png) |
| 012 | 2.059 | 1173.3 | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](012/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (3)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 002 | 2.547 | - | reparto inicial (Sobol 2/12): explorar todo el espacio | - |
| 004 | 0.000 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 026 | 2.492 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia t_col_del | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
