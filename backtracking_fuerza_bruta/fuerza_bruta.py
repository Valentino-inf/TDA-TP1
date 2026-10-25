import itertools

def leer_mochila(nombre_archivo):
    objetos = []

    with open(nombre_archivo, "r") as archivo:
        W = int(archivo.readline())

        for linea in archivo:
            peso, beneficio = linea.strip().split(",")
            objetos.append((int(peso), int(beneficio)))

    return W, objetos


def mochila_fuerza_bruta(capacidad, objetos):
    mejor_beneficio = 0
    mejor_combinacion = []
    n = len(objetos)
    
    for r in range(n + 1):
        for combinacion in itertools.combinations(objetos, r):
            peso_total = sum(item[0] for item in combinacion)
            
            if peso_total <= capacidad:
                beneficio_total = sum(item[1] for item in combinacion)
                if beneficio_total > mejor_beneficio:
                    mejor_beneficio = beneficio_total
                    mejor_combinacion = list(combinacion)
                    
    return mejor_combinacion, mejor_beneficio
