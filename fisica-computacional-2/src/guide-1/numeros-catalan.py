import numpy as np
import matplotlib.pyplot as plt

# Definimos una función para calcular el factorial de un número
def fact(n):
    """Cálculo del factorial de un número entero n."""
    fact = 1
    for n in list(range(0, int(n + 1), 1)):  # Iteramos desde 0 hasta n
        if n == 0 or n == 1:
            fact *= 1  # Factorial de 0 y 1 es 1
        elif n > 1:
            fact *= n  # Multiplicamos sucesivamente
    return fact

# Función para calcular el n-ésimo número de Catalán usando precisión simple (32 bits)

# Cálculo del n-ésimo número de Catalán mediante la definición
def catalan_def(n):
    """Calcula el n-ésimo número de Catalán usando la definición."""
    catalan_n = np.float32(fact(2 * n) / (fact(n + 1) * fact(n)))  # Fórmula cerrada
    return catalan_n

# Cálculo del n-ésimo número de Catalán mediante la forma recursiva
def catalan_rec(n):
    """Calcula el n-ésimo número de Catalán usando la forma recursiva."""
    catalan_0 = 1  # Caso base C_0 = 1
    for n in list(range(0, n, 1)):  # Iteramos desde 0 hasta n-1
        catalan_rec = np.float32(catalan_0 * (4 * n + 2) / (n + 2))  # Fórmula recursiva
        catalan_0 = catalan_rec  # Actualizamos el valor base
    return catalan_0

# Parámetro definido por el usuario
M = float(input("Ingrese el valor de M: "))  # Cota superior para los números de Catalán

# Inicialización de listas para almacenar los valores
n_values = []           # Lista de índices n
list_catalan_def = []   # Lista de números de Catalán por definición
list_catalan_rec = []   # Lista de números de Catalán por recurrencia

# Cálculo iterativo de los números de Catalán
n = 0
while True:
    C_def = catalan_def(n)  # Número de Catalán por definición
    C_rec = catalan_rec(n)  # Número de Catalán por recurrencia

    # Condición para detener el ciclo si se supera la cota M
    if C_def >= M or C_rec >= M:
        break

    # Almacenamos los valores calculados y el índice actual
    list_catalan_def.append(C_def)
    list_catalan_rec.append(C_rec)
    n_values.append(n)
    
    # Incrementamos el índice
    n += 1

# Configuración y generación del gráfico
plt.figure(figsize=(10, 6))

# Gráfico de los números de Catalán calculados por ambos métodos
plt.plot(n_values, list_catalan_def, 'x', label='Por definición (1)', color='blue')
plt.plot(n_values, list_catalan_rec, '.', label='Por recurrencia (2)', color='orange')

# Línea horizontal que representa la cota M
plt.axhline(y=M, color='red', linestyle='--', label=f'Cota M = {M}')

# Configuración de ejes y escalas
plt.yscale('log')  # Escala logarítmica en el eje y
plt.xlim((0, len(n_values)))  # Límite en el eje x

# Etiquetas y título del gráfico
plt.xlabel('n')
plt.ylabel('$C_n$ (log scale)')
plt.title('Números de Catalán bajo la cota $M$')

# Leyenda y cuadrícula
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Mostrar el gráfico
plt.show()

#######################################################################################################
### Comportamiento asintotico

# Aproximación asintótica
def catalan_aprox(n):
    return np.float32 ( (4**n) / ( n**(3/2) * np.sqrt(np.pi) ) )

# Rango de valores de n
n_values = np.arange(1, 100, dtype=np.float32)

# Cálculo de los números de Catalán
Cn = np.array([catalan_def(i) for i in n_values])
Cn_aprox = np.array([catalan_aprox(i) for i in n_values])
    
# Graficar los números de Catalán y su aproximación asintótica
plt.figure(figsize=(12, 6))
plt.plot(n_values, Cn, label=r"$C_n$ (Números de Catalán)", color="blue")
plt.plot(n_values, Cn_aprox, label=r"Asintótico $\frac{4^n}{n^{3/2} \sqrt{\pi}}$", color="orange", linestyle="dashed")

# Configuración del gráfico
plt.title("Comportamiento asintótico de los números de Catalán", fontsize=14)
plt.xlabel("$n$", fontsize=12)
plt.ylabel("$C_n$ (log scale)", fontsize=12)

plt.yscale("log")  # Escala logarítmica para mejor comparación
plt.grid(alpha=0.5)
plt.legend(fontsize=12)

# Mostrar el gráfico
plt.show()