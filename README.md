# Problema de la Mochila - TP 1 - Teoría de Algoritmos 

Este repositorio contiene las resoluciones para el TP 1 de la materia Teoría de Algoritmos TB024 curso Echevarria, grupo 17.
El proyecto explora distintas técnicas algorítmicas para resolver el **Problema de la Mochila**.

## Instalación y dependencias

El proyecto está desarrollado en Python. Para instalar las dependencias necesarias, sigue estos pasos:

1. Es recomendable crear un entorno virtual para aislar las dependencias:
```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instalar las dependencias listadas en el archivo `requirements.txt`. El proyecto utiliza `pulp` para la resolución de programación lineal:
```bash
pip install -r requirements.txt
```

## Estructura del proyecto

El proyecto está dividido en varios directorios, uno para cada técnica algorítmica:

- `backtracking_fuerza_bruta/`: Implementaciones de las soluciones por backtracking y fuerza bruta. Contiene los scripts `fuerza_bruta.py` y `backtracking.py`.
- `greedy/`: Implementación del algoritmo Greedy en `greedy_mochila.py`, junto a archivos de texto con el planteo y pseudocódigo.
- `programacion_dinamica/`: Implementaciones basadas en programación dinámica. Contiene la solución tradicional (maximizar beneficio dado el peso) en `tradicional.py`, y la alternativa (minimizar peso dado el beneficio) en `alternativo.py`.
- `programacion_lineal/`: Resolución utilizando el solver `pulp` para plantearlo como un problema de programación lineal entera en `programacion_lineal.py`.
- `pruebas/`: Directorio que agrupa los sets de datos, los generadores de problemas, y el script principal para la medición de tiempos.

Adicionalmente, se incluye el documento `enunciado.pdf` con las especificaciones y lineamientos del Trabajo Práctico.

## Cómo correr los algoritmos

TODO: actualizar esta parte cuando tengamos todos los algoritmos bajo una misma forma de correrse.

## Directorio de pruebas

El directorio `pruebas/` contiene los elementos necesarios para la validación y el análisis de complejidad empírica de los algoritmos:

- **`crear_mochila.py`**: Un script generador de datasets (provisto por la cátedra). Sirve para crear de manera aleatoria archivos de texto con distintas configuraciones de objetos.
- **Archivos `.txt` (ej. `mochila10.txt`, `mochila20.txt`, etc.)**: Sets de datos de prueba pre-generados de distintos tamaños ($n$). La primera línea indica la capacidad $W$ de la mochila, y las siguientes líneas representan los objetos en formato `peso,beneficio`.
- **`pruebas.py`**: Es el script de evaluación. Se encarga de cargar los diferentes archivos `.txt`, invocar los algoritmos de cada módulo (fuerza bruta, backtracking y greedy) y medir los tiempos de ejecución mediante la librería `time`. Esto permite obtener los datos necesarios para realizar los gráficos y la comparativa de tiempos real versus la teórica que exige el TP.
