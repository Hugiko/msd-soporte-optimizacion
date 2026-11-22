# Vaciado del original: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-22 20:51

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (4)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 2.423 | 212.9 | reparto inicial (Sobol 1/12): explorar todo el espacio | [ver](001/vonmises.png) |
| 002 | 2.401 | 294.3 | reparto inicial (Sobol 2/12): explorar todo el espacio | [ver](002/vonmises.png) |
| 003 | 2.413 | 315.5 | reparto inicial (Sobol 3/12): explorar todo el espacio | [ver](003/vonmises.png) |
| 006 | 2.404 | 310.6 | reparto inicial (Sobol 6/12): explorar todo el espacio | [ver](006/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (2)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 004 | 2.161 | - | reparto inicial (Sobol 4/12): explorar todo el espacio | - |
| 005 | 2.300 | - | reparto inicial (Sobol 5/12): explorar todo el espacio | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
