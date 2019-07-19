import control as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

from rutinas.MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info


def system_creator_tf(self, numerador, denominador):
    system = ctrl.tf(numerador, denominador)
    t, y = ctrl.impulse_response(system)

    if self.main.tfdiscretocheckBox2.isChecked():
        system = ctrl.sample_system(
            system, self.dt, self.main.tfcomboBox2.currentText()
        )

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, 2 * np.max(t), self.dt)
        else:
            T = np.arange(0, 2 * np.max(t), 0.01)
    except ValueError:
        T = np.arange(0, 100, 0.1)

    return system, T


def system_creator_ss(self, A, B, C, D):
    system = ctrl.ss(A, B, C, D)
    t, y = ctrl.impulse_response(system)

    if self.main.ssdiscretocheckBox2.isChecked():
        system = ctrl.sample_system(
            system, self.dt, self.main.sscomboBox2.currentText()
        )

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, 2 * np.max(t), self.dt)
        else:
            T = np.arange(0, 2 * np.max(t), 0.01)
    except ValueError:
        T = np.arange(0, 100, 0.1)

    return system, T


def rutina_step_plot(self, system, T):
    U = np.ones_like(T)
    t, y, _ = ctrl.forced_response(system, T, U)

    self.main.stepGraphicsView2.canvas.axes.clear()
    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.stepGraphicsView2.canvas.axes.step(t, y, where="mid")
    else:
        self.main.stepGraphicsView2.canvas.axes.plot(t, y)

    self.main.stepGraphicsView2.canvas.axes.grid(color="lightgray")
    self.main.stepGraphicsView2.canvas.axes.set_title("Respuesta escalon")
    self.main.stepGraphicsView2.canvas.axes.xaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.2f s")
    )
    self.main.stepGraphicsView2.canvas.axes.set_xlabel("Tiempo")
    self.main.stepGraphicsView2.canvas.axes.set_ylabel("Respuesta")
    self.main.stepGraphicsView2.canvas.draw()
    self.main.stepGraphicsView2.toolbar.update()
    return t, y