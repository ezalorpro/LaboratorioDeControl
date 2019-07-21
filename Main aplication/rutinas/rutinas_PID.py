import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import json

from rutinas.MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info


def system_creator_tf(self, numerador, denominador):
    system = ctrl.tf(numerador, denominador)
    
    if self.main.kpCheckBox2.isChecked():
        kp = self.main.kpHSlider2.value()/50
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value()/50
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value()/50
    else:
        kd = 0
    
    pid = ctrl.tf([kd, kp, ki],[1, 0])
    
    if self.main.tfdelaycheckBox2.isChecked():
        Delay = ctrl.tf(*ctrl.pade(json.loads(self.main.tfdelayEdit2.text()), 2))
    else:
        Delay = 1
    
    system = ctrl.feedback(pid*Delay*system)
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
        kp = self.main.kpHSlider2.value()/50
    else:
        kp = 0
    if self.main.kiCheckBox2.isChecked():
        ki = self.main.kiHSlider2.value()/50
    else:
        ki = 0
    if self.main.kdCheckBox2.isChecked():
        kd = self.main.kdHSlider2.value()/50
    else:
        kd = 0
    
    pid = ctrl.tf([kd, kp, ki],[1, 0])
    
    if self.main.ssdelaycheckBox2.isChecked():
        Delay = ctrl.tf(*ctrl.pade(json.loads(self.main.ssdelayEdit2.text()), 2))
    else:
        Delay = 1
        
    system = ctrl.tf2ss(ctrl.feedback(pid*Delay*system))
    
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


def system_creator_tf_tuning(self, numerador, denominador):
    system_op = ctrl.tf(numerador, denominador)
    t, y = ctrl.impulse_response(system_op)
    
    if self.main.tfdelaycheckBox2.isChecked():
        Delay = ctrl.tf(*ctrl.pade(json.loads(self.main.tfdelayEdit2.text()), 2))
    else:
        Delay = 1
    
    system_op = Delay*system_op
    
    if self.main.tfdiscretocheckBox2.isChecked():
        system_op = ctrl.sample_system(
            system_op, self.dt, self.main.tfcomboBox2.currentText()
        )

    try:
        if ctrl.isdtime(system_op, strict=True):
            T = np.arange(0, 2 * np.max(t), self.dt)
        else:
            T = np.arange(0, 2 * np.max(t), 0.01)
    except ValueError:
        T = np.arange(0, 100, 0.1)
    
    U = np.ones_like(T)
    
    t, y, _ = ctrl.forced_response(system_op, T, U)
    
    i_max = np.argmax(np.abs(np.gradient(y)))

    for index, i in enumerate(y):
        if i >= 0.63:
            indexv = index
            break
   
    slop = (y[i_max] - y[i_max - 1]) / (t[i_max] - t[i_max - 1])
    x1 = (0 - y[i_max]) / (slop) + t[i_max]
    x2 = t[indexv]
    y2 = slop * (x2 - t[i_max]) + y[i_max]
    
    tau = x2 - x1
    alpha = x1
    print(alpha)
    K_proceso = 1/y[-1]

    if alpha != 0:
        kp = ((1 / K_proceso) * (tau / alpha) * ((4 / 3) + (1 / 4) * (alpha / tau)))
        ti = alpha * ((32 + 6 * (alpha / tau)) / (13 + 8 * (alpha / tau)))
        td = alpha * (4 / (11 + 2 * (alpha / tau)))
    else:
        kp = 1/K_proceso
        ti = 100000
        td = 0
    
    kp = kp/2
    ki = kp/ti
    kd = kp*td
    
    system = ctrl.tf(numerador, denominador)
        
    pid = ctrl.tf([kd, kp, ki],[1, 0])
    
    system = ctrl.feedback(pid*Delay*system)
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

    return system, T, kp, ki, kd


def system_creator_ss_tuning(self, A, B, C, D):
    pass


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

def update_gain_labels(self, kp=0, ki=0, kd=0, autotuning=False):
    if autotuning:
        self.main.kpHSlider2.blockSignals(True)
        self.main.kiHSlider2.blockSignals(True)
        self.main.kdHSlider2.blockSignals(True)
        
        self.main.kpHSlider2.setValue(kp*50)
        self.main.kiHSlider2.setValue(ki*50)
        self.main.kdHSlider2.setValue(kd*50)
        
        self.main.kpHSlider2.blockSignals(False)
        self.main.kiHSlider2.blockSignals(False)
        self.main.kdHSlider2.blockSignals(False)
    
    self.main.kpValueLabel2.setText(str(self.main.kpHSlider2.value()/50))
    self.main.kiValueLabel2.setText(str(self.main.kiHSlider2.value()/50))
    self.main.kdValueLabel2.setText(str(self.main.kdHSlider2.value()/50))
    
    

def rutina_system_info(self, system, T, kp=0, ki=0, kd=0, autotuning=False):
    info = ctrl.step_info(system, T)

    Datos = ""
    
    Datos += str(system) + "\n"
    Datos += "----------------------------------------------\n"
    
    for k, v in info.items():
        Datos += f"{k} : {v:5.3f}\n"

    dcgain = ctrl.dcgain(system)
    Datos += f"Ganancia DC: {real(dcgain):5.3f}\n"
    
    if autotuning:
        Datos += f"Kp: {kp}\n"
        Datos += f"Ki: {ki}\n"
        Datos += f"Kd: {kd}\n"

    if self.main.PIDstackedWidget.currentIndex() == 0:
        self.main.tfdatosTextEdit2.setPlainText(Datos)
    else:
        self.main.ssdatosTextEdit2.setPlainText(Datos)