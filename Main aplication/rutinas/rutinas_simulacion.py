from PySide2 import QtCore, QtGui, QtWidgets
import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
from collections import deque
from functools import partial
import matplotlib.ticker as mticker
import time
import copy
import json


class SimpleThread(QtCore.QThread):
    finished = QtCore.Signal(object, str)
    update_progresBar = QtCore.Signal(object, float)

    def __init__(self, window, regresar, update_bar, list_info, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.window = window
        self.finished.connect(regresar)
        self.update_progresBar.connect(update_bar)

    def run(self):
        for i in range(100):
            self.update_progresBar.emit(self.window, i * 100 / 100)
            time.sleep(0.5)
        self.finished.emit(self.window, 'hola')

    def run_pid(self):
        if isinstance(system, ctrl.TransferFunction):
            ss = ctrl.tf2ss(system)
        else:
            ss = system

        x = np.zeros_like(ss.B)
        buffer = deque([0] * int(system.delay / 0.1))
        h = 0.1
        salida = [0]
        sc_t = [0]
        si_t = [0]
        error_a = 0
        for i, _ in enumerate(T[1:]):
            sc_t, si_t, error_a = PID(salida[i], u[i], h, si_t, error_a, kp, ki, kd)
            buffer.appendleft(sc_t)
            inputValue = buffer.pop()
            y, x = runge_kutta(system, x, h, inputValue)
            salida.append(np.asscalar(y[0]))

    def runge_kutta(self, ss, x, h, inputValue):
        k1 = h * (ss.A * x + ss.B * inputValue)
        k2 = h * (ss.A * (x + k1/2) + ss.B * inputValue)
        k3 = h * (ss.A * (x + k2/2) + ss.B * inputValue)
        k4 = h * (ss.A * (x+k3) + ss.B * inputValue)

        x = x + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
        y = ss.C * x + ss.D * inputValue
        return y, x


    def PID(vm, set_point, ts, s_integral, error_anterior, kp, ki, kd):
        error = set_point - vm
        s_proporcional = error
        s_integral = s_integral + error*ts
        s_derivativa = (error-error_anterior) / ts
        s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
        error_anterior = error
        return s_control, s_integral, error_anterior
