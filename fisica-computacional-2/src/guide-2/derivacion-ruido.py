import numpy as np
import matplotlib.pyplot as plt

# Función para calcular la derivada centrada
def derivada_centrada(x, f):
    """
    Calcula la derivada centrada para una serie de datos (xi, fi).

    Parámetros:
    x (array): Valores de x (equispaciados).
    f (array): Valores de la función evaluados en los puntos x.

    Retorna:
    df_dx : array
        Derivada centrada estimada en los puntos interiores de x.
    """
    h = x[1] - x[0]  # Paso entre puntos (asume que x es equiespaciado)
    df_dx = (f[2:] - f[:-2]) / (2 * h)  # Derivada centrada para los puntos interiores

    return df_dx

# Generación de datos con ruido
from numpy import pi, linspace, sin, random

gen = random.default_rng()
x = linspace(0, 2 * pi, 256)
f = sin(x) + gen.uniform(low=-1e-2, high=1e-2, size=x.size)

# Derivada centrada
df_dx = derivada_centrada(x, f)

# Ajustar x para la derivada centrada (pierde los extremos)
x_df = x[1:-1]

# Graficar la función original con ruido
plt.figure(figsize=(10, 6))
plt.plot(x, f, label="f(x) con ruido", color="blue")
plt.title("Función f(x) con ruido")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()

# Graficar la derivada centrada
plt.figure(figsize=(10, 6))
plt.plot(x_df, df_dx, label="Derivada centrada de f(x)", color="red")
plt.title("Derivada centrada de f(x)")
plt.xlabel("x")
plt.ylabel("df/dx")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()