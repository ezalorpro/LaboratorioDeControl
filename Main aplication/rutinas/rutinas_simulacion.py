import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
from collections import deque
from functools import partial
import matplotlib.ticker as mticker
import copy
import json


def runge_kutta(self, system, T, u, kp, ki, kd):
    if isinstance(system, ctrl.TransferFunction):
        ss = ctrl.tf2ss(system)
    else:
        ss = system
        
    x = np.zeros_like(ss.B)
    buffer = deque([0]*int(system.delay/0.1))
    h = 0.1
    salida = [0]
    sc_t = [0]
    si_t = [0]
    error_a = 0
    for i, _ in enumerate(T[1:]):
        sc_t, si_t, error_a = PID(salida[i], u[i], h, si_t, error_a, kp, ki, kd)
        buffer.appendleft(sc_t)
        inputValue = buffer.pop()
        
        k1 = h * (ss.A * x + ss.B * inputValue)
        k2 = h * (ss.A * (x+k1/2) + ss.B * inputValue)
        k3 = h * (ss.A * (x+k2/2) + ss.B * inputValue)
        k4 = h * (ss.A * (x+k3) + ss.B * inputValue)
        
        x = x + (1/6)*(k1 + 2*k2 + 2*k3 + k4)
        y = ss.C * x + ss.D * inputValue
        salida.append(np.asscalar(y[0]))
        
    return T, salida


def PID(vm, set_point, ts, s_integral, error_anterior, kp, ki, kd):
    error = set_point - vm
    s_proporcional = error
    s_integral = s_integral + error * ts
    s_derivativa = (error - error_anterior) / ts
    s_control = s_proporcional * kp + s_integral * ki + s_derivativa * kd
    error_anterior = error
    return s_control, s_integral, error_anterior