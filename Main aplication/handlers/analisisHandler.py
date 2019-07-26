from rutinas.rutinas_analisis import *
import json


def AnalisisHandler(self):

    self.main.tfcalcButton1.clicked.connect(lambda: calcular_analisis(self))
    self.main.sscalcButton1.clicked.connect(lambda: calcular_analisis(self))

    self.main.tfdiscretocheckBox1.stateChanged.connect(lambda: analisis_bool_discreto(self))

    self.main.tfradioButton1.toggled.connect(lambda: analisis_stacked_to_tf(self))
    self.main.ssradioButton1.toggled.connect(lambda: analisis_stacked_to_ss(self))


def calcular_analisis(self):
    system_ss = 0
    if (self.main.tfdiscretocheckBox1.isChecked()
        and self.main.AnalisisstackedWidget.currentIndex() == 0):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit1.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (self.main.ssdiscretocheckBox1.isChecked() 
          and self.main.AnalisisstackedWidget.currentIndex() == 1):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit1.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    else:
        self.dt = None

    if self.main.AnalisisstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit1.text())
        dem = json.loads(self.main.tfdemEdit1.text())
        system, T, system_delay = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit1.text())
        B = json.loads(self.main.ssBEdit1.text())
        C = json.loads(self.main.ssCEdit1.text())
        D = json.loads(self.main.ssDEdit1.text())
        system, T, system_delay, system_ss = system_creator_ss(self, A, B, C, D)

    if system_delay is None:
        t1, y1 = rutina_impulse_plot(self, system, T)
        t2, y2 = rutina_step_plot(self, system, T)
        mag, phase, omega = rutina_bode_plot(self, system)
        real, imag, freq = rutina_nyquist_plot(self, system)
        rutina_nichols_plot(self, system)
    else:
        t1, y1 = rutina_impulse_plot(self, system_delay, T)
        t2, y2 = rutina_step_plot(self, system_delay, T)
        mag, phase, omega = rutina_bode_plot(self, system_delay)
        real, imag, freq = rutina_nyquist_plot(self, system_delay)
        rutina_nichols_plot(self, system_delay)
    
    if not system_ss:
        rutina_root_locus_plot(self, system)
        rutina_system_info(self, system, T, mag, phase, omega)
    else:
        rutina_root_locus_plot(self, system_ss)
        rutina_system_info(self, system_ss, T, mag, phase, omega)

def analisis_bool_discreto(self):
    if self.main.tfdiscretocheckBox1.isChecked():
        self.main.tfperiodoEdit1.setEnabled(True)
    else:
        self.main.tfperiodoEdit1.setDisabled(True)


def analisis_stacked_to_tf(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(0)


def analisis_stacked_to_ss(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(1)
