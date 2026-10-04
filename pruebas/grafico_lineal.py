import os
import sys
import math
import random
import statistics
import time
import matplotlib.pyplot as plt

# Agrega la carpeta principal a sys.path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from programacion_lineal.programacion_lineal import mochila_lineal

DIRECTORIO = os.path.dirname(os.path.abspath(__file__))

tamanios = [10, 20, 50, 90, 100, 500, 1000, 5000, 10000]
INSTANCIAS = 5      # instancias aleatorias distintas por tamaño
REPETICIONES = 3    # corridas por instancia (se toma la mediana)
SEMILLA = 17


# Misma distribución que crear_mochila.py, pero en memoria y con semilla fija
def generar_mochila(n):
    capacidad = n * 50
    objetos = [(random.randint(1, 200), random.randint(1, 1000)) for _ in range(n)]
    return capacidad, objetos


def medir(capacidad, objetos):
    # Corrida descartada: la primera invocación de CBC paga costos de arranque
    mochila_lineal(capacidad, objetos)

    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        seleccionados, beneficio = mochila_lineal(capacidad, objetos)
        tiempos.append(time.perf_counter() - inicio)

    assert sum(objeto[0] for objeto in seleccionados) <= capacidad
    return statistics.median(tiempos), beneficio


random.seed(SEMILLA)
tiempos = []
minimos = []
maximos = []
lineas = ["n,instancia,capacidad,beneficio,tiempo_mediana_s"]

# El tiempo de CBC depende de la instancia (cuantos nodos explora el branch and
# bound), no solo de n: por eso se promedian varias instancias por tamaño.
for n in tamanios:
    tiempos_n = []
    for instancia in range(INSTANCIAS):
        capacidad, objetos = generar_mochila(n)
        tiempo, beneficio = medir(capacidad, objetos)
        tiempos_n.append(tiempo)
        lineas.append(f"{n},{instancia},{capacidad},{beneficio},{tiempo:.6f}")
    tiempos.append(statistics.mean(tiempos_n))
    minimos.append(min(tiempos_n))
    maximos.append(max(tiempos_n))
    print(f"n = {n:>5}  promedio = {tiempos[-1]:.5f} s  "
          f"[{minimos[-1]:.5f}, {maximos[-1]:.5f}]")

# Ajuste por minimos cuadrados de T(n) = a * n log(n) + b, minimizando el error
# relativo (peso 1/T^2) para que los n chicos no queden opacados por los grandes.
# El termino b es necesario: cada llamada lanza el proceso de CBC y se comunica
# con el por archivos, lo que agrega un costo fijo que no depende de n.
teorica_base = [n * math.log2(n) for n in tamanios]
pesos = [1 / t ** 2 for t in tiempos]
s_w = sum(pesos)
s_f = sum(w * f for w, f in zip(pesos, teorica_base))
s_t = sum(w * t for w, t in zip(pesos, tiempos))
s_ff = sum(w * f * f for w, f in zip(pesos, teorica_base))
s_ft = sum(w * f * t for w, f, t in zip(pesos, teorica_base, tiempos))
a = (s_w * s_ft - s_f * s_t) / (s_w * s_ff - s_f ** 2)
b = (s_t - a * s_f) / s_w

teorica_ajustada = [a * f + b for f in teorica_base]
errores = [[t - mn for t, mn in zip(tiempos, minimos)],
           [mx - t for t, mx in zip(tiempos, maximos)]]

fig, (eje_lineal, eje_log) = plt.subplots(1, 2, figsize=(13, 5.5))

for eje in (eje_lineal, eje_log):
    eje.errorbar(tamanios, tiempos, yerr=errores, marker="o", capsize=3,
                 label=f"Tiempo experimental (promedio de {INSTANCIAS} instancias)")
    eje.plot(tamanios, teorica_ajustada, marker="o", linestyle="--",
             label="Ajuste a·n log n + b")
    eje.set_xlabel("Cantidad de objetos (n)")
    eje.set_ylabel("Tiempo (segundos)")
    eje.grid(True, which="both", alpha=0.4)
    eje.legend()

eje_lineal.set_title("Escala lineal")
eje_log.set_xscale("log")
eje_log.set_yscale("log")
eje_log.set_title("Escala logarítmica")

fig.suptitle("Programación lineal (PuLP + CBC): tiempo experimental vs. ajuste")
fig.tight_layout()

fig.savefig(os.path.join(DIRECTORIO, "lineal_tiempos.png"), dpi=300)
plt.close(fig)

with open(os.path.join(DIRECTORIO, "lineal_tiempos.csv"), "w") as archivo:
    archivo.write("\n".join(lineas) + "\n")

print("Grafico generado: lineal_tiempos.png")
print(f"Ajuste: a = {a:.3e} s, b = {b:.3e} s")
