from rutinas.rutinas_simulacion import *
from rutinas.rutinas_fuzzy import FuzzyController
from PySide2 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
import numpy as np
import copy
import json


def SimulacionHandler(self):
    self.main.progressBar.hide()
    self.main.simularButton.clicked.connect(lambda: calcular_simulacion(self))

    self.main.tfdiscretocheckBox4.clicked['bool'].connect(
        self.main.samplesSimulacion.setDisabled)

    self.main.ssdiscretocheckBox4.clicked['bool'].connect(
        self.main.samplesSimulacion.setDisabled)

    # self.main.tfdiscretocheckBox4.stateChanged.connect(
    #     lambda: simulacion_bool_discreto(self))

    self.main.tfradioButton4.toggled.connect(lambda: simulacion_stacked_to_tf(self))
    self.main.ssradioButton4.toggled.connect(lambda: simulacion_stacked_to_ss(self))
    self.main.loadController.clicked.connect(lambda: get_pathcontroller(self))
    self.main.esquemaSimulacion.currentIndexChanged.connect(lambda: accion_esquema_selector(self))


def calcular_simulacion(self):
    if self.main.tfdelaycheckBox4.isChecked(
    ) and self.main.SimulacionstackedWidget.currentIndex() == 0:
        try:
            _ = json.loads(self.main.tfdelayEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    if self.main.ssdelaycheckBox4.isChecked(
    ) and self.main.SimulacionstackedWidget.currentIndex() == 1:
        try:
            _ = json.loads(self.main.ssdelayEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    system_ss = 0

    if (self.main.tfdiscretocheckBox4.isChecked() and
            self.main.SimulacionstackedWidget.currentIndex() == 0):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (self.main.ssdiscretocheckBox4.isChecked() and
          self.main.SimulacionstackedWidget.currentIndex() == 1):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit4.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    else:
        self.dt = 1/int(self.main.samplesSimulacion.text())

    if self.main.SimulacionstackedWidget.currentIndex() == 0:
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
            self.main.kdSimulacion.text(),
            self.main.NSimulacion.text()
        ],
        self.main.pathController.text()
    ]

    self.thread = SimpleThread(self,
                               plot_final_results,
                               update_progresBar_function,
                               list_info)
    self.thread.start()


def simulacion_bool_discreto(self):
    if self.main.tfdiscretocheckBox4.isChecked():
        self.main.tfperiodoEdit4.setEnabled(True)
    else:
        self.main.tfperiodoEdit4.setDisabled(True)


def simulacion_stacked_to_tf(self):
    self.main.SimulacionstackedWidget.setCurrentIndex(0)
    if self.main.tfdiscretocheckBox4.isChecked():
        self.main.samplesSimulacion.setDisabled(True)
    else:
        self.main.samplesSimulacion.setEnabled(True)



def simulacion_stacked_to_ss(self):
    self.main.SimulacionstackedWidget.setCurrentIndex(1)
    if self.main.ssdiscretocheckBox4.isChecked():
        self.main.samplesSimulacion.setDisabled(True)
    else:
        self.main.samplesSimulacion.setEnabled(True)


def get_pathcontroller(self):
    path_cargar = QtWidgets.QFileDialog.getOpenFileName(selectedFilter="*.json")
    self.main.pathController.setText(path_cargar[0])


def accion_esquema_selector(self):
    index = self.main.esquemaSimulacion.currentIndex()

    if index == 0:
        self.main.loadController.setDisabled(True)

    if index == 1:
        self.main.loadController.setEnabled(True)


def update_progresBar_function(self, value):
    self.main.progressBar.setValue(value)


def plot_final_results(self, result):
    self.main.simulacionGraph.canvas.axes1.clear()

    if result[4]:
        self.main.simulacionGraph.canvas.axes1.step(result[0],
                                                    result[1],
                                                    where="mid",
                                                    label='y(t)')
    else:
        self.main.simulacionGraph.canvas.axes1.plot(result[0], result[1], label='y(t)')

    self.main.simulacionGraph.canvas.axes1.plot(result[0],
                                                result[3],
                                                linestyle='--',
                                                label='setpoint',
                                                alpha=0.5)

    self.main.simulacionGraph.canvas.axes1.grid(color="lightgray")
    self.main.simulacionGraph.canvas.axes1.legend()
    self.main.simulacionGraph.canvas.draw()

    self.main.simulacionGraph.canvas.axes2.clear()

    if result[4]:
        self.main.simulacionGraph.canvas.axes2.step(result[0],
                                                    result[2],
                                                    '#2ca02c',
                                                    where="mid",
                                                    label='señal de control')
    else:
        self.main.simulacionGraph.canvas.axes2.plot(result[0],
                                                    result[2],
                                                    '#2ca02c',
                                                    label='señal de control')

    self.main.simulacionGraph.canvas.axes2.grid(color="lightgray")
    self.main.simulacionGraph.canvas.axes2.legend()
    self.main.simulacionGraph.canvas.draw()

    self.main.simulacionGraph.toolbar.update()
    self.main.progressBar.setValue(0)
    self.main.progressBar.hide()
    self.main.principalTab.setEnabled(True)