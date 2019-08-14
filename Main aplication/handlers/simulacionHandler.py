from rutinas.rutinas_simulacion import *
from rutinas.rutinas_fuzzy import FuzzyController
from PySide2 import QtCore, QtGui, QtWidgets
import numpy as np
import copy
import json


def SimulacionHandler(self):
    self.main.progressBar.hide()
    self.main.simularButton.clicked.connect(lambda: calcular_simulacion(self))

    self.main.tfdiscretocheckBox4.stateChanged.connect(
        lambda: analisis_bool_discreto(self))

    self.main.tfradioButton4.toggled.connect(lambda: analisis_stacked_to_tf(self))
    self.main.ssradioButton4.toggled.connect(lambda: analisis_stacked_to_ss(self))


def calcular_simulacion(self):
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

    if (self.main.tfdiscretocheckBox4.isChecked() and
            self.main.AnalisisstackedWidget.currentIndex() == 0):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (self.main.ssdiscretocheckBox4.isChecked() and
          self.main.AnalisisstackedWidget.currentIndex() == 1):
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
        system, T = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit4.text())
        B = json.loads(self.main.ssBEdit4.text())
        C = json.loads(self.main.ssCEdit4.text())
        D = json.loads(self.main.ssDEdit4.text())
        system, T = system_creator_ss(self, A, B, C, D)

    if not self.main.escalonCheck.isChecked():
        escalon = float(self.main.escalonSimulacion.text())
    else:
        escalon = json.loads(self.main.escalonAvanzado.text())

    list_info = [
        self.main.esquemaSimulacion.currentIndex(),
        system,
        T,
        self.dt,
        escalon,
        self.main.sensorCheck.isChecked(),
        self.main.accionadorCheck.isChecked(),
        self.main.saturadorCheck.isChecked(),
        [
            self.main.kpSimulacion.text(),
            self.main.kiSimulacion.text(),
            self.main.kdSimulacion.text()
        ],
        self.main.pathController.text()
    ]

    self.thread = SimpleThread(self,
                               plot_final_results,
                               update_progresBar_function,
                               list_info)
    self.thread.start()


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


def plot_final_results(self, result):
    print(result)