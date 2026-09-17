import numpy as np
import matplotlib.pyplot as plt

#Importo el archivo de datos
Data = np.genfromtxt("data.dat", delimiter=" ")
#Defino arreglos que tendran los datos:
x = Data[1:,0]  #x_i
f = Data[1:,1]  #f_i
df = Data[1:,2] #f'_i

# Función para estimar la derivada numéricamente usando el esquema dado
def numerical_derivative(x, f):
    # Calcular el espaciado h entre puntos
    h = x[1] - x[0]  # Asume x equiespaciados

    # Recortar los índices válidos para el cálculo
    valid_indices = range(3, len(x) - 3)
    x_rec = x[valid_indices]  # índices donde se calcula la derivada

    # Cálculo de la derivada
    deriv = [(f[i - 3] - 27 * f[i - 1] + 27 * f[i + 1] - f[i + 3]) / (48 * h) for i in valid_indices]

    return np.array(x_rec), np.array(deriv)

# Función principal que incluye gráficos y cálculo del error
def analyze_data(x, f, df):
    # Calcular la derivada numérica
    x_rec, df_num = numerical_derivative(x, f)
    
    # Recortar df para que coincidan con la longitud de df_num
    df_rec = df[3:-3]  # Ajustamos también la derivada analítica
    
    # Calcular el error absoluto
    error_abs = np.abs(df_rec - df_num)
    
    # Graficar resultados
    fig, ax = plt.subplots(3, sharex=True, figsize=(10, 12))
    
    # Personalización global
    plt.subplots_adjust(hspace=0.4)  # Ajustar espacio entre subgráficos
    # Función original
    ax[0].plot(x, f, label="Función original $f(x)$", color="blue", linewidth=2)
    ax[0].set_ylabel("$f(x)$", fontsize=14)
    ax[0].legend(fontsize=12, loc="upper right")
    ax[0].grid(True, linestyle="--", alpha=0.6)
    ax[0].set_title("Análisis de la función y sus derivadas", fontsize=16, fontweight="bold")
    
    # Comparación de derivadas
    ax[1].plot(x, df, label="Derivada exacta $f'(x)$", linestyle="--", color="green", linewidth=2)
    ax[1].plot(x_rec, df_num, label="Aproximación numérica", linestyle="-.", color="orange", linewidth=2)
    ax[1].set_ylabel("$f'(x)$", fontsize=14)
    ax[1].legend(fontsize=12, loc="upper right")
    ax[1].grid(True, linestyle="--", alpha=0.6)
    
    # Error absoluto
    ax[2].plot(x_rec, error_abs, label="Error absoluto", color="red", linestyle=":", linewidth=2)
    ax[2].set_xlabel("$x$", fontsize=14)
    ax[2].set_ylabel("Error absoluto", fontsize=14)
    ax[2].legend(fontsize=12, loc="upper right")
    ax[2].grid(True, linestyle="--", alpha=0.6)
    
    # Estilo general
    for axis in ax:
        axis.tick_params(axis="both", labelsize=12)

    plt.show()

# Probar el script con los casos dados
if __name__ == "__main__":
    # Caso 1: Función sinusoidal
    gen = np.random.default_rng()
    x1 = np.linspace(0, 2 * np.pi, 256)
    f1 = np.sin(x1) + gen.uniform(low=-1e-2, high=1e-2, size=x1.size)
    df1 = np.cos(x1)
    print("Caso 1: Función sinusoidal")
    analyze_data(x1, f1, df1)

    # Caso 2: Funciones de Legendre
    from scipy.special import legendre
    p, q = legendre(5), legendre(3)
    dp, dq = p.deriv(), q.deriv()
    x2 = np.linspace(-0.7, 0.7, 512)
    f2 = q(2 * p(x2)) + 0.01 * np.random.randn(x2.size)
    df2 = 2 * dq(2 * p(x2)) * dp(x2)
    print("Caso 2: Funciones de Legendre")
    analyze_data(x2, f2, df2)
