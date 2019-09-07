import numpy as np
import control as ctrl
from matplotlib import pyplot as plt
from scipy.integrate import RK45
import time


def dopri5(ss, x, h, inputValue):
    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 5))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 40) + np.dot(k2, 9 / 40))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 44 / 45) + np.dot(k2, -56 / 15) + np.dot(k3, 32 / 9))) +
         np.dot(ss.B, inputValue)))
    k5 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 19372 / 6561) + np.dot(k2, -25360 / 2187) +
                         np.dot(k3, 64448 / 6561) + np.dot(k4, -212 / 729))) +
                 np.dot(ss.B, inputValue)))
    k6 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 9017 / 3168) + np.dot(k2, -355 / 33) +
                         np.dot(k3, 46732 / 5247) + np.dot(k4, 49 / 176) +
                         np.dot(k5, -5103 / 18656))) + np.dot(ss.B, inputValue)))
    k7 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 35 / 384) + np.dot(k3, 500 / 1113) + np.dot(
                    k4, 125 / 192) + np.dot(k5, -2187 / 6784) + np.dot(k6, 11 / 84))) +
         np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 35 / 384) + np.dot(k3, 500 / 1113) + np.dot(k4, 125 / 192) +
                np.dot(k5, -2187 / 6784) + np.dot(k6, 11 / 84))

    x4th = x + (np.dot(k1, 5179 / 57600) + np.dot(k3, 7571 / 16695) +
                np.dot(k4, 393 / 640) + np.dot(k5, -92097 / 339200) +
                np.dot(k6, 187 / 2100) + np.dot(k7, 1 / 40))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y5th.item(), y4th.item(), x5th, x4th


def fehlberg45(ss, x, h, inputValue):
    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 4))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 32) + np.dot(k2, 9 / 32))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 1932 / 2197) + np.dot(k2, -7200 / 2197) +
                         np.dot(k3, 7296 / 2197))) + np.dot(ss.B, inputValue)))
    k5 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, 439 / 216) + np.dot(k2, -8) + np.dot(k3, 3680 / 513) +
                 np.dot(k4, -845 / 4104))) + np.dot(ss.B, inputValue)))
    k6 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, -8 / 27) + np.dot(k2, 2) + np.dot(k3, -3544 / 2565) +
                 np.dot(k4, 1859 / 4104) + np.dot(k5, -11 / 40))) +
         np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 16 / 135) + np.dot(k3, 6656 / 12825) +
                np.dot(k4, 28561 / 56430) + np.dot(k5, -9 / 50) + np.dot(k6, 2 / 55))

    x4th = x + (np.dot(k1, 25 / 216) + np.dot(k3, 1408 / 2565) + np.dot(k4, 2197 / 4104) +
                np.dot(k5, -1 / 5))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y4th.item(), y5th.item(), x4th, x5th


def bogacki_shampine23(ss, x, h, inputValue):
    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k2, 3 / 4))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 2/9) + np.dot(k2, 1/3) +
                         np.dot(k3, 4/9))) + np.dot(ss.B, inputValue)))

    x3th = x + (np.dot(k1, 2 / 9) + np.dot(k2, 1 / 3) + np.dot(k3, 4 / 9))

    x2th = x + (np.dot(k1, 7/24) + np.dot(k2, 1/4) + np.dot(k3, 1/3) +
                np.dot(k4, 1/8))

    y3th = ss.C * x3th + ss.D * inputValue
    y2th = ss.C * x2th + ss.D * inputValue
    return y2th.item(), y3th.item(), x2th, x3th

def cash_karp(ss, x, h, inputValue):
    k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
    k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 5))) + np.dot(ss.B, inputValue)))
    k3 = np.dot(h,
                (np.dot(ss.A, (x + np.dot(k1, 3 / 40) + np.dot(k2, 9 / 40))) +
                 np.dot(ss.B, inputValue)))
    k4 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 3/10) + np.dot(k2, -9/10) +
                         np.dot(k3, 6/5))) + np.dot(ss.B, inputValue)))
    k5 = np.dot(
        h,
        (np.dot(ss.A,
                (x + np.dot(k1, -11/54) + np.dot(k2, 5/2) + np.dot(k3, -70/27) +
                 np.dot(k4, 35/27))) + np.dot(ss.B, inputValue)))
    k6 = np.dot(h,
                (np.dot(ss.A,
                        (x + np.dot(k1, 1631 / 55296) + np.dot(k2, 175 / 512) +
                         np.dot(k3, 575 / 13824) + np.dot(k4, 44275 / 110592) +
                         np.dot(k5, 253 / 4096))) + np.dot(ss.B, inputValue)))

    x5th = x + (np.dot(k1, 37 / 378) + np.dot(k3, 250 / 621) + np.dot(k4, 125 / 594) + np.dot(k6, 512 / 1771))

    x4th = x + (np.dot(k1, 2825 / 27648) + np.dot(k3, 18575 / 48384) +
                np.dot(k4, 13525 / 55296) + np.dot(k5, 277 / 14336) + np.dot(k6, 1 / 4))

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y4th.item(), y5th.item(), x4th, x5th


def norm(x):
    """Compute RMS norm."""
    return np.linalg.norm(x) / x.size**0.5


N = 100
kp = 1
ki = 1
kd = 1

pid = ctrl.tf2ss(
    ctrl.TransferFunction([1], [0.1, 1]) *
    ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

x_pidB = np.zeros_like(pid.B)
x_pidS = np.zeros_like(pid.B)

sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
vstadosB = np.zeros_like(sistema.B)
vstadosS = np.zeros_like(sistema.B)

min_step_decrease = 0.2
max_step_increase = 5
h_ant = 0.0001
rtol = 1e-3
atol = 5e-6
tiempo = 0
tbound = 30
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0
sf1 = 0.95
sf2 = 4
counter = 0
start = time.time()
# dopri5
# fehlberg45dot
RK = fehlberg45

while tiempo < tbound:
    counter += 1
    error = sp - yb
    while True:
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo

        ypidb, y4th, x_five, x_four = RK(pid, x_pidB, h_ant, error)

        scale = atol + np.maximum(np.abs(x_pidB), np.abs(x_five)) * rtol
        delta1 = np.abs(x_five - x_four)
        error_norm = norm(delta1 / scale)

        if error_norm == 0:
            h_est = h_ant * max_step_increase
        elif error_norm < 1:
            h_est = h_ant * min(max_step_increase, max(1, sf1 * error_norm**(-1 / (4+1))))
        else:
            h_ant = h_ant * min(1, max(min_step_decrease, sf1 * error_norm**(-1 / (4+1))))
            continue

        yb, __, vstadosB, _ = RK(sistema, vstadosB, h_ant, ypidb)
        break

    print(tiempo)
    salida.append(yb)
    tiempo += h_ant
    tiempo_out.append(tiempo)
    h_ant = h_est
    x_pidB = x_five

print(counter)
print(len(tiempo_out))
print(f'{time.time() - start}')
plt.plot(tiempo_out, salida)
plt.grid()
plt.show()