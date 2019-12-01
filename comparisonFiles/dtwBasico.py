import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import correlate
from scipy.stats import energy_distance
from scipy.integrate import cumtrapz
import control as ctrl
from dtw import dtw, warpArea
from matplotlib import pyplot as plt

pointsBig = 800
t1 = np.linspace(0, 20, 350)
t2 = np.linspace(0, 20, pointsBig)

Gs1 = ctrl.tf([1], [1, 1])
Gs2 = ctrl.tf([1], [1.1, 1])

T1, Y1 = ctrl.step_response(Gs1, t1)
T2, Y2 = ctrl.step_response(Gs2, t2)

funcion = interp1d(T1, Y1)
Y1 = funcion(T2)

# comparacion = dtw(Y1, Y2, keep_internals=True)
# print(warpArea(comparacion))

indice = np.argmax(np.abs(Y2 - Y1))

plt.plot(T2, Y1, color="#001C7F", label='MATLAB')
plt.plot([T2[indice]]*2, [Y1[indice], Y2[indice]], color='k', linewidth='3', label='Diferencia maxima')
plt.plot(T2, Y2, 'r', linestyle='-.', label='Laboratorio Virtual')
plt.fill_between(T2, Y1, Y2, alpha=0.4, color="#001C7F", label='Area de diferencia')

plt.xlabel('tiempo')
plt.title('Respuesta escalon para el Set 1')
plt.legend()
plt.grid()
plt.show()

print(f'{"Error absoluto: ":<38}{np.abs(Y2[indice]-Y1[indice]):.4f}')
print(f'{"Error porcentual maximo: ":<38}{np.abs(Y2[indice]-Y1[indice])*100/Y2[indice]:.4f} %')
print(f'{"Distancia de energia: ":<38}{energy_distance(Y1, Y2):.4f}')
print(f'{"Diferencia de areas: ":<38}{np.abs(cumtrapz(Y1, T2)[-1] - cumtrapz(Y2, T2)[-1]):.4f}')
print(f'{"Raiz del Error cuadratico medio: ":<38}{np.sqrt((np.subtract(Y1, Y2)**2).mean()):.4f}')
print(f'{"Distancia euclidiana: ":<38}{np.linalg.norm(Y1-Y2):.4f}')
