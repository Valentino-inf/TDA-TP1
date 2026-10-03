import pulp

# Pre: 
#   Capacidad: máxima de la mochila
#   Objetos: lista de tuplas (peso, valor)
# Post:
#   objetos_seleccionados: lista de tuplas de los objetos seleccionados
#   valor_total: valor máximo obtenido
def mochila_lineal(capacidad, objetos):
    n = len(objetos)
    problema = pulp.LpProblem("mochila", pulp.LpMaximize)

    x = [
      pulp.LpVariable(f"x{i}", cat=pulp.LpBinary) 
      for i in range(n)
    ]

    problema += pulp.lpSum(
      objetos[i][1] * x[i] 
      for i in range(n)
    )

    problema += pulp.lpSum(
      objetos[i][0] * x[i] 
      for i in range(n)
    ) <= capacidad

    problema.solve(pulp.PULP_CBC_CMD(msg=False))

    # A continuación, 
    # obtengo y calculo valor total

    objetos_seleccionados = [
        objetos[i] for i in range(n)
        if pulp.value(x[i]) == 1
    ]

    valor_total = sum(
        obj[1]
        for obj in objetos_seleccionados
    )

    return objetos_seleccionados, valor_total