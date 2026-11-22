# Refuerzo + vaciado: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 22:28

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (5)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 037 **MEJOR** | 2.505 | 180.0 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | [ver](037/vonmises.png) |
| 029 | 2.510 | 181.7 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_s0, trim_z | [ver](029/vonmises.png) |
| 027 | 2.515 | 179.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, t_col_tra | [ver](027/vonmises.png) |
| 023 | 2.528 | 179.6 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | [ver](023/vonmises.png) |
| 025 | 2.528 | 179.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_s0, r_cut | [ver](025/vonmises.png) |

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (18)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.544 | 179.4 | reparto inicial (Sobol 1/12): explorar todo el espacio | - |
| 013 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 001; cambia  | - |
| 014 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | - |
| 015 | 2.541 | 179.7 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | - |
| 016 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | - |
| 017 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | [ver](017/vonmises.png) |
| 018 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia  | [ver](018/vonmises.png) |
| 019 | 2.548 | 178.1 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | [ver](019/vonmises.png) |
| 020 | 2.552 | 178.1 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | [ver](020/vonmises.png) |
| 021 | 2.556 | 178.2 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | [ver](021/vonmises.png) |
| 022 | 2.565 | 183.8 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | [ver](022/vonmises.png) |
| 024 | 2.499 | 185.9 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia t_col_del | [ver](024/vonmises.png) |
| 028 | 2.496 | 185.3 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia trim_s0, t_col_tra | [ver](028/vonmises.png) |
| 030 | 2.512 | 180.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, t_col_tra | [ver](030/vonmises.png) |
| 031 | 2.490 | 183.2 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, r_cut | [ver](031/vonmises.png) |
| 032 | 2.498 | 183.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia cav_s0, r_cut, t_col_del, t_col_tra | [ver](032/vonmises.png) |
| 033 | 2.487 | 183.1 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia trim_z, t_col_del | [ver](033/vonmises.png) |
| 036 | 2.505 | 181.3 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | [ver](036/vonmises.png) |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (10)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 003 | 1.565 | 779.7 | reparto inicial (Sobol 3/12): explorar todo el espacio | - |
| 005 | 2.195 | 618.0 | reparto inicial (Sobol 5/12): explorar todo el espacio | - |
| 006 | 2.409 | 302.8 | reparto inicial (Sobol 6/12): explorar todo el espacio | - |
| 007 | 1.971 | 331.5 | reparto inicial (Sobol 7/12): explorar todo el espacio | - |
| 008 | 2.212 | 639.1 | reparto inicial (Sobol 8/12): explorar todo el espacio | - |
| 009 | 2.140 | 355.2 | reparto inicial (Sobol 9/12): explorar todo el espacio | - |
| 010 | 2.357 | 911.5 | reparto inicial (Sobol 10/12): explorar todo el espacio | - |
| 011 | 2.404 | 612.7 | reparto inicial (Sobol 11/12): explorar todo el espacio | - |
| 012 | 2.059 | 1173.3 | reparto inicial (Sobol 12/12): explorar todo el espacio | - |
| 038 | 2.384 | 414.3 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.04); cambia trim_s0, trim_z | [ver](038/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (5)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 002 | 2.547 | - | reparto inicial (Sobol 2/12): explorar todo el espacio | - |
| 004 | 0.000 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 026 | 2.492 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia t_col_del | - |
| 034 | 0.000 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut, t_col_tra | - |
| 035 | 0.000 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut, t_col_del | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
