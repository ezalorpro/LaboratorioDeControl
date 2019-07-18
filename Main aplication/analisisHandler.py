from rutinas_analisis import *
import json


def AnalisisHandler(self):
    self.main.tfcalcButton1.clicked.connect(lambda: calcular_analisis(self))
    self.main.sscalcButton1.clicked.connect(lambda: calcular_analisis(self))

    self.main.tfdiscretocheckBox1.stateChanged.connect(lambda: bool_discreto(self))

    self.main.tfradioButton1.toggled.connect(lambda: stacked_to_tf(self))
    self.main.ssradioButton1.toggled.connect(lambda: stacked_to_ss(self))


def calcular_analisis(self):
    if (
        self.main.tfdiscretocheckBox1.isChecked()
        and self.main.AnalisisstackedWidget.currentIndex() == 0
    ):
        self.dt = json.loads(self.main.tfperiodoEdit1.text())
    elif (
        self.main.ssdiscretocheckBox1.isChecked()
        and self.main.AnalisisstackedWidget.currentIndex() == 1
    ):
        self.dt = json.loads(self.main.ssperiodoEdit1.text())
    else:
        self.dt = None

    if self.main.AnalisisstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit1.text())
        dem = json.loads(self.main.tfdemEdit1.text())
        system, T = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit1.text())
        B = json.loads(self.main.ssBEdit1.text())
        C = json.loads(self.main.ssCEdit1.text())
        D = json.loads(self.main.ssDEdit1.text())
        system, T = system_creator_ss(self, A, B, C, D)

    t1, y1 = rutina_impulse_plot(self, system, T)
    t2, y2 = rutina_step_plot(self, system, T)
    mag, phase, omega = rutina_bode_plot(self, system)
    real, imag, freq = rutina_nyquist_plot(self, system)
    rutina_root_locus_plot(self, system)


def bool_discreto(self):
    if self.main.tfdiscretocheckBox1.isChecked():
        self.main.tfperiodoEdit1.setEnabled(True)
    else:
        self.main.tfperiodoEdit1.setDisabled(True)


def stacked_to_tf(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(0)


def stacked_to_ss(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(1)
