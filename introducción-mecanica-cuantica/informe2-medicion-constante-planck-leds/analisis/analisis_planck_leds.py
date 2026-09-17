import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# =============================================================================
# CONSTANTES FÍSICAS FUNDAMENTALES
# =============================================================================
CARGA_ELECTRON = 1.602176634e-19  # C
VELOCIDAD_LUZ = 299792458.0       # m/s
H_PLANCK_REF = 6.62607015e-34     # J·s (valor de referencia)

# =============================================================================
# DATOS EXPERIMENTALES - MEDICIONES DE VOLTAJES UMBRAL
# =============================================================================
VOLTAJES_LED = {
    "azul":     [2.22, 2.22, 2.22, 2.22, 2.22],
    "amarillo": [1.70, 1.70, 1.70, 1.70, 1.70],
    "verde":    [1.70, 1.70, 1.70, 1.70, 1.70],
    "naranja":  [1.56, 1.55, 1.55, 1.54, 1.54],
}

LONGITUDES_ODA_LED = {
    "azul": 472.5,    # nm
    "amarillo": 580.0,
    "verde": 532.0,
    "naranja": 599.5,
}

def preparar_datos_frecuencia_voltaje():
    """
    Prepara arrays de frecuencia (x) y voltaje umbral (y) para el ajuste lineal
    """
    frecuencias = []
    voltajes = []
    
    for color, lista_voltajes in VOLTAJES_LED.items():
        lambda_nm = LONGITUDES_ODA_LED.get(color)
        if lambda_nm is None:
            continue
            
        # Calcular frecuencia a partir de longitud de onda
        frecuencia = VELOCIDAD_LUZ / (lambda_nm * 1e-9)
        
        # Añadir todas las réplicas para este color
        for voltaje in lista_voltajes:
            frecuencias.append(frecuencia)
            voltajes.append(voltaje)
            
    return np.array(frecuencias), np.array(voltajes)

def ajuste_lineal_minimos_cuadrados(x, y):
    """
    Realiza ajuste lineal por mínimos cuadrados y calcula incertidumbres
    """
    # Ajuste lineal
    coeficientes, matriz_covarianza = np.polyfit(x, y, deg=1, cov=True)
    pendiente, intercepto = coeficientes
    
    # Cálculo de incertidumbres
    error_pendiente = np.sqrt(matriz_covarianza[0, 0])
    error_intercepto = np.sqrt(matriz_covarianza[1, 1])
    
    # Valores predichos y R²
    y_predicho = pendiente * x + intercepto
    ss_residual = np.sum((y - y_predicho)**2)
    ss_total = np.sum((y - np.mean(y))**2)
    r_cuadrado = 1 - (ss_residual / ss_total) if ss_total > 0 else np.nan
    
    return pendiente, intercepto, error_pendiente, error_intercepto, y_predicho, r_cuadrado

def generar_grafico_ajuste(x, y, pendiente, intercepto, archivo_salida):
    """
    Genera gráfico de dispersión con recta de ajuste lineal
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Puntos experimentales
    ax.scatter(x, y, alpha=0.7, s=60, label='Datos experimentales', color='blue')
    
    # Recta de ajuste
    x_ajuste = np.linspace(x.min() * 0.98, x.max() * 1.02, 200)
    y_ajuste = pendiente * x_ajuste + intercepto
    ax.plot(x_ajuste, y_ajuste, 'r-', linewidth=2, label='Ajuste lineal')
    
    ax.set_xlabel('Frecuencia (Hz)', fontsize=12)
    ax.set_ylabel('Voltaje umbral ΔV (V)', fontsize=12)
    ax.set_title('Efecto Fotoeléctrico: ΔV vs Frecuencia', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    fig.savefig(archivo_salida, dpi=200, bbox_inches='tight')
    plt.close(fig)

def generar_grafico_residuos(x, y, pendiente, intercepto, archivo_salida):
    """
    Genera gráfico de residuos del ajuste lineal
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    y_predicho = pendiente * x + intercepto
    residuos = y - y_predicho
    
    ax.scatter(x, residuos, alpha=0.7, s=50, color='green')
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1)
    
    ax.set_xlabel('Frecuencia (Hz)', fontsize=12)
    ax.set_ylabel('Residuos (V)', fontsize=12)
    ax.set_title('Análisis de Residuos del Ajuste Lineal', fontsize=14)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    fig.savefig(archivo_salida, dpi=200, bbox_inches='tight')
    plt.close(fig)

def ejecutar_analisis_completo():
    """
    Función principal - Ejecuta todo el análisis paso a paso
    """
    print("\n ANÁLISIS DEL EFECTO FOTOELÉCTRICO")
    print("=" * 50)
    
    # 1. PREPARACIÓN DE DATOS
    frecuencias, voltajes = preparar_datos_frecuencia_voltaje()
    print(f"   • Puntos de datos: {len(frecuencias)}")
    print(f"   • Rango de frecuencias: {frecuencias.min():.2e} - {frecuencias.max():.2e} Hz")
    
    # 2. AJUSTE LINEAL
    m, b, m_err, b_err, y_pred, r2 = ajuste_lineal_minimos_cuadrados(frecuencias, voltajes)
    
    # 3. ESTIMACIÓN DE h
    h_estimado = CARGA_ELECTRON * m
    h_error = CARGA_ELECTRON * m_err
    
    error_absoluto = abs(h_estimado - H_PLANCK_REF)
    error_relativo = (error_absoluto / H_PLANCK_REF) * 100
    
    # 4. PRESENTACIÓN DE RESULTADOS
    print("\n RESULTADOS DEL ANÁLISIS")
    print("=" * 50)
    print(f"PARÁMETROS DEL AJUSTE LINEAL:")
    print(f"   • Pendiente (m):      ({m:.4e} ± {m_err:.1e}) V/Hz")
    print(f"   • Intercepto (b):     ({b:.3f} ± {b_err:.3f}) V")
    print(f"   • Coeficiente R²:     {r2:.4f}")
    
    print(f"\n ESTIMACIÓN DE LA CONSTANTE DE PLANCK:")
    print(f"   • h estimado:         ({h_estimado:.4e} ± {h_error:.1e}) J·s")
    print(f"   • h referencia:       {H_PLANCK_REF:.8e} J·s")
    print(f"   • Error absoluto:     {error_absoluto:.3e} J·s")
    print(f"   • Error relativo:     {error_relativo:.2f} %")
    
    # 5. GENERACIÓN DE GRÁFICOS
    directorio = Path(".")
    
    generar_grafico_ajuste(frecuencias, voltajes, m, b, 
                          directorio / "ajuste_lineal_efecto_fotoelectrico.png")
    
    generar_grafico_residuos(frecuencias, voltajes, m, b,
                            directorio / "residuos_ajuste.png")
    
    print("\n ANÁLISIS COMPLETADO")
    print("=" * 50)
    print("Gráficos guardados:")
    print("   • ajuste_lineal_efecto_fotoelectrico.png")
    print("   • residuos_ajuste.png")

# =============================================================================
# EJECUCIÓN DIRECTA DEL PROGRAMA
# =============================================================================

# El programa comienza aquí automáticamente cuando lo ejecutas
print("Iniciando análisis del efecto fotoeléctrico...")
ejecutar_analisis_completo()
print("FIN")