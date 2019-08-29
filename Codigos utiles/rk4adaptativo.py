import numpy as np
import control as ctrl
from matplotlib import pyplot as plt

def runge_kutta(ss, x, h, inputValue):
    k1 = h*(ss.A * x + ss.B * inputValue)
    k2 = h*(ss.A * (x + k1/2) + ss.B * inputValue)
    k3 = h*(ss.A * (x + k2/2) + ss.B * inputValue)
    k4 = h*(ss.A * (x + k3) + ss.B * inputValue)

    x = x + (1/6)*(k1 + k2*2 + k3*2 + k4)
    y = ss.C * x + ss.D * inputValue
    return y.item(), x


N = 100
kp = 1
ki = 1
kd = 1

pid = ctrl.tf2ss(
    ctrl.TransferFunction([N * kd + kp, N * kp + ki, N * ki],
                          [1, N, 0]))

x_pidB = np.zeros_like(pid.B)
x_pidS = np.zeros_like(pid.B)

sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1]))
vstadosB = np.zeros_like(sistema.B)
vstadosS = np.zeros_like(sistema.B)

min_step = 0.01
max_step = 0.5
h_ant = 0.0002
rtol = 2e-3
atol = 1e-6
tiempo = 0
tbound = 30
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0
sf1 = 0.92
sf2 = 4

while tiempo < tbound:
    error = sp - yb
    while True:
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo

        ypidb, x_pidBn = runge_kutta(pid, x_pidB, h_ant, error)
        ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant / 2, error)
        ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant / 2, error)

        scale = rtol * (np.abs(x_pidBn) + np.abs(x_pidSn)) / 2
        delta1 = np.abs(x_pidBn - x_pidSn)
        error_ratio = np.max(delta1 / (scale+atol))

        h_est = sf1 * h_ant * (1 / error_ratio)**(1 / 5)

        if h_est > sf2 * h_ant:
            h_est = sf2 * h_ant
            if error_ratio < 1:
                h_ant = h_est
                continue
        elif h_est < h_ant / sf2:
            h_est = h_ant / sf2
            if error_ratio < 1:
                h_ant = h_est
                continue

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
    x_pidB = x_pidBn
    x_pidS = x_pidBn

print(len(tiempo_out))
plt.plot(tiempo_out, salida)
plt.show()