from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt


# ========================
# Funciones generales
# ========================

def ajuste_lineal(x, y):
    """Ajusta y = a x + b y devuelve polinomio, malla, pendiente e intercepto."""
    coefs = np.polyfit(x, y, 1)
    polinomio = np.poly1d(coefs)
    x_list = np.linspace(np.min(x), np.max(x), 1000)
    a, b = coefs
    return polinomio, x_list, a, b


def coeficiente_determinacion(x, y, polinomio):
    """Calcula R^2 para el ajuste lineal."""
    y_fit = polinomio(x)
    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    return 1 - ss_res / ss_tot


def angulo_critico_desde_ajuste(a, b):
    """
    Estima el ángulo crítico imponiendo y = 1 en el ajuste y = a x + b.

    Se despeja x_c = (1 - b)/a y luego theta_c = arcsin(x_c).
    Si x_c queda fuera del intervalo [0, 1], no hay valor real de theta_c.
    """
    x_c = (1 - b) / a
    if 0 <= x_c <= 1:
        return x_c, np.degrees(np.arcsin(x_c))
    return x_c, None


def graficar_experimento(datos, carpeta_salida, mostrar=False):
    """Grafica un experimento, guarda la figura y devuelve los resultados."""
    x = np.array(datos["x"], dtype=float)
    y = np.array(datos["y"], dtype=float)

    polinomio, x_list, a, b = ajuste_lineal(x, y)
    r2 = coeficiente_determinacion(x, y, polinomio)
    x_c, theta_c = angulo_critico_desde_ajuste(a, b)

    plt.style.use("bmh")
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

    ax.scatter(x, y, label="Datos")
    ax.plot(x_list, polinomio(x_list), "r", label=f"Ajuste: y = {a:.3f}x + {b:.3f}")

    ax.set_xlabel("sin(θ₁)")
    ax.set_ylabel("sin(θ₂)")
    ax.set_title(datos["titulo"])
    ax.legend()

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    ruta_figura = carpeta_salida / datos["archivo"]
    fig.savefig(ruta_figura)

    if mostrar:
        plt.show()
    else:
        plt.close(fig)

    return {
        "nombre": datos["nombre"],
        "archivo": str(ruta_figura),
        "pendiente": a,
        "intercepto": b,
        "R2": r2,
        "x_critico": x_c,
        "theta_critico_deg": theta_c,
    }


def imprimir_resultados(resultados):
    """Imprime una tabla breve con los ajustes lineales obtenidos."""
    print("\nResumen de ajustes lineales\n" + "=" * 80)
    for res in resultados:
        print(f"\n[{res['nombre']}]")
        print(f"Figura guardada en  : {res['archivo']}")
        print(f"Pendiente a        : {res['pendiente']:.12f}")
        print(f"Intercepto b       : {res['intercepto']:.12f}")
        print(f"R^2                : {res['R2']:.12f}")
        print(f"x crítico, y=1     : {res['x_critico']:.12f}")
        if res["theta_critico_deg"] is None:
            print("theta crítico      : indefinido, x crítico queda fuera de [0, 1]")
        else:
            print(f"theta crítico      : {res['theta_critico_deg']:.3f}°")


# ========================
# Datos reportados
# ========================

# Los arreglos siguientes usan los valores de sin(theta) redondeados tal como
# aparecen en las tablas del informe. Esto permite reproducir las pendientes
# de los gráficos originales.

experimentos = [
    {
        "nombre": "Agua con café, figura 1",
        "titulo": "sin(θ₁) vs sin(θ₂) agua con café",
        "archivo": "1.png",
        # Tabla: agua con café, incidencia por cara plana.
        # Para reproducir el ajuste y = 1.324x + 0.037 se invierten las columnas:
        # x = sin(theta_2), y = sin(theta_1).
        "theta1_deg": [10, 20, 30, 40, 50, 60, 70],
        "sin_theta1": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
        "theta2_deg": [6, 13, 21, 28, 33, 39, 43],
        "sin_theta2": [0.10, 0.22, 0.36, 0.47, 0.54, 0.63, 0.68],
        "x": [0.10, 0.22, 0.36, 0.47, 0.54, 0.63, 0.68],
        "y": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
    },
    {
        "nombre": "Agua desde cara curva",
        "titulo": "sin(θ₁) vs sin(θ₂) agua desde cara curva",
        "archivo": "2.png",
        # Tabla: agua, incidencia por cara curva.
        # Para reproducir y = 0.888x - 0.056 se usan x = sin(theta_2), y = sin(theta_1).
        "theta1_deg": [10, 20, 30, 40, 66],
        "sin_theta1": [0.17, 0.34, 0.50, 0.64, 0.91],
        "theta2_deg": [15, 39, 44, 64, 46],
        "sin_theta2": [0.26, 0.63, 0.69, 0.90, 0.72],
        "x": [0.26, 0.63, 0.69, 0.90, 0.72],
        "y": [0.17, 0.34, 0.50, 0.64, 0.91],
    },
    {
        "nombre": "Agua desde cara plana",
        "titulo": "sin(θ₁) vs sin(θ₂) agua desde cara plana",
        "archivo": "3.png",
        # Tabla: agua, incidencia por cara plana.
        # El punto (0,0) se omite para reproducir y = 1.597x - 0.285.
        # Además, se usan x = sin(theta_2), y = sin(theta_1).
        "theta1_deg": [10, 20, 30, 40, 50, 60, 70],
        "sin_theta1": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
        "theta2_deg": [16, 23, 30, 36, 41, 45, 50],
        "sin_theta2": [0.28, 0.39, 0.50, 0.59, 0.66, 0.71, 0.77],
        "x": [0.28, 0.39, 0.50, 0.59, 0.66, 0.71, 0.77],
        "y": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
    },
    {
        "nombre": "Agua con café por cara curva",
        "titulo": "sin(θ₁) vs sin(θ₂) agua con café por cara curva",
        "archivo": "4.png",
        # Tabla: agua con café, incidencia por cara curva.
        # Aquí se usan directamente x = sin(theta_1), y = sin(theta_2).
        "theta1_deg": [7, 10, 20, 30, 40],
        "sin_theta1": [0.12, 0.17, 0.34, 0.50, 0.64],
        "theta2_deg": [10, 15, 30, 45, 62],
        "sin_theta2": [0.17, 0.26, 0.50, 0.71, 0.88],
        "x": [0.12, 0.17, 0.34, 0.50, 0.64],
        "y": [0.17, 0.26, 0.50, 0.71, 0.88],
    },
    {
        "nombre": "Agua con café por cara plana, figura 5",
        "titulo": "sin(θ₁) vs sin(θ₂) agua con café por cara plana",
        "archivo": "5.png",
        # Esta figura del informe repite los mismos datos y el mismo ajuste de la figura 1.
        "theta1_deg": [10, 20, 30, 40, 50, 60, 70],
        "sin_theta1": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
        "theta2_deg": [6, 13, 21, 28, 33, 39, 43],
        "sin_theta2": [0.10, 0.22, 0.36, 0.47, 0.54, 0.63, 0.68],
        "x": [0.10, 0.22, 0.36, 0.47, 0.54, 0.63, 0.68],
        "y": [0.17, 0.34, 0.50, 0.64, 0.77, 0.87, 0.94],
    },
    {
        "nombre": "Acrílico, reflexión total interna",
        "titulo": "srefracción y reflexión total interna en una lente semicircular de acrílico.",
        "archivo": "6.png",
        # Tabla: acrílico.
        # El punto (0,0) se omite para reproducir y = 1.464x - 0.004.
        "theta1_deg": [5, 10, 15, 20, 25, 30, 35, 40],
        "sin_theta1": [0.09, 0.17, 0.26, 0.34, 0.43, 0.50, 0.57, 0.64],
        "theta2_deg": [7, 16, 22, 30, 38, 46, 56, 70],
        "sin_theta2": [0.12, 0.26, 0.37, 0.50, 0.62, 0.72, 0.83, 0.94],
        "x": [0.09, 0.17, 0.26, 0.34, 0.43, 0.50, 0.57, 0.64],
        "y": [0.12, 0.26, 0.37, 0.50, 0.62, 0.72, 0.83, 0.94],
    },
]


# ========================
# Ejecución
# ========================

if __name__ == "__main__":
    carpeta_salida = Path("figuras_snell")

    resultados = []
    for experimento in experimentos:
        resultados.append(graficar_experimento(experimento, carpeta_salida, mostrar=False))

    imprimir_resultados(resultados)

    print("\nListo. Las figuras quedaron guardadas en la carpeta:")
    print(carpeta_salida.resolve())
