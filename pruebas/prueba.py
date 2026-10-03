import sys
import os
import time
import argparse
import matplotlib.pyplot as plt

# Agrega la carpeta principal a sys.path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from greedy.greedy_mochila import mochila, leer_mochila
from backtracking_fuerza_bruta.fuerza_bruta import mochila_fuerza_bruta
from backtracking_fuerza_bruta.backtracking import mochila_backtracking
from programacion_lineal.programacion_lineal import mochila_lineal
from programacion_dinamica.tradicional import mochila_pd_tradicional
from programacion_dinamica.alternativo import mochila_pd_alternativo

class Logger(object):
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

def medir_tiempo(algoritmo, capacidad, objetos, repeticiones=1):
    inicio = time.perf_counter()
    for _ in range(repeticiones):
        seleccionados, beneficio = algoritmo(capacidad, objetos)
    fin = time.perf_counter()
    tiempo_promedio = (fin - inicio) / repeticiones
    return seleccionados, beneficio, tiempo_promedio

def imprimir_resultados(nombre, seleccionados, beneficio, tiempo, capacidad):
    peso_total = sum(objeto[0] for objeto in seleccionados)
    print(f"## {nombre}")
    print(f"- Beneficio obtenido: {beneficio}")
    print(f"- Peso total: {peso_total}")
    print(f"- Respeta capacidad: {peso_total <= capacidad}")
    print(f"- Tiempo promedio: {tiempo} segundos\n")

def probar_greedy(capacidad, objetos):
    seleccionados, beneficio, tiempo = medir_tiempo(mochila, capacidad, objetos, repeticiones=100)
    imprimir_resultados("GREEDY", seleccionados, beneficio, tiempo, capacidad)
    return tiempo

def probar_backtracking(capacidad, objetos, n):
    reps_bt = 30 if n < 50 else 15
    seleccionados, beneficio, tiempo = medir_tiempo(mochila_backtracking, capacidad, objetos, repeticiones=reps_bt)
    imprimir_resultados("BACKTRACKING", seleccionados, beneficio, tiempo, capacidad)
    return tiempo

def probar_fuerza_bruta(capacidad, objetos, n):
    if n <= 25:
        seleccionados, beneficio, tiempo = medir_tiempo(mochila_fuerza_bruta, capacidad, objetos, repeticiones=1)
        imprimir_resultados("FUERZA BRUTA", seleccionados, beneficio, tiempo, capacidad)
        return tiempo
    else:
        print(f"## FUERZA BRUTA\nOmitido: {n} muchos objetos para Fbruta\n")
        return None

def probar_lineal(capacidad, objetos):
    seleccionados, beneficio, tiempo = medir_tiempo(mochila_lineal, capacidad, objetos, repeticiones=10)
    imprimir_resultados("PROGRAMACIÓN LINEAL", seleccionados, beneficio, tiempo, capacidad)
    return tiempo

def probar_pd_tradicional(capacidad, objetos):
    seleccionados, beneficio, tiempo = medir_tiempo(mochila_pd_tradicional, capacidad, objetos, repeticiones=10)
    imprimir_resultados("PROGRAMACION DINAMICA TRADICIONAL", seleccionados, beneficio, tiempo, capacidad)
    return tiempo

def probar_pd_alternativo(capacidad, objetos):
    seleccionados, beneficio, tiempo = medir_tiempo(mochila_pd_alternativo, capacidad, objetos, repeticiones=10)
    imprimir_resultados("PROGRAMACION DINAMICA ALTERNATIVO", seleccionados, beneficio, tiempo, capacidad)
    return tiempo

def main():
    parser = argparse.ArgumentParser(description="Ejecuta la prueba de la mochila para un archivo.")
    parser.add_argument("--archivo", type=str, help="Ruta al archivo de prueba.")
    parser.add_argument("--nombre", type=str, help="Nombre de la prueba para guardar los resultados.")
    args = parser.parse_args()
        
    nombre_archivo = args.archivo

    if args.nombre:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        dir_resultados = os.path.join(script_dir, "resultados", args.nombre)
        os.makedirs(dir_resultados, exist_ok=True)
        archivo_resultado = os.path.join(dir_resultados, "resultado.md")
        sys.stdout = Logger(archivo_resultado)
        print(f"# PRUEBA: {args.nombre}\n")

    try:
        capacidad, objetos = leer_mochila(nombre_archivo)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{nombre_archivo}'")
        sys.exit(1)
        
    n = len(objetos)

    print(f"- Archivo: {nombre_archivo}")
    print(f"- Cantidad de objetos: {n}")
    print(f"- Capacidad: {capacidad}\n")

    tiempos = {
        "Greedy": probar_greedy(capacidad, objetos),
        "PD Tradicional": probar_pd_tradicional(capacidad, objetos),
        "PD Alternativo": probar_pd_alternativo(capacidad, objetos),
        "Prog. Lineal": probar_lineal(capacidad, objetos),
        "Backtracking": probar_backtracking(capacidad, objetos, n)}

    t_fuerza_bruta = probar_fuerza_bruta(capacidad, objetos, n)
    if t_fuerza_bruta is not None:
        tiempos["Fuerza Bruta"] = t_fuerza_bruta

    if args.nombre:
        grafico_path = os.path.join(dir_resultados, "tiempos.png")
        
        nombres = list(tiempos.keys())
        valores = list(tiempos.values())
        
        plt.figure(figsize=(10, 6))
        plt.bar(nombres, valores, color='skyblue')
        plt.xlabel('Algoritmos')
        plt.ylabel('Tiempo (segundos)')
        plt.title('Tiempos de ejecución por algoritmo')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(grafico_path)
        plt.close()

        print(f"## Gráfico de tiempos\n")
        print(f'<img src="tiempos.png" alt="Gráfico de tiempos" />\n')

        print(f"## Tabla de resultados\n")
        print(f"| Algoritmo | Tiempo (segundos) |")
        print(f"|---|---|")
        for nombre, tiempo in tiempos.items():
            print(f"| {nombre} | {tiempo:.8f} |")
        print("\n")

if __name__ == "__main__":
    main()
