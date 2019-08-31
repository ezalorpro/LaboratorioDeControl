import numpy as np
import control as ctrl
from matplotlib import pyplot as plt
import time
from math import factorial

def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size**0.5


def runge_kutta(ss, x, h, inputValue):
    k1 = h * (ss.A * x + ss.B * inputValue)
    k2 = h * (ss.A * (x + k1/2) + ss.B * (inputValue))
    k3 = h * (ss.A * (x + k2/2) + ss.B * (inputValue))
    k4 = h * (ss.A * (x+k3) + ss.B * (inputValue))

    x = x + (1/6)*(k1 + k2*2 + k3*2 + k4)
    y = ss.C * x + ss.D * inputValue
    return y.item(), x

N = 100
kp = 1
ki = 1
kd = 1

pid = ctrl.tf2ss(ctrl.TransferFunction([1], [0.1, 1])*
    ctrl.TransferFunction([N * kd + kp, N * kp + ki, N * ki],
                          [1, N, 0]))

x_pidB = np.zeros_like(pid.B)
x_pidS = np.zeros_like(pid.B)

sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
vstadosB = np.zeros_like(sistema.B)

min_step_decrease = 0.2
max_step_increase = 5
h_ant = 0.0001
rtol = 1e-3
atol = 1e-6
tiempo = 0
tbound = 30
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0
sf1 = 0.9
sf2 = 5
sc_t = [0]
start = time.time()
counter = 0

while tiempo < tbound:
    error = sp - yb
    while True:
        counter +=1
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo
            ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant, error)
        else:
            ypidb, x_pidBn = runge_kutta(pid, x_pidB, h_ant, error)
            ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant / 2, error)
            ypids, x_pidSn = runge_kutta(pid, x_pidSn, h_ant / 2, error)

            # scale = atol + np.maximum(np.abs(x_pidBn), np.abs(x_pidB)) * rtol
            scale = atol + rtol * (np.abs(x_pidSn) + np.abs(x_pidBn)) / 2 
            delta1 = np.abs(x_pidBn - x_pidSn)
            error_norm = norm(delta1 / scale)

            if error_norm == 0:
                h_est = h_ant * max_step_increase
            elif error_norm < 1:
                h_est = h_ant * min(max_step_increase, max(1, sf1 * error_norm**(-1 / (4+1))))
            else:
                h_ant = h_ant * max(min_step_decrease, sf1 * error_norm**(-1 / (4+1)))
                continue

            # scale = rtol * (np.abs(x_pidSn) + np.abs(x_pidBn))/2
            # delta1 = np.abs(x_pidBn - x_pidSn)
            # error_ratio = np.max(delta1 / (scale+atol))

            # h_est = sf1 * h_ant * (1 / error_ratio)**(1 / 5)

            # delta1 = np.max(np.abs(x_pidBn - x_pidSn)/h_ant)

            # if delta1 > rtol:
            #     h_ant =  h_ant * (rtol / (2*delta1))**(1 / 5)
            #     continue
            # else:
            #     h_est = h_ant * (rtol / (2*delta1))**(1 / 5)

            # if error_ratio >= 1:
            #     h_ant = h_est
            #     continue

            # if h_est > sf2 * h_ant:
            #     h_est = sf2 * h_est
            # elif h_est < h_ant / sf2:
            #     h_est = h_est / sf2
            # else:
            #     h_est = h_est

            # if h_est > max_step:
            #     h_est = max_step
            # elif h_est < min_step:
            #     h_est = min_step
        print(tiempo)
        # print(tiempo)
        sc_t.append(ypids)
        yb, vstadosB = runge_kutta(sistema, vstadosB, h_ant, ypids)
        break

        # ypids, vstadosSn = runge_kutta(pid, x_pidS, h_ant / 2, sp)
        # ypids, vstadosSn = runge_kutta(pid, x_pidS, h_ant / 2, sp)
        # h_est = h_ant * (tol / abs(yb - ys))**(1 / 5)

        # if h_est < h_ant:
        #     h_ant = h_est
        # else:
        #     break

    salida.append(yb)
    tiempo += h_ant
    tiempo_out.append(tiempo)

    h_ant = h_est
    x_pidB = x_pidSn
    x_pidS = x_pidSn
    input_a1 = error
    input_a2 = ypids

print(counter)
print(len(tiempo_out))
print(f'{time.time() - start}')
plt.plot(tiempo_out, salida)
plt.grid()
plt.show()

plt.plot(tiempo_out, sc_t)
plt.grid()
plt.show()