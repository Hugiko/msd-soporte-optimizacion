# Refuerzo + vaciado: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-23 00:11

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (20)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 071 **MEJOR** | 2.436 | 182.7 | [rama R1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.20); cambia trim_ang, r_cut (rama fina: solo mueve trim_s0, trim_z, r_cut, cav_a, trim_a, cav_z1, trim_ang) | [ver](071/vonmises.png) |
| 075 | 2.436 | 182.7 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.40); cambia  (rama fina: solo mueve trim_s0, r_cut, trim_z, trim_a, cav_a, cav_len, trim_ang) | [ver](075/vonmises.png) |
| 070 | 2.443 | 182.6 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.20); cambia trim_z, r_cut, z_col (rama fina: solo mueve trim_s0, trim_z, r_cut, cav_z1, trim_a, R_pocket, z_col) | [ver](070/vonmises.png) |
| 066 | 2.459 | 179.8 | [rama R1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.10); cambia  (rama fina: solo mueve trim_s0, trim_z, r_cut, cav_a, trim_a, trim_ang, z_col) | [ver](066/vonmises.png) |
| 065 | 2.460 | 180.2 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_z, r_cut (rama fina: solo mueve trim_s0, trim_z, r_cut, trim_a, cav_a, trim_ang, cav_z1) | [ver](065/vonmises.png) |
| 063 | 2.463 | 180.3 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.10); cambia trim_s0, trim_z (rama fina: solo mueve trim_s0, trim_z, r_cut, trim_a, cav_a, R_pocket, trim_ang) | [ver](063/vonmises.png) |
| 064 | 2.456 | 185.7 | [rama R1.1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.10); cambia trim_z (rama fina: solo mueve trim_s0, r_cut, trim_z, trim_a, cav_a, cav_z1, R_pocket) | [ver](064/vonmises.png) |
| 054 | 2.488 | 180.3 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.03); cambia r_cut (rama fina: solo mueve trim_s0, trim_z, trim_a, R_pocket, r_cut, cav_a, cav_z1) | - |
| 049 | 2.488 | 180.4 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.05); cambia cav_z0, trim_z (rama fina: solo mueve trim_s0, cav_z0, R_pocket, trim_z, trim_a, cav_a, t_col_del) | - |
| 043 | 2.494 | 179.8 | [rama R1.1] rama nueva (fina, paso 0.10) desde el diseno 039; cambia cav_z0, r_cut (rama fina: solo mueve trim_z, trim_s0, R_pocket, cav_z0, cav_a, r_cut, trim_a) | - |
| 047 | 2.488 | 182.9 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.10); cambia cav_s0, trim_s0, trim_z, r_cut (rama fina: solo mueve trim_z, trim_s0, cav_a, R_pocket, cav_s0, r_cut, trim_a) | - |
| 039 | 2.493 | 182.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | - |
| 037 | 2.505 | 180.0 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | - |
| 074 | 2.506 | 180.4 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.40); cambia trim_s0, trim_ang, r_cut (rama fina: solo mueve trim_s0, r_cut, trim_z, trim_a, R_pocket, trim_ang, cav_z1) | [ver](074/vonmises.png) |
| 029 | 2.510 | 181.7 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_s0, trim_z | - |
| 027 | 2.515 | 179.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, t_col_tra | - |
| 061 | 2.513 | 181.7 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_s0 (rama fina: solo mueve trim_s0, trim_z, r_cut, R_pocket, trim_a, cav_a, trim_ang) | [ver](061/vonmises.png) |
| 044 | 2.521 | 180.0 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_s0, R_pocket, z_col (rama fina: solo mueve trim_s0, trim_z, R_pocket, cav_a, trim_a, z_col, t_col_del) | - |
| 023 | 2.528 | 179.6 | [rama R1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia t_col_del | - |
| 025 | 2.528 | 179.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_s0, r_cut | - |

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (39)

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
| 024 | 2.499 | 185.9 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia t_col_del | - |
| 028 | 2.496 | 185.3 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia trim_s0, t_col_tra | - |
| 030 | 2.512 | 180.4 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, t_col_tra | - |
| 031 | 2.490 | 183.2 | [rama R1] varios pasos sin mejora: paso mas corto (0.15); cambia trim_z, r_cut | - |
| 032 | 2.498 | 183.6 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia cav_s0, r_cut, t_col_del, t_col_tra | - |
| 033 | 2.487 | 183.1 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.07); cambia trim_z, t_col_del | - |
| 036 | 2.505 | 181.3 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_z | - |
| 041 | 2.484 | 186.5 | [rama R1] pequeno cambio alrededor del mejor de la rama (paso 0.04); cambia trim_s0, r_cut | - |
| 046 | 2.484 | 179.0 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.10); cambia cav_z0, trim_s0, r_cut (rama fina: solo mueve trim_s0, trim_z, cav_a, R_pocket, r_cut, trim_a, cav_z0) | - |
| 048 | 2.480 | 179.2 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.05); cambia trim_s0, trim_z, r_cut (rama fina: solo mueve trim_s0, trim_z, cav_s0, cav_a, R_pocket, trim_a, r_cut) | - |
| 050 | 2.481 | 181.1 | [rama R1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.05); cambia cav_z0, trim_z (rama fina: solo mueve trim_s0, R_pocket, trim_z, cav_a, r_cut, trim_a, t_col_del) | - |
| 051 | 2.482 | 179.3 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.05); cambia trim_s0, r_cut (rama fina: solo mueve trim_s0, trim_z, R_pocket, cav_a, trim_a, r_cut, t_col_del) | - |
| 052 | 2.477 | 181.9 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.05); cambia trim_s0, trim_z, t_col_del (rama fina: solo mueve trim_s0, trim_z, cav_a, R_pocket, r_cut, trim_a, t_col_del) | - |
| 053 | 2.480 | 182.6 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.05); cambia trim_s0, trim_z, trim_ang, r_cut (rama fina: solo mueve trim_s0, trim_z, cav_a, R_pocket, trim_a, r_cut, trim_ang) | - |
| 055 | 2.482 | 182.8 | [rama R1.1] el ultimo paso mejoro: sigue en esa linea (paso 0.03); cambia trim_s0 (rama fina: solo mueve trim_s0, trim_z, trim_a, R_pocket, r_cut, cav_a, cav_z1) | - |
| 057 | 2.486 | 180.3 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.03); cambia  (rama fina: solo mueve trim_s0, trim_z, trim_a, r_cut, R_pocket, cav_z1, cav_a) | - |
| 058 | 2.485 | 179.7 | [rama R1.1] varios pasos sin mejora: paso mas corto (0.03); cambia  (rama fina: solo mueve trim_s0, trim_z, trim_a, r_cut, R_pocket, cav_a, trim_ang) | - |
| 060 | 2.462 | 180.3 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_s0, trim_z (rama fina: solo mueve trim_s0, trim_z, trim_a, r_cut, R_pocket, cav_a, cav_z1) | [ver](060/vonmises.png) |
| 062 | 2.466 | 182.1 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.10); cambia trim_s0, trim_z (rama fina: solo mueve trim_s0, trim_z, r_cut, trim_a, cav_a, trim_ang, R_pocket) | [ver](062/vonmises.png) |
| 067 | 2.452 | 179.6 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20); cambia trim_z, trim_ang, r_cut (rama fina: solo mueve trim_s0, trim_z, r_cut, cav_a, trim_a, trim_ang, cav_z1) | [ver](067/vonmises.png) |
| 068 | 2.440 | 182.0 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20); cambia trim_s0, trim_z, trim_ang, r_cut (rama fina: solo mueve trim_s0, trim_z, r_cut, trim_a, cav_a, cav_z1, trim_ang) | [ver](068/vonmises.png) |
| 069 | 2.444 | 182.8 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.20); cambia trim_z, trim_ang, r_cut (rama fina: solo mueve trim_s0, trim_z, r_cut, cav_a, trim_a, cav_z1, trim_ang) | [ver](069/vonmises.png) |
| 073 | 2.395 | 192.7 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.40); cambia trim_z, z_col (rama fina: solo mueve trim_s0, r_cut, trim_z, trim_a, R_pocket, trim_ang, z_col) | [ver](073/vonmises.png) |
| 077 | 2.434 | 183.3 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20); cambia  (rama fina: solo mueve trim_s0, r_cut, trim_z, R_pocket, trim_a, trim_ang, cav_z1) | [ver](077/vonmises.png) |
| 078 | 2.434 | 183.3 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.20); cambia  (rama fina: solo mueve trim_s0, r_cut, R_pocket, trim_z, trim_a, trim_ang, cav_z1) | [ver](078/vonmises.png) |
| 079 | 2.432 | 183.2 | [rama R1.1.1] varios pasos sin mejora: paso mas corto (0.20); cambia trim_z (rama fina: solo mueve trim_s0, r_cut, trim_z, R_pocket, trim_a, trim_ang, cav_z1) | [ver](079/vonmises.png) |
| 080 | 2.432 | 183.1 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_z (rama fina: solo mueve trim_s0, r_cut, trim_z, R_pocket, trim_a, trim_ang, cav_z1) | [ver](080/vonmises.png) |
| 081 | 2.425 | 183.7 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia trim_z (rama fina: solo mueve trim_s0, r_cut, trim_z, R_pocket, trim_a, trim_ang, cav_z1) | [ver](081/vonmises.png) |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (15)

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
| 038 | 2.384 | 414.3 | [rama R1] el ultimo paso mejoro: sigue en esa linea (paso 0.04); cambia trim_s0, trim_z | - |
| 045 | 2.494 | 227.3 | [rama R1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia r_cut (rama fina: solo mueve trim_z, trim_s0, cav_a, cav_z0, trim_a, R_pocket, r_cut) | - |
| 056 | 1.660 | 464.2 | aleatorio (respaldo) | - |
| 059 | 1.719 | 571.8 | aleatorio (respaldo) | [ver](059/vonmises.png) |
| 072 | 2.280 | 1230.9 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.40); cambia trim_s0 (rama fina: solo mueve trim_s0, trim_z, r_cut, trim_a, trim_ang, R_pocket, cav_z1) | [ver](072/vonmises.png) |
| 076 | 2.431 | 294.3 | [rama R1.1.1] pequeno cambio alrededor del mejor de la rama (paso 0.20); cambia R_pocket (rama fina: solo mueve trim_s0, r_cut, trim_z, cav_a, trim_a, trim_ang, R_pocket) | [ver](076/vonmises.png) |

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
