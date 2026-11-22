# Diseno desde cero: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 21:45

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (22)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 1.510 | 1933.7 | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](001/vonmises.png) |
| 002 | 1.607 | 1664.8 | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](002/vonmises.png) |
| 003 | 1.384 | 902.6 | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](003/vonmises.png) |
| 004 | 1.233 | 2493.1 | reparto inicial (Sobol 4/12): explorar todo el espacio | [ver](004/vonmises.png) |
| 005 | 1.415 | 1642.8 | reparto inicial (Sobol 5/12): explorar todo el espacio | [ver](005/vonmises.png) |
| 006 | 1.490 | 1384.6 | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](006/vonmises.png) |
| 007 | 0.972 | 1853.1 | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](007/vonmises.png) |
| 008 | 2.063 | 1174.5 | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](008/vonmises.png) |
| 009 | 1.765 | 612.1 | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](009/vonmises.png) |
| 010 | 1.297 | 1583.2 | reparto inicial (Sobol 10/12): explorar todo el espacio | [ver](010/vonmises.png) |
| 011 | 1.219 | 2089.0 | reparto inicial (Sobol 11/12): explorar todo el espacio | [ver](011/vonmises.png) |
| 012 | 1.636 | 1656.4 | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](012/vonmises.png) |
| 013 | 1.921 | 537.2 | [rama C1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 009; cambia R_pocket, w_bar, phi_end, H... | [ver](013/vonmises.png) |
| 014 | 1.994 | 564.1 | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia w_bar, phi_end, W_top, W_bot... | [ver](014/vonmises.png) |
| 015 | 2.056 | 498.0 | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia R_pocket, w_bar, phi_end, W_top... | [ver](015/vonmises.png) |
| 016 | 2.232 | 468.4 | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia R_pocket, w_bar, phi_end, W_top... | [ver](016/vonmises.png) |
| 017 | 2.477 | 447.2 | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia R_pocket, w_bar, W_top, W_bot... | [ver](017/vonmises.png) |
| 018 | 2.507 | 450.3 | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.60); cambia w_bar, r_f | [ver](018/vonmises.png) |
| 019 | 2.380 | 456.2 | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia R_pocket, w_bar, phi_end, t_lug | [ver](019/vonmises.png) |
| 020 | 2.473 | 445.9 | [rama C1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.60); cambia R_pocket, r_f | [ver](020/vonmises.png) |
| 021 | 2.467 | 444.0 | [rama C1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.60); cambia t_lug | [ver](021/vonmises.png) |
| 022 | 2.459 | 433.7 | [rama C1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia t_lug | [ver](022/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
