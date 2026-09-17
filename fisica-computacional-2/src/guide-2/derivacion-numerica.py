# Importamos las bibliotecas necesarias.
import numpy as np
import matplotlib.pyplot as plt

# Definimos el rango de valores de x. 
# Se asegura que x > 0 para evitar problemas con ln(x).
x_values = np.linspace(0.5, 12, 200)  # Genera 200 valores equiespaciados entre 0.5 y 12.

# Definimos el tamaño del paso h para las diferencias finitas.
h = 0.1

# Función para calcular y graficar las derivadas numéricas usando esquemas finitos.
def Esquemas_de_diferencias(f,df, x_vals=x_values, h=h):
    """
    Calcula y grafica la derivada analítica y las derivadas numéricas usando esquemas adelantado, retrasado y centrado.
    
    Parámetros:
        f (function): Función a derivar numéricamente.
        df (function): Derivada analítica de la función f.
        x_vals (array): Valores de x donde se calcularán las derivadas.
        h (float): Tamaño del paso para las diferencias finitas.
    """
 
    # Calculamos las derivadas analíticas.
    df_analitica = np.array([df(x) for x in x_vals])
    
    # Calculamos las derivadas numéricas usando diferencias adelantadas.
    df_adelantada = np.array([(f(x + h) - f(x)) / h for x in x_vals])
    
    # Calculamos las derivadas numéricas usando diferencias retrasadas.
    df_retrasada = np.array([(f(x) - f(x - h)) / h for x in x_vals]) 
    
    # Calculamos las derivadas numéricas usando diferencias centradas.
    df_centrada = np.array([(f(x + h) - f(x - h)) / (2 * h) for x in x_vals])

    #Ajustamos las dimensiones del gráfico.
    plt.figure(figsize=(10, 6))
    # Graficamos las derivadas analíticas y numéricas calculadas.
    plt.plot(x_vals, df_analitica, color="orange", linewidth=2.5, linestyle="--", label="Derivada analítica")  # Línea naranja gruesa y discontinua.
    plt.plot(x_vals, df_adelantada, color="green", label="Derivada adelantada")  # Línea verde.
    plt.plot(x_vals, df_retrasada, color="red", label="Derivada retrasada")  # Línea roja.
    plt.plot(x_vals, df_centrada, color="blue", label="Derivada centrada")  # Línea azul.

    # Agregamos leyenda y títulos a la gráfica.
    plt.legend()  # Muestra la leyenda.
    plt.title(f"Comparación entre las Derivadas numéricas y analitica para la función {f.nombre}")  # Título con el nombre de la función.
    plt.xlabel("x")  # Etiqueta del eje x.
    plt.ylabel(f"{f.nombre}")  # Etiqueta del eje y.
    plt.grid(True)  # Muestra una cuadrícula para facilitar la lectura.

    # Ajustamos la disposición de la gráfica y la mostramos.
    plt.tight_layout()
    return plt.show()

# Función para calcular el error relativo entre derivadas analíticas y numéricas.
def Error_relativo(f, df, x_vals=x_values, h=h):
    """
    Calcula y grafica el error relativo entre la derivada numérica y la derivada analítica.
    
    Parámetros:
        f (function): Función a derivar.
        df (function): Derivada analítica de la función f.
        x_vals (array): Valores de x para evaluar las derivadas.
        h (float): Tamaño del paso para las diferencias finitas.
    """
    # Calculamos las derivadas analíticas.
    df_analitica = np.array([df(x) for x in x_vals])
    
    # Calculamos las derivadas numéricas usando los tres esquemas.
    df_adelantada = np.array([(f(x + h) - f(x)) / h for x in x_vals])
    df_retrasada = np.array([(f(x) - f(x - h)) / h for x in x_vals]) 
    df_centrada = np.array([(f(x + h) - f(x - h)) / (2 * h) for x in x_vals])
    
    # Calculamos el error relativo para cada esquema.
    error_adelantada = np.abs(df_adelantada - df_analitica) / np.abs(df_analitica)
    error_retrasada = np.abs(df_retrasada - df_analitica) / np.abs(df_analitica)
    error_centrada = np.abs(df_centrada - df_analitica) / np.abs(df_analitica)
    
    #Ajustamos las dimensiones del gráfico.
    plt.figure(figsize=(10, 6))
    # Graficamos el error relativo para los tres esquemas.
    plt.plot(x_vals, error_adelantada, color="green", label="Error derivada adelantada")  # Línea verde.
    plt.plot(x_vals, error_retrasada, color="red", label="Error derivada retrasada")  # Línea roja.
    plt.plot(x_vals, error_centrada, color="blue", label="Error derivada centrada")  # Línea azul.
    
    # Personalizamos la gráfica.
    plt.legend()
    plt.title(f"Error relativo para la función {f.nombre}")
    plt.xlabel("x")
    plt.ylabel("Error relativo")
    plt.grid(True)
    plt.tight_layout()
    return plt.show()

# Definimos las funciones y sus derivadas analíticas para evaluar esquemas de derivación numérica.
# Además, asignamos un atributo `nombre` con representación en formato LaTeX para personalizar los gráficos.

# Función seno y su derivada analítica:
def f(x):   return np.sin(x)  # Calcula el seno de x.
f.nombre = r'$\sin(x)$'  # Representación LaTeX para el título de las gráficas.

def df(x):  return np.cos(x)  # La derivada analítica de sin(x) es cos(x).

# Función exponencial y su derivada analítica:
def g(x):   return np.exp(x)  # Calcula la exponencial de x, e^x.
g.nombre = r'$e^x$'  # Representación LaTeX para el título de las gráficas.

def dg(x):  return np.exp(x)  # La derivada analítica de e^x es e^x.

# Función logaritmo natural y su derivada analítica:
def ln(x):  return np.log(x)  # Calcula el logaritmo natural de x. Nota: x > 0.
ln.nombre = r'$\ln(x)$'  # Representación LaTeX para el título de las gráficas.

def dln(x): return 1/x  # La derivada analítica de ln(x) es 1/x. Nota: x > 0.

# Función cuadrática y su derivada analítica:
def j(x):   return x**2  # Calcula el cuadrado de x.
j.nombre = r'$x^2$'  # Representación LaTeX para el título de las gráficas.

def dj(x):  return 2*x  # La derivada analítica de x^2 es 2x.

# Calculamos las derivadas numéricas para cada función utilizando esquemas finitos
# y graficamos los resultados en comparación con las derivadas analíticas.
Esquemas_de_diferencias(f, df, x_vals=x_values, h=h)  # Esquemas para f(x) = sin(x).
Esquemas_de_diferencias(g, dg, x_vals=x_values, h=h)  # Esquemas para g(x) = e^x.
Esquemas_de_diferencias(ln, dln, x_vals=x_values, h=h)  # Esquemas para ln(x).
Esquemas_de_diferencias(j, dj, x_vals=x_values, h=h)  # Esquemas para j(x) = x^2.

# Calculamos el error relativo entre las derivadas numéricas y analíticas,
# y graficamos los errores relativos como función de x para cada función.
Error_relativo(f, df, x_vals=x_values, h=h)  # Error relativo para f(x) = sin(x).
Error_relativo(g, dg, x_vals=x_values, h=h)  # Error relativo para g(x) = e^x.
Error_relativo(ln, dln, x_vals=x_values, h=h)  # Error relativo para ln(x).
Error_relativo(j, dj, x_vals=x_values, h=h)  # Error relativo para j(x) = x^2.