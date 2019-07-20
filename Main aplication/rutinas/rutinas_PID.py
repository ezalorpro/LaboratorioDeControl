import control as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker

from rutinas.MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info


def system_creator_tf(self, numerador, denominador):
    system = ctrl.tf(numerador, denominador)
    
    if self.main.kpCheckBox2.isChecked():
        kp = self.main.kpHSlider2.value()/20
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value()/20
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value()/50
    else:
        kd = 0
    
    pid = ctrl.tf([kd, kp, ki],[1, 0])
    
    system = ctrl.feedback(pid*system)
    
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
    
    if self.main.kpCheckBox2.isChecked():
        kp = self.main.kpHSlider2.value()/20
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value()/20
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value()/50
    else:
        kd = 0
    
    pid = ctrl.tf([kd, kp, ki],[1, 0])
    
    system = ctrl.tf2ss(ctrl.feedback(pid*system))
    
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

def update_gain_labels(self):
    self.main.kpValueLabel2.setText(str(self.main.kpHSlider2.value()/20))
    self.main.kiValueLabel2.setText(str(self.main.kiHSlider2.value()/20))
    self.main.kdValueLabel2.setText(str(self.main.kdHSlider2.value()/50))
    

def rutina_system_info(self, system, T):
    info = ctrl.step_info(system, T)

    Datos = ""
    
    Datos += str(system) + "\n"
    Datos += "----------------------------------------------\n"
    
    for k, v in info.items():
        Datos += f"{k} : {v:5.3f}\n"

    dcgain = ctrl.dcgain(system)
    Datos += f"Ganancia DC: {real(dcgain):5.3f}\n"

    if self.main.PIDstackedWidget.currentIndex() == 0:
        self.main.tfdatosTextEdit2.setPlainText(Datos)
    else:
        self.main.ssdatosTextEdit2.setPlainText(Datos)