from rutinas.rutinas_simulacion import *
from rutinas.rutinas_fuzzy import FuzzyController
from PySide2 import QtCore, QtGui, QtWidgets
import numpy as np
import copy
import json


def SimulacionHandler(self):

    self.main.simularButton.clicked.connect(lambda: testing(self))

    self.main.tfdiscretocheckBox4.stateChanged.connect(
        lambda: analisis_bool_discreto(self)
    )

    self.main.tfradioButton4.toggled.connect(lambda: analisis_stacked_to_tf(self))
    self.main.ssradioButton4.toggled.connect(lambda: analisis_stacked_to_ss(self))


def calcular_analisis(self):
    if self.main.tfdelaycheckBox4.isChecked(
    ) and self.main.AnalisisstackedWidget.currentIndex() == 0:
        try:
            _ = json.loads(self.main.tfdelayEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    if self.main.ssdelaycheckBox4.isChecked(
    ) and self.main.AnalisisstackedWidget.currentIndex() == 1:
        try:
            _ = json.loads(self.main.ssdelayEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    system_ss = 0

    if (
        self.main.tfdiscretocheckBox4.isChecked() and
        self.main.AnalisisstackedWidget.currentIndex() == 0
    ):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (
        self.main.ssdiscretocheckBox4.isChecked() and
        self.main.AnalisisstackedWidget.currentIndex() == 1
    ):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    else:
        self.dt = None

    if self.main.AnalisisstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit4.text())
        dem = json.loads(self.main.tfdemEdit4.text())
        system, T, system_delay = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit4.text())
        B = json.loads(self.main.ssBEdit4.text())
        C = json.loads(self.main.ssCEdit4.text())
        D = json.loads(self.main.ssDEdit4.text())
        system, T, system_delay, system_ss = system_creator_ss(self, A, B, C, D)

    if system_delay is None:
        t1, y1 = rutina_impulse_plot(self, system, T)
        t2, y2 = rutina_step_plot(self, system, T)
        mag, phase, omega = rutina_bode_plot(self, system)
        real, imag, freq = rutina_nyquist_plot(self, system)
        rutina_root_locus_plot(self, system)
        rutina_nichols_plot(self, system)
    else:
        t1, y1 = rutina_impulse_plot(self, system_delay, T)
        t2, y2 = rutina_step_plot(self, system_delay, T)
        mag, phase, omega = rutina_bode_plot(self, system_delay)
        real, imag, freq = rutina_nyquist_plot(self, system_delay)
        rutina_root_locus_plot(self, system_delay)
        rutina_nichols_plot(self, system_delay)


def analisis_bool_discreto(self):
    if self.main.tfdiscretocheckBox4.isChecked():
        self.main.tfperiodoEdit4.setEnabled(True)
    else:
        self.main.tfperiodoEdit4.setDisabled(True)


def analisis_stacked_to_tf(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(0)


def analisis_stacked_to_ss(self):
    self.main.AnalisisstackedWidget.setCurrentIndex(1)

def testing(self):
    self.thread = SimpleThread(self, print_final_result, update_progresBar_function, 0)
    self.thread.start()

def update_progresBar_function(self, value):
    self.main.progressBar.setValue(value)

def print_final_result(self, result):
    print(result)