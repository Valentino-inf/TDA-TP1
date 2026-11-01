import csv
import os
import statistics
import sys
import time

import matplotlib.pyplot as plt

# Agrega la carpeta principal a sys.path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greedy.greedy_mochila import mochila, leer_mochila
from backtracking_fuerza_bruta.fuerza_bruta import mochila_fuerza_bruta
from backtracking_fuerza_bruta.backtracking import mochila_backtracking
from programacion_lineal.programacion_lineal import mochila_lineal
from programacion_dinamica.tradicional import mochila_pd_tradicional
from programacion_dinamica.alternativo import mochila_pd_alternativo

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))

TAMANIOS = [10, 20, 50, 90, 100, 200, 300, 500, 1000]

MAX_N_FUERZA_BRUTA = 20
MAX_N_PD_ALTERNATIVO = 500

# (clave, etiqueta, funcion, limite de n, color, marcador)
ALGORITMOS = [
    ("fuerza_bruta", "Fuerza bruta", mochila_fuerza_bruta, MAX_N_FUERZA_BRUTA, "#2a78d6", "o"),
    ("backtracking", "Backtracking", mochila_backtracking, None, "#eb6834", "s"),
    ("greedy", "Greedy", mochila, None, "#1baf7a", "^"),
    ("pd_tradicional", "PD tradicional", mochila_pd_tradicional, None, "#eda100", "D"),
    ("pd_alternativo", "PD alternativo", mochila_pd_alternativo, MAX_N_PD_ALTERNATIVO, "#e87ba4", "v"),
    ("lineal", "Prog. lineal", mochila_lineal, None, "#008300", "P"),
]


def repeticiones(clave, n):
    """Cantidad de corridas por medicion: mas para los algoritmos rapidos."""
    if clave == "greedy":
        return 100
    if clave == "fuerza_bruta":
        return 3 if n <= 10 else 1
    if clave == "pd_alternativo":
        return 5 if n <= 100 else (3 if n <= 300 else 1)
    if clave == "pd_tradicional":
        return 5 if n <= 300 else 2
    if clave == "lineal":
        return 5
    return 10  # backtracking


def medir(algoritmo, capacidad, objetos, reps):
    tiempos = []
    for _ in range(reps):
        inicio = time.perf_counter()
        seleccionados, beneficio = algoritmo(capacidad, objetos)
        tiempos.append(time.perf_counter() - inicio)
    assert sum(objeto[0] for objeto in seleccionados) <= capacidad
    return statistics.median(tiempos), beneficio


def medir_todo():
    filas = []
    for n in TAMANIOS:
        archivo = f"mochila{n}.txt"
        capacidad, objetos = leer_mochila(os.path.join(DIRECTORIO, archivo))
        fila = {"archivo": archivo, "n": n, "capacidad": capacidad}
        for clave, etiqueta, funcion, limite, _, _ in ALGORITMOS:
            if limite is not None and n > limite:
                fila[f"tiempo_{clave}_s"] = ""
                fila[f"beneficio_{clave}"] = ""
                continue
            tiempo, beneficio = medir(funcion, capacidad, objetos, repeticiones(clave, n))
            fila[f"tiempo_{clave}_s"] = tiempo
            fila[f"beneficio_{clave}"] = beneficio
            print(f"{archivo:>16}  {etiqueta:<15} {tiempo:12.6f} s  beneficio={beneficio}", flush=True)
        filas.append(fila)
    return filas


def guardar_csv(filas, salida):
    columnas = ["archivo", "n", "capacidad"]
    for clave, *_ in ALGORITMOS:
        columnas += [f"tiempo_{clave}_s", f"beneficio_{clave}"]
    with open(salida, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({
                columna: (f"{valor:.6f}" if isinstance(valor, float) else valor)
                for columna, valor in fila.items()
            })


def graficar(filas, salida):
    fig, eje = plt.subplots(figsize=(10, 6))
    for clave, etiqueta, _, _, color, marcador in ALGORITMOS:
        puntos = [(f["n"], f[f"tiempo_{clave}_s"]) for f in filas if f[f"tiempo_{clave}_s"] != ""]
        eje.plot(
            [p[0] for p in puntos], [p[1] for p in puntos],
            marker=marcador, markersize=7, linewidth=2, color=color, label=etiqueta,
        )
    eje.set_xscale("log")
    eje.set_yscale("log")
    eje.set_xlabel("Cantidad de objetos (n)")
    eje.set_ylabel("Tiempo de ejecución (segundos)")
    eje.set_title("Comparación de los 6 algoritmos sobre los mismos sets (mochila10 a mochila1000)")
    eje.grid(True, which="both", linestyle="--", alpha=0.4)
    eje.legend()
    fig.tight_layout()
    fig.savefig(salida, dpi=300)
    plt.close(fig)


def imprimir_tabla_latex(filas):
    print("\nFilas para la tabla del informe:")
    for fila in filas:
        celdas = [str(fila["n"])]
        for clave, *_ in ALGORITMOS:
            tiempo = fila[f"tiempo_{clave}_s"]
            if tiempo == "":
                celdas.append("--")
            else:
                mantisa, exponente = f"{tiempo:.2e}".split("e")
                celdas.append(f"${mantisa} \\cdot 10^{{{int(exponente)}}}$")
        print(" & ".join(celdas) + r" \\")


def main():
    filas = medir_todo()
    guardar_csv(filas, os.path.join(DIRECTORIO, "conclusion_tiempos.csv"))
    graficar(filas, os.path.join(DIRECTORIO, "conclusion_tiempos.png"))
    imprimir_tabla_latex(filas)


if __name__ == "__main__":
    main()
