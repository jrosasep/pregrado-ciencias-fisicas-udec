import numpy as np
import matplotlib.pyplot as plt

H = 100  # Altura inicial en metros

Delta_t = 0.01  # Intervalos de tiempo en segundos

g = 9.81 #Aceleración de gravedad terrestre

# Generar el intervalo de tiempo (hasta el instante de impacto t_f + Delta t)
tiempo = np.arange(0, np.sqrt(2 * H / g), Delta_t)

#Cálculo e impresión en pantalla de la velocidad en cada instante Delta t
for i in range( len(tiempo) ):
    velocidad = - g * tiempo[i]
    print(f"t = {tiempo[i]:.2f} s, v(t) = {velocidad:.2f} m/s")

#Gráfico Altura vs Tiempo

#Guardar en la memoria el array de posiciones
posiciones = np.zeros( len(tiempo) )

#Cálculo de la posición en cada instante Delta t
for i in range( len(tiempo) ):
    posiciones[i] = H - 0.5 * g * tiempo[i]**2

#Creación de grafico Altura vs Tiempo
plt.figure(figsize=(8, 6))
plt.plot(tiempo, posiciones, label="Altura (m) vs Tiempo (s)")

#Etiquetas del gráfico
plt.title(f"Caída libre de una pelota desde H = {H} m respecto del suelo")
plt.xlabel("Tiempo (s)")
plt.ylabel("Altura (m)")
plt.grid(True)
plt.legend()

# Flecha para indicar el momento de impacto de la pelota con el suelo
plt.annotate('Momento de impacto', 
             xy=(tiempo[-1], 0), 
             xytext=(tiempo[-1]-1, H*(2/5)),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.show()
