# Análisis de Complejidad Temporal - Programación Dinámica

A continuación se detalla el análisis del orden de complejidad temporal para ambos algoritmos desarrollados. En ambos casos, el problema de la mochila 
se resuelve mediante un enfoque pseudo-polinomial utilizando programación dinámica.

Definimos las siguientes variables para el análisis:
* $N$: Cantidad total de elementos (ítems).
* $W$: Capacidad máxima (peso) de la mochila.
* $V$: Beneficio máximo posible (la sumatoria de los beneficios de todos los ítems).

---

## 1. Planteo Tradicional (`traditional.py`)
**Objetivo:** Maximizar el beneficio para una capacidad fija.

### Análisis:
1. **Lectura y parseo del archivo:** Iterar sobre las líneas del archivo para construir la lista de elementos toma un tiempo de $\mathcal{O}(N)$.
2. **Inicialización del arreglo:** Se crea un arreglo de tamaño $W+1$ que toma un tiempo de $\mathcal{O}(W)$.
3. **Lógica Principal (Programación Dinámica):**
   * Existe un bucle externo que itera sobre los $N$ elementos.
   * Por cada elemento, existe un bucle interno que itera desde la capacidad máxima $W$ hasta el peso del elemento, lo que en el peor de los casos significa iterar $W$ veces.
   * Las operaciones dentro del bucle interno (comparación, suma y asignación) se ejecutan en tiempo constante $\mathcal{O}(1)$.
   * Por lo tanto, el doble bucle toma un tiempo de $\mathcal{O}(N \times W)$.

**Complejidad Temporal Final:** $\mathcal{O}(N \times W)$

---

## 2. Planteo Alternativo (`alternative.py`)
**Objetivo:** Minimizar el peso para alcanzar un beneficio fijo.

### Análisis:
1. **Lectura y parseo del archivo:** Al igual que en el algoritmo anterior, iterar sobre las líneas para construir los elementos y calcular la suma total de beneficios ($V$) toma $\mathcal{O}(N)$.
2. **Inicialización del arreglo:** Se crea un arreglo de tamaño $V+1$ que toma un tiempo de $\mathcal{O}(V)$.
3. **Lógica Principal (Programación Dinámica):**
   * El bucle externo itera sobre los $N$ elementos.
   * El bucle interno itera sobre todos los posibles beneficios, desde $V$ hasta 0 (es decir, $V$ iteraciones por cada elemento).
   * Las operaciones dentro de los bucles son de acceso, suma, cálculo de máximo y asignación en tiempo constante $\mathcal{O}(1)$.
   * Este bloque toma un tiempo de $\mathcal{O}(N \times V)$.
4. **Búsqueda del resultado óptimo:** Una vez llenada la tabla, se realiza un último bucle de a lo sumo $V$ iteraciones para encontrar el máximo beneficio que cumple con la capacidad de la mochila, tomando $\mathcal{O}(V)$.

**Complejidad Temporal Final:** $\mathcal{O}(N \times V)$

---

### Conclusión
* El **planteo tradicional** es preferible y más eficiente cuando la capacidad $W$ es relativamente pequeña en comparación con la sumatoria de los beneficios $V$.
* El **planteo alternativo** resulta mucho más veloz y es la mejor opción cuando los beneficios son pequeños pero la capacidad de la mochila $W$ es exageradamente grande.
