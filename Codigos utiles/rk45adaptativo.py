import numpy as np
import control as ctrl
from matplotlib import pyplot as plt
from scipy.integrate import RK45

def runge_kutta_45_DP(ss, x, h, inputValue):
    k1 = h*(ss.A * x + ss.B * inputValue)
    k2 = h*(ss.A * (x + k1/5) + ss.B * inputValue)
    k3 = h*(ss.A * (x + k1*3/40 + k2*9/40) + ss.B * inputValue)
    k4 = h*(ss.A * (x + k1*44/45 + k2 * (-56 / 15) + k3*32/39) + ss.B * inputValue)
    k5 = h*(ss.A * (x + k1*19372/6561 + k2 * (-25360 / 2187)) + k3*64448/6561 + k4 * (-212 / 729) + ss.B * inputValue)
    k6 = h*(ss.A * (x + k1*9017/3168 + k2 * (-355 / 33) + k3*46732/5247 + k4*49/176 + k5 * (-5103 / 18656)) + ss.B * inputValue )
    k7 = h*(ss.A * (x + k1*35/384 + k2*0 + k3*500/1113 + k4*125/192 + k5 * (-2187 / 6784) + k6*11/84) + ss.B * inputValue)

    x5th = x + (k1*35/384 + k2*0 + k3*500/1113 + k4*125/192 + k5*(-2187 / 6784) + k6*11/84 + k7*0)

    x4th = x + (k1*5179/57600 + k2*0 + k3*7571/16695 + k4*393/640 + k5*(-92097 / 339200) + k6*187/2100 + k7*1/40)

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y5th.item(), y4th.item(), x5th, x4th


def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size**0.5


N = 100
kp = 1
ki = 1
kd = 1

pid = ctrl.tf2ss(ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

x_pidB = np.zeros_like(pid.B)
x_pidS = np.zeros_like(pid.B)

sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
vstadosB = np.zeros_like(sistema.B)
vstadosS = np.zeros_like(sistema.B)

min_step_decrease = 0.2
max_step_increase = 5
h_ant = 0.000001
rtol = 1e-3
atol = 1e-6
tiempo = 0
tbound = 30
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0
sf1 = 0.9
sf2 = 4

while tiempo < tbound:
    error = sp - yb
    while True:
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo

        ypidb, y4th, x_five, x_four = runge_kutta_45_DP(pid, x_pidB, h_ant, error)

        scale = atol + np.maximum(np.abs(x_pidB), np.abs(x_five)) * rtol
        delta1 = np.abs(x_five - x_four)
        error_norm = norm(delta1 / scale)

        if error_norm == 0:
            h_est = h_ant*max_step_increase
        elif error_norm < 1:
            h_est = h_ant * min(max_step_increase,
                               max(1, sf1 * error_norm**(-1 / (4+1))))
        else:
            h_ant = h_ant * max(min_step_decrease, sf1 * error_norm**(-1 / (4+1)))
            continue

        # h_est = sf1 * h_ant * (1 / error_ratio)**(1 / 5)

        # if error_ratio >= 1:
        #     h_ant = h_est
        #     continue

        # if h_est > sf2 * h_ant:
        #     h_est = sf2 * h_ant
        # elif h_est < h_ant / sf2:
        #     h_est = h_ant / sf2
        # else:
        #     h_est = h_ant

        # if abs(h_ant - h_est) > max_step_increase:
        #     h_est = h_ant + max_step_increase

        # if h_est < min_step:
        #     h_est = min_step

        yb, __, vstadosB, _ = runge_kutta_45_DP(sistema, vstadosB, h_ant, ypidb)
        break
    print(tiempo)
    salida.append(yb)
    tiempo += h_ant
    tiempo_out.append(tiempo)
    h_ant = h_est
    x_pidB = x_five

print(len(tiempo_out))
plt.plot(tiempo_out, salida)
plt.show()