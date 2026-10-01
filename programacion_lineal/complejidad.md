# Análisis de Complejidad Temporal - Programación Lineal

`mochila_lineal` hace dos trabajos distintos y cada uno tarda un tiempo distinto

1° etapa. Recorre los objetos una cantidad fija de veces: \(O(n)\).
2° etapa. Le pide a CBC que busque la mejor combinación. En el peor caso crece como \(2^n\).

## 1° etapa: escribir el problema y leer la respuesta

| Qué hace el código                                         | Por qué es \(O(n)\)                                 |
| ---------------------------------------------------------- | --------------------------------------------------- |
| Crea una variable \(x_i\) por objeto                       | Crea una variable por cada uno de los \(n\) objetos |
| Escribe la suma de beneficios                              | Suma \(n\) términos, uno por objeto                 |
| Escribe la suma de pesos y pide que no supere la capacidad | Suma \(n\) términos                                 |
| Mira qué variables quedaron en 1 y suma su beneficio       | Recorre las \(n\) variables una vez                 |

Si hay el doble de objetos, este trabajo crece más o menos el doble. La capacidad de la mochila no entra en la cuenta: el problema siempre tiene \(n\) variables y una sola restricción, sea la capacidad chica o enorme.

La memoria también es \(O(n)\), porque se guarda una variable por objeto.

Este tramo deja el problema escrito en el formato que PuLP entiende.

## 2° etapa: Buscar la solución

`problema.solve(...)` le pasa ese problema a CBC (PuLP), que decide qué objetos entran.

Hay \(2^n\) combinaciones posibles. CBC descarta grupos enteros de combinaciones cuando ya sabe que no pueden mejorar el mejor beneficio encontrado. En el peor caso, la cantidad de grupos que llega a mirar igual crece como \(2^n\). Agregar un objeto puede duplicar ese tiempo. Con el doble de objetos, el peor caso pasa de \(2^n\) a \(2^{2n}\).

## Archivos de crear_mochila.py

Respecto a los archivos de `crear_mochila.py` esa búsqueda larga casi no ocurre. CBC primero afloja la regla de entrar o no entrar, y permite tomar una fracción de un objeto. Ese problema más fácil se resuelve ordenando los objetos por beneficio/peso, en \(O(n \log n)\). Como mucho un objeto queda partido. CBC decide si ese objeto entra entero o queda afuera, y con eso cierra la búsqueda. En estos datos los pesos van de 1 a 200 y la capacidad es \(n \cdot 50\), así que ese corte alcanza en pocos pasos.

Al medir estos sets, el tiempo suele crecer parecido a \(a \cdot n\) o a \(a \cdot n \log n\): lo que tarda Python en armar el problema, más el ordenamiento de CBC. Esa curva describe estos archivos. En otro set, la búsqueda de CBC puede crecer como \(2^n\).
