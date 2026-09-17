# Calor espefico del agua:
c_H2O = 4186.0 # [\frac{J}{Kg°C}]    
    
# Valores de las masas, en gramos [g]:
m_Al = 69.0 #[g]. Masa del cilindro de aluminio (Al).
m_Fe = 230.8 #g. Masa del bloque de hierro (Fe).

# --------------------------------------------------------------------
# MEZCLA AGUA–HIERRO (Fe) — tres corridas con distintos volúmenes de agua
#   m_H2O = {400, 300, 200} g   |   T_i_H2O = 16 °C
#   m_Fe = 230.8 g              |   T_i_Fe = 99 °C
#   T_eq = {21, 23, 27} °C
# --------------------------------------------------------------------

############################# CORRIDA Fe — 1 #############################
# Temperaturas registradas
T_i_H2O___H2O_and_Fe__run1 = 16.0  # [°C]
T_i_Fe___H2O_and_Fe__run1  = 99.0  # [°C]
T_eq___H2O_and_Fe__run1    = 21.0  # [°C]

# Masas
m_H2O___H2O_and_Fe__run1 = 400.0   # [g]
m_Fe___H2O_and_Fe__run1  = m_Fe    # [g]

# Información de la experiencia reunida en una sola variable
data___H2O_and_Fe__run1 = (
    m_H2O___H2O_and_Fe__run1, m_Fe___H2O_and_Fe__run1,
    T_i_H2O___H2O_and_Fe__run1, T_i_Fe___H2O_and_Fe__run1,
    T_eq___H2O_and_Fe__run1, c_H2O
)

############################# CORRIDA Fe — 2 #############################
T_i_H2O___H2O_and_Fe__run2 = 16.0  # [°C]
T_i_Fe___H2O_and_Fe__run2  = 99.0  # [°C]
T_eq___H2O_and_Fe__run2    = 23.0  # [°C]

m_H2O___H2O_and_Fe__run2 = 300.0   # [g]
m_Fe___H2O_and_Fe__run2  = m_Fe    # [g]

data___H2O_and_Fe__run2 = (
    m_H2O___H2O_and_Fe__run2, m_Fe___H2O_and_Fe__run2,
    T_i_H2O___H2O_and_Fe__run2, T_i_Fe___H2O_and_Fe__run2,
    T_eq___H2O_and_Fe__run2, c_H2O
)

############################# CORRIDA Fe — 3 #############################
T_i_H2O___H2O_and_Fe__run3 = 16.0  # [°C]
T_i_Fe___H2O_and_Fe__run3  = 99.0  # [°C]
T_eq___H2O_and_Fe__run3    = 27.0  # [°C]

m_H2O___H2O_and_Fe__run3 = 200.0   # [g]
m_Fe___H2O_and_Fe__run3  = m_Fe    # [g]

data___H2O_and_Fe__run3 = (
    m_H2O___H2O_and_Fe__run3, m_Fe___H2O_and_Fe__run3,
    T_i_H2O___H2O_and_Fe__run3, T_i_Fe___H2O_and_Fe__run3,
    T_eq___H2O_and_Fe__run3, c_H2O
)

# --------------------------------------------------------------------
# MEZCLA AGUA–ALUMINIO (Al) — tres corridas
#   m_Al = 69.0 g               |   T_i_Al = 100 °C
#   m_H2O = {210, 251, 285.7} g |   T_i_H2O = {16.5, 17.0, 18.0} °C
#   T_eq = {22.0, 21.0, 21.4} °C
# --------------------------------------------------------------------

############################# CORRIDA Al — 1 #############################
T_i_H2O___H2O_and_Al__run1 = 16.5  # [°C]
T_i_Al___H2O_and_Al__run1  = 100.0 # [°C]
T_eq___H2O_and_Al__run1    = 22.0  # [°C]

m_H2O___H2O_and_Al__run1 = 210.0   # [g]
m_Al___H2O_and_Al__run1  = m_Al    # [g]

data___H2O_and_Al__run1 = (
    m_H2O___H2O_and_Al__run1, m_Al___H2O_and_Al__run1,
    T_i_H2O___H2O_and_Al__run1, T_i_Al___H2O_and_Al__run1,
    T_eq___H2O_and_Al__run1, c_H2O
)

############################# CORRIDA Al — 2 #############################
T_i_H2O___H2O_and_Al__run2 = 17.0  # [°C]
T_i_Al___H2O_and_Al__run2  = 100.0 # [°C]
T_eq___H2O_and_Al__run2    = 21.0  # [°C]

m_H2O___H2O_and_Al__run2 = 251.0   # [g]
m_Al___H2O_and_Al__run2  = m_Al    # [g]

data___H2O_and_Al__run2 = (
    m_H2O___H2O_and_Al__run2, m_Al___H2O_and_Al__run2,
    T_i_H2O___H2O_and_Al__run2, T_i_Al___H2O_and_Al__run2,
    T_eq___H2O_and_Al__run2, c_H2O
)

############################# CORRIDA Al — 3 #############################
T_i_H2O___H2O_and_Al__run3 = 18.0   # [°C]
T_i_Al___H2O_and_Al__run3  = 100.0  # [°C]
T_eq___H2O_and_Al__run3    = 21.4   # [°C]

m_H2O___H2O_and_Al__run3 = 285.7    # [g]
m_Al___H2O_and_Al__run3  = m_Al     # [g]

data___H2O_and_Al__run3 = (
    m_H2O___H2O_and_Al__run3, m_Al___H2O_and_Al__run3,
    T_i_H2O___H2O_and_Al__run3, T_i_Al___H2O_and_Al__run3,
    T_eq___H2O_and_Al__run3, c_H2O
)

# --------------------------------------------------------------------
# Listas para iterar sobre la función c_2
# --------------------------------------------------------------------

datasets__Fe = [data___H2O_and_Fe__run1, data___H2O_and_Fe__run2, data___H2O_and_Fe__run3]
datasets__Al = [data___H2O_and_Al__run1, data___H2O_and_Al__run2, data___H2O_and_Al__run3]

# =========================
# Descriptores de CASO
# =========================
case__H2O_Fe = {
    "caso": "Mezcla calorimétrica H2O–Fe en medio adiabático",
    "s1": "H2O",
    "s2": "Fe",
    "datasets": datasets__Fe,
}

case__H2O_Al = {
    "caso": "Mezcla calorimétrica H2O–Al en medio adiabático",
    "s1": "H2O",
    "s2": "Al",
    "datasets": datasets__Al,
}

def c_2(data_1_and_2, etiqueta=None):
    """
    Calcula c_2 (p.ej., calor específico del cuerpo 2) por mezcla y
    MUESTRA en pantalla los datos usados entre las sustancias 1 y 2.

    data = (m_1[g], m_2[g], T_i_1[°C], T_i_2[°C], T_eq[°C], c_1[J/(kg·°C)])
    """
    # Desempaquetar y conservar originales para imprimir en sus unidades
    m_1, m_2, T_i_1, T_i_2, T_eq, c_1 = data_1_and_2
    m1_g, m2_g = m_1, m_2  # guardar en g para el print

    # Mensaje con los datos usados
    print(
        f"--> {etiqueta}:"
        f"\n    m1 = {m1_g:.1f} g, T_i1 = {T_i_1:.2f} °C"
        f"\n    m2 = {m2_g:.1f} g, T_i2 = {T_i_2:.2f} °C"
        f"\n    T_eq = {T_eq:.2f} °C"
        f"\n    c_1 = {c_1:.2f} J/(kg·°C)"
    )

    # Cálculo (g → kg) y retorno como float nativo
    m_1 *= 1e-3  # g → kg
    m_2 *= 1e-3  # g → kg
    c2 = c_1 * (m_1 * (T_eq - T_i_1)) / (m_2 * (T_i_2 - T_eq))
    return float(round(c2, 2))

def analisis(case, nombre=""):
    """
    Aplica c_2 a las corridas definidas dentro de un 'case' con metadatos.
    Imprime una sola vez una explicación de variables; en cada llamada
    anuncia el CASO (p.ej., 'Mezcla calorimétrica H2O–Fe ... — 3 corridas'),
    muestra los resultados de cada corrida y un RESUMEN estadístico final.

    Parámetros
    ----------
    case : dict
        Debe incluir las claves:
        - "caso": nombre técnico del caso
        - "s1": nombre de la sustancia 1
        - "s2": nombre de la sustancia 2
        - "datasets": lista de corridas (tuplas) para c_2
    nombre : str, opcional
        Respaldo si 'case["caso"]' no está presente.
    """
    # Encabezado explicativo global (una sola vez)
    if not getattr(analisis, "_header_printed", False):
        print(
            "=== Análisis de mezclas calorimétricas ===\n"
            "Variables y unidades:\n"
            "  - m1 [g]: masa de la sustancia 1 (p.ej., agua)\n"
            "  - m2 [g]: masa de la sustancia 2 (p.ej., metal/hielo)\n"
            "  - T_i1 [°C]: temperatura inicial de la sustancia 1\n"
            "  - T_i2 [°C]: temperatura inicial de la sustancia 2\n"
            "  - T_eq [°C]: temperatura de equilibrio después de mezclar\n"
            "  - c_1 [J/(kg·°C)]: calor específico conocido de la sustancia 1\n\n"
            "Fórmula usada (calorímetro ideal):\n"
            "  c2 = c1 · [ m1 (T_eq − T_i1) ] / [ m2 (T_i2 − T_eq) ], con m en kg.\n"
            "  (Se convierte m1, m2 de g a kg automáticamente.)\n"
        )
        analisis._header_printed = True

    datasets  = case["datasets"]
    case_name = case.get("caso") or nombre or "Caso sin nombre"
    s1 = case.get("s1", "Sustancia 1")
    s2 = case.get("s2", "Sustancia 2")

    print(f"== Caso: {case_name} — {len(datasets)} corridas ==")
    print(f"   (Sustancia 1: {s1}; Sustancia 2: {s2})\n")

    resultados = []
    for i, d in enumerate(datasets, 1):
        etiqueta = f"DATOS_repetición_#{i}"
        c2 = c_2(d, etiqueta=etiqueta)
        print(f"    Resultado: c_2 = {c2:.2f} J/(kg·°C)\n")
        resultados.append(float(c2))

    # --- RESUMEN ESTADÍSTICO sobre 'resultados' ---
    from statistics import mean, stdev
    n = len(resultados)
    mu = mean(resultados) if n else float("nan")
    sd = stdev(resultados) if n > 1 else 0.0
    se = sd / (n**0.5) if n > 1 else 0.0

    print(f"== Resumen {case_name} ==")
    print(f"  numero_de_repeticiones= {n}")
    print(f"  resultados = {resultados}")
    print(f"  promedio(c_2) = {mu:.2f} J/(kg·°C)")
    print(f"  desviacion estándar (σ) = {sd:.2f} J/(kg·°C)")
    print(f"  error estándar = {se:.2f} J/(kg·°C)\n")

    print(f"Fin del calculo del calor latente de la segunda sustancia para el caso: {case_name}\n")
    return resultados


# Ejecutar el análisis de datos
res_fe = analisis(case__H2O_Fe)
res_al = analisis(case__H2O_Al)



