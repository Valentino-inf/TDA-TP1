def leer_mochila(nombre_archivo):
    objetos = []

    with open(nombre_archivo, "r") as archivo:
        W = int(archivo.readline())

        for linea in archivo:
            peso, beneficio = linea.strip().split(",")
            objetos.append((int(peso), int(beneficio)))

    return W, objetos

def mochila_fuerza_bruta(capacidad, objetos, indice=0):
    if indice == len(objetos) or capacidad == 0:
        return [], 0
        
    peso_actual = objetos[indice][0]
    beneficio_actual = objetos[indice][1]
    
    if peso_actual > capacidad:
        return mochila_fuerza_bruta(capacidad, objetos, indice + 1)
        
    objetos_incluyendo, beneficio_sub_incluyendo = mochila_fuerza_bruta(
        capacidad - peso_actual, objetos, indice + 1
    )
    beneficio_incluyendo = beneficio_actual + beneficio_sub_incluyendo
    
    objetos_excluyendo, beneficio_excluyendo = mochila_fuerza_bruta(capacidad, objetos, indice + 1)
    
    if beneficio_incluyendo > beneficio_excluyendo:
        return [objetos[indice]] + objetos_incluyendo, beneficio_incluyendo
    else:
        return objetos_excluyendo, beneficio_excluyendo
