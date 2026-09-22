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

def mochila_fuerza_bruta(capacidad, objetos, indice=0):
    if indice == len(objetos) or capacidad == 0:
        return 0
        
    peso_actual = objetos[indice][0]
    beneficio_actual = objetos[indice][1]
    
    if peso_actual > capacidad:
        return mochila_fuerza_bruta(capacidad, objetos, indice + 1)
        
    beneficio_incluyendo = beneficio_actual + mochila_fuerza_bruta(
        capacidad - peso_actual, objetos, indice + 1
    )
    
    beneficio_excluyendo = mochila_fuerza_bruta(capacidad, objetos, indice + 1)
    
    return max(beneficio_incluyendo, beneficio_excluyendo)


nombre_archivo = "mochila1000.txt"

capacidad_total, lista_objetos = leer_archivo_mochila("/home/valentino/facu/TDA/mochila1000.txt")

objetos_prueba = lista_objetos[:20]

capacidad_prueba = 1000
maximo_beneficio = mochila_fuerza_bruta(capacidad_prueba, objetos_prueba)
print(f"¡Terminado! El beneficio máximo posible para estos 20 objetos es: {maximo_beneficio}")