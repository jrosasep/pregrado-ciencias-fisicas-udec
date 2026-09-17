import numpy as np

# CONSTANTES EXPERIMENTALES

m = 1  # Orden de difracción utilizado en el análisis (m = 1 para el primer máximo)
L = 0.205  # [m] distancia entre la red de difracción y la regla/pantalla
dL = 0.002  # [m] incertidumbre en L
a = np.round(1/600000, 6+3)  # [m] paso (espaciamiento) de la red: 600 líneas/mm

# DATOS DEL PRIMER MONTAJE

dX = 0.004  # [m] incertidumbre estimada en la medición de X
X_rojo = 0.085   # [m]
X_verde = 0.069  # [m]
X_azul = 0.061   # [m]
X_morado = 0.053 # [m]
X_celeste = 0.063 # [m]

X_colors_values_primer_montaje = {
    "luz roja": X_rojo,
    "luz verde": X_verde,
    "luz azul": X_azul,
    "luz morada": X_morado,
    "luz celeste": X_celeste
}

# DATOS DEL SEGUNDO MONTAJE

X_rojo_2 = 0.082     # [m]
X_verde_2 = 0.069    # [m]
X_azul_2 = 0.060     # [m]
X_morado_2 = 0.055   # [m]
X_celeste_2 = 0.0625 # [m]
X_amarillo_2 = 0.077 # [m]
X_naranjo_2 = 0.079  # [m]

X_colors_values_segundo_montaje = {
    "luz roja": X_rojo_2,
    "luz verde": X_verde_2,
    "luz azul": X_azul_2,
    "luz morada": X_morado_2,
    "luz celeste": X_celeste_2,
    "luz amarilla": X_amarillo_2,
    "luz naranja": X_naranjo_2
}

# FUNCIONES DE ANÁLISIS

def error(X, dX=0.004, L=0.205, dL=0.002, a=np.round(1/600000, 6+3)):
    """
    Calcula la contribución estimada a la incertidumbre de la longitud de onda (dLambda_i)
    para cada color, en base a la propagación de errores en x y L.
    """
    for color, X_i in X.items():
        dLambda_i = (np.abs((a * L**2) / ((X_i**2 + L**2)**(3/2))) * dX) + \
                    (np.abs((a * L * X_i) / ((X_i**2 + L**2)**(3/2))) * dL)
        print(f"Para {color}:")
        print(f"  X = {X_i} [m]")
        print(f"  Error estimado en λ = {dLambda_i} [m]")


def analisis(X, dX=0.004, dL=0.002, L=0.205, m=1, a=np.round(1/600000, 6+3)):
    """
    Para cada color:
    - Calcula el ángulo theta = arctan(X/L)
    - Calcula la longitud de onda lambda = a * sin(theta)
    - Propaga errores para estimar la incertidumbre en theta y en lambda
    - Imprime todos los valores relevantes
    """
    print(f"Espaciamiento de la red a = {a} [m].")
    print(f"Orden de difracción considerado m = {m}.")
    print(f"Distancia L = {L} [m].")

    for color, X_i in X.items():
        theta_i = np.round(np.arctan(X_i / L), 3)
        lambda_i = np.round(a * np.sin(theta_i), 7+3)

        dtheta_i = (np.abs(L / (X_i**2 + L**2)) * dX) + \
                   (np.abs(X_i / (X_i**2 + L**2)) * dL)

        dLambda_i = (np.abs((a * L**2) / ((X_i**2 + L**2)**(3/2))) * dX) + \
                    (np.abs((a * L * X_i) / ((X_i**2 + L**2)**(3/2))) * dL)

        print("=====================================================")
        print(f"Para {color}:")
        print(f"  X = {X_i} [m]")
        print(f"  Error estimado en X = {dX} [m]")
        print(f"  theta = {theta_i} rad")
        print(f"  Error estimado en theta = {dtheta_i} rad")
        print(f"  lambda = {lambda_i} [m]")
        print(f"  Error estimado en lambda = {dLambda_i} [m]")


# EJECUCIÓN DEL ANÁLISIS COMPARATIVO ENTRE MONTAJES

print("=====================================================")
print("Primer montaje")
print("=====================================================")
analisis(X=X_colors_values_primer_montaje)
# error(X=X_colors_values_primer_montaje)

print("=====================================================")
print("Segundo montaje")
print("=====================================================")
analisis(X=X_colors_values_segundo_montaje)
# error(X=X_colors_values_segundo_montaje)
