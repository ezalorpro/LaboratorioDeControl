from rutinas.rutinas_simulacion import *
from rutinas.rutinas_fuzzy import FuzzyController
from rutinas.rutinas_rk import *
from PySide2 import QtCore, QtGui, QtWidgets
from matplotlib import pyplot as plt
import numpy as np
import copy
import json


def SimulacionHandler(self):
    self.main.progressBar.hide()

    self.main.controller1Frame.hide()
    self.main.controller2Frame.hide()
    self.main.kpFrame.show()
    self.main.kiFrame.show()
    self.main.kdFrame.show()

    self.main.simularButton.clicked.connect(lambda: calcular_simulacion(self))

    self.main.tfdiscretocheckBox4.clicked['bool'].connect(
        self.main.samplesSimulacion.setDisabled)

    self.main.ssdiscretocheckBox4.clicked['bool'].connect(
        self.main.samplesSimulacion.setDisabled)

    self.main.tfradioButton4.toggled.connect(lambda: simulacion_stacked_to_tf(self))
    self.main.ssradioButton4.toggled.connect(lambda: simulacion_stacked_to_ss(self))
    self.main.loadController1.clicked.connect(lambda: get_pathcontroller1(self))
    self.main.loadController2.clicked.connect(lambda: get_pathcontroller2(self))
    self.main.esquemaSimulacion.currentIndexChanged.connect(lambda: accion_esquema_selector(self))
    # self.main.kdCheck.stateChanged.connect(lambda: enabled_N(self))


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
        system = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit4.text())
        B = json.loads(self.main.ssBEdit4.text())
        C = json.loads(self.main.ssCEdit4.text())
        D = json.loads(self.main.ssDEdit4.text())
        system = system_creator_ss(self, A, B, C, D)

    if not self.main.escalonCheck.isChecked():
        escalon = float(self.main.escalonSimulacion.text())
    else:
        escalon = json.loads(self.main.escalonAvanzado.text())

    rk_base, metodo_adaptativo, solver_config = configuration_data(self)

    list_info = [
        self.main.esquemaSimulacion.currentIndex(),
        system,
        float(self.main.tiempoSimulacion.text()),
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
        ], [self.main.pathController1.text(), self.main.pathController2.text()],
        rk_base,
        metodo_adaptativo,
        solver_config
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


def get_pathcontroller1(self):
    path_cargar = QtWidgets.QFileDialog.getOpenFileName(filter="JSON (*.json)")
    self.main.pathController1.setText(path_cargar[0])


def get_pathcontroller2(self):
    path_cargar = QtWidgets.QFileDialog.getOpenFileName(filter="JSON (*.json)")
    self.main.pathController2.setText(path_cargar[0])


def configuration_data(self):
    rtol = float(self.main.rtolLineEdit.text())
    atol = float(self.main.atolLineEdit.text())
    max_step_inc = float(self.main.maxStepIncr.text())
    min_step_dec = float(self.main.minStepDecr.text())
    safety_factor = float(self.main.safetyFactor.text())

    if self.main.solverMethod.currentIndex() <= 8:
        metodo_adaptativo = rk_doble_paso_adaptativo
    else:
        metodo_adaptativo = rk_embebido_adaptativo

    if self.main.solverMethod.currentIndex() == 0:
        rk_metodo = runge_kutta2
        rk_base = rk_metodo
        ordenq = 2
    elif self.main.solverMethod.currentIndex() == 1:
        rk_metodo = runge_kutta3
        rk_base = rk_metodo
        ordenq = 3
    elif self.main.solverMethod.currentIndex() == 2:
        rk_metodo = heun3
        rk_base = rk_metodo
        ordenq = 3
    elif self.main.solverMethod.currentIndex() == 3:
        rk_metodo = ralston3
        rk_base = rk_metodo
        ordenq = 3
    elif self.main.solverMethod.currentIndex() == 4:
        rk_metodo = SSPRK3
        rk_base = rk_metodo
        ordenq = 3
    elif self.main.solverMethod.currentIndex() == 5:
        rk_metodo = runge_kutta4
        rk_base = rk_metodo
        ordenq = 4
    elif self.main.solverMethod.currentIndex() == 6:
        rk_metodo = tres_octavos4
        rk_base = rk_metodo
        ordenq = 4
    elif self.main.solverMethod.currentIndex() == 7:
        rk_metodo = ralston4
        rk_base = rk_metodo
        ordenq = 4
    elif self.main.solverMethod.currentIndex() == 8:
        rk_metodo = runge_kutta5
        rk_base = rk_metodo
        ordenq = 5
    elif self.main.solverMethod.currentIndex() == 9:
        rk_metodo = bogacki_shampine23
        rk_base = runge_kutta2
        ordenq = 2
    elif self.main.solverMethod.currentIndex() == 10:
        rk_metodo = fehlberg45
        rk_base = runge_kutta4
        ordenq = 4
    elif self.main.solverMethod.currentIndex() == 11:
        rk_metodo = cash_karp45
        rk_base = runge_kutta4
        ordenq = 4
    elif self.main.solverMethod.currentIndex() == 12:
        rk_metodo = dopri54
        rk_base = runge_kutta5
        ordenq = 4

    return rk_base, metodo_adaptativo, [rk_metodo, ordenq, rtol, atol, max_step_inc, min_step_dec, safety_factor]




def accion_esquema_selector(self):

    self.main.controller1Frame.hide()
    self.main.controller2Frame.hide()
    self.main.kpFrame.hide()
    self.main.kiFrame.hide()
    self.main.kdFrame.hide()

    index = self.main.esquemaSimulacion.currentIndex()
    self.main.tabSimulation.setCurrentIndex(0)

    if index == 0:
        self.main.controller1Frame.hide()
        self.main.controller2Frame.hide()
        self.main.kpFrame.show()
        self.main.kiFrame.show()
        self.main.kdFrame.show()
        self.main.kdCheck.show()
        self.main.kiCheck.show()
        self.main.NFrame.show()
        self.main.labelFiltro.show()

        if self.main.kdCheck.isChecked():
            self.main.NSimulacion.setEnabled(True)
        else:
            self.main.NSimulacion.setDisabled(True)

        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pidClasico.png"))


    if index in [1, 2, 3, 7]:
        self.main.controller1Frame.show()
        self.main.controller2Frame.hide()
        self.main.kpFrame.hide()
        self.main.kiFrame.hide()
        self.main.kdFrame.hide()
        self.main.NSimulacion.setEnabled(True)
        self.main.NFrame.show()
        self.main.labelFiltro.hide()

        if index == 1:
            self.main.esquemaSimulacionGraph.setPixmap(
                QtGui.QPixmap(":/imagenes/imagenes/pidDifuso.png"))

        if index == 2:
            self.main.esquemaSimulacionGraph.setPixmap(
                QtGui.QPixmap(":/imagenes/imagenes/piDifuso.png"))

        if index == 3:
            self.main.esquemaSimulacionGraph.setPixmap(
                QtGui.QPixmap(":/imagenes/imagenes/pdDifuso.png"))

        if index == 7:
            self.main.esquemaSimulacionGraph.setPixmap(
                QtGui.QPixmap(":/imagenes/imagenes/GainScheduler.png"))

    if index == 4:
        self.main.controller1Frame.show()
        self.main.controller2Frame.show()
        self.main.kpFrame.hide()
        self.main.kiFrame.hide()
        self.main.kdFrame.hide()
        self.main.NSimulacion.setEnabled(True)
        self.main.NFrame.show()
        self.main.labelFiltro.hide()
        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pipdDifuso.png"))

    if index == 5:
        self.main.controller1Frame.show()
        self.main.controller2Frame.hide()
        self.main.kpFrame.hide()
        self.main.kiFrame.hide()
        self.main.kdFrame.show()
        self.main.kdCheck.hide()
        self.main.kdCheck.setChecked(True)
        self.main.kdSimulacion.setEnabled(True)
        self.main.NSimulacion.setEnabled(True)
        self.main.NFrame.show()
        self.main.labelFiltro.hide()
        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/piplusDDifuso.png"))

    if index == 6:
        self.main.controller1Frame.show()
        self.main.controller2Frame.hide()
        self.main.kpFrame.hide()
        self.main.kiFrame.show()
        self.main.kdFrame.hide()
        self.main.kiCheck.hide()
        self.main.kiCheck.setChecked(True)
        self.main.kiSimulacion.setEnabled(True)
        self.main.NSimulacion.setEnabled(True)
        self.main.NFrame.show()
        self.main.labelFiltro.hide()
        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pdplusIDifuso.png"))

    if index == 8:
        self.main.controller1Frame.show()
        self.main.controller2Frame.hide()
        self.main.kpFrame.show()
        self.main.kiFrame.show()
        self.main.kdFrame.show()
        self.main.kdCheck.show()
        self.main.kiCheck.show()
        self.main.NSimulacion.setEnabled(True)
        self.main.NFrame.show()
        self.main.NSimulacion.setEnabled(True)
        self.main.labelFiltro.show()

        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pidplusDifuso.png"))


# def enabled_N(self):

#     index = self.main.esquemaSimulacion.currentIndex()

#     if self.main.kdCheck.isChecked() and index in [0, 5, 8]:
#         self.main.kdSimulacion.setEnabled(True)
#         self.main.NSimulacion.setEnabled(True)

#     elif not self.main.kdCheck.isChecked() and index in [0, 5]:
#         self.main.kdSimulacion.setDisabled(True)
#         self.main.NSimulacion.setDisabled(True)
#     elif index == 8:
#         self.main.kdSimulacion.setDisabled(True)


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
    self.main.tabSimulation.setCurrentIndex(1)