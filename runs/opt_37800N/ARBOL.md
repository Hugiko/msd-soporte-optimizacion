# Arbol genealogico de la busqueda

Cada caja es una **rama**: una linea de busqueda que parte de un diseno y prueba cambios a su alrededor.
Al terminar, su mejor diseno crea dos ramas hijas: **fina** (cambios pequenos) y **amplia** (cambios grandes).
Azul = activa | gris = terminada | verde grueso = contiene el MEJOR diseno de todos.

## Vaciado del original

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
V0["V0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 213 MPa (#001)"]:::fin
V1["V1 - inicial, paso 0.30<br/>30 pruebas<br/>aun sin validos; el mas cercano 194 MPa (#031)"]:::fin
V0 --> V1
V1_1["V1.1 - fina, paso 0.10<br/>0 pruebas<br/>sin resultados aun"]:::activa
V1 --> V1_1
V1_2["V1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
V1 --> V1_2
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
R1_2["R1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1 --> R1_2
R1_1_1["R1.1.1 - fina, paso 0.10<br/>10 pruebas<br/>mejor: 2.459 kg, 180 MPa (#066)"]:::mejor
R1_1 --> R1_1_1
R1_1_2["R1.1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1 --> R1_1_2
R1_1_3["R1.1.3 - cruce, paso 0.20<br/>0 pruebas<br/>sin resultados aun"]:::activa
R1_1 --> R1_1_3
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
C1_1["C1.1 - fina, paso 0.10<br/>0 pruebas<br/>sin resultados aun"]:::activa
C1 --> C1_1
C1_2["C1.2 - amplia, paso 0.35<br/>0 pruebas<br/>sin resultados aun"]:::activa
C1 --> C1_2
```

