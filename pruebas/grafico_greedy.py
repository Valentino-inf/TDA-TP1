import math
import matplotlib.pyplot as plt

tamanios = [10, 20, 50, 90, 100, 500, 1000, 5000, 10000]

tiempos = [
    0.000001689280,
    0.000002921810,
    0.000006529700,
    0.000012225130,
    0.000014572150,
    0.000071820000,
    0.000148769780,
    0.000957232990,
    0.002141300510,
]

# Valores de la funcion teorica n log(n)
teorica_base = [n * math.log2(n) for n in tamanios]

# Ajuste por minimos cuadrados de T(n) = c * n log(n)
numerador = sum(t * f for t, f in zip(tiempos, teorica_base))
denominador = sum(f * f for f in teorica_base)
c = numerador / denominador

teorica_ajustada = [c * f for f in teorica_base]

plt.figure(figsize=(9, 6))

plt.plot(tamanios, tiempos, marker="o", label="Tiempo experimental")
plt.plot(tamanios, teorica_ajustada, marker="o",
         label="Ajuste teorico O(n log n)")

plt.xlabel("Cantidad de objetos (n)")
plt.ylabel("Tiempo promedio (segundos)")
plt.title("Greedy: tiempo experimental vs. O(n log n)")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("greedy_tiempos.png", dpi=300)
plt.close()

print("Grafico generado: greedy_tiempos.png")
print("Constante de ajuste c =", c)
