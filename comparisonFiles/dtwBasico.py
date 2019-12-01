import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import correlate
import control as ctrl
from dtw import dtw, warpArea
from matplotlib import pyplot as plt

pointsBig = 400
t1 = np.linspace(0, 10, 350)
t2 = np.linspace(0, 10, pointsBig)

Gs1 = ctrl.tf([1], [1, 1])
Gs2 = ctrl.tf([1], [1.5, 1])

T1, Y1 = ctrl.step_response(Gs1, t1)
T2, Y2 = ctrl.step_response(Gs2, t2)

funcion = interp1d(T1, Y1)
Y1 = funcion(T2)

# comparacion = dtw(Y1, Y2, keep_internals=True)
# print(warpArea(comparacion))

plt.plot(T2, Y1, color="#12711C")
indice = np.argmax(np.abs(Y2 - Y1))
plt.plot([T2[indice]]*2, [Y1[indice], Y2[indice]])
plt.plot(T2, Y2, linestyle='-.')
plt.fill_between(T2, Y1, 0, alpha=0.2, color='r')
plt.fill_between(T2, Y2, 0, alpha=0.2, color='r')
plt.fill_between(T2, Y1, Y2, alpha=0.2, color='r')
plt.show()

print(np.argmax(np.abs(Y2-Y1)))
