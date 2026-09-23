def mochila(W, objetos):

    objetos_validos = [
    objeto for objeto in objetos
    if objeto[0] <= W
    ]

    objetos_ordenados = sorted(
        objetos_validos,
        key=lambda objeto: objeto[1] / objeto[0],
        reverse=True
    )

    seleccionados = []
    peso_acumulado = 0
    beneficio_acumulado = 0
    elemento_critico = None

    for objeto in objetos_ordenados:
        peso = objeto[0]
        beneficio = objeto[1]

        if peso_acumulado + peso <= W:
            seleccionados.append(objeto)
            peso_acumulado += peso
            beneficio_acumulado += beneficio
        else:
            elemento_critico = objeto
            break

    if elemento_critico is None:
        return seleccionados, beneficio_acumulado

    if beneficio_acumulado >= elemento_critico[1]:
        return seleccionados, beneficio_acumulado
    else:
        return [elemento_critico], elemento_critico[1]

def leer_mochila(nombre_archivo):
    objetos = []

    with open(nombre_archivo, "r") as archivo:
        W = int(archivo.readline())

        for linea in archivo:
            peso, beneficio = linea.strip().split(",")
            objetos.append((int(peso), int(beneficio)))

    return W, objetos

# Caso 1: gana P1

#W = 10

#objetos = [
#    (4, 20),  # A
#   (5, 20),  # B
#   (3, 9)    # C
#]

#seleccionados, beneficio = mochila(W, objetos)

#print("Objetos seleccionados:", seleccionados)
#print("Beneficio:", beneficio)



# Caso 2: gana P2

# W = 10

# objetos = [
#     (2, 20),  # A
#     (9, 81)   # B
# ]

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio) 




# Caso borde 1: no hay objetos

# W = 10
# objetos = []

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio)



# Caso borde 2: capacidad exacta

# W = 10

# objetos = [
#     (4, 20),
#     (6, 18)
# ]

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio)



# Caso borde 3: objeto que pesa más que la capacidad

# W = 10

# objetos = [
#     (4, 20),
#     (15, 100)
# ]

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio)




# Caso borde 4: ningún objeto entra

# W = 10

# objetos = [
#     (15, 100),
#     (20, 200),
#     (11, 50)
# ]

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio)




# Caso borde 5: un único objeto ocupa exactamente toda la capacidad

# W = 10

# objetos = [
#     (10, 50)
# ]

# seleccionados, beneficio = mochila(W, objetos)

# print("Objetos seleccionados:", seleccionados)
# print("Beneficio:", beneficio)




# Prueba con mochila1000.txt

W, objetos = leer_mochila("mochila1000.txt")

seleccionados, beneficio = mochila(W, objetos)

peso_total = sum(objeto[0] for objeto in seleccionados)

print("Cantidad de objetos:", len(objetos))
print("Capacidad:", W)
print("Cantidad seleccionada:", len(seleccionados))
print("Beneficio obtenido:", beneficio)
print("Peso total seleccionado:", peso_total)
print("Respeta capacidad:", peso_total <= W)


#Notas: 

Implementado el algoritmo greedy de mochila 0/1 con garantía 1/2. 
Se verificaron los ejemplos realizados manualmente y distintos casos borde. 
Además, se probó con una instancia de 1000 objetos, obteniendo una solución de 
beneficio 411063 y peso 49972 para una capacidad máxima de 50000.