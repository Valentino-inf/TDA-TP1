import sys

#aumento el limite de recursion(sino no compila)
sys.setrecursionlimit(2500)

def leer_archivo_mochila(nombre_archivo):
    objetos = []
    with open(nombre_archivo, "r") as arch:
        capacidad = int(arch.readline())
        for linea in arch:
            linea = linea.strip()
            if linea:
                datos = linea.split(",")
                objetos.append((int(datos[0]), int(datos[1])))
    return capacidad, objetos

def calcular_rama(indice, peso_acumulado, beneficio_acumulado, capacidad, objetos):
    beneficio = beneficio_acumulado
    peso_actual = peso_acumulado
    i = indice
    
    while i < len(objetos) and peso_actual + objetos[i][0] <= capacidad:
        peso_actual += objetos[i][0]
        beneficio += objetos[i][1]
        i += 1
        
    return beneficio

def mochila_backtracking(capacidad, objetos):
    objetos.sort(key=lambda x: x[1]/x[0], reverse=True)
    
    mejor_beneficio = 0

    def explorar(indice, peso_acumulado, beneficio_acumulado):
        nonlocal mejor_beneficio
        
        if beneficio_acumulado > mejor_beneficio:
            mejor_beneficio = beneficio_acumulado
            
        if indice == len(objetos):
            return

        beneficio_futuro = calcular_rama(indice, peso_acumulado, beneficio_acumulado, capacidad, objetos)
        if beneficio_futuro <= mejor_beneficio:
            return

        peso_actual = objetos[indice][0]
        beneficio_actual = objetos[indice][1]
        
        if peso_acumulado + peso_actual <= capacidad:
            explorar(
                indice + 1, 
                peso_acumulado + peso_actual, 
                beneficio_acumulado + beneficio_actual
            )

        explorar(indice + 1, peso_acumulado, beneficio_acumulado)

    explorar(0, 0, 0)
    
    return mejor_beneficio


capacidad_total, lista_objetos = leer_archivo_mochila("/home/valentino/facu/TDA/mochila1000.txt")

maximo_beneficio = mochila_backtracking(capacidad_total, lista_objetos)
print(f"El beneficio máximo posible es: {maximo_beneficio}")