from PySide2 import QtCore, QtGui, QtWidgets
from rutinas.rutinas_fuzzy import FuzzyController
import controlmdf as ctrl
import numpy as np
from scipy import real, imag
from scipy import signal
from matplotlib import pyplot as plt
from collections import deque
import matplotlib.ticker as mticker
import time
import copy
import json


class SimpleThread(QtCore.QThread):
    finished = QtCore.Signal(object, list)
    update_progresBar = QtCore.Signal(object, float)

    def __init__(self, window, regresar, update_bar, list_info, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.window = window
        self.window.main.principalTab.setDisabled(True)
        self.window.main.progressBar.show()
        time.sleep(0.1)
        self.finished.connect(regresar)
        self.update_progresBar.connect(update_bar)
        self.list_info = copy.deepcopy(list_info)

        self.esquema = self.list_info[0]
        self.system = self.list_info[1]
        self.Tiempo = self.list_info[2]
        self.dt = self.list_info[3]
        self.escalon = self.list_info[4]
        self.sensor_flag = self.list_info[5]
        self.accionador_flag = self.list_info[6]
        self.saturador_flag = self.list_info[7]
        self.kp, self.ki, self.kd, self.N = map(float, self.list_info[8])
        self.fuzzy_path1, self.fuzzy_path2 = self.list_info[9]
        self.rk_base = self.list_info[10]
        self.metodo_adaptativo = self.list_info[11]
        self.solver_configuration = self.list_info[12]


    def run(self):
        if self.esquema in [0]:
            Tiempo, y, sc, u = self.run_pid()
            self.finished.emit(
                self.window,
                [Tiempo, y, sc, u, ctrl.isdtime(self.system, strict=True)])
            return

        if self.esquema in [1,2,3,4,5,6,7,8]:
            Tiempo, y, sc, u = self.run_fuzzy()
            self.finished.emit(
                self.window,
                [Tiempo, y, sc, u, ctrl.isdtime(self.system, strict=True)])

    def run_pid(self):
        if self.window.main.kpCheck.isChecked():
            kp = float(self.kp)
        else:
            kp = 0

        if self.window.main.kiCheck.isChecked():
            ki = float(self.ki)
        else:
            ki = 0

        if self.window.main.kdCheck.isChecked():
            kd = float(self.kd)
        else:
            kd = 0

        if isinstance(self.system, ctrl.TransferFunction):
            self.system = ctrl.tf2ss(self.system)

        tiempo_total = self.Tiempo
        tiempo = 0

        if isinstance(self.escalon, float):
            u = self.escalon
            max_tiempo = [self.Tiempo]
        else:
            it = iter(self.escalon)
            u_value = [0]
            max_tiempo = []
            for i, valor in enumerate(it):
                max_tiempo.append(next(it))
                u_value.append(valor)
            index_tbound = len(max_tiempo)
            max_tiempo.append(tiempo_total)
            tiempo += max_tiempo[0] - 0.0000011

        ten_percent = int(tiempo_total * 20 / 100)
        if ten_percent == 0:
            ten_percent = 1

        x = np.zeros_like(self.system.B)
        h = 0.000001

        salida = deque([0])
        sc_f = deque([0])
        sc_t = 0
        si_t = 0

        if ctrl.isdtime(self.system, strict=True):
            error_a = deque([0] * 2)
            solve = self.ss_discreta
            PIDf = self.PID_discreto
            h_new = self.dt
            h = self.dt
        else:
            error_a = deque([0] * 2)
            # self.filtroPID = Lowpassfilter(1 / self.dt, (self.N - 1) / np.pi)
            solve = self.rk_base
            PIDf = self.metodo_adaptativo

        if self.window.main.accionadorCheck.isChecked():
            acc_num = json.loads(self.window.main.numAccionador.text())
            acc_dem = json.loads(self.window.main.demAccionador.text())
            acc_system = ctrl.tf2ss(ctrl.TransferFunction(acc_num, acc_dem, delay=0))
            if ctrl.isdtime(
                    self.system, strict=True
            ) and self.window.main.SimulacionstackedWidget.currentIndex() == 0:
                acc_system = ctrl.sample_system(
                    acc_system, self.dt, self.window.main.tfcomboBox4.currentText())
            elif ctrl.isdtime(self.system, strict=True):
                acc_system = ctrl.sample_system(
                    acc_system, self.dt, self.window.main.sscomboBox4.currentText())

            acc_x = np.zeros_like(acc_system.B)

        if self.window.main.saturadorCheck.isChecked():
            lim_inferior = float(self.window.main.inferiorSaturador.text())
            lim_superior = float(self.window.main.superiorSaturador.text())

        if self.window.main.sensorCheck.isChecked():
            sensor_num = json.loads(self.window.main.numSensor.text())
            sensor_dem = json.loads(self.window.main.demSensor.text())
            sensor_system = ctrl.tf2ss(ctrl.TransferFunction(sensor_num, sensor_dem, delay=0))
            if ctrl.isdtime(
                    self.system, strict=True
            ) and self.window.main.SimulacionstackedWidget.currentIndex() == 0:
                acc_system = ctrl.sample_system(
                    sensor_system, self.dt, self.window.main.tfcomboBox4.currentText())
            elif ctrl.isdtime(self.system, strict=True):
                acc_system = ctrl.sample_system(
                    sensor_system, self.dt, self.window.main.sscomboBox4.currentText())
            sensor_x = np.zeros_like(sensor_system.B)
            salida2 = deque([0])

        if self.N*kd == 0:
            self.N = 50
            kd = 0
            pid = ctrl.tf2ss(ctrl.TransferFunction(
                    [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
        else:
            pid = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) * ctrl.TransferFunction(
                    [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))

        x_pid = np.zeros_like(pid.B)

        i = 0
        setpoint_window = 0
        Tiempo_list = [0]
        setpoint = [0]

        while tiempo < tiempo_total:

            if not isinstance(self.escalon, float):
                if tiempo + h >= max_tiempo[
                        setpoint_window] and setpoint_window < index_tbound:
                    setpoint_window += 1
                    print(tiempo)
                    print(u_value[setpoint_window])
                    print(h)
                u = u_value[setpoint_window]

            error = u - salida[i]

            if ctrl.isdtime(self.system, strict=True):
                sc_t, si_t, error_a = PIDf(error, h, si_t, error_a, kp, ki, kd)
            else:
                h, h_new, sc_t, x_pid = PIDf(pid, h, tiempo, max_tiempo[setpoint_window], x_pid, error, *self.solver_configuration)

            if self.window.main.accionadorCheck.isChecked():
                sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

            if self.window.main.saturadorCheck.isChecked():
                sc_t = min(max(sc_t, lim_inferior), lim_superior)

            y, x = solve(self.system, x, h, sc_t)

            sc_f.append(sc_t)

            if self.window.main.sensorCheck.isChecked():
                salida2.append(y)
                y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

            salida.append(y)

            if int(tiempo) % ten_percent == 0:
                self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

            setpoint.append(u)
            tiempo +=h
            Tiempo_list.append(tiempo)
            h = h_new
            i +=1

        if self.window.main.sensorCheck.isChecked():
            salida = salida2
        return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

    def run_fuzzy(self):

        if self.window.main.kpCheck.isChecked():
            kp = float(self.kp)
        else:
            kp = 0

        if self.window.main.kiCheck.isChecked():
            ki = float(self.ki)
        else:
            ki = 0

        if self.window.main.kdCheck.isChecked():
            kd = float(self.kd)
        else:
            kd = 0

        if len(self.fuzzy_path1) > 1 and self.esquema in [1, 2, 3, 4, 5, 6, 7, 8]:
            with open(self.fuzzy_path1, "r") as f:
                InputList1, OutputList1, RuleEtiquetas1 = json.load(f)

            fuzzy_c1 = FuzzyController(InputList1, OutputList1, RuleEtiquetas1)

        if len(self.fuzzy_path2) > 1 and self.esquema in [4]:
            with open(self.fuzzy_path2, "r") as f:
                InputList2, OutputList2, RuleEtiquetas2 = json.load(f)

            fuzzy_c2 = FuzzyController(InputList2, OutputList2, RuleEtiquetas2)

        if isinstance(self.system, ctrl.TransferFunction):
            self.system = ctrl.tf2ss(self.system)

        tiempo_total = self.Tiempo
        tiempo = 0

        if isinstance(self.escalon, float):
            u = self.escalon
            max_tiempo = [self.Tiempo]
        else:
            it = iter(self.escalon)
            u_value = [0]
            max_tiempo = []
            for i, valor in enumerate(it):
                max_tiempo.append(next(it))
                u_value.append(valor)
            index_tbound = len(max_tiempo)
            max_tiempo.append(tiempo_total)
            tiempo += max_tiempo[0] - 0.0000011

        ten_percent = int(tiempo_total * 20 / 100)

        if ten_percent == 0:
            ten_percent = 1

        x = np.zeros_like(self.system.B)
        h = 0.000001

        salida = deque([0])
        sc_f = deque([0])
        sc_t = 0
        si_t = 0

        if ctrl.isdtime(self.system, strict=True):
            error_a = deque([0] * 2)
            solve = self.ss_discreta
            PIDf = self.PID_discreto
            h_new = self.dt
            h = self.dt
        else:
            error_a = deque([0] * 2)
            # self.filtroPID = Lowpassfilter(1 / self.dt, (self.N - 1) / np.pi)
            solve = self.rk_base
            PIDf = self.metodo_adaptativo

        if self.window.main.accionadorCheck.isChecked():
            acc_num = json.loads(self.window.main.numAccionador.text())
            acc_dem = json.loads(self.window.main.demAccionador.text())
            acc_system = ctrl.tf2ss(ctrl.TransferFunction(acc_num, acc_dem, delay=0))
            if ctrl.isdtime(
                    self.system, strict=True
            ) and self.window.main.SimulacionstackedWidget.currentIndex() == 0:
                acc_system = ctrl.sample_system(
                    acc_system, self.dt, self.window.main.tfcomboBox4.currentText())
            elif ctrl.isdtime(self.system, strict=True):
                acc_system = ctrl.sample_system(
                    acc_system, self.dt, self.window.main.sscomboBox4.currentText())

            acc_x = np.zeros_like(acc_system.B)

        if self.window.main.saturadorCheck.isChecked():
            lim_inferior = float(self.window.main.inferiorSaturador.text())
            lim_superior = float(self.window.main.superiorSaturador.text())

        if self.window.main.sensorCheck.isChecked():
            sensor_num = json.loads(self.window.main.numSensor.text())
            sensor_dem = json.loads(self.window.main.demSensor.text())
            sensor_system = ctrl.tf2ss(
                ctrl.TransferFunction(sensor_num, sensor_dem, delay=0))
            if ctrl.isdtime(
                    self.system, strict=True
            ) and self.window.main.SimulacionstackedWidget.currentIndex() == 0:
                acc_system = ctrl.sample_system(
                    sensor_system, self.dt, self.window.main.tfcomboBox4.currentText())
            elif ctrl.isdtime(self.system, strict=True):
                acc_system = ctrl.sample_system(
                    sensor_system, self.dt, self.window.main.sscomboBox4.currentText())
            sensor_x = np.zeros_like(sensor_system.B)
            salida2 = deque([0])

        i = 0
        setpoint_window = 0
        Tiempo_list = [0]
        setpoint = [0]

        if self.esquema == 1:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)

            derivada2 = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))

            x_derivada2 = np.zeros_like(derivada2.B)

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[-1]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new2, d2_error, x_derivada2 = PIDf(derivada2, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada2, error, *self.solver_configuration)

                        h, h_new1, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)

                        h_new = min(h_new1, h_new2)
                    else:
                        d_error = 0
                        d2_error = 0

                sc_t = sc_t + fuzzy_c1.calcular_valor([error, d_error, d2_error],
                                                      [0] * 1)[0] * h

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 2:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                sc_t = sc_t + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 3:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                sc_t = fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0]

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 4:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)
            spi = 0

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                spi = spi + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h
                spd = fuzzy_c2.calcular_valor([error, d_error], [0] * 1)[0]
                sc_t = spi + spd

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 5:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)
            spi = 0

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                spi = spi + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h
                sc_t = spi + d_error*kd

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 6:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)
            spi = 0

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                        d_error = 0

                spi = spi + error*h
                spd = fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0]
                sc_t = spi*ki + spd

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 7:

            derivada = ctrl.tf2ss(
                ctrl.TransferFunction([1], [0.1, 1]) *
                ctrl.TransferFunction([self.N, 0], [1, self.N]))
            x_derivada = np.zeros_like(derivada.B)
            spi = 0

            if self.N == 0:
                h = 0.05
                h_new = h

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                kp, ki, kd = fuzzy_c1.calcular_valor([error, d_error], [0] * 3)

                spi = spi + error*h
                sc_t = spi*ki + d_error*kd + error*kp

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 8:

            if self.N*kd == 0:
                self.N = 50
                kd = 0
                pid = ctrl.tf2ss(ctrl.TransferFunction(
                        [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
            else:
                pid = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [0.1, 1]) * ctrl.TransferFunction(
                        [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))

            x_pid = np.zeros_like(pid.B)

            while tiempo < tiempo_total:
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                error = u - salida[i]

                if ctrl.isdtime(self.system, strict=True):
                    s_pid, si_t, error_a = PIDf(error, h, si_t, error_a, kp, ki, kd)
                else:
                    h, h_new, s_pid, x_pid = PIDf(pid, h, tiempo,
                                                 max_tiempo[setpoint_window], x_pid, error, *self.solver_configuration)

                s_fuzzy = fuzzy_c1.calcular_valor([error], [0] * 1)[0]

                sc_t = s_pid + s_fuzzy

                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                y, x = solve(self.system, x, h, sc_t)

                sc_f.append(sc_t)

                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                salida.append(y)

                if int(tiempo) % ten_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                setpoint.append(u)
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)


    def ss_discreta(self, ss, x, _, inputValue):
        x = np.dot(ss.A, x) + np.dot(ss.B, inputValue)
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        return y, x

    # def derivada_filtrada(self, vm, set_point, ts, error_anterior):
    #     error = set_point - vm
    #     error_derivativo = self.filtro.filtrar(error)
    #     s_derivativa1 = (error_derivativo - error_anterior[0]) / ts
    #     s_derivativa2 = (error_derivativo - 2 * error_anterior[0] + error_anterior[1]) / (ts**2)
    #     error_anterior.pop()
    #     error_anterior.appendleft(error_derivativo)
    #     return error, s_derivativa1, s_derivativa2, error_anterior

    # def PID(self, vm, set_point, ts, s_integral, error_anterior, kp, ki, kd):
    #     error = set_point - vm
    #     s_proporcional = error
    #     s_integral = s_integral + error*ts
    #     error_derivativo = self.filtroPID.filtrar(error)
    #     # error_derivativo = (error + sum(error_anterior))/(len(error_anterior) + 1)
    #     s_derivativa = (error_derivativo - error_anterior[0]) / ts
    #     s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
    #     error_anterior.pop()
    #     error_anterior.appendleft(error_derivativo)
    #     return s_control, s_integral, error_anterior

    def PID_discreto(self, error, ts, s_integral, error_anterior, kp, ki, kd):
        s_proporcional = error
        s_integral = s_integral + error*ts
        s_derivativa = (error - error_anterior[0]) / ts
        s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
        error_anterior.pop()
        error_anterior.appendleft(error)
        return s_control, s_integral, error_anterior

    def derivadas_discretas(self, error, ts, error_anterior):
        s_derivativa = (error-error_anterior[0]) / ts
        s_derivativa2 = (error - 2 * error_anterior[0] + error_anterior[1]) / (ts**2)
        error_anterior.pop()
        error_anterior.appendleft(error)
        return s_derivativa, s_derivativa2, error_anterior


# class Lowpassfilter:
#     """ Filtro pasa-bajo promediador"""

#     def __init__(self, fsampling, fcorte):
#         self.fsampling = fsampling
#         self.fcorte = fcorte
#         self.fcorte_normalizada = self.fcorte / self.fsampling

#         if self.fcorte_normalizada <= 0:
#             self.order = 0
#         else:
#             self.order = int(
#                 np.sqrt(0.196202 + pow(self.fcorte_normalizada, 2)) / self.fcorte_normalizada)
#             self.samples0 = self.order * deque([0])

#     def filtrar(self, entrada):

#         if self.order == 0:
#             return 0

#         self.samples0.pop()
#         self.samples0.appendleft(entrada)
#         salida = sum(self.samples0) / self.order

#         return salida


def system_creator_tf(self, numerador, denominador):
    if self.main.tfdelaycheckBox4.isChecked():
        delay = json.loads(self.main.tfdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.TransferFunction(numerador, denominador, delay=delay)

    if delay and not self.main.tfdiscretocheckBox4.isChecked():
        pade = ctrl.TransferFunction(*ctrl.pade(delay, int(self.main.padeOrder.text())))
        system = system*pade

    if self.main.tfdiscretocheckBox4.isChecked():
        system = ctrl.sample_system(system,
                                    self.dt,
                                    self.main.tfcomboBox4.currentText(),
                                    delay=delay)
        if delay:
            delayV = [0] * (int(delay / self.dt) + 1)
            delayV[0] = 1
            system = system * ctrl.TransferFunction([1], delayV, self.dt)

    return system


def system_creator_ss(self, A, B, C, D):
    if self.main.ssdelaycheckBox4.isChecked():
        delay = json.loads(self.main.ssdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.StateSpace(A, B, C, D, delay=delay)

    if delay and not self.main.ssdiscretocheckBox4.isChecked():
        pade = ctrl.TransferFunction(*ctrl.pade(delay, int(self.main.padeOrder.text())))
        system = system*pade

    if self.main.ssdiscretocheckBox4.isChecked():
        system = ctrl.sample_system(system,
                                    self.dt,
                                    self.main.sscomboBox4.currentText(),
                                    delay=delay)
        if delay:
            delayV = [0] * (int(delay / self.dt) + 1)
            delayV[0] = 1
            system = system * ctrl.TransferFunction([1], delayV, self.dt)

    return system
