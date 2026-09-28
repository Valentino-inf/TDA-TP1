import pulp

# Pre: 
#   Capacidad: máxima de la mochila
#   Objetos: lista de tuplas (peso, valor)
# Post:
#   valor_total: valor máximo obtenido
#   objetos_seleccionados: índices de los objetos seleccionados
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
        i for i in range(n)
        if pulp.value(x[i]) == 1
    ]

    valor_total = sum(
        objetos[i][1]
        for i in objetos_seleccionados
    )

    return valor_total, objetos_seleccionados