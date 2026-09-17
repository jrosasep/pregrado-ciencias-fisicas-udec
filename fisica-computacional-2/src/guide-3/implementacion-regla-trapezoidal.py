import numpy as np

def regla_trapezoidal(x, y):
    """
    Calcula la integral aproximada usando la regla trapezoidal para datos tabulados.
    
    Parámetros:
        x (array): Valores de las coordenadas x (deben estar ordenados).
        y (array): Valores de las coordenadas y correspondientes a x.

    Retorna:
        float: Valor aproximado de la integral.
    """
    n = len(x)
    if n < 2 or len(y) != n:
        raise ValueError("x e y deben tener el mismo número de puntos y al menos 2 valores.")
    
    integral = 0
    for i in range(1, n):
        h = x[i] - x[i-1]
        integral += (y[i-1] + y[i]) * h / 2
    return integral

# Ejemplo de uso:
# Datos tabulados (x, y)
x = np.array([0, 1, 2, 3])
y = np.array([1, 2, 0, 3])

# Calcular la integral aproximada
resultado = regla_trapezoidal(x, y)
print(f"Resultado de la integral: {resultado}")
