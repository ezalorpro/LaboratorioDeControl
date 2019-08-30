import numpy as np
import control as ctrl
from matplotlib import pyplot as plt
from scipy.integrate import RK45
import time

C = np.array([1/5, 3/10, 4/5, 8/9, 1])
A = [np.array([1/5]),
        np.array([3/40, 9/40]),
        np.array([44/45, -56/15, 32/9]),
        np.array([19372/6561, -25360/2187, 64448/6561, -212/729]),
        np.array([9017/3168, -355/33, 46732/5247, 49/176, -5103/18656])]
B = np.array([35/384, 0, 500/1113, 125/192, -2187/6784, 11/84])
E = np.array([-71/57600, 0, 71/16695, -71/1920, 17253/339200, -22/525,
                1/40])
# Corresponds to the optimum value of c_6 from [2]_.
P = np.array([
    [1, -8048581381/2820520608, 8663915743/2820520608,
        -12715105075/11282082432],
    [0, 0, 0, 0],
    [0, 131558114200/32700410799, -68118460800/10900136933,
        87487479700/32700410799],
    [0, -1754552775/470086768, 14199869525/1410260304,
        -10690763975/1880347072],
    [0, 127303824393/49829197408, -318862633887/49829197408,
        701980252875 / 199316789632],
    [0, -282668133/205662961, 2019193451/616988883, -1453857185/822651844],
    [0, 40617522/29380423, -110615467/29380423, 69997945/29380423]])

def state_space(x, ssA, ssB, inputValue):
    return ssA*x + ssB*inputValue


def rk_scipy(fun, t, y, f, h, A, B, C, E, K):
    K[0] = f
    for s, (a, c) in enumerate(zip(A, C)):
        dy = np.dot(K[:s + 1].T, a) * h
        K[s + 1] = fun(y + dy, ss.A, ss.B, inputValue)

    y_new = y + h * np.dot(K[:-1].T, B)
    f_new = fun(y_new)

    K[-1] = f_new
    error = np.dot(K.T, E) * h

    return y_new, f_new, error


def runge_kutta_45_DP(ss, x, h, inputValue):
    k1 = h*(ss.A * x + ss.B * inputValue)
    k2 = h*(ss.A * (x + k1/5) + ss.B * (inputValue + h/5))
    k3 = h * (ss.A * (x + k1*3/40 + k2*9/40) + ss.B * (inputValue + h*3/10))
    k4 = h*(ss.A * (x + k1*44/45 + k2 * (-56 / 15) + k3*32/39) + ss.B * (inputValue + h*4/5))
    k5 = h * (ss.A * (x + k1*19372/6561 + k2 * (-25360 / 2187) + k3*64448/6561 + k4 *
                      (-212 / 729)) + ss.B * (inputValue + h*8/9))
    k6 = h * (ss.A *
              (x + k1*9017/3168 + k2 * (-355 / 33) + k3*46732/5247 + k4*49/176 + k5 *
               (-5103 / 18656)) + ss.B * (inputValue + h))
    k7 = h * (ss.A * (x + k1*35/384 + k2*0 + k3*500/1113 + k4*125/192 + k5 *
                      (-2187 / 6784) + k6*11/84) + ss.B * (inputValue + h))

    x5th = x + (k1*35/384 + k2*0 + k3*500/1113 + k4*125/192 + k5*(-2187 / 6784) + k6*11/84 + k7*0)

    x4th = x + (k1*5179/57600 + k2*0 + k3*7571/16695 + k4*393/640 + k5*(-92097 / 339200) + k6*187/2100 + k7*1/40)

    y5th = ss.C * x5th + ss.D * inputValue
    y4th = ss.C * x4th + ss.D * inputValue
    return y5th.item(), y4th.item(), x5th, x4th


# def runge_kutta_45_DP(ss, x, h, inputValue):
#     k1 = h * (ss.A * x + ss.B * inputValue)
#     k2 = h * (ss.A * (x + k1/2) + ss.B * inputValue)
#     k3 = h * (ss.A * (x + k1/256 + k2*255/256) + ss.B * inputValue)
#     # k4 = h * (ss.A * (x + k1*44/45 + k2 * (-56 / 15) + k3*32/39) + ss.B * inputValue)
#     # k5 = h * (ss.A * (x + k1*19372/6561 + k2 * (-25360 / 2187) + k3*64448/6561 + k4 *
#     #                   (-212 / 729)) + ss.B * inputValue)
#     # k6 = h * (ss.A *
#     #           (x + k1*9017/3168 + k2 * (-355 / 33) + k3*46732/5247 + k4*49/176 + k5 *
#     #            (-5103 / 18656)) + ss.B * inputValue)
#     # k7 = h * (ss.A * (x + k1*35/384 + k2*0 + k3*500/1113 + k4*125/192 + k5 *
#     #                   (-2187 / 6784) + k6*11/84) + ss.B * inputValue)

#     x5th = x + (k1/256 + k2*255/256)

#     x4th = x + (k1/512 + k2*255/256 + k3/512)

#     y5th = ss.C * x5th + ss.D * inputValue
#     y4th = ss.C * x4th + ss.D * inputValue
#     return y5th.item(), y4th.item(), x5th, x4th


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

min_step_decrease = 0.5
max_step_increase = 20
h_ant = 0.0000001
rtol = 1e-7
atol = 1e-7
tiempo = 0
tbound = 15
sp = 1
salida = [0]
tiempo_out = [0]
yb = 0
sf1 = 0.9
sf2 = 4
counter = 0
start = time.time()
while tiempo < tbound:
    counter += 1
    error = sp - yb
    while True:
        if tiempo + h_ant >= tbound:
            h_ant = tbound - tiempo

        ypidb, y4th, x_five, x_four = runge_kutta_45_DP(pid, x_pidB, h_ant, error)

        scale = atol + np.maximum(np.abs(x_four), np.abs(x_five)) * rtol
        delta1 = np.abs(x_five - x_four)
        error_norm = norm(delta1 / scale)

        if error_norm == 0:
            h_est = h_ant*max_step_increase
        elif error_norm < 1:
            h_est = h_ant * min(max_step_increase,
                               max(1, sf1 * error_norm**(-1 / (4))))
        else:
            h_ant = h_ant * max(min_step_decrease, sf1 * error_norm**(-1 / (4)))
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

print(counter)
print(len(tiempo_out))
print(f'{time.time() - start}')
plt.plot(tiempo_out, salida)
plt.show()