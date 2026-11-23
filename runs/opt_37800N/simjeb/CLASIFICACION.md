# SimJEB modificado: clasificacion de disenos

Limite: 187 MPa | carga 37800 N | actualizado 2026-11-23 08:40

## VALIDOS, ordenados por puntuacion masa-seguridad (tension <= 187 MPa y desplazamiento <= 0.25 mm) (21)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 037 **MEJOR** | 1.914 | 165.3 | [rama S1] varios pasos sin mejora: paso mas corto (0.60); cambia ali1_x, ali1_r, ali2_x | [ver](037/vonmises.png) |
| 043 | 1.914 | 165.3 | [rama S1] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia t_col_tra, ali1_y | [ver](043/vonmises.png) |
| 044 | 1.914 | 165.3 | [rama S1.1] rama nueva (fina, paso 0.10) desde el diseno 037; cambia ali1_r (rama fina: solo mueve semilla, t_col_del, ali2_r, z_col, ali1_r) | [ver](044/vonmises.png) |
| 048 | 1.914 | 165.3 | [rama S1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia ali1_y (rama fina: solo mueve semilla, t_col_del, z_col, ali2_r, ali1_y) | [ver](048/vonmises.png) |
| 050 | 1.914 | 165.3 | [rama S1.1] varios pasos sin mejora: paso mas corto (0.10); cambia ali1_y, ali1_r (rama fina: solo mueve semilla, t_col_del, z_col, ali1_r, ali1_y) | [ver](050/vonmises.png) |
| 040 | 1.923 | 164.9 | [rama S1] varios pasos sin mejora: paso mas corto (0.60); cambia t_col_tra | [ver](040/vonmises.png) |
| 033 | 1.921 | 167.7 | [rama S1] el ultimo paso mejoro: sigue en esa linea (paso 0.30); cambia z_col, ali1_x, ali1_y, ali1_r... | [ver](033/vonmises.png) |
| 042 | 1.926 | 166.1 | [rama S1] varios pasos sin mejora: paso mas corto (0.60); cambia t_col_tra | [ver](042/vonmises.png) |
| 032 | 1.953 | 167.2 | [rama S1] pequeno cambio alrededor del mejor de la rama (paso 0.30); cambia z_col, ali1_y, ali1_r, ali2_r | [ver](032/vonmises.png) |
| 034 | 1.968 | 163.8 | [rama S1] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia t_col_tra, ali1_r, ali2_x | [ver](034/vonmises.png) |
| 039 | 1.968 | 164.0 | [rama S1] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia ali2_x, ali2_y | [ver](039/vonmises.png) |
| 038 | 1.974 | 163.9 | [rama S1] el ultimo paso mejoro: sigue en esa linea (paso 0.60); cambia ali2_x, ali2_y | [ver](038/vonmises.png) |
| 011 | 1.975 | 164.1 | torneo de referencias SimJEB (11/30): SimJEB n.o 237 (block, Bol) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 178 MPa) | - |
| 036 | 1.975 | 164.1 | [rama S1] varios pasos sin mejora: paso mas corto (0.60); cambia ali1_x, ali2_x | [ver](036/vonmises.png) |
| 035 | 1.970 | 167.5 | [rama S1] pequeno cambio alrededor del mejor de la rama (paso 0.60); cambia ali1_r, ali2_x, ali2_y | [ver](035/vonmises.png) |
| 031 | 2.132 | 165.5 | [rama S1] rama nueva (inicial, paso 0.30) desde el diseno 011; cambia t_col_del, z_col, ali1_r, ali2_y | [ver](031/vonmises.png) |
| 041 | 2.211 | 176.7 | [rama S2] rama nueva (inicial, paso 0.30) desde el diseno 013; cambia ali2_x, ali2_r | [ver](041/vonmises.png) |
| 013 | 2.236 | 176.5 | torneo de referencias SimJEB (13/30): SimJEB n.o 474 (block, Kiran Kumar A) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 127 MPa) | - |
| 016 | 2.272 | 174.4 | torneo de referencias SimJEB (16/30): SimJEB n.o 527 (block, NIKHIL KHOBRAGADE) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 135 MPa) | - |
| 022 | 2.412 | 175.8 | torneo de referencias SimJEB (22/30): SimJEB n.o 476 (block, Kiran Kumar A) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 130 MPa) | - |
| 002 | 3.644 | 152.8 | torneo de referencias SimJEB (2/30): SimJEB n.o 79 (block, Fritz VZ) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 193 MPa) | - |

## CERCA DEL LIMITE (hasta +10 %): candidatos a verificar con malla fina (5)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 012 | 2.063 | 196.5 | torneo de referencias SimJEB (12/30): SimJEB n.o 186 (block, Tomek F.) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 168 MPa) | - |
| 014 | 2.162 | 195.2 | torneo de referencias SimJEB (14/30): SimJEB n.o 290 (flat, Marinus Reutelingsperger) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 170 MPa) | - |
| 015 | 2.241 | 189.5 | torneo de referencias SimJEB (15/30): SimJEB n.o 475 (block, Kiran Kumar A) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 142 MPa) | - |
| 019 | 2.253 | 201.3 | torneo de referencias SimJEB (19/30): SimJEB n.o 107 (block, julius) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 179 MPa) | - |
| 021 | 2.299 | 201.1 | torneo de referencias SimJEB (21/30): SimJEB n.o 289 (flat, Marinus Reutelingsperger) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 173 MPa) | - |

## DESCARTADOS (superan el limite): se guardan para explicar en el informe por que no valen (23)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 001 | 1.301 | 284.6 | torneo de referencias SimJEB (1/30): SimJEB n.o 321 (block, Antonio Cruz) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 176 MPa) | - |
| 003 | 1.652 | 283.2 | torneo de referencias SimJEB (3/30): SimJEB n.o 199 (flat, Armin) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 174 MPa) | - |
| 004 | 1.667 | 406.4 | torneo de referencias SimJEB (4/30): SimJEB n.o 575 (flat, Gustavo Vieira) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 190 MPa) | - |
| 005 | 1.739 | 215.3 | torneo de referencias SimJEB (5/30): SimJEB n.o 485 (block, saeid mirshahidi) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 174 MPa) | - |
| 006 | 1.824 | 368.7 | torneo de referencias SimJEB (6/30): SimJEB n.o 380 (block, Richard Amancio) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 169 MPa) | - |
| 007 | 1.823 | 287.9 | torneo de referencias SimJEB (7/30): SimJEB n.o 192 (flat, Tomek F.) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 174 MPa) | - |
| 008 | 1.823 | 287.9 | torneo de referencias SimJEB (8/30): SimJEB n.o 191 (flat, Tomek F.) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 182 MPa) | - |
| 009 | 1.853 | 446.7 | torneo de referencias SimJEB (9/30): SimJEB n.o 182 (block, ZHICHAO LI) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 191 MPa) | - |
| 010 | 1.853 | 443.9 | torneo de referencias SimJEB (10/30): SimJEB n.o 183 (block, ZHICHAO LI) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 193 MPa) | - |
| 018 | 2.369 | 207.1 | torneo de referencias SimJEB (18/30): SimJEB n.o 165 (block, Andy Brookman) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 121 MPa) | - |
| 020 | 2.266 | 449.4 | torneo de referencias SimJEB (20/30): SimJEB n.o 384 (block, JuanCR) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 187 MPa) | - |
| 023 | 2.366 | 242.5 | torneo de referencias SimJEB (23/30): SimJEB n.o 195 (flat, Armin) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 189 MPa) | - |
| 024 | 0.852 | 621.0 | torneo de referencias SimJEB (24/30): SimJEB n.o 519 (flat, Pranav Panchal) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 250 MPa) | - |
| 025 | 0.934 | 494.7 | torneo de referencias SimJEB (25/30): SimJEB n.o 395 (block, Ririwin) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 233 MPa) | - |
| 026 | 0.988 | 602.7 | torneo de referencias SimJEB (26/30): SimJEB n.o 63 (block, Arfi'an) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 247 MPa) | [ver](026/vonmises.png) |
| 027 | 1.179 | 296.4 | torneo de referencias SimJEB (27/30): SimJEB n.o 375 (arch, Andrew Coyne) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 228 MPa) | [ver](027/vonmises.png) |
| 028 | 1.191 | 526.9 | torneo de referencias SimJEB (28/30): SimJEB n.o 120 (arch, Arfi'an) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 244 MPa) | [ver](028/vonmises.png) |
| 029 | 1.298 | 342.6 | torneo de referencias SimJEB (29/30): SimJEB n.o 256 (butterfly, Richard) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 242 MPa) | [ver](029/vonmises.png) |
| 030 | 1.317 | 686.4 | torneo de referencias SimJEB (30/30): SimJEB n.o 213 (flat, Tomek F.) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 239 MPa) | [ver](030/vonmises.png) |
| 045 | 0.842 | 621.8 | [rama S1.2] rama nueva (amplia, paso 0.35) desde el diseno 037; cambia semilla, ali2_x | [ver](045/vonmises.png) |
| 046 | 1.912 | 232.7 | [rama S1.1] pequeno cambio alrededor del mejor de la rama (paso 0.10); cambia ali1_r, ali2_y (rama fina: solo mueve semilla, t_col_del, ali1_r, ali2_y, z_col) | [ver](046/vonmises.png) |
| 047 | 1.407 | 590.3 | [rama S1.2] pequeno cambio alrededor del mejor de la rama (paso 0.35); cambia semilla | [ver](047/vonmises.png) |
| 049 | 1.849 | 310.1 | [rama S1.2] pequeno cambio alrededor del mejor de la rama (paso 0.35); cambia t_col_tra, ali1_y, ali2_x, ali2_y | [ver](049/vonmises.png) |

## FALLIDOS (geometria / malla / solver): registrados y penalizados (1)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
| 017 | 2.237 | - | torneo de referencias SimJEB (17/30): SimJEB n.o 238 (block, dominic baldrica) tal cual, como PUNTO DE PARTIDA para modificarlo despues (no puede ser el mejor: la pieza final debe ser nueva; tension estimada por SimJEB 154 MPa) | - |

## FILTRADOS por el modelo (casi seguro que no cumplian): no se calcularon en ANSYS (0)

| # | masa (kg) | tension (MPa) | motivo | imagen |
|---|---|---|---|---|
