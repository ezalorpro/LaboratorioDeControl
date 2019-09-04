from rutinas.rutinas_PID import *
from rutinas.rutinas_CSV import *
import json


def TuningHandler(self):
    self.tfSliderValue = self.main.tfreolutionSpin2.value()
    self.ssSliderValue = self.main.ssreolutionSpin2.value()

    self.main.tfcalcButton2.clicked.connect(lambda: chequeo_de_accion(self))
    self.main.sscalcButton2.clicked.connect(lambda: chequeo_de_accion(self))

    self.main.kpHSlider2.valueChanged.connect(lambda: chequeo_de_accion(self))
    self.main.kiHSlider2.valueChanged.connect(lambda: chequeo_de_accion(self))
    self.main.kdHSlider2.valueChanged.connect(lambda: chequeo_de_accion(self))

    self.main.pidTiempoSlider.valueChanged.connect(lambda: chequeo_de_accion(self))
    self.main.pidNSlider.valueChanged.connect(lambda: chequeo_de_accion(self))

    self.main.kpCheckBox2.stateChanged.connect(lambda: chequeo_de_accion(self))
    self.main.kiCheckBox2.stateChanged.connect(lambda: chequeo_de_accion(self))
    self.main.kdCheckBox2.stateChanged.connect(lambda: chequeo_de_accion(self))

    self.main.tfdiscretocheckBox2.stateChanged.connect(lambda: PID_bool_discreto(self))

    self.main.tfradioButton2.toggled.connect(lambda: PID_stacked_to_tf(self))
    self.main.ssradioButton2.toggled.connect(lambda: PID_stacked_to_ss(self))
    self.main.csvradioButton2.toggled.connect(lambda: PID_stacked_to_csv(self))

    self.main.tfAutoTuningcheckBox2.clicked['bool'].connect(
        lambda: tf_habilitar_sliders_checkbox(self)
    )
    self.main.ssAutoTuningcheckBox2.clicked['bool'].connect(
        lambda: ss_habilitar_sliders_checkbox(self)
    )

    self.main.tfreolutionSpin2.valueChanged.connect(lambda: actualizar_sliders_tf(self))
    self.main.ssreolutionSpin2.valueChanged.connect(lambda: actualizar_sliders_ss(self))


def chequeo_de_accion(self):
    if not self.main.tfAutoTuningcheckBox2.isChecked(
    ) and self.main.PIDstackedWidget.currentIndex() == 0:
        calcular_PID(self)
    elif not self.main.ssAutoTuningcheckBox2.isChecked(
    ) and self.main.PIDstackedWidget.currentIndex() == 1:
        calcular_PID(self)
    elif self.main.tfAutoTuningcheckBox2.isChecked(
    ) and self.main.PIDstackedWidget.currentIndex() == 0:
        calcular_autotuning(self)
    elif self.main.ssAutoTuningcheckBox2.isChecked(
    ) and self.main.PIDstackedWidget.currentIndex() == 1:
        calcular_autotuning(self)
    else:
        calcular_csv(self)


def calcular_PID(self):

    if self.main.tfdelaycheckBox2.isChecked() and self.main.PIDstackedWidget.currentIndex(
    ) == 0:
        try:
            _ = json.loads(self.main.tfdelayEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    if self.main.ssdelaycheckBox2.isChecked() and self.main.PIDstackedWidget.currentIndex(
    ) == 1:
        try:
            _ = json.loads(self.main.ssdelayEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    system_ss = 0

    if (
        self.main.tfdiscretocheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 0
    ):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (
        self.main.ssdiscretocheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 1
    ):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    else:
        self.dt = None

    if self.main.PIDstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit2.text())
        dem = json.loads(self.main.tfdemEdit2.text())
        system_pid, T, system_delay, kp, ki, kd = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit2.text())
        B = json.loads(self.main.ssBEdit2.text())
        C = json.loads(self.main.ssCEdit2.text())
        D = json.loads(self.main.ssDEdit2.text())
        system_pid, T, system_delay, system_ss, kp, ki, kd = system_creator_ss(self, A, B, C, D)

    if system_delay is None:
        t2, y2 = rutina_step_plot(self, system_pid, T, kp, ki, kd)
    else:
        t2, y2 = rutina_step_plot(self, system_delay, T, kp, ki, kd)

    if not system_ss:
        rutina_system_info(self, system_pid, T, t2, y2)
        update_gain_labels(self, resolution=self.tfSliderValue)
        update_time_and_N_labels(self)
    else:
        rutina_system_info(self, system_ss, T, t2, y2)
        update_gain_labels(self, resolution=self.ssSliderValue)
        update_time_and_N_labels(self)


def calcular_autotuning(self):

    if self.main.tfdelaycheckBox2.isChecked() and self.main.PIDstackedWidget.currentIndex(
    ) == 0:
        try:
            _ = json.loads(self.main.tfdelayEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    if self.main.ssdelaycheckBox2.isChecked() and self.main.PIDstackedWidget.currentIndex(
    ) == 1:
        try:
            _ = json.loads(self.main.ssdelayEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Delay no valido")
            self.error_dialog.exec_()
            return

    system_ss = 0

    if (
        self.main.tfdiscretocheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 0
    ):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (
        self.main.ssdiscretocheckBox2.isChecked() and
        self.main.PIDstackedWidget.currentIndex() == 1
    ):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText(
                "El alfa calculado es igual o menor a 0, lo cual es invalido para auto-tuning, se recomienda agregar un Delay mayor a 0.3"
            )
            self.error_dialog.exec_()
            return
    else:
        self.dt = None

    if self.main.PIDstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit2.text())
        dem = json.loads(self.main.tfdemEdit2.text())
        try:
            system_pid, T, system_delay, kp, ki, kd = system_creator_tf_tuning(self, num, dem)
        except TypeError:
            self.error_dialog.setInformativeText(
                "El alfa calculado es igual o menor a 0.05, lo cual es invalido para auto-tuning, se recomienda agregar un Delay mayor a 0.3"
            )
            self.error_dialog.exec_()
            return
    else:
        A = json.loads(self.main.ssAEdit2.text())
        B = json.loads(self.main.ssBEdit2.text())
        C = json.loads(self.main.ssCEdit2.text())
        D = json.loads(self.main.ssDEdit2.text())
        try:
            system_pid, T, system_delay, system_ss, kp, ki, kd = system_creator_ss_tuning(self, A, B, C, D)
        except TypeError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return

    if system_delay is None:
        t2, y2 = rutina_step_plot(self, system_pid, T, kp, ki, kd)
    else:
        t2, y2 = rutina_step_plot(self, system_delay, T, kp, ki, kd)

    if not system_ss:
        rutina_system_info(self, system_pid, T, t2, y2, kp, ki, kd, autotuning=True)
        update_gain_labels(
            self, kp, ki, kd, autotuning=True, resolution=self.tfSliderValue
        )
        update_time_and_N_labels(self)
    else:
        rutina_system_info(self, system_ss, T, t2, y2, kp, ki, kd, autotuning=True)
        update_gain_labels(
            self, kp, ki, kd, autotuning=True, resolution=self.ssSliderValue
        )
        update_time_and_N_labels(self)


def calcular_csv(self):
    pass


def PID_bool_discreto(self):
    if self.main.tfdiscretocheckBox2.isChecked():
        self.main.tfperiodoEdit2.setEnabled(True)
    else:
        self.main.tfperiodoEdit2.setDisabled(True)


def PID_stacked_to_tf(self):
    self.main.PIDstackedWidget.setCurrentIndex(0)
    self.main.GraphStakedTuning.setCurrentIndex(0)
    tf_habilitar_sliders_checkbox(self)
    update_gain_labels(self, resolution=self.tfSliderValue)


def tf_habilitar_sliders_checkbox(self):
    
    self.main.pidNSlider.setEnabled(True)
    
    if self.main.tfAutoTuningcheckBox2.isChecked():
        self.main.kpCheckBox2.setDisabled(True)
        self.main.kiCheckBox2.setDisabled(True)
        self.main.kdCheckBox2.setDisabled(True)
        self.main.kpHSlider2.setDisabled(True)
        self.main.kiHSlider2.setDisabled(True)
        self.main.kdHSlider2.setDisabled(True)
    else:
        self.main.kpCheckBox2.setEnabled(True)
        self.main.kiCheckBox2.setEnabled(True)
        self.main.kdCheckBox2.setEnabled(True)

        if self.main.kpCheckBox2.isChecked():
            self.main.kpHSlider2.setEnabled(True)
        else:
            self.main.kpHSlider2.setDisabled(True)

        if self.main.kiCheckBox2.isChecked():
            self.main.kiHSlider2.setEnabled(True)
        else:
            self.main.kiHSlider2.setDisabled(True)

        if self.main.kdCheckBox2.isChecked():
            self.main.kdHSlider2.setEnabled(True)
        else:
            self.main.kdHSlider2.setDisabled(True)


def PID_stacked_to_ss(self):
    self.main.PIDstackedWidget.setCurrentIndex(1)
    self.main.GraphStakedTuning.setCurrentIndex(0)
    ss_habilitar_sliders_checkbox(self)
    update_gain_labels(self, resolution=self.ssSliderValue)


def ss_habilitar_sliders_checkbox(self):
    
    self.main.pidNSlider.setEnabled(True)
    
    if self.main.ssAutoTuningcheckBox2.isChecked():
        self.main.kpCheckBox2.setDisabled(True)
        self.main.kiCheckBox2.setDisabled(True)
        self.main.kdCheckBox2.setDisabled(True)
        self.main.kpHSlider2.setDisabled(True)
        self.main.kiHSlider2.setDisabled(True)
        self.main.kdHSlider2.setDisabled(True)
    else:
        self.main.kpCheckBox2.setEnabled(True)
        self.main.kiCheckBox2.setEnabled(True)
        self.main.kdCheckBox2.setEnabled(True)

        if self.main.kpCheckBox2.isChecked():
            self.main.kpHSlider2.setEnabled(True)
        else:
            self.main.kpHSlider2.setDisabled(True)

        if self.main.kiCheckBox2.isChecked():
            self.main.kiHSlider2.setEnabled(True)
        else:
            self.main.kiHSlider2.setDisabled(True)

        if self.main.kdCheckBox2.isChecked():
            self.main.kdHSlider2.setEnabled(True)
        else:
            self.main.kdHSlider2.setDisabled(True)


def actualizar_sliders_tf(self):
    self.tfSliderValue = self.main.tfreolutionSpin2.value()
    update_gain_labels(self, resolution=self.tfSliderValue)


def actualizar_sliders_ss(self):
    self.ssSliderValue = self.main.ssreolutionSpin2.value()
    update_gain_labels(self, resolution=self.ssSliderValue)


def PID_stacked_to_csv(self):
    self.main.PIDstackedWidget.setCurrentIndex(2)
    self.main.GraphStakedTuning.setCurrentIndex(1)
    self.main.kpCheckBox2.setDisabled(True)
    self.main.kiCheckBox2.setDisabled(True)
    self.main.kdCheckBox2.setDisabled(True)
    self.main.kpHSlider2.setDisabled(True)
    self.main.kiHSlider2.setDisabled(True)
    self.main.kdHSlider2.setDisabled(True)
    self.main.pidNSlider.setDisabled(True)