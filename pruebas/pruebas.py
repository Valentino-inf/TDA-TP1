import time

from greedy.greedy_mochila import mochila, leer_mochila
from backtracking_fuerza_bruta.fuerza_bruta import mochila_fuerza_bruta
from backtracking_fuerza_bruta.backtracking import mochila_backtracking


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
    n = len(objetos)

    print("\n" + "="*50)
    print("Archivo:", nombre_archivo)
    print("Cantidad de objetos:", n)
    print("Capacidad:", W)
    
    ##GREEDY
    print("\n--- GREEDY ---")
    seleccionados, beneficio, tiempo = medir_tiempo(
        mochila,
        W,
        objetos,
        repeticiones=100
    )

    peso_total = sum(objeto[0] for objeto in seleccionados)

    print("Beneficio obtenido:", beneficio)
    print("Peso total:", peso_total)
    print("Respeta capacidad:", peso_total <= W)
    print("Tiempo promedio:", tiempo, "segundos")

    ##BACKTRACKING
    print("\n--- BACKTRACKING ---")
    reps_bt = 30 if n < 50 else 15
    
    seleccionados, beneficio, tiempo = medir_tiempo(
        mochila_backtracking,
        W,
        objetos,
        repeticiones=reps_bt
    )

    peso_total = sum(objeto[0] for objeto in seleccionados)

    print("Beneficio obtenido:", beneficio)
    print("Peso total:", peso_total)
    print("Respeta capacidad:", peso_total <= W)
    print("Tiempo promedio:", tiempo, "segundos")

    ##FBRUTA
    print("\n--- FUERZA BRUTA ---")
    if n <= 25:
        seleccionados, beneficio, tiempo = medir_tiempo(
            mochila_fuerza_bruta,
            W,
            objetos,
            repeticiones=1
        )

        peso_total = sum(objeto[0] for objeto in seleccionados)

        print("Beneficio obtenido:", beneficio)
        print("Peso total:", peso_total)
        print("Respeta capacidad:", peso_total <= W)
        print("Tiempo promedio:", tiempo, "segundos")
    else:
        print(f"Omitido: {n} muchos objetos para Fbruta")