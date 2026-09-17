import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Configuración de estilo para gráficos más atractivos
plt.style.use('seaborn-v0_8')
plt.rcParams['font.family'] = 'DejaVu Sans'

ELEM_CHARGE = 1.602176634e-19  # C
C_LIGHT = 299_792_458.0        # m/s

# Voltajes medidos (mismo conjunto de datos)
V_RED_mV = np.array([101.3, 95.1, 96.6, 77.4])
V_GREEN_mV = np.array([287.8, 284.0, 281.9, 270.0])
V_BLUE_mV = np.array([377.5, 372.0, 370.0, 368.0])

VOLTAGES_mV = {
    "rojo": V_RED_mV,
    "verde": V_GREEN_mV,
    "azul": V_BLUE_mV,
}

# Longitudes de onda nominales (nm) asociadas a la luz incidente
WAVELENGTHS_NM = {
    "rojo": 688.0,
    "verde": 533.0,
    "azul": 473.0,
}

# Colores para el gráfico
COLORS_PLOT = {
    "rojo": '#FF6B6B',
    "verde": '#4ECDC4',
    "azul": '#45B7D1',
}


def voltage_stats(v_mV):
    mean = np.mean(v_mV)
    std = np.std(v_mV, ddof=1)
    return mean, std


colors = ["rojo", "verde", "azul"]
freqs = []
v_means = []
v_stds = []

for color in colors:
    v_mean_mV, v_std_mV = voltage_stats(VOLTAGES_mV[color])
    v_mean_V = v_mean_mV * 1e-3
    lam_nm = WAVELENGTHS_NM[color]
    lam_m = lam_nm * 1e-9
    freq = C_LIGHT / lam_m

    v_means.append(v_mean_V)
    v_stds.append(v_std_mV * 1e-3)
    freqs.append(freq)

freqs = np.array(freqs)
v_means = np.array(v_means)
v_stds = np.array(v_stds)

# Ajuste lineal V(f) = a f + b
coeffs = np.polyfit(freqs, v_means, 1)
a, b = coeffs
f_fit = np.linspace(freqs.min() * 0.95, freqs.max() * 1.05, 200)
V_fit = a * f_fit + b

# Cálculo de h (constante de Planck) y función trabajo efectiva W
h_exp = a * ELEM_CHARGE
h_teorico = 6.62607015e-34
error_porcentual = abs((h_exp - h_teorico) / h_teorico) * 100

W_exp = -ELEM_CHARGE * b        # J
W_exp_eV = W_exp / ELEM_CHARGE  # eV (aprox. igual a -b, pero lo dejamos explícito)

# Crear figura
fig, ax = plt.subplots(figsize=(10, 7))

# Graficar puntos con colores representativos y línea de ajuste
for i, color in enumerate(colors):
    ax.errorbar(
        freqs[i], v_means[i], yerr=v_stds[i],
        fmt='o', markersize=10, capsize=8, capthick=2,
        color=COLORS_PLOT[color], elinewidth=2,
        label=f'Luz {color} ({WAVELENGTHS_NM[color]} nm)',
        markerfacecolor=COLORS_PLOT[color], markeredgecolor='white',
        markeredgewidth=2
    )

# Línea de ajuste
ax.plot(
    f_fit, V_fit, '--', color='#2E86AB', linewidth=2.5,
    alpha=0.8, label=f'Ajuste lineal: $V = {a:.2e} f + {b:.2e}$'
)

# Etiquetas y título
ax.set_xlabel("Frecuencia $f$ (Hz)", fontsize=14, fontweight='bold')
ax.set_ylabel("Voltaje de freno $V_0$ (V)", fontsize=14, fontweight='bold')
ax.set_title("Efecto fotoeléctrico: Voltaje vs frecuencia de la luz",
             fontsize=16, fontweight='bold', pad=20)

# Formato científico en ejes
ax.ticklabel_format(style='sci', axis='both', scilimits=(0, 0))
ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))

# Grid y fondo
ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
ax.set_axisbelow(True)

# Leyenda
legend = ax.legend(
    loc='upper left', frameon=True, framealpha=0.9,
    edgecolor='black', fontsize=11
)
legend.get_frame().set_facecolor('#F8F9FA')

# Texto con resultados del ajuste
textstr = (
    f'm = {a:.2e} V/Hz\n'
    f'b = {b:.2e} V\n'
    f'$h_{{\\text{{exp}}}}$ = {h_exp:.2e} J·s\n'
    f'$h_{{\\text{{ref}}}}$ = {h_teorico:.2e} J·s\n'
    f'Error en $h$: {error_porcentual:.1f}%\n'
    f'$W_{{\\text{{exp}}}}$ = {W_exp:.2e} J\n'
    f'$W_{{\\text{{exp}}}}$ ≈ {W_exp_eV:.2f} eV'
)
props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)

ax.text(
    0.98, 0.02, textstr,
    transform=ax.transAxes,
    fontsize=11,
    verticalalignment='bottom',
    horizontalalignment='right',
    bbox=props
)

plt.tight_layout()
plt.savefig("grafico_V_vs_f.pdf")
plt.show()
