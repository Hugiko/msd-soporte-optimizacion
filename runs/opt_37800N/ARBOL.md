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
V1["V1 - inicial, paso 0.30<br/>13 pruebas<br/>aun sin validos; el mas cercano 200 MPa (#024)"]:::activa
V0 --> V1
```

## Refuerzo + vaciado

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
R0["R0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 179 MPa (#001)"]:::fin
R1["R1 - inicial, paso 0.30<br/>12 pruebas<br/>mejor: 2.528 kg, 180 MPa (#023)"]:::mejor
R0 --> R1
```

## Diseno desde cero

```mermaid
graph TD
classDef activa fill:#d6eaff,stroke:#1f6fb5,color:#000
classDef fin fill:#eeeeee,stroke:#888,color:#000
classDef mejor fill:#c8f0c0,stroke:#1a9850,stroke-width:4px,color:#000
C0["C0 - reparto inicial<br/>12 pruebas<br/>aun sin validos; el mas cercano 612 MPa (#009)"]:::fin
C1["C1 - inicial, paso 0.30<br/>12 pruebas<br/>aun sin validos; el mas cercano 434 MPa (#022)"]:::activa
C0 --> C1
```

