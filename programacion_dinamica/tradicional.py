def mochila_pd_tradicional(capacidad, objetos):
    n = len(objetos)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        peso = objetos[i-1][0]
        beneficio = objetos[i-1][1]
        for w in range(capacidad + 1):
            if peso <= w:
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - peso] + beneficio)
            else:
                dp[i][w] = dp[i-1][w]
                
    seleccionados = []
    w = capacidad
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i-1][w]:
            seleccionados.append(objetos[i-1])
            w -= objetos[i-1][0]
            
    seleccionados.reverse()
    return seleccionados, dp[n][capacidad]
