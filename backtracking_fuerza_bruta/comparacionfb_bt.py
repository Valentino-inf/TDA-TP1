import sys
import os
import time
import random
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from fuerza_bruta import mochila_fuerza_bruta
from backtracking import mochila_backtracking

def generar_caso_aleatorio(n):
    capacidad = n * 10
    objetos = [(random.randint(1, 15), random.randint(10, 100)) for _ in range(n)]
    return capacidad, objetos

def medir_tiempo(algoritmo, capacidad, objetos, repeticiones=3):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        algoritmo(capacidad, objetos)
    fin = time.perf_counter()
    return (fin - inicio) / repeticiones

def main():
    tamanos_n = [5, 10, 15, 18, 20, 22, 24]
    tiempos_fb = []
    tiempos_bt = []

    print(f"{'N':<5} | {'Fuerza Bruta (s)':<20} | {'Backtracking (s)':<20}")
    print("-" * 55)

    for n in tamanos_n:
        W, objetos = generar_caso_aleatorio(n)
        reps_bt = 10 if n < 20 else 3
        
        t_bt = medir_tiempo(mochila_backtracking, W, objetos, repeticiones=reps_bt)
        tiempos_bt.append(t_bt)
        
        t_fb = medir_tiempo(mochila_fuerza_bruta, W, objetos, repeticiones=1)
        tiempos_fb.append(t_fb)
        
        print(f"{n:<5} | {t_fb:<20.6f} | {t_bt:<20.6f}")

    plt.figure(figsize=(10, 6))
    plt.plot(tamanos_n, tiempos_fb, label='Fuerza Bruta (O(2^n) sin podas)', marker='o', color='red', linewidth=2)
    plt.plot(tamanos_n, tiempos_bt, label='Backtracking (con podas)', marker='s', color='green', linewidth=2)
    plt.xticks(tamanos_n)
    plt.xlabel('Cantidad de Objetos (N)')
    plt.ylabel('Tiempo de ejecución (segundos)')
    plt.title('Comparación de Crecimiento: Fuerza Bruta vs Backtracking')
    plt.legend()
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.yscale('log') 
    plt.tight_layout()
    plt.savefig("crecimiento_fb_vs_bt.png")

if __name__ == "__main__":
    main()