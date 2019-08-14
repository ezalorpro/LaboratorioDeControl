from PySide2 import QtCore, QtGui, QtWidgets
import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
from collections import deque
import matplotlib.ticker as mticker
import time
import copy
import json


class SimpleThread(QtCore.QThread):
    finished = QtCore.Signal(object, list)
    update_progresBar = QtCore.Signal(object, float)

    def __init__(self, window, regresar, update_bar, list_info, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.window = window
        self.window.main.principalTab.setDisabled(True)
        self.window.main.progressBar.show()
        time.sleep(0.1)
        self.finished.connect(regresar)
        self.update_progresBar.connect(update_bar)
        self.list_info = copy.deepcopy(list_info)

        self.esquema = self.list_info[0]
        self.system = self.list_info[1]
        self.Tiempo = self.list_info[2]
        self.dt = self.list_info[3]
        self.escalon = self.list_info[4]
        self.sensor_flag = self.list_info[5]
        self.accionador_flag = self.list_info[6]
        self.saturador_flag = self.list_info[7]
        self.kp, self.ki, self.kd = map(float, self.list_info[8])
        self.fuzzy_path = self.list_info[9]


    def run(self):
        if self.esquema in [0, 1, 2, 3]:
            y, sc, u = self.run_pid()
            self.finished.emit(
                self.window,
                [self.Tiempo, y, sc, u, ctrl.isdtime(self.system, strict=True)])
            return

    def run_pid(self):
        if self.window.main.kpCheck.isChecked():
            kp = float(self.kp)
        else:
            kp = 0

        if self.window.main.kiCheck.isChecked():
            ki = float(self.ki)
        else:
            ki = 0

        if self.window.main.kdCheck.isChecked():
            kd = float(self.kd)
        else:
            kd = 0

        if isinstance(self.system, ctrl.TransferFunction):
            self.system = ctrl.tf2ss(self.system)

        if isinstance(self.escalon, float):
            u = np.ones_like(self.Tiempo)
            u = u*self.escalon
        else:
            it = iter(self.escalon)
            u = np.zeros_like(self.Tiempo)
            for i, valor in enumerate(it):
                ini = int(next(it) / self.dt)
                u[ini:] = valor

        max_tiempo = len(self.Tiempo)
        ten_percent = max_tiempo*10/100
        x = np.zeros_like(self.system.B)
        buffer = deque([0] * int(self.system.delay / self.dt))
        h = self.dt

        salida = deque([0])
        sc_f = deque([0])
        sc_t = 0
        si_t = 0
        error_a = 0

        if ctrl.isdtime(self.system, strict=True):
            solve = self.ss_discreta
        else:
            solve = self.runge_kutta

        for i, _ in enumerate(self.Tiempo[1:]):
            sc_t, si_t, error_a = self.PID(salida[i], u[i], h, si_t, error_a, kp, ki, kd)
            buffer.appendleft(sc_t)
            y, x = solve(self.system, x, h, buffer.pop())
            sc_f.append(sc_t)
            salida.append(np.asscalar(y[0]))
            if i % ten_percent == 0:
                self.update_progresBar.emit(self.window, i * 100 / max_tiempo)

        return copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(u)

    def runge_kutta(self, ss, x, h, inputValue):
        k1 = h * (ss.A * x + ss.B * inputValue)
        k2 = h * (ss.A * (x + k1/2) + ss.B * inputValue)
        k3 = h * (ss.A * (x + k2/2) + ss.B * inputValue)
        k4 = h * (ss.A * (x+k3) + ss.B * inputValue)

        x = x + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
        y = ss.C * x + ss.D * inputValue
        return y, x

    def ss_discreta(self, ss, x, _, inputValue):
        x = ss.A * x + ss.B * inputValue
        y = ss.C * x + ss.D * inputValue
        return y, x

    def PID(self, vm, set_point, ts, s_integral, error_anterior, kp, ki, kd):
        error = set_point - vm
        s_proporcional = error
        s_integral = s_integral + error*ts
        s_derivativa = (error-error_anterior) / ts
        s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
        error_anterior = error
        return s_control, s_integral, error_anterior


def system_creator_tf(self, numerador, denominador):
    if self.main.tfdelaycheckBox4.isChecked():
        delay = json.loads(self.main.tfdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.TransferFunction(numerador, denominador, delay=delay)

    if self.main.tfdiscretocheckBox4.isChecked():
        system = ctrl.sample_system(system,
                                    self.dt,
                                    self.main.tfcomboBox4.currentText(),
                                    delay=delay)
    else:
        fs = int(self.main.samplesSimulacion.text())

    t = float(self.main.tiempoSimulacion.text())

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t, self.dt)
        else:
            T = np.arange(0, t, 1 / fs)
    except ValueError:
        T = np.arange(0, 100, 0.01)

    return system, T


def system_creator_ss(self, A, B, C, D):
    if self.main.ssdelaycheckBox4.isChecked():
        delay = json.loads(self.main.ssdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.StateSpace(A, B, C, D, delay=delay)
    t, y = ctrl.impulse_response(system)

    if self.main.ssdiscretocheckBox4.isChecked():
        system = ctrl.sample_system(system,
                                    self.dt,
                                    self.main.sscomboBox4.currentText(),
                                    delay=delay)
    else:
        fs = int(self.main.samplesSimulacion.text())

    t = float(self.main.tiempoSimulacion.text())

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t, self.dt)
        else:
            T = np.arange(0, t, 1 / fs)
    except ValueError:
        T = np.arange(0, 100, 0.01)

    return system, T
