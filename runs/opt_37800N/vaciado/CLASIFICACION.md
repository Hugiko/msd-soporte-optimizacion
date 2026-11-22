# Vaciado del original: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 21:43

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (1)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 021 | 2.422 | 200.5 | [rama V1] [aun sin disenos validos] el ultimo paso mejoro: sigue en esa linea (paso 0.15); cambia cav_z1, r_cut | [ver](021/vonmises.png) |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (18)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.423 | 212.9 | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](001/vonmises.png) |
| 002 | 2.401 | 294.3 | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](002/vonmises.png) |
| 003 | 2.413 | 315.5 | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](003/vonmises.png) |
| 006 | 2.404 | 310.6 | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](006/vonmises.png) |
| 007 | 1.845 | 635.7 | reparto inicial (Sobol 7/12): explorar todo el espacio | [ver](007/vonmises.png) |
| 008 | 2.002 | 2392.5 | reparto inicial (Sobol 8/12): explorar todo el espacio | [ver](008/vonmises.png) |
| 009 | 1.968 | 496.8 | reparto inicial (Sobol 9/12): explorar todo el espacio | [ver](009/vonmises.png) |
| 011 | 1.882 | 715.6 | reparto inicial (Sobol 11/12): explorar todo el espacio | [ver](011/vonmises.png) |
| 012 | 2.229 | 612.6 | reparto inicial (Sobol 12/12): explorar todo el espacio | [ver](012/vonmises.png) |
| 013 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] rama nueva (inicial, paso 0.30) desde el diseno 001; cambia cav_z0, cav_z1, trim_z | [ver](013/vonmises.png) |
| 014 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_len, trim_a, r_cut | [ver](014/vonmises.png) |
| 015 | 2.420 | 289.4 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia cav_s0, cav_len, cav_a, cav_z1... | [ver](015/vonmises.png) |
| 016 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_s0, cav_len, cav_a, cav_z0... | [ver](016/vonmises.png) |
| 017 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.30); cambia cav_s0, cav_z0 | [ver](017/vonmises.png) |
| 018 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia cav_z1, trim_z, r_cut | [ver](018/vonmises.png) |
| 019 | 2.423 | 212.9 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.15); cambia trim_ang | [ver](019/vonmises.png) |
| 020 | 2.422 | 212.8 | [rama V1] [aun sin disenos validos] varios pasos sin mejora: paso mas corto (0.15); cambia trim_s0, r_cut | [ver](020/vonmises.png) |
| 022 | 2.412 | 327.5 | [rama V1] [aun sin disenos validos] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia R_pocket | [ver](022/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (3)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 004 | 2.161 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 005 | 2.300 | - | reparto inicial (Sobol 5/12): explorar todo el espacio | - |
| 010 | 0.000 | - | reparto inicial (Sobol 10/12): explorar todo el espacio | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
