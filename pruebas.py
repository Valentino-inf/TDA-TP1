# Cantidad de repeticiones según el algoritmo.
# Para algoritmos rápidos se pueden usar varias repeticiones y promediar.
# Para fuerza bruta se pueden usar menos repeticiones si los tiempos son altos.

import time

from greedy_mochila import mochila, leer_mochila


ARCHIVOS = [
    "mochila10.txt",
    "mochila20.txt",
    "mochila50.txt",
    "mochila90.txt"
]


def medir_tiempo(algoritmo, W, objetos, repeticiones=1):

    inicio = time.perf_counter()

    for _ in range(repeticiones):
        seleccionados, beneficio = algoritmo(W, objetos)

    fin = time.perf_counter()

    tiempo_promedio = (fin - inicio) / repeticiones

    return seleccionados, beneficio, tiempo_promedio


for nombre_archivo in ARCHIVOS:

    W, objetos = leer_mochila(nombre_archivo)

    seleccionados, beneficio, tiempo = medir_tiempo(
        mochila,
        W,
        objetos,
        repeticiones=100
    )

    peso_total = sum(objeto[0] for objeto in seleccionados)

    print("\nArchivo:", nombre_archivo)
    print("Cantidad de objetos:", len(objetos))
    print("Capacidad:", W)
    print("Beneficio obtenido:", beneficio)
    print("Peso total:", peso_total)
    print("Respeta capacidad:", peso_total <= W)
    print("Tiempo promedio:", tiempo, "segundos")