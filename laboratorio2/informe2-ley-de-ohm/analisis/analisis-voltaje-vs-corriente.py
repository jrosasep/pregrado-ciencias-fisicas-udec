import numpy as np
import matplotlib.pyplot as plt
plt.style.use('bmh')

def ajuste_lineal_y_grafico(I, V, titulo="V vs I"):
    """
    Ajusta y grafica V = a*I + b para los datos dados.
    Parámetros:
        I: iterable de corrientes (A)
        V: iterable de voltajes (V)
        titulo: (opcional) título del gráfico
    Retorna:
        (a, b): pendiente (Ohm) e intercepto (V)
    """
    I = np.asarray(I, dtype=float)
    V = np.asarray(V, dtype=float)

    # Ajuste: V = a*I + b
    a, b = np.polyfit(I, V, 1)  # a = pendiente (≈ resistencia en ohmios), b = intercepto (V)

    # Para dibujar la recta entre el mínimo y máximo de I
    I_linea = np.linspace(np.min(I), np.max(I), 200)
    V_linea = a * I_linea + b

    # Reporte básico en consola
    print("=== Ajuste lineal V = a*I + b ===")
    print(f"a (pendiente)  = {a:.6g}  [Ohm]")
    print(f"b (intercepto) = {b:.6g}  [V]")

    # Gráfico
    plt.scatter(I, V, label="Datos", zorder=3)
    plt.plot(I_linea, V_linea, label=f"Ajuste: V = {a:.3g}·I + {b:.3g}")
    plt.xlabel("Corriente I (A)")
    plt.ylabel("Voltaje V (V)")
    plt.title(titulo)
    plt.grid(True, zorder=0)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return a, b

def ajuste_log_led(I, V, titulo="LED: V vs I (x log)"):
    """
    Ajuste logarítmico para datos de LED: V = a*ln(I) + b
    - I en amperes (debe ser > 0)
    - V en volts
    Grafica V vs I con curva ajustada.
    Retorna: (a, b, n, Is)
    """
    I = np.asarray(I, dtype=float)
    V = np.asarray(V, dtype=float)

    # Filtrar corrientes no positivas (ln indefinido)
    mask = I > 0
    if np.count_nonzero(mask) < 2:
        raise ValueError("Se requieren al menos 2 corrientes positivas para el ajuste logarítmico.")
    I = I[mask]
    V = V[mask]

    x = np.log(I)  # ln(I)
    a, b = np.polyfit(x, V, 1)  # V ~ a*ln(I) + b

    # Parámetros físicos aproximados
    V_T = 0.02585  # Volts (≈ 25 °C)
    n = a / V_T
    Is = np.exp(-b / a)

    # Curva ajustada para graficar
    I_fit = np.logspace(np.log10(I.min()), np.log10(I.max()), 200)
    V_fit = a * np.log(I_fit) + b

    # Gráfico (x log)
    plt.figure()
    plt.plot(I, V, "o", label="Datos")        # puntos medidos
    plt.plot(I_fit, V_fit, "-", label=f"Ajuste: V = {a:.3g}·ln(I) + {b:.3g}")  # curva log
    plt.xlabel("Corriente I (A)")
    plt.ylabel("Voltaje V (V)")
    plt.title(titulo)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Reporte
    print("=== Ajuste LED (V = a·ln(I) + b) ===")
    print(f"a = {a:.6g}  [V]   (≈ n·V_T)")
    print(f"b = {b:.6g}  [V]")
    print(f"n ≈ {n:.3g}   (factor de idealidad, usando V_T≈25.85 mV)")
    print(f"I_s ≈ {Is:.3e}  [A]")

    return a, b, n, Is

if __name__ == "__main__":
    # Resistencia R=100 K\ohm data
    V_resistencia = [2.0, 3.0, 2.9, 2.8, 2.6, 2.4, 2.2, 1.8, 1.6, 1.4]
    I_resistencia = [20e-6, 31e-6, 29e-6, 28.5e-6, 26.5e-6, 24.4e-6, 22e-6, 18.7e-6, 16.1e-6, 14.7e-6]
    
    # Ampolleta data
    V_ampolleta = [3.4, 3.6, 4.0, 4.3, 4.5, 1.75, 0.95, 1.5, 0.6, 2.5]
    I_ampolleta = [0.38, 0.39, 0.41, 0.43, 0.44, 0.26, 0.19, 0.24, 0.15, 0.31]

    # LED amarillo data
    V_led_amarillo = [1.90, 1.80, 1.85, 1.87, 1.88, 1.91, 1.93, 1.94, 1.96, 1.98]
    I_led_amarillo = [1.0e-3, 0.1e-3, 0.3e-3, 0.5e-3, 0.7e-3, 1.6e-3, 2.1e-3, 2.6e-3, 3.4e-3, 6.6e-3]

    # LED rojo data
    V_led_rojo = [1.78, 1.816, 1.835, 1.871, 1.911, 1.930, 1.944, 1.951, 1.965, 1.975]
    I_led_rojo = [0.19e-3, 0.350e-3, 0.510e-3, 1.014e-3, 1.895e-3, 2.452e-3, 2.894e-3, 3.139e-3, 3.630e-3, 3.997e-3]
    
    # LED verde data
    V_led_verde = [1.884, 1.919, 1.945, 1.964, 1.982, 1.991, 2.001, 2.011, 2.021, 2.037]
    I_led_verde = [0.206e-3, 0.409e-3, 0.737e-3, 1.120e-3, 1.575e-3, 1.854e-3, 2.249e-3, 2.649e-3, 3.103e-3, 3.610e-3]
    
    # Llama a la función para cada conjunto
    ajuste_lineal_y_grafico(I_resistencia, V_resistencia, titulo="Resistencia")
    ajuste_lineal_y_grafico(I_ampolleta, V_ampolleta, titulo="Ampolleta ")
    ajuste_log_led(I_led_amarillo, V_led_amarillo, titulo="LED amarillo")
    ajuste_log_led(I_led_rojo, V_led_rojo, titulo="LED rojo")
    ajuste_log_led(I_led_verde, V_led_verde, titulo="LED verde")