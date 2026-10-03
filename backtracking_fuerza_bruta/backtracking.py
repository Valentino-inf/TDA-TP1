import sys

#aumento el limite de recursion(sino no compila)
sys.setrecursionlimit(2500)

def leer_mochila(nombre_archivo):
    objetos = []

    with open(nombre_archivo, "r") as archivo:
        W = int(archivo.readline())

        for linea in archivo:
            peso, beneficio = linea.strip().split(",")
            objetos.append((int(peso), int(beneficio)))

    return W, objetos


def calcular_rama(indice, peso_acumulado, beneficio_acumulado, capacidad, objetos):
    beneficio = beneficio_acumulado
    peso_actual = peso_acumulado
    i = indice
    
    while i < len(objetos) and peso_actual + objetos[i][0] <= capacidad:
        peso_actual += objetos[i][0]
        beneficio += objetos[i][1]
        i += 1

    # Fraccion del primer objeto que no entra: asi la cota es superior (relajacion lineal)
    if i < len(objetos):
        restante = capacidad - peso_actual
        beneficio += objetos[i][1] * restante / objetos[i][0]

    return beneficio

def mochila_backtracking(capacidad, objetos):
    objetos = sorted(objetos, key=lambda x: x[1]/x[0], reverse=True)
    
    mejor_beneficio = 0
    mejor_combinacion = []

    def explorar(indice, peso_acumulado, beneficio_acumulado, combinacion_actual):
        nonlocal mejor_beneficio, mejor_combinacion
        
        if beneficio_acumulado > mejor_beneficio:
            mejor_beneficio = beneficio_acumulado
            mejor_combinacion = combinacion_actual[:]
            
        if indice == len(objetos):
            return

        beneficio_futuro = calcular_rama(indice, peso_acumulado, beneficio_acumulado, capacidad, objetos)
        if beneficio_futuro <= mejor_beneficio:
            return

        peso_actual = objetos[indice][0]
        beneficio_actual = objetos[indice][1]
        
        if peso_acumulado + peso_actual <= capacidad:
            combinacion_actual.append(objetos[indice])
            explorar(
                indice + 1, 
                peso_acumulado + peso_actual, 
                beneficio_acumulado + beneficio_actual,
                combinacion_actual
            )
            combinacion_actual.pop()

        explorar(indice + 1, peso_acumulado, beneficio_acumulado, combinacion_actual)

    explorar(0, 0, 0, []) 
    
    return mejor_combinacion, mejor_beneficio
