import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 1) DATOS EXPERIMENTALES (SI)
# -----------------------------------------------------------

# RESORTE 1 

resorte1_name = 1
resorte1_delta_x_m = np.array([0.097, 0.176, 0.252, 0.332, 0.427, 0.503])  # m
resorte1_F_N = np.array([2.45, 4.90, 7.35, 9.82, 12.26, 14.71])            # N
resorte1 = resorte1_name , resorte1_delta_x_m , resorte1_F_N

# RESORTE 2

resorte2_name = 2
resorte2_delta_x_m = np.array([0.150, 0.200, 0.250, 0.300])  # m
resorte2_F_N = np.array([1.64, 2.13, 2.62, 3.11])            # N
resorte2 = resorte2_name , resorte2_delta_x_m , resorte2_F_N

# -----------------------------------------------------------
# 2) REGRESIÓN LINEAL: F = k * x + b
# -----------------------------------------------------------

def lineal_regresion_and_graphics(resorte):
    name, delta_x_m, F_N = resorte
    
    coeffs = np.polyfit(delta_x_m, F_N, 1)
    k_fit, b_fit = coeffs[0], coeffs[1]
    
    # Predicción y coeficiente R^2
    F_pred = np.polyval(coeffs, delta_x_m)
    residuals = F_N - F_pred
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((F_N - np.mean(F_N))**2)
    r2 = 1 - ss_res/ss_tot
    
# -----------------------------------------------------------
# 3) GRÁFICO
# -----------------------------------------------------------

    plt.figure(figsize=(12,6))  # Formato horizontal para informe
    
    # Puntos experimentales
    plt.scatter(delta_x_m, F_N, marker='x', s=80, linewidths=2,
                label='Datos experimentales', color="black")
    
    # Generar curva suave del ajuste
    x_dense = np.linspace(delta_x_m.min()*0.9, delta_x_m.max()*1.1, 200)
    F_dense = np.polyval(coeffs, x_dense)
    plt.plot(x_dense, F_dense, linewidth=2.5,
             label=f'Ajuste lineal:  F = ({k_fit:.2f})·x + ({b_fit:.2f})', color="orange")
    
    # Títulos y etiquetas
    plt.title(f'Fuerza vs Elongación — Resorte {name}', fontsize=14)
    plt.xlabel('Elongación  $\\Delta x$  (m)', fontsize=12)
    plt.ylabel('Fuerza  $F$  (N)', fontsize=12)
    
    # Cuadrícula y leyenda
    plt.grid(alpha=0.3)
    plt.legend(loc='upper left', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'F_vs_DeltaX_resorte_{name}.png', dpi=300)
    plt.show()

# -----------------------------------------------------------
# 4) IMPRESIÓN DE RESULTADOS
# -----------------------------------------------------------

    print(f"==== AJUSTE LINEAL Resorte {name} F = k·x + b ====")
    print(f"k = {k_fit:.3f} N/m")
    print(f"b = {b_fit:.3f} N")
    print(f"R^2 = {r2:.5f}")
    print("")
    
# -----------------------------------------------------------
# 5) EJECUTAR FUNCIONES
# -----------------------------------------------------------

lineal_regresion_and_graphics(resorte1)
lineal_regresion_and_graphics(resorte2)