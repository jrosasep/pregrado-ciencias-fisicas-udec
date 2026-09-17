import numpy as np
import matplotlib.pyplot as plt
from EcuacionesDiferencialesOrdinarias import RungeKutta4

# Ecuación diferencial en forma de sistema
def edo_bessel(y, x):
    y1, y2 = y
    dy1dx = y2
    dy2dx = -y2 / x - y1
    return np.array([dy1dx, dy2dx])

# Parámetros
x_min, x_max = 1e-6, 20  # x = epsilon para evitar singularidad
pasos = 1000
x_intervalo = np.linspace(x_min, x_max, pasos)
condiciones_iniciales = np.array([1, 0])  # Condiciones iniciales

# Solución numérica con Runge-Kutta
y_rk4 = RungeKutta4(edo_bessel, r0=condiciones_iniciales, t=x_intervalo)
J0_rk4 = y_rk4[:, 0]

# Gráfica de la solución numérica
plt.figure(figsize=(10, 6))
plt.plot(x_intervalo, J0_rk4, label="Método de Runge-Kutta 4")
plt.xlabel("x")
plt.ylabel("J0(x)")
plt.title("Solución numérica de la ecuación de Bessel")
plt.legend()
plt.grid()
plt.show()

# Solución integral
def J0_integral(x):
    phi = np.linspace(0, np.pi, 1000)  # Discretización de phi
    dphi = phi[1] - phi[0]
    integral = np.trapz(np.cos(x[:, None] * np.sin(phi)), dx=dphi, axis=1)
    return integral / np.pi

# Solución integral
J0_int = J0_integral(x_intervalo)

# Gráfica de la solución integral
plt.figure(figsize=(10, 6))
plt.plot(x_intervalo, J0_int, label="Solución Integral (Regla Trapezoidal)")
plt.xlabel("x")
plt.ylabel("J0(x)")
plt.title("Solución Integral de la Ecuación de Bessel")
plt.legend()
plt.grid()
plt.show()

# Error relativo
error_relativo = np.abs(J0_rk4 - J0_int) / np.abs(J0_int)

# Gráfica del error relativo
plt.figure(figsize=(10, 6))
plt.plot(x_intervalo, error_relativo, label="Error Relativo")
plt.xlabel("x")
plt.ylabel("Error Relativo")
plt.title("Error Relativo entre Métodos Numéricos")
plt.legend()
plt.grid()
plt.show()
