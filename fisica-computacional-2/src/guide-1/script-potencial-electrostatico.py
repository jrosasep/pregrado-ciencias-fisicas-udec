import numpy as np
import matplotlib.pyplot as plt

a = 2    # Separación entre las cargas en metros
q1 = 1e-9   # Carga 1 en Coulombs
q2 = 1e-9   # Carga 2 en Coulombs
k = 8.99e9  # N·m²/C²   # Constante de Coulomb

pos_q1 = (-a/2, 0)  # Posicion de la carga q1 en el plano (x,y)
pos_q2 = (a/2, 0)   # Posicion de la carga q2 en el plano (x,y)

# Función para calcular el potencial electrostático en un punto (x, y)
def potencial(x, y, q, pos):
    """
    Calcula el potencial electrostático debido a una carga puntual en una posición dada.

    Esta función utiliza la ley de Coulomb para determinar el potencial en un punto del plano 
    (x, y) generado por una carga q situada en la posición "pos = (x_0, y_0)". El 
    potencial electrostático se define como:

        V(x, y) = k * q / r

    donde:
        - k = 8.99e9 N·m^2/C^2 , es la constante de Coulomb,
        - q es la magnitud de la carga,
        - r es la distancia entre el punto (x, y) y la posición de la carga (x_q, y_q).

    Argumentos
    ----------
    x : (float o array) Coordenada x del punto donde se evalúa el potencial.
    y : (float o array) Coordenada y del punto donde se evalúa el potencial.
    q : (float) Magnitud de la carga puntual.
    pos : (tupla) Posición de la carga puntual, dada como "(x_0, y_0)".

    Retorna
    -------
    V : (float o array) Potencial electrostático en el punto o puntos especificados por (x, y).
          Si "x" y "y" son arrays, retorna un array con los valores del potencial para cada punto.
    """
    rx, ry = x - pos[0], y - pos[1]
    r = np.sqrt(rx**2 + ry**2)
    return k * q / r

# Generamos el subconjunto del plano (x,y)
x = np.linspace(-5, 5, 400)     # [x_i, x_f]
y = np.linspace(-5, 5, 400)     # [y_i, y_f]

X, Y = np.meshgrid(x, y)    # I = [x_i, x_f] X [y_i, y_f]

# Calculamos el potencial total para los tres casos:
def calcular_potencial_total(q1, q2):
    """
    Calcula el potencial electrostático total generado por dos cargas puntuales en un plano.

    Esta función evalúa el potencial electrostático en una región del plano (x, y) debido a dos 
    cargas puntuales q_1 y q_2 ubicadas en posiciones específicas. Se utiliza la superposición 
    de potenciales, es decir:

        V_{total}(x, y) = V_1(x, y) + V_2(x, y)

    donde:
        - V_1 es el potencial generado por la carga q_1,
        - V_2 es el potencial generado por la carga q_2.

    Esta función llama internamente a la función "potencial" para calcular los potenciales 
    individuales.

    Argumentos
    ----------
    q1 : (float) Magnitud de la primera carga puntual q_1.
    q2 : (float) Magnitud de la segunda carga puntual q_2.

    Retorna
    -------
    V_total : (array) Matriz con los valores del potencial total en cada punto del plano.

    Notas
    -----
    - Las variables "X" y "Y" deben definirse antes de llamar a esta función mediante "np.meshgrid".
    - Las posiciones de las cargas "pos_q1" y "pos_q2" deben asignarse correctamente antes de la llamada.
    - Esta implementación asume que las cargas están en el plano (x, y), sin considerar efectos tridimensionales.

    """
    V1 = potencial(X, Y, q1, pos_q1)    # Potencial debido a la primera carga
    V2 = potencial(X, Y, q2, pos_q2)    # Potencial debido a la segunda carga
    return V1 + V2  # Superposición de potenciales

# Creamos una figura con subplots para los tres casos
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Caso 1: Ambas cargas positivas
V = calcular_potencial_total(q1, q2)
axes[0].contourf(X, Y, V, levels=50, cmap="coolwarm")
axes[0].set_title("Ambas cargas positivas")
axes[0].set_xlabel("x (m)")
axes[0].set_ylabel("y (m)")

# Caso 2: Ambas cargas negativas
V = calcular_potencial_total(-q1, -q2)
axes[1].contourf(X, Y, V, levels=50, cmap="coolwarm")
axes[1].set_title("Ambas cargas negativas")
axes[1].set_xlabel("x (m)")

# Caso 3: Cargas opuestas
V = calcular_potencial_total(q1, -q2)
axes[2].contourf(X, Y, V, levels=50, cmap="coolwarm")
axes[2].set_title("Cargas opuestas")
axes[2].set_xlabel("x (m)")

# Ajuste de la visualización
for ax in axes:
    ax.set_aspect("equal")

plt.tight_layout()
plt.show()
