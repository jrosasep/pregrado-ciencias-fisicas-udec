import numpy as np
import matplotlib.pyplot as plt
from EcuacionesDiferencialesOrdinarias import SaltoRana

# Definir la aceleración para el problema normalizado de Kepler
def a_kepler_normalizado(r, t):
    norm_r3 = np.linalg.norm(r) ** 3
    return -r / norm_r3

# Función para calcular parámetros orbitales
def calcular_parametros_orbitales(r):
    # Calcular distancias radiales
    distancias = np.linalg.norm(r, axis=1)
    r_max = np.max(distancias)  # Distancia máxima
    r_min = np.min(distancias)  # Distancia mínima

    # Semieje mayor (a) y excentricidad (e)
    a = (r_max + r_min) / 2
    e = (r_max - r_min) / (r_max + r_min)

    # Semieje menor (b)
    b = a * np.sqrt(1 - e**2)

    return a, b, e

# Verificar áreas barridas (Segunda Ley de Kepler)
def calcular_areas_barridas(r, v, dt):
    # Convertir vectores 2D a 3D agregando una dimensión z=0
    r_3d = np.hstack((r, np.zeros((r.shape[0], 1))))
    v_3d = np.hstack((v, np.zeros((v.shape[0], 1))))
    return 0.5 * np.linalg.norm(np.cross(r_3d, v_3d), axis=1) * dt

# Parámetros iniciales
v0_tildes = [0.5, 1.0, 1.5]
t_max = 20
dt = 0.01
t = np.arange(0, t_max, dt)

# Constante para verificar T^2/a^3
kepler_constantes = []

for v0_tilde in v0_tildes:
    r0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, v0_tilde])
    r, v = SaltoRana(a_kepler_normalizado, r0, v0, t)

    energia = 0.5 * np.sum(v**2, axis=1) - 1.0 / np.linalg.norm(r, axis=1)
    # Convertir r y v a 3D para calcular el momento angular
    r_3d = np.hstack((r, np.zeros((r.shape[0], 1))))
    v_3d = np.hstack((v, np.zeros((v.shape[0], 1))))
    momento_angular = np.linalg.norm(np.cross(r_3d, v_3d), axis=1)

    if v0_tilde < 1:  # Verificar leyes de Kepler solo para trayectorias cerradas
        a, b, e = calcular_parametros_orbitales(r)

        # Primera Ley: Verificar ajuste elíptico
        x = r[:, 0]
        y = r[:, 1]
        eliptico = np.allclose((x**2 / a**2) + (y**2 / b**2), 1, atol=0.05)

        # Segunda Ley: Calcular áreas barridas
        areas = calcular_areas_barridas(r, v, dt)
        areas_constante = np.allclose(areas, np.mean(areas), atol=0.05)

        # Tercera Ley: Relación T^2 / a^3
        T = t[np.argmax(r[:, 0] < 0)]  # Tiempo para completar una órbita
        kepler_constantes.append(T**2 / a**3)

        print(f"v0~ = {v0_tilde}:")
        print(f"  Semieje mayor (a): {a:.4f}")
        print(f"  Semieje menor (b): {b:.4f}")
        print(f"  Excentricidad (e): {e:.4f}")
        print(f"  Cumple Primera Ley (Elíptico): {eliptico}")
        print(f"  Cumple Segunda Ley (Áreas): {areas_constante}")
        print(f"  Periodo orbital (T): {T:.4f}")
        print(f"  Relación T^2/a^3: {T**2 / a**3:.4f}\n")

# Verificar Tercera Ley para todas las trayectorias cerradas
if len(kepler_constantes) > 1:
    kepler_promedio = np.mean(kepler_constantes)
    print(f"Tercera Ley: Constante promedio T^2/a^3 ≈ {kepler_promedio:.4f}")

# Graficar trayectorias, energía y momento angular
for v0_tilde in v0_tildes:
    r0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, v0_tilde])
    r, v = SaltoRana(a_kepler_normalizado, r0, v0, t)

    energia = 0.5 * np.sum(v**2, axis=1) - 1.0 / np.linalg.norm(r, axis=1)
    r_3d = np.hstack((r, np.zeros((r.shape[0], 1))))
    v_3d = np.hstack((v, np.zeros((v.shape[0], 1))))
    momento_angular = np.linalg.norm(np.cross(r_3d, v_3d), axis=1)

    plt.figure(1)
    plt.plot(r[:, 0], r[:, 1], label=f"v0~={v0_tilde}")

    plt.figure(2)
    plt.plot(t, energia, label=f"v0~={v0_tilde}")

    plt.figure(3)
    plt.plot(t, momento_angular, label=f"v0~={v0_tilde}")

# Personalizar gráficos
plt.figure(1)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trayectoria del cometa (normalizada)")
plt.legend()
plt.axis('equal')

plt.figure(2)
plt.xlabel("Tiempo")
plt.ylabel("Energía total (normalizada)")
plt.title("Conservación de la energía")
plt.legend()

plt.figure(3)
plt.xlabel("Tiempo")
plt.ylabel("Momento angular (normalizado)")
plt.title("Conservación del momento angular")
plt.legend()

plt.show()
