import numpy as np
import pandas as pd

# ===========================================================
# 1) DATOS EXPERIMENTALES
#    y_sup, y_inf medidos respecto de y=0 (equilibrio)
# ===========================================================

# RESORTE 1

resorte1_name = "1"
resorte1_k = 29.953 # N/m
resorte1_m = 0.250 # kg
resorte1_ysup_m = np.array([11.0, 11.0, 11.0, 11.0, 11.0,10.0, 10.0, 10.0, 9.0, 9.0, 9.0]) #cm
resorte1_yinf_m = np.array([20.0, 20.3,20.7,20.5,20.4,21.0,21.5,21.5, 22.5,22.3,23.5]) #cm
resorte1 = resorte1_name, resorte1_k , resorte1_m, resorte1_ysup_m, resorte1_yinf_m 

# RESORTE 2

resorte2_name = "2"
resorte2_k = 9.800 # N/m
resorte2_m = 0.250 # kg
resorte2_ysup_m = np.array([28.2, 27.2, 26.2, 25.2, 24.2]) # cm
resorte2_yinf_m = np.array([37.2, 38.6, 39.7, 40.8, 41.4]) # cm
resorte2 = resorte2_name, resorte2_k , resorte2_m, resorte2_ysup_m, resorte2_yinf_m

# ===========================================================
#3) ANÁLISIS DE DATOS
# ===========================================================
def compute_amplitude_table(resorte, g=9.81):
    
    name, k, m, ysup_m, yinf_m = resorte
    
    # Conversión de cm a m
    ysup_m = ysup_m / 100.0 # m
    yinf_m = yinf_m / 100.0 # m
    
    # Calculo de \delta y
    dy = np.abs(yinf_m - ysup_m) / 2.0
    
    # Calculo de energias
    Eg = m * g * dy
    Ee = 0.5 * k * dy**2
    Emec = Eg + Ee

    df = pd.DataFrame({
        "N": np.arange(1, len(dy) + 1),
        "y_sup (m)": np.round(ysup_m, 3),
        "y_inf (m)": np.round(yinf_m, 3),
        "Delta_y (m)": np.round(dy, 3),
        "E_grav (J)": np.round(Eg, 3),
        "E_elast (J)": np.round(Ee, 3),
        "E_mec (J)": np.round(Emec, 3),
    }) 
    
# ===========================================================
# 4) IMPRESIÓN DE RESULTADOS
# ===========================================================    
    
    print(f"==== ENERGÍAS Resorte {name} ====")
    print(f"Parámetros: m = {m:.3f} kg, k = {k:.2f} N/m, g = {g:.2f} m/s^2")
    print(df.to_string(index=False))
    print("")
    return none
    
# ===========================================================
# 5 ) EJECUTAR FUNCIONES
# ===========================================================

compute_amplitude_table(resorte1)
compute_amplitude_table(resorte2)