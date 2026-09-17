import numpy as np
import matplotlib.pyplot as plt
import jinja2

#Se definen las constantes:   
G = 6.67430e-11  # m^3 kg^-1 s^-2
M = 5.97e24      # kg
R = 6371e3       # m (radio de la Tierra)

# Función para calcular h en función de T:
def height_h(T):
    return (G * M * T**2 / (4 * np.pi**2))**(1/3) - R


# Periodos en segundos:
T_values = np.arange(15 * 60, 6 * 3600 + 1, 15 * 60)

# Valores de h en metros:
h_values = [height_h(T) for T in T_values]

# Preparar datos para LaTeX:
data = [{"T": T, "h": h} for T, h in zip(T_values, h_values)]

# Gráfico de h(T) vs T:
plt.figure(figsize=(10, 6))
plt.plot(T_values, h_values, label="Altitud $h(T)$")
plt.xlabel("Periodo $T$ (s)")
plt.ylabel("Altitud $h$ (m)")
plt.title("Altitud $h$ en función del Periodo $T$")
plt.grid()
plt.legend()
plt.savefig("grafico_altitud.pdf")
plt.show()

# Tabla de datos y gráfico en LaTeX:
Texto = r"""
\documentclass{article}
\usepackage{graphicx}
\usepackage{booktabs}
\begin{document}

\section*{Tabla de Altitudes para Diferentes Períodos}

\begin{table}[h!]
    \centering
        \begin{tabular}{@{}cc@{}}
            \toprule
                \textbf{Periodo $T$ (s)} & \textbf{Altitud $h$ (m)} \\ \midrule
                    {% for row in data %}
                    {{ row.T }} & {{ row.h | round(2)}} \\
                    {% endfor %}
            \bottomrule
    \end{tabular}
\end{table}

\section*{Gráfico de Altitud $h$ en Función de $T$}

\includegraphics[width=\textwidth]{grafico_altitud.pdf}

\end{document}
"""

# Renderizar plantilla:
latex_template = jinja2.Template(Texto)
latex_output = latex_template.render(data=data)

# Guardar como archivo .tex
with open("tabla_altitudes.tex", "w") as f:
    f.write(latex_output)

# Definimos los periodos sideral y solar:
T_sideral = 86148  # segundos
T_solar = 86400  # segundos

# Calculamos la altura sideral y solar:
h_sideral = height_h(T_sideral)
h_solar = height_h(T_solar)

# Calculamos la diferencia:
diferencia = abs(h_solar - h_sideral)
print(f"Diferencia de altitud: {diferencia:.2f} metros")