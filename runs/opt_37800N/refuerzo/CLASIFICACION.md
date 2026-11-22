# Refuerzo + vaciado: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 22:41

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (7)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 043 **MEJOR** | 2.494 | 179.8 | [rama R1.1] rama nueva (fina, paso 0.10) desde el diseno 039; cambia cav_z0, r_cut (rama fina: solo mueve trim_z, trim_s0, R_pocket, cav_z0, cav_a, r_cut, trim_a) | [ver](043/vonmises.png) |
| 039 | 2.493 | 182.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | [ver](039/vonmises.png) |
| 037 | 2.505 | 180.0 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | [ver](037/vonmises.png) |
| 029 | 2.510 | 181.7 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_s0, trim_z | [ver](029/vonmises.png) |
| 027 | 2.515 | 179.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, t_col_tra | [ver](027/vonmises.png) |
| 023 | 2.528 | 179.6 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | [ver](023/vonmises.png) |
| 025 | 2.528 | 179.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_s0, r_cut | [ver](025/vonmises.png) |

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (19)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.544 | 179.4 | reparto inicial (Sobol 1/12): explorar todo el espacio | - |
| 013 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 001; cambia  | - |
| 014 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | - |
| 015 | 2.541 | 179.7 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | - |
| 016 | 2.544 | 179.4 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | - |
| 017 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia  | - |
| 018 | 2.546 | 177.6 | [rama R1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia  | - |
| 019 | 2.548 | 178.1 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia  | - |
| 020 | 2.552 | 178.1 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | - |
| 021 | 2.556 | 178.2 | [rama R1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia t_col_del | - |
| 022 | 2.565 | 183.8 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | - |
| 024 | 2.499 | 185.9 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia t_col_del | [ver](024/vonmises.png) |
| 028 | 2.496 | 185.3 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia trim_s0, t_col_tra | [ver](028/vonmises.png) |
| 030 | 2.512 | 180.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, t_col_tra | [ver](030/vonmises.png) |
| 031 | 2.490 | 183.2 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, r_cut | [ver](031/vonmises.png) |
| 032 | 2.498 | 183.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia cav_s0, r_cut, t_col_del, t_col_tra | [ver](032/vonmises.png) |
| 033 | 2.487 | 183.1 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia trim_z, t_col_del | [ver](033/vonmises.png) |
| 036 | 2.505 | 181.3 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | [ver](036/vonmises.png) |
| 041 | 2.484 | 186.5 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_s0, r_cut | [ver](041/vonmises.png) |

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

## FALLIDOS (geometria / malla / solver): registrados y penalizados (7)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 002 | 2.547 | - | reparto inicial (Sobol 2/12): explorar todo el espacio | - |
| 004 | 0.000 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 026 | 2.492 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia t_col_del | - |
| 034 | 0.000 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut, t_col_tra | - |
| 035 | 0.000 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.07); cambia r_cut, t_col_del | - |
| 040 | 0.000 | - | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.04); cambia t_col_tra | - |
| 042 | 2.476 | - | [rama R1] varios pasos sin mejora: paso mas corto (0.04); cambia trim_s0, r_cut | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
