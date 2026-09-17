import numpy as np

# Método de Newton-Raphson iterativo con detalles de la solución
def newton_raphson(f, df, x0, tolerancia=1e-6, iteracion_max=1000):
    x = x0
    iteraciones = 0
    while abs(f(x)) > tolerancia and iteraciones < iteracion_max:
        h = f(x) / df(x)
        x = x - h
        iteraciones += 1
    if abs(f(x)) <= tolerancia:
        print(f"Root: {x}, f(x): {f(x)}, iteraciones: {iteraciones}")
        return x
    else:
        print("No se encontró raíz dentro del límite de iteraciones.")
        return None

# Caso 1: x^3 - 21x^2 + 120x - 100 = 0
def f1(x):
    return x**3 - 21*x**2 + 120*x - 100

def df1(x):
    return 3*x**2 - 42*x + 120

# Caso 2: x = 2^(-x)
def f2(x):
    return x - 2**(-x)

def df2(x):
    return 1 + np.log(2) * 2**(-x)

# Caso 3: tan(x) = 1/x
def f3(x):
    return np.tan(x) - 1/x

def df3(x):
    return 1/np.cos(x)**2 + 1/x**2

# Semillas iniciales
semillas_case1 = [2, 10, 18]  # Aproximaciones iniciales para Caso 1
semilla_case2 = 0.5  # Aproximación inicial para Caso 2
semillas_case3 = [0.5, 2.0]  # Aproximaciones iniciales para Caso 3

# Soluciones con impresión
print("Ecuación 1:")
soluciones_case1 = [newton_raphson(f1, df1, x0) for x0 in semillas_case1]

print("\nEcuación 2:")
solucion_case2 = newton_raphson(f2, df2, semilla_case2)

print("\nEcuación 3:")
soluciones_case3 = [newton_raphson(f3, df3, x0) for x0 in semillas_case3]
