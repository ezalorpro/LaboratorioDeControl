import numpy as np
import control as ctrl
from matplotlib import pyplot as plt

def runge_kutta(ss, x, h, inputValue):
    k1 = h * (ss.A * x + ss.B * inputValue)
    k2 = h * (ss.A * (x + k1/2) + ss.B * inputValue)
    k3 = h * (ss.A * (x + k2/2) + ss.B * inputValue)
    k4 = h * (ss.A * (x + k3) + ss.B * inputValue)

    x = x + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
    y = ss.C * x + ss.D * inputValue
    return y.item(), x

N = 100
kd = 1
kp = 1
ki = 1

pid = ctrl.tf2ss(
    ctrl.TransferFunction([1],
                          [1]))

x_pidB = np.zeros_like(pid.B)
x_pidS = np.zeros_like(pid.B)

sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
vstadosB = np.zeros_like(sistema.B)
vstadosS = np.zeros_like(sistema.B)

min_step = 0.01
max_step = 0.6
h_ant = 0.0001
tol = 1e-6
tiempo = 0
tbound = 30
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0

while tiempo < tbound:
    error = sp - yb
    while True:
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo

        ypidb, x_pidBn = runge_kutta(pid, x_pidB, h_ant, error)
        ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant / 2, error)
        ypids, x_pidSn = runge_kutta(pid, x_pidS, h_ant / 2, error)

        try:
            h_est = h_ant * (tol / abs(ypidb - ypids))**(1 / 5)
        except ZeroDivisionError:
            h_est = h_ant*1.01

        if h_est < h_ant:
            h_ant = h_est
            continue

        if h_est < min_step:
            h_est = min_step
        elif h_est > max_step:
            h_est = max_step
        
        yb, vstadosB = runge_kutta(sistema, vstadosB, h_ant, ypidb)
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


plt.plot(tiempo_out, salida)
plt.show()