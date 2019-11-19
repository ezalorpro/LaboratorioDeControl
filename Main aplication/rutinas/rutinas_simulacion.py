""" 
[Archivo que contiene la clase SimpleThread la cual ejecuta la simulacion de sistemas de control en hilo diferente al principal, esto se realiza de esta forma debido a que la simulacion puede tardar en algunos casos varios segundos, de ejecutarse en el hilo principal presentaria un comportamiento de bloqueo en la ventana principal] 
"""


from rutinas.rutinas_fuzzy import FuzzyController
from rutinas.rutinas_fuzzy import FISParser
from collections import deque
from PySide2 import QtCore

import controlmdf as ctrl
import numpy as np

import copy
import json


class SimpleThread(QtCore.QThread):
    """
    [Clase para realizar la simulacion de sistemas de control en un hilo diferente al principal]
    
    :param QThread: [Clase para crear un hilo paralelo al principal]
    :type QThread: [ObjectType]
    """

    finished = QtCore.Signal(object, list)
    update_progresBar = QtCore.Signal(object, float)
    error_gui = QtCore.Signal(object, int)

    def __init__(self, window, regresar, update_bar, error_gui, list_info, parent=None):
        """
        [Constructor para recibir las variables y funciones del hilo principal]
        
        :param window: [Objeto que contiene a la ventana principal]
        :type window: [object]
        :param regresar: [Funcion a la que regresa una vez terminada la simulacion, plot_final_results de simulacionHandler.py]
        :type regresar: [function]
        :param update_bar: [Funcion para actualizar la barra de progreso, update_progresBar_function de simulacionHandler.py]
        :type update_bar: [function]
        :param error_gui: [Funcion para mostrar los errores ocurridos durante la simulacion, error_gui de simulacionHandler.py]
        :type error_gui: [function]
        :param list_info: [Lista con toda la informacion necesaria]
        :type list_info: [list]
        :param parent: [Sin efecto], defaults to None
        :type parent: [NoneType], optional
        """

        QtCore.QThread.__init__(self, parent)

        self.window = window
        self.window.main.principalTab.setDisabled(True)
        self.window.main.progressBar.show()
        self.finished.connect(regresar)
        self.update_progresBar.connect(update_bar)
        self.error_gui.connect(error_gui)
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
        self.flag_filtro = self.list_info[13]

    def stop(self):
        """ [Funcion para detener el hilo] """
        self._isRunning = False

    def run(self):
        """ [Funcion a ejecutar cuando se hace el llamado a self.start()] """

        # PID Clasico
        if self.esquema in [0]:
            try:
                Tiempo, y, sc, u = self.run_pid()
                self.finished.emit(
                    self.window,
                    [Tiempo, y, sc, u, ctrl.isdtime(self.system, strict=True)])
                self.stop()
            except:
                self.error_gui.emit(self.window, 0)
                self.stop()

        # Esquemas difusos
        if self.esquema in [1,2,3,4,5,6,7,8]:
            try:
                Tiempo, y, sc, u = self.run_fuzzy()
                self.finished.emit(
                    self.window,
                    [Tiempo, y, sc, u, ctrl.isdtime(self.system, strict=True)])
                self.stop()

            except IndexError:
                self.error_gui.emit(self.window, 1)
                self.stop()

            except AssertionError:
                self.error_gui.emit(self.window, 2)
                self.stop()

    def run_pid(self):
        """ [Funcion para realizar la simulacion de sistemas de control con controlador PID clasico] """

        # Captura de las ganancias
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

        # Transformando a ecuaciones de espacio de estados en caso de que sea funcion de transferencia
        if isinstance(self.system, ctrl.TransferFunction):
            self.system = ctrl.tf2ss(self.system)

        x = np.zeros_like(self.system.B)

        tiempo_total = self.Tiempo
        tiempo = 0

        if isinstance(self.escalon, float):
            # Escalon simple
            u = self.escalon
            max_tiempo = [self.Tiempo]
        else:
            # Escalon avanzado
            it = iter(self.escalon)
            u_value = deque([0])
            max_tiempo = []
            for i, valor in enumerate(it):
                max_tiempo.append(next(it))
                u_value.append(valor)
            index_tbound = len(max_tiempo)
            max_tiempo.append(tiempo_total)

            # Necesario para evitar tamaños de paso excesivos dado el algoritmo adaptativo
            if ctrl.isdtime(self.system, strict=True):
                tiempo += max_tiempo[0] - self.dt - self.dt/10
            else:
                tiempo += max_tiempo[0] - 0.0000011

        # Representacion del 20% de la simulacion
        twenty_percent = int(tiempo_total * 20 / 100)
        if twenty_percent == 0:
            twenty_percent = 1

        h = 0.000001  # Tamaño de paso inicial
        salida = deque([0])  # Lista de salida, se utiliza deque para mejorar la velocidad
        sc_f = deque([0])  # Lista de la señal de control, se utiliza deque para mejorar la velocidad
        sc_t = 0  # Señal de control cambiante
        si_t = 0  # Acumulador de la señal integral

        # Distincion entre continuo y discreto
        if ctrl.isdtime(self.system, strict=True):
            error_a = deque([0] * 2)
            solve = self.ss_discreta
            PIDf = self.PID_discreto
            h_new = self.dt
            h = self.dt
        else:
            error_a = deque([0] * 2)
            solve = self.rk_base
            PIDf = self.metodo_adaptativo

        # En caso de que se habilite el accionador
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

        # En caso de que se habilite el saturador
        if self.window.main.saturadorCheck.isChecked():
            lim_inferior = float(self.window.main.inferiorSaturador.text())
            lim_superior = float(self.window.main.superiorSaturador.text())

        # En caso de que se habilite el sensor
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
            # N debe mantenerce debido al algoritmo utilizado por la libreria de control para llevar de funcion de transferencia a ecuaciones de espacio de estados
            # Controlador PID con la forma:
            #    PID = kp + ki/s + (kd*N*s/(s + N))
            
            self.N = 50
            kd = 0
            pid = ctrl.tf2ss(ctrl.TransferFunction(
                    [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
        
        elif not self.flag_filtro:
            # Controlador PID con la forma:
            #    PID = kp + ki/s + (kd*N*s/(s + N))
            
            pid = ctrl.tf2ss(ctrl.TransferFunction(
                    [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
        
        else:
            # Controlador PID con la forma:
            #    PID = kp + ki/s + (kd*N*s/(s + N))*(1/(10/(N*kd) + 1))

            pid = ctrl.tf2ss(
                ctrl.TransferFunction([
                    10 * kp,
                    self.N**2 * kd**2 + self.N * kd * kp + 10 * self.N * kp + 10*ki,
                    self.N**2 * kd * kp + kd * self.N * ki + 10 * self.N * ki,
                    self.N**2 * kd * ki
                ], [10, 10 * self.N + self.N * kd, self.N**2 * kd, 0]))

        x_pid = np.zeros_like(pid.B)

        i = 0
        setpoint_window = 0
        Tiempo_list = [0]
        setpoint = [0]

        # Inicio de la simulacion
        while tiempo < tiempo_total:

            # Para alternar los valores del setpoint avanzado
            if not isinstance(self.escalon, float):
                if tiempo + h >= max_tiempo[
                        setpoint_window] and setpoint_window < index_tbound:
                    setpoint_window += 1
                u = u_value[setpoint_window]

            # Calculo del error
            error = u - salida[i]

            # Distincion de PID entre continuo y discreto
            if ctrl.isdtime(self.system, strict=True):
                sc_t, si_t, error_a = PIDf(error, h, si_t, error_a, kp, ki, kd)
            else:
                h, h_new, sc_t, x_pid = PIDf(pid, h, tiempo, max_tiempo[setpoint_window], x_pid, error, *self.solver_configuration)

            # En caso de que se habilite el accionador
            if self.window.main.accionadorCheck.isChecked():
                sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

            # En caso de que se habilite el saturador
            if self.window.main.saturadorCheck.isChecked():
                sc_t = min(max(sc_t, lim_inferior), lim_superior)

            # Salida del sistema
            y, x = solve(self.system, x, h, sc_t)

            # Acumulacion de la señal de control
            sc_f.append(sc_t)

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida2.append(y)
                y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

            # Acumulacion de la salida
            salida.append(y)

            # Actualizacion de la barra de progreso cada 20% de avance
            if int(tiempo) % twenty_percent == 0:
                self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

            # Acumulacion del setpoint
            setpoint.append(u)

            # Acumulacion del tiempo
            tiempo +=h
            Tiempo_list.append(tiempo)
            h = h_new
            i +=1

        # En caso de que se habilite el sensor
        if self.window.main.sensorCheck.isChecked():
            salida = salida2

        return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

    def run_fuzzy(self):
        """ [Funcion para realizar la simulacion de sistemas de control de esquemas difusos] """

        # Captura de las ganancias
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

        # Creacion del controlador difuso
        if len(self.fuzzy_path1) > 1 and self.esquema in [1, 2, 3, 4, 5, 6, 7, 8]:
            if '.json' in self.fuzzy_path1:
                with open(self.fuzzy_path1, "r") as f:
                    InputList1, OutputList1, RuleEtiquetas1 = json.load(f)
            else:
                temp_parser = FISParser(self.fuzzy_path1)
                try:
                    InputList1, OutputList1, RuleEtiquetas1 = temp_parser.fis_to_json()
                except TypeError:
                    raise IndexError

            try:
                controlador_validator(self, self.esquema, InputList1, OutputList1, RuleEtiquetas1)
            except AssertionError:
                raise AssertionError

            fuzzy_c1 = FuzzyController(InputList1, OutputList1, RuleEtiquetas1)

        # Creacion del controlador difuso 2 (PD)
        if len(self.fuzzy_path2) > 1 and self.esquema in [4]:
            if '.json' in self.fuzzy_path2:
                with open(self.fuzzy_path2, "r") as f:
                    InputList2, OutputList2, RuleEtiquetas2 = json.load(f)
            else:
                temp_parser = FISParser(self.fuzzy_path2)
                try:
                    InputList2, OutputList2, RuleEtiquetas2 = temp_parser.fis_to_json()
                except TypeError:
                    raise IndexError

            try:
                controlador_validator(self, self.esquema, InputList2, OutputList2, RuleEtiquetas2)
            except AssertionError:
                raise AssertionError

            fuzzy_c2 = FuzzyController(InputList2, OutputList2, RuleEtiquetas2)

        # Transformando a ecuaciones de espacio de estados en caso de que sea funcion de transferencia
        if isinstance(self.system, ctrl.TransferFunction):
            self.system = ctrl.tf2ss(self.system)

        x = np.zeros_like(self.system.B)

        tiempo_total = self.Tiempo
        tiempo = 0

        if isinstance(self.escalon, float):
            # Escalon simple
            u = self.escalon
            max_tiempo = [self.Tiempo]
        else:
            # Escalon avanzado
            it = iter(self.escalon)
            u_value = [0]
            max_tiempo = []
            for i, valor in enumerate(it):
                max_tiempo.append(next(it))
                u_value.append(valor)
            index_tbound = len(max_tiempo)
            max_tiempo.append(tiempo_total)

            # Necesario para evitar tamaños de paso excesivos dado el algoritmo adaptativo
            tiempo += max_tiempo[0] - 0.0000011

        # Representacion del 20% de la simulacion
        twenty_percent = int(tiempo_total * 20 / 100)
        if twenty_percent == 0:
            twenty_percent = 1

        h = 0.000001  # Tamaño de paso inicial
        salida = deque([0])  # Lista de salida, se utiliza deque para mejorar la velocidad
        sc_f = deque([0])  # Lista de la señal de control, se utiliza deque para mejorar la velocidad
        sc_t = 0  # Señal de control cambiante
        si_t = 0  # Acumulador de la señal integral

        # Distincion entre continuo y discreto
        if ctrl.isdtime(self.system, strict=True):
            error_a = deque([0] * 2)
            solve = self.ss_discreta
            PIDf = self.PID_discreto
            h_new = self.dt
            h = self.dt
        else:
            error_a = deque([0] * 2)
            solve = self.rk_base
            PIDf = self.metodo_adaptativo

        # En caso de que se habilite el accionador
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

        # En caso de que se habilite el saturador
        if self.window.main.saturadorCheck.isChecked():
            lim_inferior = float(self.window.main.inferiorSaturador.text())
            lim_superior = float(self.window.main.superiorSaturador.text())

        # En caso de que se habilite el sensor
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

        # Particularizacion por cada esquema
        if self.esquema == 1:  # PID difuso

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)

                # Para la segunda derivada del error
                derivada2 = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada2 = np.zeros_like(derivada2.B)
            
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)

                # Para la segunda derivada del error
                derivada2 = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada2 = np.zeros_like(derivada2.B)
                
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                derivada2 = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada2 = np.zeros_like(derivada2.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[-1]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new2, d2_error, x_derivada2 = PIDf(derivada2, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada2, error, *self.solver_configuration)

                        htemp, h_new1, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                        h = min(h, htemp)
                        h_new = min(h_new1, h_new2)
                    else:
                        d_error = 0
                        d2_error = 0

                # Calculo del controaldor difuso
                sc_t = sc_t + fuzzy_c1.calcular_valor([error, d_error, d2_error],
                                                      [0] * 1)[0] * h

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 2:  # PI difuso

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo del controlador difuso
                sc_t = sc_t + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 3:  # PD difuso

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
            
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo del controlador difuso
                sc_t = fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0]

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 4:  # PI difuso + PD difuso

            spi = 0

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
            
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo de los controaldores difusos
                spi = spi + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h
                spd = fuzzy_c2.calcular_valor([error, d_error], [0] * 1)[0]
                sc_t = spi + spd

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window, int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo +=h
                Tiempo_list.append(tiempo)
                h = h_new
                i +=1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 5:  # PI difuso + D clasico

            spi = 0

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
            
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo del controlador difuso
                spi = spi + fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0] * h
                sc_t = spi + d_error*kd

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 6:  # PD difuso + I Clasico

            spi = 0

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
            
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                           max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo del controaldor difuso
                spi = spi + error*h
                spd = fuzzy_c1.calcular_valor([error, d_error], [0] * 1)[0]
                sc_t = spi*ki + spd

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 7:  # Programador de ganancias

            spi = 0

            if not self.N == 0 and self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([1], [10 / self.N, 1]) *
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
                
            elif not self.N == 0 and not self.flag_filtro:
                # Para la derivada del error
                derivada = ctrl.tf2ss(
                    ctrl.TransferFunction([self.N, 0], [1, self.N]))
                x_derivada = np.zeros_like(derivada.B)
            
            else:
                # En caso de que N sea igual a cero
                derivada = ctrl.tf2ss(ctrl.TransferFunction([0], [1]))
                x_derivada = np.zeros_like(derivada.B)
                h = 0.05
                h_new = h

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    d_error, d2_error, error_a = self.derivadas_discretas(error, h, error_a)
                else:
                    if self.N != 0:
                        h, h_new, d_error, x_derivada = PIDf(derivada, h, tiempo,
                                                            max_tiempo[setpoint_window], x_derivada, error, *self.solver_configuration)
                    else:
                        d_error = 0

                # Calculo del controaldor difuso
                kp, ki, kd = fuzzy_c1.calcular_valor([error, d_error], [0] * 3)

                spi = spi + error*h
                sc_t = spi*ki + d_error*kd + error*kp

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)

        if self.esquema == 8:  # PID clasico + difuso simple

            if self.N*kd == 0:
                # N debe mantenerce debido al algoritmo utilizado por la libreria de control para llevar de funcion de transferencia a ecuaciones de espacio de estados
                # Controlador PID con la forma:
                #    PID = kp + ki/s + (kd*N*s/(s + N))
                
                self.N = 50
                kd = 0
                pid = ctrl.tf2ss(ctrl.TransferFunction(
                        [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
            
            elif not self.flag_filtro:
                # Controlador PID con la forma:
                #    PID = kp + ki/s + (kd*N*s/(s + N))
                
                pid = ctrl.tf2ss(ctrl.TransferFunction(
                        [self.N * kd + kp, self.N * kp + ki, self.N * ki], [1, self.N, 0]))
            
            else:
                # Controlador PID con la forma:
                #    PID = kp + ki/s + (kd*N*s/(s + N))*(1/(10/(N*kd) + 1))

                pid = ctrl.tf2ss(
                    ctrl.TransferFunction([
                        10 * kp,
                        self.N**2 * kd**2 + self.N * kd * kp + 10 * self.N * kp + 10*ki,
                        self.N**2 * kd * kp + kd * self.N * ki + 10 * self.N * ki,
                        self.N**2 * kd * ki
                    ], [10, 10 * self.N + self.N * kd, self.N**2 * kd, 0]))

            x_pid = np.zeros_like(pid.B)

            # Inicio de la simulacion
            while tiempo < tiempo_total:

                # Para alternar los valores del setpoint avanzado
                if not isinstance(self.escalon, float):
                    if tiempo + h >= max_tiempo[
                            setpoint_window] and setpoint_window < index_tbound:
                        setpoint_window += 1
                    u = u_value[setpoint_window]

                # Calculo del error
                error = u - salida[i]

                # Distincion entre continuo y discreto
                if ctrl.isdtime(self.system, strict=True):
                    s_pid, si_t, error_a = PIDf(error, h, si_t, error_a, kp, ki, kd)
                else:
                    h, h_new, s_pid, x_pid = PIDf(pid, h, tiempo,
                                                 max_tiempo[setpoint_window], x_pid, error, *self.solver_configuration)

                # calculo del controlador difuso
                s_fuzzy = fuzzy_c1.calcular_valor([error], [0] * 1)[0]

                # Suma del controlador clasico y difuso
                sc_t = s_pid + s_fuzzy

                # En caso de que se habilite el accionador
                if self.window.main.accionadorCheck.isChecked():
                    sc_t, acc_x = solve(acc_system, acc_x, h, sc_t)

                # En caso de que se habilite el saturador
                if self.window.main.saturadorCheck.isChecked():
                    sc_t = min(max(sc_t, lim_inferior), lim_superior)

                # Salida del sistema
                y, x = solve(self.system, x, h, sc_t)

                # Acumulacion de la señal de control
                sc_f.append(sc_t)

                # En caso de que se habilite el sensor
                if self.window.main.sensorCheck.isChecked():
                    salida2.append(y)
                    y, sensor_x = solve(sensor_system, sensor_x, h, salida2[-1])

                # Acumulacion de la salida
                salida.append(y)

                # Actualizacion de la barra de progreso cada 20% de avance
                if int(tiempo) % twenty_percent == 0:
                    self.update_progresBar.emit(self.window,
                                                int(tiempo) * 100 / tiempo_total)

                # Acumulacion del setpoint
                setpoint.append(u)

                # Acumulacion del tiempo
                tiempo += h
                Tiempo_list.append(tiempo)
                h = h_new
                i += 1

            # En caso de que se habilite el sensor
            if self.window.main.sensorCheck.isChecked():
                salida = salida2

            return copy.deepcopy(Tiempo_list), copy.deepcopy(salida), copy.deepcopy(sc_f), copy.deepcopy(setpoint)


    def ss_discreta(self, ss, x, _, inputValue):
        """
        [Funcion para calcular la respuesta del sistema por medio de la representacion discreta de las ecuaciones de espacio de estados]
        
        :param ss: [Representacion del sistema]
        :type ss: [LTI]
        :param x: [Vector de estado]
        :type x: [numpyArray]
        :param _: [No importa]
        :type _: [float]
        :param inputValue: [Valor de entrada al sistema]
        :type inputValue: [float]
        """
        y = np.dot(ss.C, x) + np.dot(ss.D, inputValue)
        x = np.dot(ss.A, x) + np.dot(ss.B, inputValue)
        return y, x

    def PID_discreto(self, error, ts, s_integral, error_anterior, kp, ki, kd):
        """
        [Funcion para calcular el PID en forma discreta]
        
        :param error: [Señal de error]
        :type error: [float]
        :param ts: [Periodo de muestreo]
        :type ts: [float]
        :param s_integral: [Acumulador de la señal integral]
        :type s_integral: [float]
        :param error_anterior: [deque con el error anterior]
        :type error_anterior: [deque Object]
        :param kp: [Ganancia proporcional]
        :type kp: [float]
        :param ki: [Ganancia integral]
        :type ki: [float]
        :param kd: [Ganancia derivativa]
        :type kd: [float]
        """
        s_proporcional = error
        s_integral = s_integral + error*ts
        s_derivativa = (error - error_anterior[0]) / ts
        s_control = s_proporcional*kp + s_integral*ki + s_derivativa*kd
        error_anterior.pop()
        error_anterior.appendleft(error)
        return s_control, s_integral, error_anterior

    def derivadas_discretas(self, error, ts, error_anterior):
        """
        [Funcion para calcular la derivada del error y la segunda derivada del error]
        
        :param error: [Señal de error]
        :type error: [float]
        :param ts: [Periodo de muestreo]
        :type ts: [float]
        :param error_anterior: [deque con el error anterior]
        :type error_anterior: [deque Object]
        """
        s_derivativa = (error-error_anterior[0]) / ts
        s_derivativa2 = (error - 2 * error_anterior[0] + error_anterior[1]) / (ts**2)
        error_anterior.pop()
        error_anterior.appendleft(error)
        return s_derivativa, s_derivativa2, error_anterior


def system_creator_tf(self, numerador, denominador):
    """
    [Funcion para la creacion del sistema a partir de los coeficientes del numerador y del denominador de la funcion de transferencia]
    
    :param numerador: [Coeficientes del numerador]
    :type numerador: [list]
    :param denominador: [Coeficientes del denominador]
    :type denominador: [list]
    """

    if self.main.tfdelaycheckBox4.isChecked():
        delay = json.loads(self.main.tfdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.TransferFunction(numerador, denominador, delay=delay)

    # Agregando delay con aproximacion por pade para sistemas continuos
    if delay and not self.main.tfdiscretocheckBox4.isChecked():
        pade = ctrl.TransferFunction(*ctrl.pade(delay, int(self.main.padeOrder.text())))
        system = system*pade

    # En caso de que el sistema sea discreto
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
    """
    [Funcion para la creacion del sistema a partir de la matriz de estado, matriz de entrada, matriz de salida y la matriz de transmision directa la ecuacion de espacio de estados]
    
    :param A: [Matriz de estados]
    :type A: list
    :param B: [Matriz de entrada]
    :type B: [list]
    :param C: [Matriz de salida]
    :type C: [list]
    :param D: [Matriz de transmision directa]
    :type D: [list]
    """

    if self.main.ssdelaycheckBox4.isChecked():
        delay = json.loads(self.main.ssdelayEdit4.text())
    else:
        delay = 0

    system = ctrl.StateSpace(A, B, C, D, delay=delay)

    # Agregando delay con aproximacion por pade para sistemas continuos
    if delay and not self.main.ssdiscretocheckBox4.isChecked():
        pade = ctrl.TransferFunction(*ctrl.pade(delay, int(self.main.padeOrder.text())))
        system = system*pade

    # En caso de que el sistema sea discreto
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


def controlador_validator(self, esquema, InputList, OutputList, RuleEtiquetas):
    """
    [Funcion para validar los controladores difusos con respecto al esquema de control seleccionado]
    
    :param esquema: [Esquema de control seleccionado representado por un valor]
    :type esquema: [int]
    :param InputList: [Lista de entradas]
    :type InputList: [list]
    :param OutputList: [Lista de salidas]
    :type OutputList: [list]
    :param RuleEtiquetas: [Lista con set de reglas]
    :type RuleEtiquetas: [list]
    """
    
    if esquema == 1: # PID difuso
        if len(InputList) == 3 and len(OutputList) == 1 and len(RuleEtiquetas) != 0:
            return
        else:
            raise AssertionError

    if esquema in [2, 3, 4, 5, 6]:  # PI difuso, PD difuso, PI difuso + PD difuso, PI difuso + D Clasico, PD difuso + I Clasico
        if len(InputList) == 2 and len(OutputList) == 1 and len(RuleEtiquetas) != 0:
            return
        else:
            raise AssertionError

    if esquema == 7:  # Programador de ganancias
        if len(InputList) == 2 and len(OutputList) == 3 and len(RuleEtiquetas) != 0:
            return
        else:
            raise AssertionError

    if esquema == 8:  # PID Clasico + Difuso simple
        if len(InputList) == 1 and len(OutputList) == 1 and len(RuleEtiquetas) != 0:
            return
        else:
            raise AssertionError