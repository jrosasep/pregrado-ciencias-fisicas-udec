import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ========================
# Configuración general
# ========================

CARPETA_FIGURAS = Path("figuras_ondas_estacionarias")
GUARDAR_GRAFICOS = True
MOSTRAR_GRAFICOS = False

np.set_printoptions(precision=4, suppress=False)


# ========================
# Funciones generales
# ========================

def ajuste_lineal(x, y):
    """Ajusta y = a x + b y devuelve polinomio, malla, pendiente e intercepto."""
    coefs = np.polyfit(x, y, 1)
    p = np.poly1d(coefs)
    x_list = np.linspace(np.min(x), np.max(x), 1000)
    a, b = coefs
    return p, x_list, a, b


def error_porcentual(valor_obs, valor_ref):
    """Calcula error porcentual absoluto respecto a un valor de referencia."""
    return np.abs((valor_obs - valor_ref) / valor_ref) * 100


def guardar_o_mostrar(fig, archivo):
    """Guarda y/o muestra la figura según la configuración global."""
    if GUARDAR_GRAFICOS:
        CARPETA_FIGURAS.mkdir(exist_ok=True)
        fig.savefig(CARPETA_FIGURAS / archivo, dpi=100)
    if MOSTRAR_GRAFICOS:
        plt.show()
    plt.close(fig)


# ========================
# Escenarios físicos
# ========================

def escenario_tension_variable(datos):
    """
    Escenario: frecuencia fija, tensión observada.

    De la relación de ondas estacionarias
        f_n = n/(2L) sqrt(T/mu),
    si f se mantiene fija, entonces
        T = 4 L^2 f^2 mu (1/n^2).

    Por eso se grafica T versus 1/n^2.
    """
    n = datos["modos"].astype(float)
    T_obs = datos["medida_obs"].astype(float)
    L, f, mu_ref = datos.get("L"), datos.get("fijo"), datos.get("mu")

    # Eje linealizado
    x = 1 / n**2
    y = T_obs

    # Ajuste lineal
    p, x_list, a, b = ajuste_lineal(x, y)
    y_fit = p(x)

    # Densidad lineal por pendiente, si están dadas las constantes
    mu_est = None
    err_mu_pct = None
    T_esperada = None
    err_T_teorica_pct = None

    if L is not None and f is not None:
        mu_est = a / (4 * L**2 * f**2)
        if mu_ref is not None:
            err_mu_pct = error_porcentual(mu_est, mu_ref)
            T_esperada = 4 * L**2 * f**2 * mu_ref / n**2
            err_T_teorica_pct = error_porcentual(T_obs, T_esperada)

    err_ajuste_pct = error_porcentual(y, y_fit)

    # Resultados en consola
    print(f"\n[{datos['nombre']}]")
    print("Pendiente a =", a)
    print("Intercepto b =", b)
    if mu_est is not None:
        print("mu (ajuste) =", mu_est)
    if mu_ref is not None:
        print("mu (ref)    =", mu_ref)
    if err_mu_pct is not None:
        print("Error % mu =", err_mu_pct)
    print("Errores % respecto al ajuste lineal en T:", err_ajuste_pct)
    if err_T_teorica_pct is not None:
        print("Errores % respecto a T esperada:", err_T_teorica_pct)

    # Gráfico
    fig = plt.figure(figsize=(6.4, 4.8), dpi=100)
    plt.scatter(x, y, label="Datos observados (T)")
    plt.plot(x_list, p(x_list), "r", label="Ajuste lineal")
    plt.xlabel("1 / n^2")
    plt.ylabel("Tensión (N)")
    plt.title(datos["nombre"])
    plt.legend()
    guardar_o_mostrar(fig, datos["archivo"])

    return {
        "nombre": datos["nombre"],
        "pendiente": a,
        "intercepto": b,
        "mu_ajuste": mu_est,
        "mu_ref": mu_ref,
        "error_mu_pct": err_mu_pct,
        "error_ajuste_pct": err_ajuste_pct,
    }


def escenario_frecuencia_variable(datos):
    """
    Escenario: tensión fija, frecuencia observada.

    De la relación de ondas estacionarias
        f_n = n/(2L) sqrt(T/mu),
    si T se mantiene fija, entonces f_n es proporcional a n.

    Por eso se grafica f versus n.
    """
    n = datos["modos"].astype(float)
    f_obs = datos["medida_obs"].astype(float)
    L, T, mu_ref = datos.get("L"), datos.get("fijo"), datos.get("mu")

    # Eje linealizado
    x = n
    y = f_obs

    # Ajuste lineal
    p, x_list, s, b = ajuste_lineal(x, y)
    y_fit = p(x)

    # Densidad lineal por pendiente, si están dadas las constantes
    mu_est = None
    err_mu_pct = None
    f_esperada = None
    err_f_teorica_pct = None

    if L is not None and T is not None:
        mu_est = T / (4 * L**2 * s**2)
        if mu_ref is not None:
            err_mu_pct = error_porcentual(mu_est, mu_ref)
            f_esperada = np.sqrt(T / mu_ref) * n / (2 * L)
            err_f_teorica_pct = error_porcentual(f_obs, f_esperada)

    err_ajuste_pct = error_porcentual(y, y_fit)

    # Resultados en consola
    print(f"\n[{datos['nombre']}]")
    print("Pendiente s =", s)
    print("Intercepto b =", b)
    if mu_est is not None:
        print("mu (ajuste) =", mu_est)
    if mu_ref is not None:
        print("mu (ref)    =", mu_ref)
    if err_mu_pct is not None:
        print("Error % mu =", err_mu_pct)
    print("Errores % respecto al ajuste lineal en f:", err_ajuste_pct)
    if err_f_teorica_pct is not None:
        print("Errores % respecto a f esperada:", err_f_teorica_pct)

    # Gráfico
    fig = plt.figure(figsize=(6.4, 4.8), dpi=100)
    plt.scatter(x, y, label="Datos observados (f)")
    plt.plot(x_list, p(x_list), "r", label="Ajuste lineal")
    plt.xlabel("n (modo)")
    plt.ylabel("Frecuencia (Hz)")
    plt.title(datos["nombre"])
    plt.legend()
    guardar_o_mostrar(fig, datos["archivo"])

    return {
        "nombre": datos["nombre"],
        "pendiente": s,
        "intercepto": b,
        "mu_ajuste": mu_est,
        "mu_ref": mu_ref,
        "error_mu_pct": err_mu_pct,
        "error_ajuste_pct": err_ajuste_pct,
    }


# ========================
# Datos experimentales
# ========================

# Protocolo 1: tensión variable, frecuencia fija.
# Estos datos corresponden a los gráficos tension_variable_1, 2 y 3.
datos_tension_variable = [
    {
        "nombre": "Cuerda 1, Tensión Variable",
        "modos": np.array([1, 2, 3, 4, 5]),
        "medida_obs": np.array([2.55, 0.68, 0.29, 0.19, 0.09]),  # Tensión en N
        "L": 0.9,          # Longitud en m
        "fijo": 62,        # Frecuencia fija en Hz
        "mu": 1 / 10 * 0.44 / 145,  # Densidad lineal de referencia en kg/m
        "archivo": "tension_variable_1.png",
    },
    {
        "nombre": "Cuerda 2, Tensión Variable",
        "modos": np.array([2, 3, 4, 5, 6, 7, 8]),
        "medida_obs": np.array([5.19, 2.45, 1.37, 0.78, 0.49, 0.39, 0.29]),  # Tensión en N
        "L": 1.0,          # Longitud en m
        "fijo": 41,        # Frecuencia fija en Hz
        "mu": 1 / 10 * 6.39 / 123,  # Densidad lineal de referencia en kg/m
        "archivo": "tension_variable_2.png",
    },
    {
        "nombre": "Cuerda 3, Tensión Variable",
        "modos": np.array([5, 6, 7, 8]),
        "medida_obs": np.array([2.452, 1.962, 1.471, 0.981]),  # Tensión en N
        "L": 1.0,          # Longitud en m
        "fijo": 44,        # Frecuencia fija en Hz
        "mu": 1 / 10 * 14.7 / 119,  # Densidad lineal de referencia en kg/m
        "archivo": "tension_variable_3.png",
    },
]

# Protocolo 2: frecuencia variable, tensión fija.
# Estos datos corresponden a los gráficos frecuencia_variable_1, 2 y 3.
# Si se desea estimar mu en estos casos, completar L, fijo=T y mu con las
# constantes experimentales reportadas para cada cuerda.
datos_frecuencia_variable = [
    {
        "nombre": "Cuerda 1, variable frecuencia",
        "modos": np.array([1, 2, 3, 4, 5, 6]),
        "medida_obs": np.array([21, 38, 54, 72, 91, 106]),  # Frecuencia en Hz
        "L": None,
        "fijo": None,  # Tensión fija en N
        "mu": None,
        "archivo": "frecuencia_variable_1.png",
    },
    {
        "nombre": "Cuerda 2, variable frecuencia",
        "modos": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        "medida_obs": np.array([16, 28, 39, 48, 62, 71, 81, 93, 103, 112]),  # Frecuencia en Hz
        "L": None,
        "fijo": None,  # Tensión fija en N
        "mu": None,
        "archivo": "frecuencia_variable_2.png",
    },
    {
        "nombre": "Cuerda 3, variable frecuencia",
        "modos": np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        "medida_obs": np.array([10, 22, 31, 41, 49, 58, 69, 80, 99, 109]),  # Frecuencia en Hz
        "L": None,
        "fijo": None,  # Tensión fija en N
        "mu": None,
        "archivo": "frecuencia_variable_3.png",
    },
]


# ========================
# Ejecución del análisis
# ========================

def main():
    resultados = []

    print("\n============================")
    print("Frecuencia variable, tensión fija")
    print("============================")
    for datos in datos_frecuencia_variable:
        resultados.append(escenario_frecuencia_variable(datos))

    print("\n============================")
    print("Tensión variable, frecuencia fija")
    print("============================")
    for datos in datos_tension_variable:
        resultados.append(escenario_tension_variable(datos))

    if GUARDAR_GRAFICOS:
        print(f"\nGráficos guardados en: {CARPETA_FIGURAS.resolve()}")

    return resultados


if __name__ == "__main__":
    main()
