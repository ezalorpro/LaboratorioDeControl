import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from matplotlib import pyplot as plt
from collections import deque
import matplotlib.ticker as mticker
import json

from rutinas.MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info


def system_creator_tf(self, numerador, denominador):
    if not self.main.tfdiscretocheckBox1.isChecked() and self.main.tfdelaycheckBox1.isChecked():
        delay = json.loads(self.main.tfdelayEdit1.text())
    else:
        delay = 0
        
    system = ctrl.TransferFunction(numerador, denominador, delay=delay)
    t, y = ctrl.impulse_response(system)

    if self.main.tfdiscretocheckBox1.isChecked():
        
        system = ctrl.sample_system(
            system, self.dt, self.main.tfcomboBox1.currentText()
        )
        
        if self.main.tfdelaycheckBox1.isChecked():
            delay = [0]*(int(json.loads(self.main.tfdelayEdit1.text())/self.dt) + 1)
            delay[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delay, self.dt)
        else:
            system_delay = None
    else:
        system_delay = system
    
    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, 2 * np.max(t), self.dt)
        else:
            T = np.arange(0, 2 * np.max(t), 0.01)
    except ValueError:
        T = np.arange(0, 100, 0.1)

    return system, T, system_delay


def system_creator_ss(self, A, B, C, D):
    if not self.main.ssdiscretocheckBox1.isChecked() and self.main.ssdelaycheckBox1.isChecked():
        delay = json.loads(self.main.ssdelayEdit1.text())
    else:
        delay = 0
        
    system = ctrl.StateSpace(A, B, C, D, delay=delay)
    t, y = ctrl.impulse_response(system)

    if self.main.ssdiscretocheckBox1.isChecked():
        system = ctrl.sample_system(
            system, self.dt, self.main.sscomboBox1.currentText()
        )
        
        system_ss = system
        system = ctrl.ss2tf(system)
        
        if self.main.ssdelaycheckBox1.isChecked():
            delay = [0]*(int(json.loads(self.main.ssdelayEdit1.text())/self.dt) + 1)
            delay[0] = 1
            system_delay = system * ctrl.TransferFunction([1], delay, self.dt)
        else:
            system_delay = None
    else:
        system_ss = system
        system = ctrl.ss2tf(system)
        system_delay = None

    try:
        if ctrl.isdtime(system, strict=True):
            T = np.arange(0, 2 * np.max(t), self.dt)
        else:
            T = np.arange(0, 2 * np.max(t), 0.01)
    except ValueError:
        T = np.arange(0, 100, 0.1)
        
    return system, T, system_delay, system_ss


def rutina_step_plot(self, system, T):
    U = np.ones_like(T)
    
    if not system.delay or ctrl.isdtime(system, strict=True):
        t, y, _ = ctrl.forced_response(system, T, U)
    else:
        t, y = runge_kutta(self, system, T, U)
    
    self.main.stepGraphicsView1.canvas.axes.clear()
    
    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.stepGraphicsView1.canvas.axes.step(t, y, where="mid")
    else:
        self.main.stepGraphicsView1.canvas.axes.plot(t, y)

    self.main.stepGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.stepGraphicsView1.canvas.axes.set_title("Respuesta escalon")
    self.main.stepGraphicsView1.canvas.axes.xaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.2f s")
    )
    self.main.stepGraphicsView1.canvas.axes.set_xlabel("Tiempo")
    self.main.stepGraphicsView1.canvas.axes.set_ylabel("Respuesta")
    self.main.stepGraphicsView1.canvas.draw()
    self.main.stepGraphicsView1.toolbar.update()
    return t, y


def runge_kutta(self, system, T, u):
    ss = ctrl.tf2ss(system)
    x = np.zeros_like(ss.B)
    buffer = deque([0]*int(system.delay/0.01))
    h = 0.01
    salida = []
    for i, _ in enumerate(T):
        buffer.appendleft(u[i])
        inputValue = buffer.pop()
        k1 = h * (ss.A * x + ss.B * inputValue)
        k2 = h * (ss.A * (x+k1/2) + ss.B * inputValue)
        k3 = h * (ss.A * (x+k2/2) + ss.B * inputValue)
        k4 = h * (ss.A * (x+k3) + ss.B * inputValue)
        
        x = x + (1/6)*(k1 + 2*k2 + 2*k3 + k4)
        y = ss.C * x + ss.D * inputValue
        salida.append(np.asscalar(y[0]))
        
    return T, salida

def rutina_impulse_plot(self, system, T):

    U = np.zeros_like(T)
    U[0] = 1
    
    if not system.delay or ctrl.isdtime(system, strict=True):
        t, y, _ = ctrl.forced_response(system, T, U)
    else:
        t, y = runge_kutta(self, system, T, U)

    self.main.impulseGraphicsView1.canvas.axes.clear()

    if ctrl.isdtime(system, strict=True):
        y = y[0]
        self.main.impulseGraphicsView1.canvas.axes.step(t, y, where="mid")
    else:
        self.main.impulseGraphicsView1.canvas.axes.plot(t, y)

    self.main.impulseGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.impulseGraphicsView1.canvas.axes.set_title("Respuesta impulso")
    self.main.impulseGraphicsView1.canvas.axes.xaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.2f s")
    )
    self.main.impulseGraphicsView1.canvas.axes.set_xlabel("Tiempo")
    self.main.impulseGraphicsView1.canvas.axes.set_ylabel("Respuesta")
    self.main.impulseGraphicsView1.canvas.draw()
    self.main.impulseGraphicsView1.toolbar.update()
    return t, y


def rutina_bode_plot(self, system):

    if ctrl.isdtime(system, strict=True):
        w = np.linspace(0, 100 * np.pi, 10000)
        mag, phase, omega = ctrl.bode(system, w)
    else:
        w = np.linspace(0, 100 * np.pi, 5000)
        mag, phase, omega = ctrl.bode(system, w)

    self.main.BodeGraphicsView1.canvas.axes1.clear()
    self.main.BodeGraphicsView1.canvas.axes1.semilogx(omega, 20 * np.log10(mag))
    self.main.BodeGraphicsView1.canvas.axes1.grid(True, which="both", color="lightgray")
    self.main.BodeGraphicsView1.canvas.axes1.set_title("Magnitud")
    self.main.BodeGraphicsView1.canvas.axes1.yaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.0f dB")
    )

    self.main.BodeGraphicsView1.canvas.axes2.clear()
    self.main.BodeGraphicsView1.canvas.axes2.semilogx(omega, phase * 180.0 / np.pi)
    self.main.BodeGraphicsView1.canvas.axes2.grid(True, which="both", color="lightgray")
    self.main.BodeGraphicsView1.canvas.axes2.set_title("Fase")
    self.main.BodeGraphicsView1.canvas.axes2.yaxis.set_major_formatter(
        mticker.FormatStrFormatter("%.0f °")
    )
    self.main.BodeGraphicsView1.canvas.axes2.set_xlabel("rad/s")

    self.main.BodeGraphicsView1.canvas.draw()
    self.main.BodeGraphicsView1.toolbar.update()
    return mag, phase, omega


def rutina_nyquist_plot(self, system):

    if ctrl.isdtime(system, strict=True):
        w = np.linspace(-np.pi, 10 * np.pi, 5000)
        real, imag, freq = ctrl.nyquist_plot(system, w)
    else:
        w = np.logspace(-np.pi, 2 * np.pi, 5000)
        real, imag, freq = ctrl.nyquist_plot(system, w)

    self.main.NyquistGraphicsView1.canvas.axes.cla()
    self.main.NyquistGraphicsView1.canvas.axes.plot([-1], [0], "r+")

    self.main.NyquistGraphicsView1.canvas.axes.arrow(
        real[0],
        imag[0],
        (real[1] - real[0]) / 2,
        (imag[1] - imag[0]) / 2,
        width=np.max(np.abs(real)) / 70,
    )

    self.main.NyquistGraphicsView1.canvas.axes.arrow(
        real[-1],
        imag[-1],
        (real[-1] - real[-2]) / 2,
        (imag[-1] - imag[-2]) / 2,
        width=np.max(np.abs(real)) / 70,
    )

    mindex = int(len(real) / 2)

    self.main.NyquistGraphicsView1.canvas.axes.arrow(
        real[mindex],
        imag[mindex],
        (real[mindex + 1] - real[mindex]) / 2,
        (imag[mindex + 1] - imag[mindex]) / 2,
        width=np.max(np.abs(real)) / 70,
    )

    self.main.NyquistGraphicsView1.canvas.axes.arrow(
        real[-mindex],
        -imag[-mindex],
        (real[-mindex] - real[-mindex + 1]) / 2,
        (imag[-mindex + 1] - imag[-mindex]) / 2,
        width=np.max(np.abs(real)) / 70,
    )

    self.main.NyquistGraphicsView1.canvas.axes.plot(real, imag, "tab:blue")
    self.main.NyquistGraphicsView1.canvas.axes.plot(real, -imag, "tab:blue")
    self.main.NyquistGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.NyquistGraphicsView1.canvas.axes.set_title("Diagrama de Nyquist")
    self.main.NyquistGraphicsView1.canvas.draw()
    self.main.NyquistGraphicsView1.toolbar.update()

    return real, imag, freq


def rutina_root_locus_plot(self, system):
    t, y = ctrl.root_locus(system)

    zeros = ctrl.zero(system)
    polos = ctrl.pole(system)

    self.main.rlocusGraphicsView1.canvas.axes.cla()
    self.main.rlocusGraphicsView1.canvas.axes.plot(real(t), imag(t), "b")
    self.main.rlocusGraphicsView1.canvas.axes.plot(
        [0, 0], [np.amin(imag(t)), np.amax(imag(t))], "g"
    )
    self.main.rlocusGraphicsView1.canvas.axes.scatter(
        real(polos), imag(polos), marker="x"
    )
    self.main.rlocusGraphicsView1.canvas.axes.scatter(
        real(zeros), imag(zeros), marker="o"
    )

    self.main.rlocusGraphicsView1.canvas.axes.grid(color="lightgray")
    self.main.rlocusGraphicsView1.canvas.axes.set_title("Lugar de las raicez")
    self.main.rlocusGraphicsView1.canvas.draw()
    self.main.rlocusGraphicsView1.toolbar.update()


def rutina_system_info(self, system, T, mag, phase, omega):
    info = ctrl.step_info(system, T)

    Datos = ""
    
    Datos += str(system) + "\n"
    Datos += "----------------------------------------------\n"
    
    if self.main.tfdelaycheckBox1.isChecked() and self.main.AnalisisstackedWidget.currentIndex() == 0:
        delay = json.loads(self.main.tfdelayEdit1.text())
    elif self.main.ssdelaycheckBox1.isChecked() and self.main.AnalisisstackedWidget.currentIndex() == 1:
        delay = json.loads(self.main.ssdelayEdit1.text())
    else:
        delay = 0
    
    for k, v in info.items():
        if 'PeakTime' in k or 'SettlingTime' in k:
            Datos += f"{k} : {v+delay:5.3f}\n"
        else:
            Datos += f"{k} : {v:5.3f}\n"
                
    Datos += "----------------------------------------------\n"
    dcgain = ctrl.dcgain(system)
    Datos += f"Ganancia DC: {real(dcgain):5.3f}\n"

    gm, pm, wg, wp = ctrl.margin(system)

    Datos += f"Margen de ganancia: {20 * np.log10(gm):5.3f}\n"
    Datos += f"Frecuencia de ganancia: {wg:5.3f}\n"
    Datos += f"Margen de fase: {pm:5.3f}\n"
    Datos += f"Frecuencia de fase: {wp:5.3f}\n"

    Datos += "----------------------------------------------\n"
    Datos += f"  {'Valores eigen':<18}  {'Damping':<16}  Wn\n"
    wn, damping, eigen = ctrl.damp(system, doprint=False)
    for wni, dampingi, eigeni in zip(wn, damping, eigen):

        if imag(eigeni) >= 0:
            Datos += f"{real(eigeni):5.3f} {imag(eigeni):+5.3f}j {dampingi:11.3f} {wni:15.3f} \n"
        else:
            Datos += f"{real(eigeni):5.3f} {imag(eigeni):7.3f}j {dampingi:11.3f} {wni:15.3f} \n"

    if self.main.AnalisisstackedWidget.currentIndex() == 0:
        self.main.tfdatosTextEdit1.setPlainText(Datos)
    else:
        self.main.ssdatosTextEdit1.setPlainText(Datos)
