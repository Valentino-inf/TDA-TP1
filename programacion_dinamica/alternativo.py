def mochila_pd_alternativo(capacidad, objetos):
    n = len(objetos)
    if n == 0:
        return [], 0
        
    max_benefit = sum(obj[1] for obj in objetos)
    
    dp = [[float('inf')] * (max_benefit + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = 0
        
    for i in range(1, n + 1):
        peso = objetos[i-1][0]
        beneficio = objetos[i-1][1]
        for v in range(max_benefit + 1):
            dp[i][v] = min(dp[i-1][v], dp[i-1][max(0, v - beneficio)] + peso)
            
    mejor_v = 0
    for v in range(max_benefit, -1, -1):
        if dp[n][v] <= capacidad:
            mejor_v = v
            break
            
    seleccionados = []
    v = mejor_v
    for i in range(n, 0, -1):
        if v <= 0:
            break
            
        peso = objetos[i-1][0]
        beneficio = objetos[i-1][1]
        
        # Si el valor actual viene de NO incluir el objeto i-1
        if dp[i][v] == dp[i-1][v]:
            continue
        else:
            # Si viene de incluirlo
            seleccionados.append(objetos[i-1])
            v = max(0, v - beneficio)
            
    seleccionados.reverse()
    return seleccionados, mejor_v
