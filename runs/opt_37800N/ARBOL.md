# Arbol genealogico de la busqueda

Cada caja es una **rama**: una linea de busqueda que parte de un diseno y prueba cambios a su alrededor.
Al terminar, su mejor diseno crea dos ramas hijas: **fina** (cambios pequenos) y **amplia** (cambios grandes).
Azul = activa | gris = terminada | verde grueso = contiene el MEJOR diseno de todos.

## SimJEB modificado

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
S0["S0 - reparto inicial<br/>30 pruebas<br/>mejor: 1.975 kg, 164 MPa (#011)"]:::fin
S1["S1 - inicial, paso 0.30<br/>12 pruebas<br/>mejor: 1.914 kg, 165 MPa (#037)"]:::mejor
S0 --> S1
S2["S2 - inicial, paso 0.30<br/>1 pruebas<br/>mejor: 2.211 kg, 177 MPa (#041)"]:::activa
S0 --> S2
S3["S3 - inicial, paso 0.30<br/>0 pruebas<br/>sin resultados aun"]:::activa
S0 --> S3
S1_1["S1.1 - fina, paso 0.10<br/>7 pruebas<br/>mejor: 1.914 kg, 165 MPa (#044)"]:::activa
S1 --> S1_1
S1_2["S1.2 - amplia, paso 0.35<br/>6 pruebas<br/>mejor: 1.914 kg, 165 MPa (#037)"]:::activa
S1 --> S1_2
```

## Refuerzo + vaciado

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
R0["R0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 179 MPa (#001)"]:::fin
R1["R1 - inicial, paso 0.30<br/>30 pruebas<br/>mejor: 2.493 kg, 183 MPa (#039)"]:::fin
R0 --> R1
R1_1["R1.1 - fina, paso 0.10<br/>16 pruebas<br/>mejor: 2.488 kg, 180 MPa (#054)"]:::fin
R1 --> R1_1
R1_2["R1.2 - amplia, paso 0.35<br/>1 pruebas<br/>mejor: 2.467 kg, 177 MPa (#152)"]:::activa
R1 --> R1_2
R1_1_1["R1.1.1 - fina, paso 0.10<br/>30 pruebas<br/>mejor: 2.428 kg, 183 MPa (#085)"]:::fin
R1_1 --> R1_1_1
R1_1_2["R1.1.2 - amplia, paso 0.35<br/>1 pruebas<br/>mejor: 2.488 kg, 180 MPa (#054)"]:::activa
R1_1 --> R1_1_2
R1_1_3["R1.1.3 - cruce, paso 0.20<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1 --> R1_1_3
R1_1_1_1["R1.1.1.1 - fina, paso 0.10<br/>19 pruebas<br/>mejor: 2.412 kg, 184 MPa (#127)"]:::fin
R1_1_1 --> R1_1_1_1
R1_1_1_2["R1.1.1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1_1 --> R1_1_1_2
R1_1_1_3["R1.1.1.3 - cruce, paso 0.20<br/>1 pruebas<br/>mejor: 2.461 kg, 183 MPa (#157)"]:::activa
R1_1_1 --> R1_1_1_3
RX1["RX1 - exploradora, paso 0.30<br/>24 pruebas<br/>aun sin validos; el mas cercano 285 MPa (#104)"]:::fin
R0 --> RX1
RX1_1["RX1.1 - fina, paso 0.10<br/>0 pruebas<br/>sin resultados aun"]:::activa
RX1 --> RX1_1
RX1_2["RX1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
RX1 --> RX1_2
RX1_3["RX1.3 - cruce, paso 0.20<br/>2 pruebas<br/>mejor: 2.429 kg, 183 MPa (#173)"]:::activa
RX1 --> RX1_3
R1_1_1_1_1["R1.1.1.1.1 - fina, paso 0.10<br/>18 pruebas<br/>mejor: 2.372 kg, 185 MPa (#142)"]:::fin
R1_1_1_1 --> R1_1_1_1_1
R1_1_1_1_2["R1.1.1.1.2 - amplia, paso 0.35<br/>5 pruebas<br/>mejor: 2.366 kg, 182 MPa (#162)"]:::activa
R1_1_1_1 --> R1_1_1_1_2
R1_1_1_1_3["R1.1.1.1.3 - cruce, paso 0.20<br/>3 pruebas<br/>mejor: 2.376 kg, 185 MPa (#151)"]:::activa
R1_1_1_1 --> R1_1_1_1_3
R1_1_1_1_1_1["R1.1.1.1.1.1 - fina, paso 0.10<br/>1 pruebas<br/>mejor: 2.372 kg, 185 MPa (#142)"]:::activa
R1_1_1_1_1 --> R1_1_1_1_1_1
R1_1_1_1_1_2["R1.1.1.1.1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1_1_1_1 --> R1_1_1_1_1_2
R1_1_1_1_1_3["R1.1.1.1.1.3 - cruce, paso 0.20<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1_1_1_1 --> R1_1_1_1_1_3
RX2["RX2 - exploradora, paso 0.30<br/>12 pruebas<br/>aun sin validos; el mas cercano 287 MPa (#172)"]:::fin
R0 --> RX2
RX2_1["RX2.1 - fina, paso 0.10<br/>0 pruebas<br/>sin resultados aun"]:::activa
RX2 --> RX2_1
RX2_2["RX2.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
RX2 --> RX2_2
RX2_3["RX2.3 - cruce, paso 0.20<br/>0 pruebas<br/>sin resultados aun"]:::activa
RX2 --> RX2_3
```

## Diseno desde cero

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
C0["C0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 612 MPa (#009)"]:::fin
C1["C1 - inicial, paso 0.30<br/>30 pruebas<br/>aun sin validos; el mas cercano 388 MPa (#031)"]:::fin
C0 --> C1
C1_1["C1.1 - fina, paso 0.10<br/>13 pruebas<br/>aun sin validos; el mas cercano 388 MPa (#031)"]:::fin
C1 --> C1_1
C1_2["C1.2 - amplia, paso 0.35<br/>15 pruebas<br/>aun sin validos; el mas cercano 381 MPa (#058)"]:::fin
C1 --> C1_2
C1_1_1["C1.1.1 - fina, paso 0.10<br/>1 pruebas<br/>aun sin validos; el mas cercano 388 MPa (#031)"]:::activa
C1_1 --> C1_1_1
C1_1_2["C1.1.2 - amplia, paso 0.35<br/>1 pruebas<br/>aun sin validos; el mas cercano 388 MPa (#031)"]:::activa
C1_1 --> C1_1_2
C1_2_1["C1.2.1 - fina, paso 0.10<br/>3 pruebas<br/>aun sin validos; el mas cercano 381 MPa (#058)"]:::activa
C1_2 --> C1_2_1
C1_2_2["C1.2.2 - amplia, paso 0.35<br/>2 pruebas<br/>aun sin validos; el mas cercano 381 MPa (#074)"]:::activa
C1_2 --> C1_2_2
C1_2_3["C1.2.3 - cruce, paso 0.20<br/>1 pruebas<br/>aun sin validos; el mas cercano 388 MPa (#075)"]:::activa
C1_2 --> C1_2_3
```

## Vaciado del original

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
V0["V0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 213 MPa (#001)"]:::fin
V1["V1 - inicial, paso 0.30<br/>30 pruebas<br/>aun sin validos; el mas cercano 194 MPa (#031)"]:::fin
V0 --> V1
V1_1["V1.1 - fina, paso 0.10<br/>13 pruebas<br/>aun sin validos; el mas cercano 194 MPa (#031)"]:::fin
V1 --> V1_1
V1_2["V1.2 - amplia, paso 0.35<br/>14 pruebas<br/>aun sin validos; el mas cercano 194 MPa (#031)"]:::activa
V1 --> V1_2
V1_1_1["V1.1.1 - fina, paso 0.10<br/>0 pruebas<br/>sin resultados aun"]:::activa
V1_1 --> V1_1_1
V1_1_2["V1.1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
V1_1 --> V1_1_2
```

