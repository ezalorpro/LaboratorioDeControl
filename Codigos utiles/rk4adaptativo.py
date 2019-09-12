import numpy as np
import control as ctrl
from matplotlib import pyplot as plt
import time
from math import factorial

def ejecutar():

    def norm(x):
        """Compute RMS norm."""
        return np.linalg.norm(x) / x.size**0.5

    def tres_octavos4(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 3))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h,
                    (np.dot(ss.A,
                            (x + np.dot(k1, -1 / 3) + k2)) + np.dot(ss.B, inputValue)))
        k4 = np.dot(h, (np.dot(ss.A, (x + k1 - k2 + k3)) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 1 / 8) + np.dot(k2, 3 / 8) + np.dot(k3, 3 / 8) +
                 np.dot(k4, 1 / 8))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def runge_kutta2(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))

        x = x + k2
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def runge_kutta3(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h, (np.dot(ss.A,
                               (x - k1 + np.dot(k2, 2))) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 2 / 3) + np.dot(k3, 1 / 6))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def runge_kutta4(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 2))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 1 / 2))) + np.dot(ss.B, inputValue)))
        k4 = np.dot(h, (np.dot(ss.A, (x + k3)) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 1 / 3) + np.dot(k3, 1 / 3) +
                 np.dot(k4, 1 / 6))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def runge_kutta5(ss, x, h, inputValue):  # Mejor: rtol = 1e-3, atol = 5e-6
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 4))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h,
                    (np.dot(ss.A, (x + np.dot(k1, 1 / 8) + np.dot(k2, 1 / 8))) +
                     np.dot(ss.B, inputValue)))
        k4 = np.dot(h,
                    (np.dot(ss.A,
                            (x + np.dot(k2, -1 / 2) + k3)) + np.dot(ss.B, inputValue)))
        k5 = np.dot(h,
                    (np.dot(ss.A, (x + np.dot(k1, -3 / 16) + np.dot(k4, 9 / 16))) +
                     np.dot(ss.B, inputValue)))
        k6 = np.dot(
            h,
            (np.dot(ss.A,
                    (x + np.dot(k1, -3 / 7) + np.dot(k2, 2 / 7) + np.dot(k3, 12 / 7) +
                     np.dot(k4, -12 / 7) + np.dot(k5, 8 / 7))) +
             np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 7 / 90) + np.dot(k3, 32 / 90) + np.dot(k4, 12 / 90) +
                 np.dot(k5, 32 / 90) + np.dot(k6, 7 / 90))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def heun3(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1 / 3))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 2 / 3))) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 1 / 4) + np.dot(k3, 3 / 4))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def ralston4(ss, x, h, inputValue):  # Mejor: rtol = 1e-5, atol = 5e-6
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 0.4))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h,
                    (np.dot(ss.A, (x + np.dot(k1, 0.29697761) + np.dot(k2, 0.15875964))) +
                     np.dot(ss.B, inputValue)))
        k4 = np.dot(h,
                    (np.dot(ss.A,
                            (x + np.dot(k1, 0.21810040) + np.dot(k2, -3.05096516) +
                             np.dot(k3, 3.83286476))) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 0.17476028) + np.dot(k2, -0.55148066) +
                 np.dot(k3, 1.20553560) + np.dot(k4, 0.17118478))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def ralston3(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1/2))) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k2, 3/4))) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 2 / 9) + np.dot(k2, 1 / 3) + np.dot(k3, 4 / 9))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    def SSPRK3(ss, x, h, inputValue):
        k1 = np.dot(h, (np.dot(ss.A, x) + np.dot(ss.B, inputValue)))
        k2 = np.dot(h, (np.dot(ss.A, (x + k1)) + np.dot(ss.B, inputValue)))
        k3 = np.dot(h, (np.dot(ss.A, (x + np.dot(k1, 1/4) + np.dot(k2, 1/4))) + np.dot(ss.B, inputValue)))

        x = x + (np.dot(k1, 1 / 6) + np.dot(k2, 1 / 6) + np.dot(k3, 2 / 3))
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y.item(), x

    N = 100
    kp = 20
    ki = 20
    kd = 20

    pid = ctrl.tf2ss(ctrl.TransferFunction([1], [10/(N*kd), 1])*
        ctrl.TransferFunction([N * kd + kp, N * kp + ki, N * ki],
                            [1, N, 0]))

    x_pidB = np.zeros_like(pid.B)
    x_pidS = np.zeros_like(pid.B)

    sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
    vstadosB = np.zeros_like(sistema.B)

    min_step_decrease = 0.1
    max_step_increase = 10
    h_ant = 0.000001
    rtol = 1e-3
    atol = 5e-6
    tiempo = 0
    tbound = 30
    sp = 1
    salida = [0]
    tiempo_out = [0]
    yb = 0
    sf1 = 0.95
    sf2 = 5
    sc_t = [0]
    start = time.time()
    counter = 0

    RK = runge_kutta5

    while tiempo < tbound:
        error = sp - yb
        while True:
            counter +=1
            if tiempo + h_ant >= tbound:
                h_ant = tbound - tiempo
                ypids, x_pidSn = RK(pid, x_pidS, h_ant, error)
            else:
                ypidb, x_pidBn = RK(pid, x_pidB, h_ant, error)
                ypids, x_pidSn = RK(pid, x_pidS, h_ant / 2, error)
                ypids, x_pidSn = RK(pid, x_pidSn, h_ant / 2, error)

                scale = atol + rtol * (np.abs(x_pidSn) + np.abs(x_pidBn)) / 2
                delta1 = np.abs(x_pidBn - x_pidSn)
                error_norm = norm(delta1 / scale)

                if error_norm == 0:
                    h_est = h_ant * max_step_increase
                elif error_norm < 1:
                    h_est = h_ant * min(max_step_increase, max(1, sf1 * error_norm**(-1 / (5+1))))
                else:
                    h_ant = h_ant * min(1, max(min_step_decrease, sf1 * error_norm**(-1 / (5+1))))
                    continue

            print(tiempo)
            sc_t.append(ypids)
            yb, vstadosB = RK(sistema, vstadosB, h_ant, ypids)
            break

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

if __name__ == "__main__":
    ejecutar()