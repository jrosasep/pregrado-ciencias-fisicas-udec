import numpy as np
import matplotlib.pyplot as plt
from EcuacionesDiferencialesOrdinarias import Euler

# Solución analítica
def y_analitica(t):
    return (1 / (2 * np.exp(3))) * np.exp(3 * np.cos(t))

# Derivada de la función (definida para Euler)
def f(y, t):
    return -3 * y * np.sin(t)

# Intervalo y condiciones iniciales
t_min, t_max = 0, 4 * np.pi
y0 = 1 / 2

# Valores de N
N_values = [2**8, 2**9, 2**10, 2**11]
t_analitica = np.linspace(t_min, t_max, 1000)
y_exacta = y_analitica(t_analitica)

# Gráfica
plt.figure(figsize=(12, 7))

# Solución analítica
plt.plot(t_analitica, y_exacta, label="Solución analítica", linewidth=3, linestyle='--', zorder=2)

# Implementación del métodos de Euler
for N in N_values:
    t = np.linspace(t_min, t_max, N + 1)
    y = Euler(f, r0=y0, t=t)
    plt.plot(t, y, label=f"Método de Euler con N={N}", linewidth=3, linestyle='-', markersize=5)

plt.xlabel("Tiempo (t)", fontsize=14, fontweight='bold')
plt.ylabel("y(t)", fontsize=14, fontweight='bold')
plt.title("Comparación de Soluciones: Analítica vs. Euler", fontsize=16, fontweight='bold')
plt.legend(frameon=False, loc='upper right', fontsize=12)
plt.grid(True)

plt.tight_layout()
plt.show()
