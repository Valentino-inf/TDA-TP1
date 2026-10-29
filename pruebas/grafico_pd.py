import argparse
import os
import statistics
import sys
import time
import matplotlib.pyplot as plt

# Agrega la carpeta principal a sys.path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greedy.greedy_mochila import leer_mochila
from programacion_dinamica.tradicional import mochila_pd_tradicional
from programacion_dinamica.alternativo import mochila_pd_alternativo

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))

TAMANIOS = [10, 20, 50, 90, 100, 200, 300, 500]

AD_HOC = ["mochila_gana_tradicional.txt", "mochila_gana_alternativo.txt"]

ALGORITMOS = {
    "tradicional": mochila_pd_tradicional,
    "alternativo": mochila_pd_alternativo,
}


def repeticiones(n):
    if n <= 100:
        return 5
    if n <= 300:
        return 3
    return 1


def medir(algoritmo, capacidad, objetos, reps):
    tiempos = []
    for _ in range(reps):
        inicio = time.perf_counter()
        seleccionados, beneficio = algoritmo(capacidad, objetos)
        tiempos.append(time.perf_counter() - inicio)

    assert sum(objeto[0] for objeto in seleccionados) <= capacidad
    assert sum(objeto[1] for objeto in seleccionados) == beneficio
    return statistics.median(tiempos), beneficio


def ajustar(tiempos, base):
    numerador = sum(f / t for f, t in zip(base, tiempos))
    denominador = sum((f / t) ** 2 for f, t in zip(base, tiempos))
    return numerador / denominador


def graficar_ajuste(nombre, etiqueta_base, tamanios, tiempos, base, salida):
    c = ajustar(tiempos, base)
    teorica = [c * f for f in base]
    error_max = max(abs(t - f) / t for t, f in zip(tiempos, teorica))

    fig, (eje_lineal, eje_log) = plt.subplots(1, 2, figsize=(13, 5.5))
    for eje in (eje_lineal, eje_log):
        eje.plot(tamanios, tiempos, marker="o", label="Tiempo experimental")
        eje.plot(tamanios, teorica, marker="o", linestyle="--",
                 label=f"Ajuste c·{etiqueta_base} (c = {c:.2e} s)")
        eje.set_xlabel("Cantidad de objetos (n)")
        eje.set_ylabel("Tiempo (segundos)")
        eje.grid(True, which="both", alpha=0.4)
        eje.legend()

    eje_lineal.set_title("Escala lineal")
    eje_log.set_xscale("log")
    eje_log.set_yscale("log")
    eje_log.set_title("Escala logarítmica")
    fig.suptitle(f"PD {nombre}: tiempo experimental vs. ajuste O({etiqueta_base})")
    fig.tight_layout()
    fig.savefig(os.path.join(DIRECTORIO, salida), dpi=300)
    plt.close(fig)
    return c, error_max


def graficar_comparacion(tamanios, tiempos, salida):
    fig, eje = plt.subplots(figsize=(9, 5.5))
    for nombre, serie in tiempos.items():
        eje.plot(tamanios, serie, marker="o", label=f"PD {nombre}")
    eje.set_xscale("log")
    eje.set_yscale("log")
    eje.set_xlabel("Cantidad de objetos (n)")
    eje.set_ylabel("Tiempo (segundos)")
    eje.set_title("Programación dinámica: planteo tradicional vs. alternativo")
    eje.grid(True, which="both", alpha=0.4)
    eje.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(DIRECTORIO, salida), dpi=300)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description="Mide y grafica los dos algoritmos de PD.")
    parser.add_argument("--adhoc", action="store_true",
                        help="Mide también los sets ad-hoc (tarda varios minutos).")
    args = parser.parse_args()

    tiempos = {nombre: [] for nombre in ALGORITMOS}
    capacidades = []
    beneficios_totales = []
    lineas = ["archivo,n,capacidad,beneficio_total,beneficio_optimo,tiempo_tradicional_s,tiempo_alternativo_s"]

    for n in TAMANIOS:
        archivo = f"mochila{n}.txt"
        capacidad, objetos = leer_mochila(os.path.join(DIRECTORIO, archivo))
        total = sum(objeto[1] for objeto in objetos)
        capacidades.append(capacidad)
        beneficios_totales.append(total)

        resultados = {}
        for nombre, algoritmo in ALGORITMOS.items():
            tiempo, beneficio = medir(algoritmo, capacidad, objetos, repeticiones(n))
            tiempos[nombre].append(tiempo)
            resultados[nombre] = beneficio
        assert resultados["tradicional"] == resultados["alternativo"]

        lineas.append(f"{archivo},{n},{capacidad},{total},{resultados['tradicional']},"
                      f"{tiempos['tradicional'][-1]:.6f},{tiempos['alternativo'][-1]:.6f}")
        print(f"n = {n:>4}  W = {capacidad:>6}  V = {total:>7}  "
              f"tradicional = {tiempos['tradicional'][-1]:.5f} s  "
              f"alternativo = {tiempos['alternativo'][-1]:.5f} s")

    graficar_comparacion(TAMANIOS, tiempos, "pd_comparacion.png")

    base_trad = [n * w for n, w in zip(TAMANIOS, capacidades)]
    base_alt = [n * v for n, v in zip(TAMANIOS, beneficios_totales)]
    c_trad, err_trad = graficar_ajuste("tradicional", "n·W", TAMANIOS, tiempos["tradicional"],
                                       base_trad, "pd_tradicional_ajuste.png")
    c_alt, err_alt = graficar_ajuste("alternativo", "n·V", TAMANIOS, tiempos["alternativo"],
                                     base_alt, "pd_alternativo_ajuste.png")

    print("\nGraficos generados: pd_comparacion.png, pd_tradicional_ajuste.png, pd_alternativo_ajuste.png")
    print(f"Ajuste tradicional: c = {c_trad:.3e} s por celda, error relativo maximo = {err_trad:.1%}")
    print(f"Ajuste alternativo: c = {c_alt:.3e} s por celda, error relativo maximo = {err_alt:.1%}")

    if args.adhoc:
        print("\nSets ad-hoc:")
        for archivo in AD_HOC:
            capacidad, objetos = leer_mochila(os.path.join(DIRECTORIO, archivo))
            total = sum(objeto[1] for objeto in objetos)
            fila = {}
            for nombre, algoritmo in ALGORITMOS.items():
                fila[nombre], beneficio = medir(algoritmo, capacidad, objetos, 1)
            lineas.append(f"{archivo},{len(objetos)},{capacidad},{total},{beneficio},"
                          f"{fila['tradicional']:.6f},{fila['alternativo']:.6f}")
            print(f"{archivo}: n = {len(objetos)}  W = {capacidad}  V = {total}  "
                  f"optimo = {beneficio}  tradicional = {fila['tradicional']:.4f} s  "
                  f"alternativo = {fila['alternativo']:.4f} s")

    with open(os.path.join(DIRECTORIO, "pd_tiempos.csv"), "w") as archivo:
        archivo.write("\n".join(lineas) + "\n")

    print("\nFilas para la tabla del informe (n & W & V & t_trad & t_alt):")
    for n, w, v, t_trad, t_alt in zip(TAMANIOS, capacidades, beneficios_totales,
                                      tiempos["tradicional"], tiempos["alternativo"]):
        print(f"        {n} & {w} & {v} & {t_trad:.6f} & {t_alt:.6f} \\\\")


if __name__ == "__main__":
    main()
