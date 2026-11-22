# Parte 1 – Recopilación de información (SimJEB) · borrador

## Fuente principal
- Whalen, E., Beyene, A., Mueller, C. (2021). *SimJEB: Simulated Jet Engine Bracket Dataset*. Computer Graphics Forum 40(5), Eurographics Symposium on Geometry Processing 2021. doi:10.1111/cgf.14353 · arXiv:2105.03534. Web: https://simjeb.github.io
- Conjunto de datos: Harvard Dataverse, doi:10.7910/DVN/XFUWJG.

## Qué es SimJEB (datos verificados en arXiv:2105.03534v2)
- Recoge los diseños del GE Jet Engine Bracket Challenge (GrabCAD, 2013): 635 CAD originales, 514 limpios, 411 mallados y 381 simulados.
- Todos los diseños tienen los mismos 4 agujeros de pernos, la misma interfaz de carga y las mismas condiciones de contorno.
- Simulación: estática lineal (OptiStruct), Ti-6Al-4V, malla tetraédrica de 1.er orden con tamaño medio de 2 mm.
- Pernos: RBE2 rígido sobre la superficie de cada perno, con restricción (SPC) en el centro.
- Cargas: «An RBE3 spider element was used to distribute each of the four loads across the surfaces of the interface hole». → **Nuestro modelo usa el mismo esquema** (RBE3 en el bulón y superficies de pernos empotradas).
- 4 casos de carga: vertical, horizontal, diagonal y torsional. Seis familias de diseño: *block, flat, arch, butterfly, beam, other*.

## Principios de diseño aplicables a nuestra carga (horizontal, perpendicular al bulón)
1. **Recorrido de cargas directo de las orejetas a los pernos.** La carga horizontal genera un momento de vuelco (brazo ≈ 45 mm, altura del bulón). Los pernos del lado cargado trabajan a tracción y los opuestos a compresión. Hay que llevar material en diagonal desde las orejetas hacia los cuatro pernos (familias *arch/beam*).
2. **Almas o nervios en el plano de la carga** (perpendiculares al bulón). Así trabajan a flexión con el canto máximo.
3. **Vaciados en la placa base y en los laterales**, donde el original apenas trabaja (zonas azules de `figuras/fase2_vonmises_original.png`).
4. **Radios de acuerdo generosos** en la unión de la orejeta con la base y en las protuberancias de los pernos. Es allí donde aparece la tensión máxima en el original.
5. **Orejetas**: espesor y material alrededor del agujero (relación e/D), dimensionados frente a tracción en la sección neta y frente a desgarro.

## Pendiente
- Identificar en la web de SimJEB 3–5 diseños concretos (ID, masa y tipología). La página carga los datos por JavaScript y no se han podido leer automáticamente; hay que revisarla en el navegador o descargar los metadatos de Dataverse.
- No se ha podido verificar ningún dato de los ganadores del concurso de GrabCAD; no se cita nada sin fuente.
