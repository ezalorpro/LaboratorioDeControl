import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from collections import deque
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import json

from rutinas.MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info


def system_creator_tf(self, numerador, denominador):
    if not self.main.tfdiscretocheckBox2.isChecked(
    ) and self.main.tfdelaycheckBox2.isChecked():
        delay = json.loads(self.main.tfdelayEdit2.text())
    else:
        delay = 0

    system = ctrl.TransferFunction(numerador, denominador, delay=delay)

    if self.main.kpCheckBox2.isChecked():
        kp = self.main.kpHSlider2.value() / self.tfSliderValue
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value() / self.tfSliderValue
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value() / self.tfSliderValue
    else:
        kd = 0

    t = self.main.pidTiempoSlider.value()

    if self.main.tfdiscretocheckBox2.isChecked():
        pid = ctrl.TransferFunction(
            [kd + self.dt * kp + ki * self.dt**2, -self.dt * kp - 2*kd, kd],
            [self.dt, -self.dt, 0],
            self.dt
        )

        system = ctrl.sample_system(system, self.dt, self.main.tfcomboBox2.currentText())

        if self.main.tfdelaycheckBox2.isChecked():
            delayV = [0] * (int(json.loads(self.main.tfdelayEdit2.text()) / self.dt) + 1)
            delayV[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delayV, self.dt)
            system_delay = ctrl.feedback(pid * system_delay)
        else:
            system_delay = None

        system = ctrl.feedback(pid * system)
    else:
        system_delay = system

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t+self.dt, self.dt)
        else:
            T = np.arange(0, t+0.05, 0.05)

    except ValueError:
        T = np.arange(0, 100, 0.05)

    return system, T, system_delay, kp, ki, kd


def system_creator_ss(self, A, B, C, D):
    if not self.main.ssdiscretocheckBox2.isChecked(
    ) and self.main.ssdelaycheckBox2.isChecked():
        delay = json.loads(self.main.ssdelayEdit2.text())
    else:
        delay = 0

    system = ctrl.StateSpace(A, B, C, D, delay=delay)

    if self.main.kpCheckBox2.isChecked():
        kp = self.main.kpHSlider2.value() / self.ssSliderValue
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value() / self.ssSliderValue
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value() / self.ssSliderValue
    else:
        kd = 0

    t = self.main.pidTiempoSlider.value()

    if self.main.ssdiscretocheckBox2.isChecked():
        pid = ctrl.TransferFunction(
            [kd + self.dt * kp + ki * self.dt**2, -self.dt * kp - 2*kd, kd],
            [self.dt, -self.dt, 0],
            self.dt
        )

        system = ctrl.sample_system(system, self.dt, self.main.sscomboBox2.currentText())

        system_ss = system
        system = ctrl.ss2tf(system)

        if self.main.ssdelaycheckBox2.isChecked():
            delayV = [0] * (int(json.loads(self.main.ssdelayEdit2.text()) / self.dt) + 1)
            delayV[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delayV, self.dt)
            system_delay = ctrl.feedback(pid * system_delay)
        else:
            system_delay = None

        system = ctrl.feedback(pid * system)
    else:
        system_ss = system
        system = ctrl.ss2tf(system)
        system_delay = None

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t+self.dt, self.dt)
        else:
            T = np.arange(0, t+0.05, 0.05)

    except ValueError:
        T = np.arange(0, 100, 0.05)

    return system, T, system_delay, system_ss, kp, ki, kd


def system_creator_tf_tuning(self, numerador, denominador):
    if not self.main.tfdiscretocheckBox2.isChecked(
    ) and self.main.tfdelaycheckBox2.isChecked():
        delay = json.loads(self.main.tfdelayEdit2.text())
    else:
        delay = 0

    system = ctrl.TransferFunction(numerador, denominador, delay=delay)

    t = self.main.pidTiempoSlider.value()
    T = np.arange(0, t, 0.05)
    U = np.ones_like(T)

    t_temp, y, _ = ctrl.forced_response(system, T, U)
    dc_gain = ctrl.dcgain(system)

    K_proceso, tau, alpha = model_method(self, t_temp, y, self.main.tfAutoTuningcomboBox2.currentText(), dc_gain)

    try:
        kp, ki, kd = auto_tuning_method(self, K_proceso, tau, alpha, self.main.tfAutoTuningcomboBox2.currentText())
    except TypeError:
        raise TypeError('Alfa es muy pequeño')

    if self.main.tfdiscretocheckBox2.isChecked():
        pid = ctrl.TransferFunction(
            [kd + self.dt * kp + ki * self.dt**2, -self.dt * kp - 2*kd, kd],
            [self.dt, -self.dt, 0],
            self.dt
        )

        system = ctrl.sample_system(system, self.dt, self.main.tfcomboBox2.currentText())

        if self.main.tfdelaycheckBox2.isChecked():
            delayV = [0] * (int(json.loads(self.main.tfdelayEdit2.text()) / self.dt) + 1)
            delayV[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delayV, self.dt)
            system_delay = ctrl.feedback(pid * system_delay)
        else:
            system_delay = None

        system = ctrl.feedback(pid * system)
    else:
        system_delay = system

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t+self.dt, self.dt)
        else:
            T = np.arange(0, t+0.05, 0.05)

    except ValueError:
        T = np.arange(0, 100, 0.05)

    return system, T, system_delay, kp, ki, kd


def system_creator_ss_tuning(self, A, B, C, D):
    if not self.main.ssdiscretocheckBox2.isChecked(
    ) and self.main.ssdelaycheckBox2.isChecked():
        delay = json.loads(self.main.ssdelayEdit2.text())
    else:
        delay = 0

    system = ctrl.StateSpace(A, B, C, D, delay=delay)

    t = self.main.pidTiempoSlider.value()
    T = np.arange(0, t, 0.05)
    U = np.ones_like(T)

    t_temp, y, _ = ctrl.forced_response(system, T, U)
    dc_gain = ctrl.dcgain(system)

    K_proceso, tau, alpha = model_method(self, t_temp, y, self.main.ssAutoTuningcomboBox2.currentText(), dc_gain)

    try:
        kp, ki, kd = auto_tuning_method(self, K_proceso, tau, alpha, self.main.ssAutoTuningcomboBox2.currentText())
    except TypeError:
        raise TypeError('Alfa es muy pequeño')

    if self.main.ssdiscretocheckBox2.isChecked():
        pid = ctrl.TransferFunction(
            [kd + self.dt * kp + ki * self.dt**2, -self.dt * kp - 2*kd, kd],
            [self.dt, -self.dt, 0],
            self.dt
        )

        system = ctrl.sample_system(system, self.dt, self.main.sscomboBox2.currentText())

        if self.main.ssdelaycheckBox2.isChecked():
            delayV = [0] * (int(json.loads(self.main.ssdelayEdit2.text()) / self.dt) + 1)
            delayV[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delayV, self.dt)
            system_delay = ctrl.feedback(pid * system_delay)
        else:
            system_delay = None

        system_ss = system
        system = ctrl.feedback(pid * system)
    else:
        system_ss = system
        system_delay = system

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, t+self.dt, self.dt)
        else:
            T = np.arange(0, t+0.05, 0.05)

    except ValueError:
        T = np.arange(0, 100, 0.05)

    return system, T, system_delay, system_ss, kp, ki, kd


def model_method(self, t, y, metodo, dc_gain):
    if '1er orden' in metodo:
        i_max = np.argmax(np.abs(np.gradient(y)))

        for index, i in enumerate(y):
            if i >= 0.63 * dc_gain:
                indexv = index
                break

        slop = (y[i_max] - y[i_max - 1]) / (t[i_max] - t[i_max - 1])
        x1 = (0 - y[i_max]) / (slop) + t[i_max]
        x2 = t[indexv]
        y2 = slop * (x2 - t[i_max]) + y[i_max]

        tau = x2 - x1

        if self.main.tfdelaycheckBox2.isChecked():
            alpha = x1 + json.loads(self.main.tfdelayEdit2.text())
        else:
            alpha = x1

        K_proceso = y[-1] / 1

        return K_proceso, tau, alpha


def auto_tuning_method(self, k_proceso, tau, alpha, metodo):

    if alpha <= 0.05:
        print('Alfa es demasiado pequeño')
        raise TypeError(' Alfa es demasiado pequeño')

    if 'ZN' in metodo:
        if 'P--' in metodo:
            kp = (1/k_proceso) * (tau/alpha)
            ti = np.infty
            td = 0

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(False)
            self.main.kdCheckBox2.setChecked(False)

        if 'PI-' in metodo:
            kp = (0.9/k_proceso) * (tau/alpha)
            ti = alpha * 3.33
            td = 0

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(True)
            self.main.kdCheckBox2.setChecked(False)

        if 'PID' in metodo:
            kp = (1.2/k_proceso) * (tau/alpha)
            ti = alpha * 2
            td = alpha * 0.5

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(True)
            self.main.kdCheckBox2.setChecked(True)

        kp = kp
        ki = kp / ti
        kd = kp * td

    if 'CC' in metodo:
        if 'P--' in metodo:
            kp = (1/k_proceso) * (tau/alpha) * (1 + (1/3) * (alpha/tau))
            ti = np.infty
            td = 0

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(False)
            self.main.kdCheckBox2.setChecked(False)

        if 'PI-' in metodo:
            kp = (1/k_proceso) * (tau/alpha) * (0.9 + (1/12) * (alpha/tau))
            ti = alpha * ((30 + 3 * (alpha/tau)) / (9 + 20 * (alpha/tau)))
            td = 0

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(True)
            self.main.kdCheckBox2.setChecked(False)

        if 'PD-' in metodo:
            kp = ((1/k_proceso) * (tau/alpha) * ((5/4) + (1/6) * (alpha/tau)))
            ti = np.infty
            td = alpha * ((6 - 2 * (alpha/tau)) / (22 + 3 * (alpha/tau)))

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(False)
            self.main.kdCheckBox2.setChecked(True)

        if 'PID' in metodo:
            kp = ((1/k_proceso) * (tau/alpha) * ((4/3) + (1/4) * (alpha/tau)))
            ti = alpha * ((32 + 6 * (alpha/tau)) / (13 + 8 * (alpha/tau)))
            td = alpha * (4 / (11 + 2 * (alpha/tau)))

            self.main.kpCheckBox2.setChecked(True)
            self.main.kiCheckBox2.setChecked(True)
            self.main.kdCheckBox2.setChecked(True)

        kp = kp / 2
        ki = kp / ti
        kd = kp * td

    return kp, ki, kd


def rutina_step_plot(self, system, T, kp, ki, kd):
    U = np.ones_like(T)

    if ctrl.isdtime(system, strict=True):
        t, y, _ = ctrl.forced_response(system, T, U)
    elif (
        self.main.tfdelaycheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 0
    ):
        pade = ctrl.TransferFunction(
            *ctrl.pade(json.loads(self.main.tfdelayEdit2.text()), 10)
        )
        N = self.main.pidNSlider.value()
        pid = ctrl.TransferFunction([N*kd+kp, N*kp+ki, N*ki], [1, N, 0])
        system = ctrl.feedback(pid * system * pade)
        t, y, _ = ctrl.forced_response(system, T, U)
    elif (
        self.main.ssdelaycheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 1
    ):
        pade = ctrl.TransferFunction(
            *ctrl.pade(json.loads(self.main.ssdelayEdit2.text()), 10)
        )
        N = self.main.pidNSlider.value()
        pid = ctrl.TransferFunction([N*kd+kp, N*kp+ki, N*ki], [1, N, 0])
        system = ctrl.feedback(pid * system * pade)
        t, y, _ = ctrl.forced_response(system, T, U)
    else:
        N = self.main.pidNSlider.value()
        pid = ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0])
        system = ctrl.feedback(pid * system)
        t, y, _ = ctrl.forced_response(system, T, U)

    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.stepGraphicsView2.curva.setData(t, y[:-1], stepMode=True)
    else:
        self.main.stepGraphicsView2.curva.setData(t, y, stepMode=False)

    return t, y


def runge_kutta(self, system, T, u, kp, ki, kd):
    if isinstance(system, ctrl.TransferFunction):
        ss = ctrl.tf2ss(system)
    else:
        ss = system

    x = np.zeros_like(ss.B)
    buffer = deque([0] * int(system.delay / 0.05))
    h = 0.05
    salida = [0]
    sc_t = [0]
    si_t = [0]
    error_a = 0
    for i, _ in enumerate(T[1:]):
        sc_t, si_t, error_a = PID(salida[i], u[i], h, si_t, error_a, kp, ki, kd)
        buffer.appendleft(sc_t)
        inputValue = buffer.pop()

        k1 = h * (ss.A * x + ss.B * inputValue)
        k2 = h * (ss.A * (x + k1/2) + ss.B * inputValue)
        k3 = h * (ss.A * (x + k2/2) + ss.B * inputValue)
        k4 = h * (ss.A * (x+k3) + ss.B * inputValue)

        x = x + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
        y = ss.C * x + ss.D * inputValue
        salida.append(np.asscalar(y[0]))

    return T, salida


def PID(vm, set_point, ts, s_integral, error_anterior, kp, ki, kd):
    error = set_point - vm
    s_proporcional = error
    s_integral = s_integral + error*ts
    s_derivativa = (error-error_anterior) / ts
    s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
    error_anterior = error
    return s_control, s_integral, error_anterior


def update_gain_labels(self, kp=0, ki=0, kd=0, autotuning=False, resolution=50):
    if autotuning:
        self.main.kpHSlider2.blockSignals(True)
        self.main.kiHSlider2.blockSignals(True)
        self.main.kdHSlider2.blockSignals(True)

        self.main.kpHSlider2.setValue(kp * resolution)
        self.main.kiHSlider2.setValue(ki * resolution)
        self.main.kdHSlider2.setValue(kd * resolution)

        self.main.kpHSlider2.blockSignals(False)
        self.main.kiHSlider2.blockSignals(False)
        self.main.kdHSlider2.blockSignals(False)

    self.main.kpValueLabel2.setText(str(np.around(self.main.kpHSlider2.value() / resolution, 3)))
    self.main.kiValueLabel2.setText(str(np.around(self.main.kiHSlider2.value() / resolution, 3)))
    self.main.kdValueLabel2.setText(str(np.around(self.main.kdHSlider2.value() / resolution, 3)))


def update_time_and_N_labels(self):
    self.main.pidTiempoLabelValue.setText(str(np.around(self.main.pidTiempoSlider.value(), 3)))
    self.main.pidNLabelValue.setText(str(np.around(self.main.pidNSlider.value(), 3)))


def rutina_system_info(self, system, T, t, y, kp=0, ki=0, kd=0, autotuning=False):
    info = ctrl.step_info(system, T=T, yout=y)

    Datos = ""

    Datos += str(system) + "\n"

    if self.main.tfdelaycheckBox2.isChecked() and self.main.PIDstackedWidget.currentIndex(
    ) == 0:
        delay = json.loads(self.main.tfdelayEdit2.text())
        Datos += f"Delay: {delay}\n"
    elif self.main.ssdelaycheckBox2.isChecked(
    ) and self.main.PIDstackedWidget.currentIndex() == 1:
        delay = json.loads(self.main.ssdelayEdit2.text())
        Datos += f"Delay: {delay}\n"
    else:
        delay = 0

    Datos += "----------------------------------------------\n"

    for k, v in info.items():
        Datos += f"{k} : {v:5.3f}\n"

    dcgain = ctrl.dcgain(system)
    Datos += f"Ganancia DC: {real(dcgain):5.3f}\n"

    if autotuning:
        Datos += "----------------------------------------------\n"
        Datos += f"Kp: {kp}\n"
        Datos += f"Ki: {ki}\n"
        Datos += f"Kd: {kd}\n"

    if self.main.PIDstackedWidget.currentIndex() == 0:
        self.main.tfdatosTextEdit2.setPlainText(Datos)
    else:
        self.main.ssdatosTextEdit2.setPlainText(Datos)