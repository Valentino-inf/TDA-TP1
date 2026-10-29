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
- `greedy/`: Implementación del algoritmo Greedy con garantía 1/2 en `greedy_mochila.py`.
- `programacion_dinamica/`: Implementaciones basadas en programación dinámica. Contiene la solución tradicional (maximizar beneficio dado el peso) en `tradicional.py`, y la alternativa (minimizar peso dado el beneficio) en `alternativo.py`.
- `programacion_lineal/`: Resolución utilizando el solver `pulp` para plantearlo como un problema de programación lineal entera en `programacion_lineal.py`.
- `pruebas/`: Directorio que agrupa los sets de datos, los generadores de problemas, y el script principal para la medición de tiempos.

Adicionalmente, se incluye el documento `enunciado.pdf` con las especificaciones y lineamientos del Trabajo Práctico.

## Cómo correr los algoritmos

Todos los comandos se ejecutan desde la raíz del repositorio, con el entorno virtual activado.

### Comparar los 6 algoritmos sobre un set de datos

`pruebas/prueba.py` ejecuta los seis algoritmos (fuerza bruta, backtracking, greedy, PD tradicional, PD alternativa y programación lineal) sobre un archivo y muestra, para cada uno, el beneficio obtenido, el peso total, si respeta la capacidad y el tiempo promedio:

```bash
python pruebas/prueba.py --archivo pruebas/mochila50.txt
```

Si además se indica `--nombre`, los resultados se guardan en `pruebas/resultados/<nombre>/` (`resultado.md` con la tabla y `tiempos.png` con el gráfico de barras):

```bash
python pruebas/prueba.py --archivo pruebas/mochila50.txt --nombre mochila50
```

Fuerza bruta solo se ejecuta para $n \le 25$, ya que para tamaños mayores el tiempo es inviable.

### Gráficos de tiempo experimental vs. curva teórica

- **Greedy:** `python pruebas/grafico_greedy.py` genera `greedy_tiempos.png` en el directorio desde donde se ejecuta, a partir de los tiempos ya medidos.
- **Programación lineal:** `python pruebas/grafico_lineal.py` mide `mochila_lineal` sobre 5 instancias aleatorias (con semilla fija) para cada tamaño entre 10 y 10000 objetos, y ajusta la curva $a \cdot n \log n + b$. Tarda alrededor de 30 segundos y genera `pruebas/lineal_tiempos.png` y `pruebas/lineal_tiempos.csv` (tiempo por instancia).
- **Programación dinámica:** `python pruebas/grafico_pd.py` mide ambos planteos sobre `pruebas/mochila{10,...,500}.txt`, ajusta $c \cdot n \cdot W$ (tradicional) y $c' \cdot n \cdot V$ (alternativo) y genera `pruebas/pd_comparacion.png`, `pruebas/pd_tradicional_ajuste.png`, `pruebas/pd_alternativo_ajuste.png` y `pruebas/pd_tiempos.csv`. Tarda alrededor de 2 minutos; con `--adhoc` mide además los dos sets `mochila_gana_*.txt` y tarda unos 8 minutos más. Al final imprime las filas de la tabla del informe.

La resolución por programación lineal usa CBC, el solver que viene incluido con `pulp`, por lo que no hace falta instalar nada además de `requirements.txt`.

## Directorio de pruebas

El directorio `pruebas/` contiene los elementos necesarios para la validación y el análisis de complejidad empírica de los algoritmos:

- **`crear_mochila.py`**: Un script generador de datasets (provisto por la cátedra). Sirve para crear de manera aleatoria archivos de texto con distintas configuraciones de objetos.
- **Archivos `.txt` (ej. `mochila10.txt`, `mochila20.txt`, etc.)**: Sets de datos de prueba pre-generados de distintos tamaños ($n$). La primera línea indica la capacidad $W$ de la mochila, y las siguientes líneas representan los objetos en formato `peso,beneficio`. Los `mochila{10,20,50,90,100,200,300,500,1000}.txt` siguen la distribución de `crear_mochila.py`; `mochila_gana_tradicional.txt` ($W$ chico, beneficios enormes) y `mochila_gana_alternativo.txt` ($W$ enorme, beneficios chicos) son los casos ad-hoc de la sección de programación dinámica del informe.
- **`prueba.py`**: Script de evaluación. Carga un archivo `.txt`, ejecuta los seis algoritmos y mide sus tiempos de ejecución con la librería `time`.
- **`grafico_greedy.py` y `grafico_lineal.py`**: Generan los gráficos de tiempo experimental contra la curva teórica ajustada que se incluyen en el informe.
- **`resultados/`**: Se crea al ejecutar `prueba.py` con `--nombre`. No se versiona (está en `.gitignore`).
