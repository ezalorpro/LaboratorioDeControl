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

    self.main.tfradioButton4.toggled.connect(lambda: simulacion_stacked_to_tf(self))
    self.main.ssradioButton4.toggled.connect(lambda: simulacion_stacked_to_ss(self))
    self.main.loadController1.clicked.connect(lambda: get_pathcontroller1(self))
    self.main.loadController2.clicked.connect(lambda: get_pathcontroller2(self))
    self.main.esquemaSimulacion.currentIndexChanged.connect(lambda: accion_esquema_selector(self))
    self.main.defaultConfiguration.clicked.connect(lambda: restablecer_configuracion(self))

    # Validaciones de entradas

    self.main.tfnumEdit4.editingFinished.connect(lambda: tfnum_validator(self))
    self.main.tfdemEdit4.editingFinished.connect(lambda: tfdem_validator(self))
    self.main.tfdelayEdit4.editingFinished.connect(lambda: tfdelay_validator(self))
    self.main.tfperiodoEdit4.editingFinished.connect(lambda: tfperiodo_validator(self))

    self.main.ssAEdit4.editingFinished.connect(lambda: ssA_validator(self))
    self.main.ssBEdit4.editingFinished.connect(lambda: ssB_validator(self))
    self.main.ssCEdit4.editingFinished.connect(lambda: ssC_validator(self))
    self.main.ssDEdit4.editingFinished.connect(lambda: ssD_validator(self))
    self.main.ssdelayEdit4.editingFinished.connect(lambda: ssdelay_validator(self))
    self.main.ssperiodoEdit4.editingFinished.connect(lambda: ssperiodo_validator(self))

    self.main.tiempoSimulacion.editingFinished.connect(lambda: tiempo_validator(self))
    self.main.escalonSimulacion.editingFinished.connect(lambda: escalon_validator(self))
    self.main.escalonAvanzado.editingFinished.connect(lambda: escalonAvanzado_validator(self))

    self.main.padeOrder.editingFinished.connect(lambda: pade_validator(self))
    self.main.rtolLineEdit.editingFinished.connect(lambda: rtol_validator(self))
    self.main.atolLineEdit.editingFinished.connect(lambda: atol_validator(self))
    self.main.maxStepIncr.editingFinished.connect(lambda: maxstep_validator(self))
    self.main.minStepDecr.editingFinished.connect(lambda: minstep_validator(self))
    self.main.safetyFactor.editingFinished.connect(lambda: safetyFactor_validator(self))

    self.main.numSensor.editingFinished.connect(lambda: sensornum_validator(self))
    self.main.demSensor.editingFinished.connect(lambda: sensordem_validator(self))
    self.main.numAccionador.editingFinished.connect(lambda: accionadornum_validator(self))
    self.main.demAccionador.editingFinished.connect(lambda: accionadordem_validator(self))
    self.main.inferiorSaturador.editingFinished.connect(lambda: inferiorSaturador_validator(self))
    self.main.superiorSaturador.editingFinished.connect(lambda: superiorSaturador_validator(self))

    self.main.kpSimulacion.editingFinished.connect(lambda: kp_validator(self))
    self.main.kiSimulacion.editingFinished.connect(lambda: ki_validator(self))
    self.main.kdSimulacion.editingFinished.connect(lambda: kd_validator(self))
    self.main.NSimulacion.editingFinished.connect(lambda: N_validator(self))


def tfnum_validator(self):
    try:
        _ = json.loads(self.main.tfnumEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.tfnumEdit4.setFocus()
        return


def tfdem_validator(self):
    try:
        _ = json.loads(self.main.tfdemEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.tfdemEdit4.setFocus()
        return


def tfdelay_validator(self):
    try:
        _ = float(self.main.tfdelayEdit4.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Delay no valido, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.tfdelayEdit4.setFocus()
        return


def tfperiodo_validator(self):
    try:
        _ = float(self.main.tfperiodoEdit4.text())
        if _ <= 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Periodo de muestreo no valido, debe ser un numero real mayor que cero")
        self.error_dialog.exec_()
        self.main.tfperiodoEdit4.setFocus()
        return


def ssA_validator(self):
    try:
        _ = json.loads(self.main.ssAEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, las matrices deben estar definidas entre corchetes con cada fila delimitada por otro par de corchetes y separadas entre si por comas, cada valor debera ir separado por coma.\n i.g., [[1, 1], [1, -1]]"
        )
        self.error_dialog.exec_()
        self.main.ssAEdit4.setFocus()
        return


def ssB_validator(self):
    try:
        _ = json.loads(self.main.ssBEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, las matrices deben estar definidas entre corchetes con cada fila delimitada por otro par de corchetes y separadas entre si por comas, cada valor debera ir separado por coma.\n i.g., [[1, 1], [1, -1]]"
        )
        self.error_dialog.exec_()
        self.main.ssBEdit4.setFocus()
        return


def ssC_validator(self):
    try:
        _ = json.loads(self.main.ssCEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, las matrices deben estar definidas entre corchetes con cada fila delimitada por otro par de corchetes y separadas entre si por comas, cada valor debera ir separado por coma.\n i.g., [[1, 1], [1, -1]]"
        )
        self.error_dialog.exec_()
        self.main.ssCEdit4.setFocus()
        return


def ssD_validator(self):
    try:
        _ = json.loads(self.main.ssDEdit4.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, las matrices deben estar definidas entre corchetes con cada fila delimitada por otro par de corchetes y separadas entre si por comas, cada valor debera ir separado por coma.\n i.g., [[1, 1], [1, -1]]"
        )
        self.error_dialog.exec_()
        self.main.ssDEdit4.setFocus()
        return


def ssdelay_validator(self):
    try:
        _ = float(self.main.ssdelayEdit4.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Delay no valido, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.ssdelayEdit4.setFocus()
        return


def ssperiodo_validator(self):
    try:
        _ = float(self.main.ssperiodoEdit4.text())
        if _ <= 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Periodo de muestreo no valido, debe ser un numero real mayor que cero")
        self.error_dialog.exec_()
        self.main.ssperiodoEdit4.setFocus()
        return


def tiempo_validator(self):
    try:
        _ = float(self.main.tiempoSimulacion.text())
        if _ <= 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Tiempo no valido, debe ser un numero real mayor que cero")
        self.error_dialog.exec_()
        self.main.tiempoSimulacion.setFocus()
        return


def escalon_validator(self):
    try:
        _ = float(self.main.escalonSimulacion.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Tiempo no valido, debe ser un numero real mayor que cero")
        self.error_dialog.exec_()
        self.main.escalonSimulacion.setFocus()
        return


def escalonAvanzado_validator(self):
    try:
        _ = json.loads(self.main.escalonAvanzado.text())
        if len(_) % 2 != 0:
            self.error_dialog.setInformativeText(
                "Escalon avanzado no valido, debe contener una cantidad par de valores con formato: \n [valor1, tiempo1, valor2, tiempo2, ..., valor_n, tiempo_n]")
            self.error_dialog.exec_()
            self.main.escalonAvanzado.setFocus()
            return
        for i in range(1, len(_) + 1, 2):
            for j in range(1, len(_) + 1, 2):
                if j <= i:
                    continue
                elif _[i] > _[j]:
                    self.error_dialog.setInformativeText(
                        "Escalon avanzado no valido, los valores de tiempo deben cumplir la siguiente condicion: \n tiempo1 <= tiempo2 <= tiempo3 <= ... <= tiempo_n")
                    self.error_dialog.exec_()
                    self.main.escalonAvanzado.setFocus()
                    return

    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los valores y tiempos deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 0.5, 4, 0.25, 8]")
        self.error_dialog.exec_()
        self.main.escalonAvanzado.setFocus()
        return


def pade_validator(self):
    try:
        _ = int(self.main.padeOrder.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Orden del pade no valido, debe ser un numero entero mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.padeOrder.setFocus()
        return

def rtol_validator(self):
    try:
        _ = float(self.main.rtolLineEdit.text())
        if _ <= 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Tolerancia relativa no valida, debe ser un numero real mayor que cero, se puede expresar en notacion cientifica\n i.g., 1e-3")
        self.error_dialog.exec_()
        self.main.rtolLineEdit.setFocus()
        return

def atol_validator(self):
    try:
        _ = float(self.main.atolLineEdit.text())
        if _ <= 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Tolerancia absoluta no valida, debe ser un numero real mayor que cero, se puede expresar en notacion cientifica\n i.g., 5e-6")
        self.error_dialog.exec_()
        self.main.atolLineEdit.setFocus()
        return


def maxstep_validator(self):
    try:
        _ = float(self.main.maxStepIncr.text())
        if _ <= 1:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Incremento maximo de paso no valido, debe ser un numero real mayor que 1"
        )
        self.error_dialog.exec_()
        self.main.maxStepIncr.setFocus()
        return


def minstep_validator(self):
    try:
        _ = float(self.main.minStepDecr.text())
        if _ <= 0 or _ >=1:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Decremento minimo de paso no valido, debe ser un numero real menor que 1 y mayor que cero")
        self.error_dialog.exec_()
        self.main.minStepDecr.setFocus()
        return


def safetyFactor_validator(self):
    try:
        _ = float(self.main.safetyFactor.text())
        if _ <= 0 or _ >= 1:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Factor de seguridad no valido, debe ser un numero real menor que 1 y mayor que cero"
        )
        self.error_dialog.exec_()
        self.main.safetyFactor.setFocus()
        return


def sensornum_validator(self):
    try:
        _ = json.loads(self.main.numSensor.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.numSensor.setFocus()
        return


def sensordem_validator(self):
    try:
        _ = json.loads(self.main.demSensor.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.demSensor.setFocus()
        return


def accionadornum_validator(self):
    try:
        _ = json.loads(self.main.numAccionador.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.numAccionador.setFocus()
        return


def accionadordem_validator(self):
    try:
        _ = json.loads(self.main.demAccionador.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato no valido, los coeficientes deben estar entre corchetes y separados por comas.\n i.g., [1, 2, 3]"
        )
        self.error_dialog.exec_()
        self.main.demAccionador.setFocus()
        return


def inferiorSaturador_validator(self):
    try:
        _ = float(self.main.inferiorSaturador.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Limite inferior no valido, debe ser un numero real")
        self.error_dialog.exec_()
        self.main.inferiorSaturador.setFocus()
        return


def superiorSaturador_validator(self):
    try:
        _ = float(self.main.superiorSaturador.text())
    except ValueError:
        self.error_dialog.setInformativeText(
            "Limite superior no valido, debe ser un numero real")
        self.error_dialog.exec_()
        self.main.superiorSaturador.setFocus()
        return


def kp_validator(self):
    try:
        _ = float(self.main.kpSimulacion.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Ganancia kp no valida, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.kpSimulacion.setFocus()
        return


def ki_validator(self):
    try:
        _ = float(self.main.kiSimulacion.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Ganancia ki no valida, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.kiSimulacion.setFocus()
        return


def kd_validator(self):
    try:
        _ = float(self.main.kdSimulacion.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Ganancia kd no valida, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.kdSimulacion.setFocus()
        return


def N_validator(self):
    try:
        _ = float(self.main.NSimulacion.text())
        if _ < 0:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Valor de N no valido, debe ser un numero real mayor o igual que cero")
        self.error_dialog.exec_()
        self.main.NSimulacion.setFocus()
        return


def calcular_simulacion(self):

    num = json.loads(self.main.numSensor.text())
    dem = json.loads(self.main.demSensor.text())

    if len(num) > len(dem) and self.main.sensorCheck.isChecked():
        self.error_dialog.setInformativeText(
            "Funcion de transferencia del sensor impropia, el numerador debe ser de un grado menor o igual al del denominador")
        self.error_dialog.exec_()
        self.main.toolBox.setCurrentIndex(2)
        return

    num = json.loads(self.main.numAccionador.text())
    dem = json.loads(self.main.demAccionador.text())

    if len(num) > len(dem) and self.main.accionadorCheck.isChecked():
        self.error_dialog.setInformativeText(
            "Funcion de transferencia del accionador impropia, el numerador debe ser de un grado menor o igual al del denominador")
        self.error_dialog.exec_()
        self.main.toolBox.setCurrentIndex(2)
        return

    lim_inf = float(self.main.inferiorSaturador.text())
    lim_sup = float(self.main.superiorSaturador.text())

    if lim_inf >= lim_sup and self.main.saturadorCheck.isChecked():
        self.error_dialog.setInformativeText(
            "Limites del saturador del accionador invalidos, el limite inferior debe ser menor que el limite superior"
        )
        self.error_dialog.exec_()
        self.main.toolBox.setCurrentIndex(2)
        return

    if len(self.main.pathController1.text(
    )) < 1 and self.main.esquemaSimulacion.currentIndex() in [1, 2, 3, 4, 5, 6, 7, 8]:
        self.error_dialog.setInformativeText(
            "Debe seleccionar un archivo valido para cargar el controaldor difuso")
        self.error_dialog.exec_()
        self.main.toolBox.setCurrentIndex(3)
        return

    if len(self.main.pathController2.text(
    )) < 1 and self.main.esquemaSimulacion.currentIndex() in [4]:
        self.error_dialog.setInformativeText(
            "Debe seleccionar un archivo valido para cargar el controaldor difuso 2")
        self.error_dialog.exec_()
        self.main.toolBox.setCurrentIndex(3)
        return

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
        self.dt = json.loads(self.main.tfperiodoEdit4.text())
    elif (self.main.ssdiscretocheckBox4.isChecked() and
          self.main.SimulacionstackedWidget.currentIndex() == 1):
        self.dt = json.loads(self.main.ssperiodoEdit4.text())
    else:
        self.dt = 0

    if self.main.SimulacionstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit4.text())
        dem = json.loads(self.main.tfdemEdit4.text())

        if len(num) > len(dem):
            self.error_dialog.setInformativeText(
                "Funcion de transferencia impropia, el numerador debe ser de un grado menor o igual al del denominador")
            self.error_dialog.exec_()
            self.main.ssdelayEdit1.setFocus()
            return

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
                               error_gui,
                               list_info)
    self.thread.start()


def simulacion_bool_discreto(self):
    if self.main.tfdiscretocheckBox4.isChecked():
        self.main.tfperiodoEdit4.setEnabled(True)
    else:
        self.main.tfperiodoEdit4.setDisabled(True)


def simulacion_stacked_to_tf(self):
    self.main.SimulacionstackedWidget.setCurrentIndex(0)



def simulacion_stacked_to_ss(self):
    self.main.SimulacionstackedWidget.setCurrentIndex(1)


def get_pathcontroller1(self):
    path_cargar = QtWidgets.QFileDialog.getOpenFileName(filter="JSON/FIS (*.json *.fis)")
    self.main.pathController1.setText(path_cargar[0])


def get_pathcontroller2(self):
    path_cargar = QtWidgets.QFileDialog.getOpenFileName(filter="JSON/FIS (*.json *.fis)")
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


def restablecer_configuracion(self):
    self.main.padeOrder.setText('10')
    self.main.solverMethod.setCurrentIndex(8)
    self.main.rtolLineEdit.setText('1e-3')
    self.main.atolLineEdit.setText('5e-6')
    self.main.maxStepIncr.setText('5')
    self.main.minStepDecr.setText('0.2')
    self.main.safetyFactor.setText('0.95')


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
        self.main.NSpacer.show()

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
        self.main.NSpacer.hide()

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
        self.main.NSpacer.hide()
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
        self.main.NSpacer.hide()
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
        self.main.NSpacer.hide()
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
        self.main.NSpacer.show()
        self.main.NSimulacion.setEnabled(True)

        self.main.esquemaSimulacionGraph.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pidplusDifuso.png"))


def update_progresBar_function(self, value):
    self.main.progressBar.setValue(value)


def error_gui(self, error):
    self.main.progressBar.setValue(0)
    self.main.progressBar.hide()
    self.main.principalTab.setEnabled(True)

    if error == 0:
        self.error_dialog.setInformativeText("Error inesperado")
        self.error_dialog.exec_()

    if error == 1:
        self.error_dialog.setInformativeText("No se permiten salidas negadas en los controladores")
        self.error_dialog.exec_()

    if error == 2:
        self.error_dialog.setInformativeText(
            "Controlador no valido para el esquema seleccionado")
        self.error_dialog.exec_()



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