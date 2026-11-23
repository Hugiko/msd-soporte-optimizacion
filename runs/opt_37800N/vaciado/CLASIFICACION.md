# Vaciado del original: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-23 07:13

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (20)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 021 | 2.422 | 200.5 | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia cav_z1, r_cut | - |
| 024 | 2.422 | 200.5 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_s0, cav_z0, r_cut | - |
| 031 | 2.414 | 193.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, R_pocket | - |
| 039 | 2.414 | 193.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.07); cambia R_pocket | - |
| 040 | 2.414 | 199.7 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia R_pocket | - |
| 041 | 2.414 | 199.7 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia R_pocket | - |
| 042 | 2.414 | 193.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.04); cambia R_pocket | - |
| 043 | 2.408 | 197.9 | [rama V1.1] [aun sin disenos validos] rama nueva (fina, paso 0.10) desde el diseno 031; cambia trim_s0, trim_z, R_pocket (rama fina: solo mueve R_pocket, cav_len, cav_a, trim_s0, trim_z, trim_a) | - |
| 045 | 2.408 | 195.0 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_s0, trim_z, R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, trim_ang, trim_z, trim_a) | - |
| 046 | 2.411 | 194.1 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.10); cambia trim_z, R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_a, trim_z) | - |
| 047 | 2.411 | 194.1 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.10); cambia trim_z, R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_a, trim_z) | [ver](047/vonmises.png) |
| 050 | 2.414 | 193.8 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.05); cambia R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, trim_ang, trim_z, trim_a) | [ver](050/vonmises.png) |
| 052 | 2.412 | 193.9 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.03); cambia trim_z (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_a, trim_z) | [ver](052/vonmises.png) |
| 055 | 2.413 | 199.5 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.03); cambia trim_z (rama fina: solo mueve R_pocket, trim_s0, cav_a, trim_ang, trim_z, trim_a) | [ver](055/vonmises.png) |
| 057 | 2.398 | 198.7 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.35); cambia trim_s0, r_cut | [ver](057/vonmises.png) |
| 059 | 2.400 | 200.8 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.35); cambia cav_len, trim_a, r_cut | [ver](059/vonmises.png) |
| 060 | 2.371 | 196.1 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.35); cambia cav_s0, cav_a, cav_z0, trim_s0... | [ver](060/vonmises.png) |
| 065 | 2.408 | 199.2 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.09); cambia cav_s0, trim_s0, trim_z, trim_a... | [ver](065/vonmises.png) |
| 066 | 2.413 | 194.0 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.09); cambia trim_a, r_cut, R_pocket | [ver](066/vonmises.png) |
| 068 | 2.415 | 193.8 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.09); cambia r_cut, R_pocket | [ver](068/vonmises.png) |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (45)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.423 | 212.9 | reparto inicial (Sobol 1/12): explorar todo el espacio | - |
| 002 | 2.401 | 294.3 | reparto inicial (Sobol 2/12): explorar todo el espacio | - |
| 003 | 2.413 | 315.5 | reparto inicial (Sobol 3/12): explorar todo el espacio | - |
| 006 | 2.404 | 310.6 | reparto inicial (Sobol 6/12): explorar todo el espacio | - |
| 007 | 1.845 | 635.7 | reparto inicial (Sobol 7/12): explorar todo el espacio | - |
| 008 | 2.002 | 2392.5 | reparto inicial (Sobol 8/12): explorar todo el espacio | - |
| 009 | 1.968 | 496.8 | reparto inicial (Sobol 9/12): explorar todo el espacio | - |
| 011 | 1.882 | 715.6 | reparto inicial (Sobol 11/12): explorar todo el espacio | - |
| 012 | 2.229 | 612.6 | reparto inicial (Sobol 12/12): explorar todo el espacio | - |
| 013 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 001; cambia cav_z0, cav_z1, trim_z | - |
| 014 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_len, trim_a, r_cut | - |
| 015 | 2.420 | 289.4 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_s0, cav_len, cav_a, cav_z1... | - |
| 016 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_s0, cav_len, cav_a, cav_z0... | - |
| 017 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_s0, cav_z0 | - |
| 018 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_z1, trim_z, r_cut | - |
| 019 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_ang | - |
| 020 | 2.422 | 212.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, r_cut | - |
| 022 | 2.412 | 327.5 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia R_pocket | - |
| 023 | 2.423 | 213.1 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_len, r_cut | - |
| 025 | 2.423 | 213.2 | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia cav_s0, cav_z0, r_cut | - |
| 026 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_s0, cav_len, cav_z0, cav_z1... | - |
| 027 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia trim_ang | - |
| 028 | 2.421 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_len, trim_ang | - |
| 029 | 2.394 | 207.3 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_s0, r_cut | - |
| 030 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_z, r_cut | - |
| 032 | 2.406 | 211.9 | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia trim_z | - |
| 033 | 2.414 | 212.2 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_s0, cav_z0, r_cut | - |
| 034 | 2.409 | 302.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.15); cambia cav_s0, R_pocket | - |
| 035 | 2.376 | 206.2 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0 | - |
| 036 | 2.412 | 211.7 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia trim_s0, R_pocket | - |
| 037 | 2.414 | 212.1 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia cav_z0, r_cut, R_pocket | - |
| 038 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.07); cambia cav_len, R_pocket | - |
| 044 | 2.408 | 211.8 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_s0, R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_ang, trim_z) | - |
| 048 | 2.412 | 211.7 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.05); cambia trim_s0, R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_ang, trim_a) | [ver](048/vonmises.png) |
| 049 | 2.414 | 212.1 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.05); cambia R_pocket (rama fina: solo mueve R_pocket, trim_s0, cav_a, trim_ang, trim_z, trim_a) | [ver](049/vonmises.png) |
| 051 | 2.410 | 211.7 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.05); cambia trim_z, trim_a (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_a, trim_z) | [ver](051/vonmises.png) |
| 053 | 2.413 | 212.1 | [rama V1.1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.03); cambia trim_z (rama fina: solo mueve trim_s0, R_pocket, cav_a, cav_z1, trim_ang, trim_z) | [ver](053/vonmises.png) |
| 054 | 2.423 | 212.8 | [rama V1.1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.03); cambia trim_s0 (rama fina: solo mueve R_pocket, trim_s0, cav_a, cav_z1, trim_a, trim_z) | [ver](054/vonmises.png) |
| 056 | 2.255 | 939.2 | [rama V1.2] [aun sin disenos validos] rama nueva (amplia, paso 0.35) desde el diseno 031; cambia trim_s0 | [ver](056/vonmises.png) |
| 058 | 2.360 | 208.9 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.35); cambia cav_s0, cav_z0, cav_z1, trim_s0... | [ver](058/vonmises.png) |
| 061 | 2.388 | 210.6 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.17); cambia cav_a, cav_z0, trim_s0 | [ver](061/vonmises.png) |
| 062 | 2.409 | 211.5 | [rama V1.2] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.17); cambia cav_s0, cav_len, cav_a, cav_z0... | [ver](062/vonmises.png) |
| 063 | 2.359 | 207.6 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.17); cambia trim_s0, trim_a | [ver](063/vonmises.png) |
| 064 | 2.388 | 210.6 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.17); cambia cav_z1, trim_s0, r_cut | [ver](064/vonmises.png) |
| 067 | 2.423 | 212.9 | [rama V1.2] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.09); cambia trim_s0, r_cut, R_pocket | - |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (3)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 004 | 2.161 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 005 | 2.300 | - | reparto inicial (Sobol 5/12): explorar todo el espacio | - |
| 010 | 0.000 | - | reparto inicial (Sobol 10/12): explorar todo el espacio | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
