import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import csv

# ===========================================================
# ANÁLISIS — TORQUE Y MOMENTO DE INERCIA
# Informe 6: Torque y momento de inercia
# ===========================================================
# Este script replica los gráficos usados en el informe:
#   imagenes/figure_1.png  -> radio r1 = 0.027 m
#   imagenes/figure_2.png  -> radio r2 = 0.022 m
#   imagenes/figure_3.png  -> radio r3 = 0.018 m
#
# Nota importante:
# Para reproducir exactamente los gráficos del informe, el ajuste lineal
# se realiza sobre los valores procesados que aparecen en el Cuadro 1:
#       alpha = aceleración angular reportada
#       tau   = torque reportado
# Si se recalcula tau desde m, r y a_t con más cifras significativas,
# las pendientes cambian levemente y ya no coinciden con las figuras.
# ===========================================================

# -----------------------------------------------------------
# 1) CONFIGURACIÓN GENERAL
# -----------------------------------------------------------

OUTPUT_DIR = Path(__file__).resolve().parent / "imagenes"
OUTPUT_DIR.mkdir(exist_ok=True)

plt.style.use("bmh")

# -----------------------------------------------------------
# 2) DATOS PROCESADOS REPORTADOS EN EL INFORME
# -----------------------------------------------------------
# m, r y a_t se conservan para trazabilidad.
# alpha y tau son los valores usados efectivamente para replicar los gráficos.

experimentos = [
    {
        "nombre": "r1",
        "radio_label": "r₁",
        "r": 0.027,
        "m": np.array([0.01025, 0.05000, 0.06000, 0.10000, 0.11000]),
        "a_t": np.array([0.031, 0.194, 0.235, 0.396, 0.434]),
        "alpha": np.array([1.15, 7.17, 8.72, 14.65, 16.09]),
        "tau": np.array([0.003, 0.013, 0.015, 0.025, 0.027]),
        "color": "blue",
        "archivo": "figure_1.png",
    },
    {
        "nombre": "r2",
        "radio_label": "r₂",
        "r": 0.022,
        "m": np.array([0.12000, 0.13000, 0.14000, 0.15000, 0.16000]),
        "a_t": np.array([0.403, 0.439, 0.476, 0.494, 0.535]),
        "alpha": np.array([18.30, 19.94, 21.62, 22.45, 24.32]),
        "tau": np.array([0.025, 0.027, 0.029, 0.030, 0.032]),
        "color": "red",
        "archivo": "figure_2.png",
    },
    {
        "nombre": "r3",
        "radio_label": "r₃",
        "r": 0.018,
        "m": np.array([0.12000, 0.13000, 0.14000, 0.15000, 0.16000]),
        "a_t": np.array([0.303, 0.331, 0.354, 0.377, 0.413]),
        "alpha": np.array([16.81, 18.39, 19.67, 20.98, 22.96]),
        "tau": np.array([0.021, 0.022, 0.024, 0.025, 0.027]),
        "color": "green",
        "archivo": "figure_3.png",
    },
]

# -----------------------------------------------------------
# 3) FUNCIONES DE CÁLCULO
# -----------------------------------------------------------

def ajuste_lineal(x, y):
    """Ajusta y = a*x + b y calcula R^2."""
    coefs = np.polyfit(x, y, 1)
    a, b = coefs
    y_fit = np.polyval(coefs, x)

    ss_res = np.sum((y - y_fit) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot

    return a, b, r2


def graficar_tau_vs_alpha(exp, mostrar=True):
    """Genera el gráfico tau vs alpha con la estética del informe."""
    alpha = exp["alpha"]
    tau = exp["tau"]
    a, b, r2 = ajuste_lineal(alpha, tau)

    x_fit = np.linspace(np.min(alpha), np.max(alpha), 1000)
    y_fit = a * x_fit + b

    fig, ax = plt.subplots(figsize=(10, 6), dpi=100)

    ax.scatter(
        alpha,
        tau,
        s=100,
        color=exp["color"],
        edgecolor="black",
        alpha=0.75,
        label="Datos experimentales",
    )

    ax.plot(
        x_fit,
        y_fit,
        "--",
        color=exp["color"],
        linewidth=2,
        label=f"Regresión lineal: τ = {a:.6f}α + {b:.6f}\nR² = {r2:.6f}",
    )

    ax.set_title(f"τ vs α para radio {exp['radio_label']} = {exp['r']:.3f} m", fontsize=16)
    ax.set_xlabel("Aceleración angular α (rad/s²)", fontsize=12)
    ax.set_ylabel("Torque τ (N·m)", fontsize=12)
    ax.legend(loc="upper left")

    plt.tight_layout()

    salida = OUTPUT_DIR / exp["archivo"]
    fig.savefig(salida, dpi=100)

    if mostrar:
        plt.show()

    plt.close(fig)

    return {
        "radio": exp["nombre"],
        "r_m": exp["r"],
        "alpha": alpha,
        "tau": tau,
        "pendiente_I": a,
        "intercepto_b": b,
        "r2": r2,
        "archivo": salida,
    }


def guardar_tabla_procesada(resultados):
    """Guarda los datos procesados usados en el ajuste."""
    salida = Path(__file__).resolve().parent / "datos-procesados-torque.csv"

    with salida.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["radio", "m_kg", "r_m", "a_t_m_s2", "alpha_rad_s2", "tau_N_m"])

        for exp, res in zip(experimentos, resultados):
            for m, a_t, alpha, tau in zip(exp["m"], exp["a_t"], res["alpha"], res["tau"]):
                writer.writerow([
                    exp["nombre"],
                    f"{m:.5f}",
                    f"{exp['r']:.3f}",
                    f"{a_t:.3f}",
                    f"{alpha:.2f}",
                    f"{tau:.3f}",
                ])

    return salida

# -----------------------------------------------------------
# 4) EJECUCIÓN
# -----------------------------------------------------------

def main(mostrar_graficos=True):
    resultados = []

    for exp in experimentos:
        res = graficar_tau_vs_alpha(exp, mostrar=mostrar_graficos)
        resultados.append(res)

        print(f"[{res['radio']}]")
        print(f"  I = pendiente = {res['pendiente_I']:.6f} kg·m²")
        print(f"  b = {res['intercepto_b']:.6f} N·m")
        print(f"  R² = {res['r2']:.6f}")
        print(f"  figura guardada en: {res['archivo']}")
        print()

    I_prom = np.mean([res["pendiente_I"] for res in resultados])
    print(f"Momento de inercia promedio: I_prom = {I_prom:.6e} kg·m²")

    tabla = guardar_tabla_procesada(resultados)
    print(f"Tabla procesada guardada en: {tabla}")


if __name__ == "__main__":
    main(mostrar_graficos=True)
