import sys
import os
import time

# Agrega la carpeta principal a sys.path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from greedy.greedy_mochila import mochila, leer_mochila
from backtracking_fuerza_bruta.fuerza_bruta import mochila_fuerza_bruta
from backtracking_fuerza_bruta.backtracking import mochila_backtracking
from programacion_lineal.programacion_lineal import mochila_lineal
from programacion_dinamica.tradicional import Item as ItemTradicional
from programacion_dinamica.alternativo import Item as ItemAlternativo


def medir_tiempo(algoritmo, W, objetos, repeticiones=1):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        seleccionados, beneficio = algoritmo(W, objetos)
    fin = time.perf_counter()
    tiempo_promedio = (fin - inicio) / repeticiones
    return seleccionados, beneficio, tiempo_promedio


def probar_greedy(W, objetos):
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


def probar_backtracking(W, objetos, n):
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


def probar_fuerza_bruta(W, objetos, n):
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


def wrapper_lineal(W, objetos):
    beneficio, indices = mochila_lineal(W, objetos)
    seleccionados = [objetos[i] for i in indices]
    return seleccionados, beneficio


def probar_lineal(W, objetos):
    print("\n--- PROGRAMACIÓN LINEAL ---")
    seleccionados, beneficio, tiempo = medir_tiempo(
        wrapper_lineal, W, objetos, repeticiones=10
    )
    peso_total = sum(objeto[0] for objeto in seleccionados)
    print("Beneficio obtenido:", beneficio)
    print("Peso total:", peso_total)
    print("Respeta capacidad:", peso_total <= W)
    print("Tiempo promedio:", tiempo, "segundos")


def wrapper_pd_tradicional(W, objetos):
    items = [ItemTradicional(p, b) for p, b in objetos]
    solutions = [0] * (W + 1)
    
    for item in items:
        for w in range(W, item.weight - 1, -1):
            solutions[w] = max(solutions[w], solutions[w - item.weight] + item.benefit)
            
    return [], solutions[W]


def probar_pd_tradicional(W, objetos):
    print("\n--- PD TRADICIONAL ---")
    seleccionados, beneficio, tiempo = medir_tiempo(
        wrapper_pd_tradicional, W, objetos, repeticiones=10
    )
    # Como DP Tradicional no devuelve los objetos en esta implementación, omitimos el peso
    print("Beneficio obtenido:", beneficio)
    print("Tiempo promedio:", tiempo, "segundos")


def wrapper_pd_alternativo(W, objetos):
    items = [ItemAlternativo(p, b) for p, b in objetos]
    max_benefit = sum(b for p, b in objetos)
    
    solutions = [float('inf')] * (max_benefit + 1)
    solutions[0] = 0
    
    for item in items:
        for v in range(max_benefit, -1, -1):
            solutions[v] = min(solutions[v], solutions[max(0, v - item.benefit)] + item.weight)
            
    result = 0
    for v in range(max_benefit, -1, -1):
        if solutions[v] <= W:
            result = v
            break
            
    return [], result


def probar_pd_alternativo(W, objetos):
    print("\n--- PD ALTERNATIVO ---")
    seleccionados, beneficio, tiempo = medir_tiempo(
        wrapper_pd_alternativo, W, objetos, repeticiones=10
    )
    # Como DP Alternativo no devuelve los objetos en esta implementación, omitimos el peso
    print("Beneficio obtenido:", beneficio)
    print("Tiempo promedio:", tiempo, "segundos")


def main():
    if len(sys.argv) < 2:
        print("Uso: python prueba.py <ruta_al_archivo>")
        sys.exit(1)
        
    nombre_archivo = sys.argv[1]

    try:
        W, objetos = leer_mochila(nombre_archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        sys.exit(1)
        
    n = len(objetos)

    print("\n" + "="*50)
    print("Archivo: ", nombre_archivo)
    print("Cantidad de objetos: ", n)
    print("Capacidad: ", W)
    
    probar_greedy(W, objetos)
    probar_pd_tradicional(W, objetos)
    probar_pd_alternativo(W, objetos)
    probar_lineal(W, objetos) # Está fallando
    probar_backtracking(W, objetos, n)
    probar_fuerza_bruta(W, objetos, n)


if __name__ == "__main__":
    main()
