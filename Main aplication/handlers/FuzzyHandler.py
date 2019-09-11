from handlers.modificadorMf import update_definicionmf, validacion_mf
from rutinas.rutinas_fuzzy import FuzzyController
from rutinas.rutinas_fuzzy import FISParser
from PySide2 import QtCore, QtGui, QtWidgets
import numpy as np
import copy
import json


def FuzzyHandler(self):
    self.EntradasTab = self.main.fuzzyTabWidget.widget(1)
    self.SalidasTab = self.main.fuzzyTabWidget.widget(2)
    self.ReglasTab = self.main.fuzzyTabWidget.widget(3)
    self.PruebaTab = self.main.fuzzyTabWidget.widget(4)
    self.RespuestaTab = self.main.fuzzyTabWidget.widget(5)

    self.main.guardarFuzzButton.setDisabled(True)
    self.main.guardarComoFuzzButton.setDisabled(True)
    self.main.exportarFuzzButton.setDisabled(True)

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)

    self.InputList = []
    self.OutputList = []
    self.RuleList = []
    self.RuleEtiquetas = []
    self.vector_rotacion = [-0.25, 0, 0.25, 0.5, 0.75, 1, 1.25]
    self.rotacion_windowIn = 2
    self.rotacion_windowOut = 2
    self.fuzzInitController = FuzzyController
    self.parser = FISParser

    crear_vectores_de_widgets(self)

    for i_f, o_f, it_f, ot_f, f2d, f3d in zip(
        self.inframes,
        self.outframes,
        self.intestframes,
        self.outtestframes,
        self.respuesta2dframes,
        self.respuesta3dframes,
    ):
        i_f.hide()
        o_f.hide()
        it_f.hide()
        ot_f.hide()
        f2d.hide()
        f3d.hide()

    self.main.imagenEsquemas.setPixmap(
        QtGui.QPixmap(":/imagenes/imagenes/sinEsquema.png")
    )
    self.main.estrucNumberInputs.currentIndexChanged.connect(
        lambda: imagen_entradas(self)
    )
    self.main.estrucNumberOutputs.currentIndexChanged.connect(
        lambda: imagen_salidas(self)
    )
    self.main.fuzzyEsquemasCheck.clicked["bool"].connect(lambda: check_esquema_show(self))
    self.main.fuzzyEsquemas.currentIndexChanged.connect(lambda: show_esquema(self))
    self.main.generarFuzzyButton.clicked.connect(lambda: crear_tabs(self))
    self.main.guardarFuzzButton.clicked.connect(lambda: guardar_controlador(self))
    self.main.cargarFuzzButton.clicked.connect(lambda: cargar_controlador(self))
    self.main.guardarComoFuzzButton.clicked.connect(lambda: guardarcomo_controlador(self))
    self.main.exportarFuzzButton.clicked.connect(lambda: exportar_fis(self))

    self.main.inputNumber.currentIndexChanged.connect(lambda: seleccion_entrada(self))
    self.main.inputNombre.editingFinished.connect(lambda: nombre_entrada(self))
    self.main.inputEtiquetasNum.editingFinished.connect(
        lambda: numero_de_etiquetas_in(self)
    )
    self.main.inputRange.editingFinished.connect(lambda: rango_in(self))

    self.main.etiquetaNumIn.currentIndexChanged.connect(
        lambda: seleccion_etiqueta_in(self)
    )
    self.main.etiquetaNombreIn.editingFinished.connect(lambda: nombre_etiqueta_in(self))
    self.main.etiquetaMfIn.currentIndexChanged.connect(lambda: seleccion_mf_in(self))
    self.main.etiquetaDefinicionIn.editingFinished.connect(lambda: definicion_in(self))

    self.main.outputNumber.currentIndexChanged.connect(lambda: seleccion_salida(self))
    self.main.outputNombre.editingFinished.connect(lambda: nombre_salida(self))
    self.main.outputEtiquetasNum.editingFinished.connect(
        lambda: numero_de_etiquetas_out(self)
    )
    self.main.outputRange.editingFinished.connect(lambda: rango_out(self))
    self.main.defuzzMethodOut.currentIndexChanged.connect(lambda: defuzz_metodo(self))

    self.main.etiquetaNumOut.currentIndexChanged.connect(
        lambda: seleccion_etiqueta_out(self)
    )
    self.main.etiquetaNombreOut.editingFinished.connect(lambda: nombre_etiqueta_out(self))
    self.main.etiquetaMfOut.currentIndexChanged.connect(lambda: seleccion_mf_out(self))
    self.main.etiquetaDefinicionOut.editingFinished.connect(lambda: definicion_out(self))

    self.main.fuzzyTabWidget.currentChanged.connect(lambda: rule_list_visualizacion(self))
    self.main.rulelistWidget.currentRowChanged.connect(
        lambda: seleccionar_etiquetas(self)
    )
    self.main.ruleAgregarButton.clicked.connect(lambda: rule_list_agregar(self))
    self.main.ruleEliminarButton.clicked.connect(lambda: rule_list_eliminar(self))
    self.main.ruleCambiarButton.clicked.connect(lambda: rule_list_cambiar(self))
    self.main.ruleCrearButton.clicked.connect(lambda: crear_controlador(self))

    for slider in self.intestsliders:
        slider.valueChanged.connect(lambda: prueba_input(self))


def imagen_entradas(self):
    ni = self.main.estrucNumberInputs.currentIndex() + 1
    self.main.imagenInputs.setPixmap(
        QtGui.QPixmap(":/imagenes/imagenes/entrada" + str(ni) + ".png")
    )


def imagen_salidas(self):
    no = self.main.estrucNumberOutputs.currentIndex() + 1
    self.main.imagenOutputs.setPixmap(
        QtGui.QPixmap(":/imagenes/imagenes/salida" + str(no) + ".png")
    )


def check_esquema_show(self):
    if not self.main.fuzzyEsquemasCheck.isChecked():
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/sinEsquema.png")
        )
        imagen_entradas(self)
        imagen_salidas(self)
    else:
        show_esquema(self)


def show_esquema(self):
    if self.main.fuzzyEsquemas.currentIndex() == 0:
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pidDifuso.png")
        )
        self.main.imagenInputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/entrada3.png")
        )
        self.main.imagenOutputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/salida1.png")
        )
    elif self.main.fuzzyEsquemas.currentIndex() == 1:
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/piDifuso.png"))
        self.main.imagenInputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/entrada2.png")
        )
        self.main.imagenOutputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/salida1.png")
        )
    elif self.main.fuzzyEsquemas.currentIndex() == 2:
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pdDifuso.png"))
        self.main.imagenInputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/entrada2.png")
        )
        self.main.imagenOutputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/salida1.png")
        )
    elif self.main.fuzzyEsquemas.currentIndex() == 3:
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/GainScheduler.png"))
        self.main.imagenInputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/entrada2.png")
        )
        self.main.imagenOutputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/salida3.png")
        )
    elif self.main.fuzzyEsquemas.currentIndex() == 4:
        self.main.imagenEsquemas.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/pidplusDifuso.png"))
        self.main.imagenInputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/entrada1.png")
        )
        self.main.imagenOutputs.setPixmap(
            QtGui.QPixmap(":/imagenes/imagenes/salida1.png")
        )


def crear_tabs(self):
    if not self.main.fuzzyEsquemasCheck.isChecked():
        self.setWindowTitle(
            "Laboratorio de sistemas de control - Nuevo controlador sin guardar*"
        )

        self.main.inputNumber.blockSignals(True)
        self.main.outputNumber.blockSignals(True)
        self.main.inputNombre.setReadOnly(False)
        self.main.outputNombre.setReadOnly(False)

        self.current_file = ""
        self.InputList = []
        self.OutputList = []
        self.RuleList = []
        self.RuleEtiquetas = []

        self.main.guardarFuzzButton.setEnabled(True)
        self.main.guardarComoFuzzButton.setEnabled(True)
        self.main.exportarFuzzButton.setEnabled(True)

        self.main.fuzzyTabWidget.removeTab(5)
        self.main.fuzzyTabWidget.removeTab(4)
        self.main.fuzzyTabWidget.removeTab(3)
        self.main.fuzzyTabWidget.removeTab(2)
        self.main.fuzzyTabWidget.removeTab(1)

        self.main.fuzzyTabWidget.addTab(self.EntradasTab, "Entradas")
        self.main.fuzzyTabWidget.addTab(self.SalidasTab, "Salidas")
        self.main.fuzzyTabWidget.addTab(self.ReglasTab, "Reglas")

        NumeroEntradas = int(self.main.estrucNumberInputs.currentText())
        NumeroSalidas = int(self.main.estrucNumberOutputs.currentText())

        self.main.inputNumber.clear()
        self.main.outputNumber.clear()

        for i in range(NumeroEntradas):
            self.main.inputNumber.insertItem(i, str(i + 1))
            temp_dic = inputDic_creator(self, NumeroEntradas, i)
            self.InputList.append(temp_dic)
            ini_range_etiquetas = np.arange(-20, 21, 20 / 2).tolist()
            window = 0
            for j in range(self.InputList[i]["numeroE"]):
                self.InputList[i]["etiquetas"][j] = EtiquetasDic_creator(
                    self, j, ini_range_etiquetas[window:window + 3]
                )
                window += 1

        for i in range(NumeroSalidas):
            self.main.outputNumber.insertItem(i, str(i + 1))
            temp_dic = outputDic_creator(self, NumeroSalidas, i)
            self.OutputList.append(temp_dic)
            ini_range_etiquetas = np.arange(-20, 21, 20 / 2).tolist()
            window = 0
            for j in range(self.OutputList[i]["numeroE"]):
                self.OutputList[i]["etiquetas"][j] = EtiquetasDic_creator(
                    self, j, ini_range_etiquetas[window:window + 3]
                )
                window += 1

        self.main.inputNumber.blockSignals(False)
        self.main.outputNumber.blockSignals(False)

        self.fuzzController = self.fuzzInitController(self.InputList, self.OutputList)

        seleccion_entrada(self)
        seleccion_salida(self)

        self.fuzzController.graficar_mf_in(self, 0)
        self.fuzzController.graficar_mf_out(self, 0)
    else:
        cargar_esquema(self)


def inputDic_creator(self, NumeroEntradas, i):
    inputDic = {
        "nombre": "entrada" + str(i + 1),
        "numeroE": 3,
        "etiquetas": [0] * 3,
        "rango": [-10, 10],
    }
    return inputDic


def outputDic_creator(self, NumeroSalidas, i):
    outputDic = {
        "nombre": "salida" + str(i + 1),
        "numeroE": 3,
        "etiquetas": [0] * 3,
        "rango": [-10, 10],
        "metodo": "centroid",
    }
    return outputDic


def EtiquetasDic_creator(self, j, erange):
    etiquetaDic = {
        "nombre": "etiqueta" + str(j + 1),
        "mf": "trimf",
        "definicion": round_list(erange),
    }
    return etiquetaDic


def cargar_esquema(self):
    path = self.resource_path(
        "Esquemas/" + self.main.fuzzyEsquemas.currentText() + ".json"
    )
    with open(path, "r") as f:
        self.InputList, self.OutputList, self.RuleEtiquetas = json.load(f)

    self.main.inputNombre.setReadOnly(True)
    self.main.outputNombre.setReadOnly(True)

    self.main.guardarFuzzButton.setEnabled(True)
    self.main.guardarComoFuzzButton.setEnabled(True)
    self.main.exportarFuzzButton.setEnabled(True)

    self.current_file = ""

    self.main.inputNumber.blockSignals(True)
    self.main.outputNumber.blockSignals(True)

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)

    self.main.fuzzyTabWidget.addTab(self.EntradasTab, "Entradas")
    self.main.fuzzyTabWidget.addTab(self.SalidasTab, "Salidas")
    self.main.fuzzyTabWidget.addTab(self.ReglasTab, "Reglas")

    self.main.inputNumber.clear()
    self.main.outputNumber.clear()

    for i in range(len(self.InputList)):
        self.main.inputNumber.insertItem(i, str(i + 1))

    for i in range(len(self.OutputList)):
        self.main.outputNumber.insertItem(i, str(i + 1))

    self.main.inputNumber.blockSignals(False)
    self.main.outputNumber.blockSignals(False)

    self.fuzzController = self.fuzzInitController(
        self.InputList, self.OutputList, self.RuleEtiquetas
    )
    self.RuleList = copy.deepcopy(self.fuzzController.rulelist)

    seleccion_entrada(self)
    seleccion_salida(self)

    self.fuzzController.graficar_mf_in(self, 0)
    self.fuzzController.graficar_mf_out(self, 0)

    self.setWindowTitle(
        "Laboratorio de sistemas de control - Nuevo controlador sin guardar*"
    )


def guardar_controlador(self):
    if len(self.current_file) > 0 and not '.fis' in self.current_file:
        with open(self.current_file, "w") as f:
            json.dump([self.InputList, self.OutputList, self.RuleEtiquetas], f, indent=4)
    else:
        guardarcomo_controlador(self)


def guardarcomo_controlador(self):
    path_guardar = QtWidgets.QFileDialog.getSaveFileName(filter="JSON (*.json)")
    if len(path_guardar[0]) > 1:
        self.current_file = path_guardar[0]
        with open(path_guardar[0], "w") as f:
            json.dump([self.InputList, self.OutputList, self.RuleEtiquetas], f, indent=4)
            self.setWindowTitle(
                "Laboratorio de sistemas de control - " + path_guardar[0].split("/")[-1]
            )


def exportar_fis(self):
    path_guardar = QtWidgets.QFileDialog.getSaveFileName(filter="FIS (*.fis)")
    if len(path_guardar[0]) > 1:
        self.current_file = path_guardar[0]
        temp_parser = self.parser(self.current_file, self.InputList, self.OutputList, self.RuleEtiquetas)
        temp_parser.json_to_fis()
        self.setWindowTitle("Laboratorio de sistemas de control - " +
                            path_guardar[0].split("/")[-1])


def cargar_controlador(self):
    self.path_cargar = QtWidgets.QFileDialog.getOpenFileName(filter="JSON/FIS (*.json *.fis)")
    if len(self.path_cargar[0]) > 1:

        if '.json' in self.path_cargar[0]:
            with open(self.path_cargar[0], "r") as f:
                self.InputList, self.OutputList, self.RuleEtiquetas = json.load(f)
        else:
            temp_parser = self.parser(self.path_cargar[0])
            try:
                self.InputList, self.OutputList, self.RuleEtiquetas = temp_parser.fis_to_json()
            except TypeError:
                self.error_dialog.setInformativeText("No se permiten salidas negadas")
                self.error_dialog.exec_()
                return

        self.main.guardarFuzzButton.setEnabled(True)
        self.main.guardarComoFuzzButton.setEnabled(True)
        self.main.exportarFuzzButton.setEnabled(True)
        self.main.inputNombre.setReadOnly(False)
        self.main.outputNombre.setReadOnly(False)

        self.current_file = copy.deepcopy(self.path_cargar[0])

        self.main.inputNumber.blockSignals(True)
        self.main.outputNumber.blockSignals(True)

        self.main.fuzzyTabWidget.removeTab(5)
        self.main.fuzzyTabWidget.removeTab(4)
        self.main.fuzzyTabWidget.removeTab(3)
        self.main.fuzzyTabWidget.removeTab(2)
        self.main.fuzzyTabWidget.removeTab(1)

        self.main.fuzzyTabWidget.addTab(self.EntradasTab, "Entradas")
        self.main.fuzzyTabWidget.addTab(self.SalidasTab, "Salidas")
        self.main.fuzzyTabWidget.addTab(self.ReglasTab, "Reglas")

        self.main.inputNumber.clear()
        self.main.outputNumber.clear()

        for i in range(len(self.InputList)):
            self.main.inputNumber.insertItem(i, str(i + 1))

        for i in range(len(self.OutputList)):
            self.main.outputNumber.insertItem(i, str(i + 1))

        self.main.inputNumber.blockSignals(False)
        self.main.outputNumber.blockSignals(False)

        self.fuzzController = self.fuzzInitController(
            self.InputList, self.OutputList, self.RuleEtiquetas
        )
        self.RuleList = copy.deepcopy(self.fuzzController.rulelist)

        seleccion_entrada(self)
        seleccion_salida(self)

        self.fuzzController.graficar_mf_in(self, 0)
        self.fuzzController.graficar_mf_out(self, 0)

        self.setWindowTitle(
            "Laboratorio de sistemas de control - " + self.path_cargar[0].split("/")[-1]
        )


def seleccion_entrada(self):
    ni = self.main.inputNumber.currentIndex()
    self.main.inputNombre.setText(self.InputList[ni]["nombre"])
    self.main.inputEtiquetasNum.setText(str(self.InputList[ni]["numeroE"]))
    self.main.inputRange.setText(str(self.InputList[ni]["rango"]))
    self.main.etiquetaNumIn.clear()

    for j in range(self.InputList[ni]["numeroE"]):
        self.main.etiquetaNumIn.insertItem(j, str(j + 1))

    self.main.etiquetaNombreIn.setText(self.InputList[ni]["etiquetas"][0]["nombre"])
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]["etiquetas"][0]["mf"])
    self.main.etiquetaDefinicionIn.setText(
        str(self.InputList[ni]["etiquetas"][0]["definicion"])
    )

    self.fuzzController.graficar_mf_in(self, ni)


def seleccion_salida(self):
    no = self.main.outputNumber.currentIndex()
    self.main.outputNombre.setText(self.OutputList[no]["nombre"])
    self.main.outputEtiquetasNum.setText(str(self.OutputList[no]["numeroE"]))
    self.main.outputRange.setText(str(self.OutputList[no]["rango"]))
    self.main.defuzzMethodOut.setCurrentText(self.OutputList[no]["metodo"])
    self.main.etiquetaNumOut.clear()

    for j in range(self.OutputList[no]["numeroE"]):
        self.main.etiquetaNumOut.insertItem(j, str(j + 1))

    self.main.etiquetaNombreOut.setText(self.OutputList[no]["etiquetas"][0]["nombre"])
    self.main.etiquetaMfOut.setCurrentText(self.OutputList[no]["etiquetas"][0]["mf"])
    self.main.etiquetaDefinicionOut.setText(
        str(self.OutputList[no]["etiquetas"][0]["definicion"])
    )

    self.fuzzController.graficar_mf_out(self, no)


def nombre_entrada(self):

    if self.main.inputNombre.text().strip() == '':
        self.error_dialog.setInformativeText(
            "El nombre no puede estar vacio")
        self.error_dialog.exec_()
        self.main.inputNombre.setFocus()
        return

    ni = self.main.inputNumber.currentIndex()
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    old_name = self.InputList[ni]["nombre"]
    flag = 0

    for i in self.InputList:
        if (
            i["nombre"] == self.main.inputNombre.text() and
            old_name != self.main.inputNombre.text()
        ):
            flag = 1

    if not flag:
        self.InputList[ni]["nombre"] = self.main.inputNombre.text()
    else:
        self.InputList[ni]["nombre"] = self.main.inputNombre.text() + "1"
        self.main.inputNombre.setText(self.InputList[ni]["nombre"])

    self.fuzzController.cambiar_nombre_input(self, ni, self.InputList[ni]["nombre"])
    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)


def nombre_salida(self):

    if self.main.outputNombre.text().strip() == '':
        self.error_dialog.setInformativeText(
            "El nombre no puede estar vacio")
        self.error_dialog.exec_()
        self.main.outputNombre.setFocus()
        return

    no = self.main.outputNumber.currentIndex()
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    old_name = self.OutputList[no]["nombre"]
    flag = 0

    for o in self.OutputList:
        if (
            o["nombre"] == self.main.outputNombre.text() and
            old_name != self.main.outputNombre.text()
        ):
            flag = 1

    if not flag:
        self.OutputList[no]["nombre"] = self.main.outputNombre.text()
    else:
        self.OutputList[no]["nombre"] = self.main.outputNombre.text() + "1"
        self.main.outputNombre.setText(self.OutputList[no]["nombre"])

    self.fuzzController.cambiar_nombre_output(self, no, self.OutputList[no]["nombre"])
    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)


def numero_de_etiquetas_in(self):

    try:
        _ = int(self.main.inputEtiquetasNum.text())
        if _ < 1:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "El numero de etiquetas debe ser un valor entero mayor o igual a 1")
        self.error_dialog.exec_()
        self.main.inputEtiquetasNum.setFocus()
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)

    ni = self.main.inputNumber.currentIndex()
    ne = int(self.main.inputEtiquetasNum.text())

    if self.InputList[ni]["numeroE"] > ne:
        self.main.etiquetaNumIn.blockSignals(True)

        for n in range(self.InputList[ni]["numeroE"] - 1, ne - 1, -1):
            new_list = []
            for i, sets in enumerate(copy.deepcopy(self.RuleEtiquetas)):
                for rule in sets[0]:
                    if (
                        rule[0] == self.InputList[ni]["etiquetas"][n]["nombre"] and
                        rule[1] == ni
                    ):
                        break
                    else:
                        new_list.append(self.RuleEtiquetas[i])
                        break

            self.RuleEtiquetas = copy.deepcopy(new_list)
            self.main.etiquetaNumIn.removeItem(n)

        for _ in range(ne, self.InputList[ni]["numeroE"]):
            self.InputList[ni]["etiquetas"].pop()

        self.InputList[ni]["numeroE"] = ne
        self.RuleEtiquetas = copy.deepcopy(new_list)
        self.main.etiquetaNumIn.setCurrentIndex(ne - 1)
        self.main.etiquetaNombreIn.setText(
            self.InputList[ni]["etiquetas"][ne - 1]["nombre"]
        )
        self.main.etiquetaDefinicionIn.setText(
            str(self.InputList[ni]["etiquetas"][ne - 1]["definicion"])
        )
        self.main.etiquetaMfIn.setCurrentText(
            self.InputList[ni]["etiquetas"][ne - 1]["mf"]
        )

    if self.InputList[ni]["numeroE"] < ne:
        self.main.etiquetaNumIn.blockSignals(True)
        rmin, rmax = self.InputList[ni]["rango"]

        if (ne - self.InputList[ni]["numeroE"]) == 1:
            ini_range_etiquetas = [
                self.vector_rotacion[self.rotacion_windowIn] * (rmax-rmin) + rmin,
                self.vector_rotacion[self.rotacion_windowIn + 1] * (rmax-rmin) + rmin,
                self.vector_rotacion[self.rotacion_windowIn + 2] * (rmax-rmin) + rmin,
            ]

            self.rotacion_windowIn += 1
            if self.rotacion_windowIn > 4:
                self.rotacion_windowIn = 0
        else:
            step = (rmax-rmin) / ((ne - self.InputList[ni]["numeroE"]) - 1)
            ini_range_etiquetas = np.arange(rmin - step, rmax + step + 1, step).tolist()

        window = 0
        for j in range(self.InputList[ni]["numeroE"], ne):
            self.main.etiquetaNumIn.insertItem(j, str(j + 1))
            self.InputList[ni]["etiquetas"].append(
                EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window + 3])
            )
            window += 1

        self.InputList[ni]["numeroE"] = ne

    self.fuzzController.cambio_etiquetas_input(self, self.InputList, ni)
    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)
    self.main.etiquetaNumIn.blockSignals(False)


def numero_de_etiquetas_out(self):

    try:
        _ = int(self.main.outputEtiquetasNum.text())
        if _ < 1:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "El numero de etiquetas debe ser un valor entero mayor o igual a 1")
        self.error_dialog.exec_()
        self.main.outputEtiquetasNum.setFocus()
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)

    no = self.main.outputNumber.currentIndex()
    ne = int(self.main.outputEtiquetasNum.text())

    if self.OutputList[no]["numeroE"] > ne:
        self.main.etiquetaNumOut.blockSignals(True)

        for n in range(self.OutputList[no]["numeroE"] - 1, ne - 1, -1):
            new_list = []
            for o, sets in enumerate(copy.deepcopy(self.RuleEtiquetas)):
                for rule in sets[1]:
                    if (
                        rule[0] == self.OutputList[no]["etiquetas"][n]["nombre"] and
                        rule[1] == no
                    ):
                        break
                    else:
                        new_list.append(self.RuleEtiquetas[o])
                        break

            self.RuleEtiquetas = copy.deepcopy(new_list)
            self.main.etiquetaNumOut.removeItem(n)

        for _ in range(ne, self.OutputList[no]["numeroE"]):
            self.OutputList[no]["etiquetas"].pop()

        self.OutputList[no]["numeroE"] = ne
        self.RuleEtiquetas = copy.deepcopy(new_list)
        self.main.etiquetaNumOut.setCurrentIndex(ne - 1)
        self.main.etiquetaNombreOut.setText(
            self.OutputList[no]["etiquetas"][ne - 1]["nombre"]
        )
        self.main.etiquetaDefinicionOut.setText(
            str(self.OutputList[no]["etiquetas"][ne - 1]["definicion"])
        )
        self.main.etiquetaMfOut.setCurrentText(
            self.OutputList[no]["etiquetas"][ne - 1]["mf"]
        )

    if self.OutputList[no]["numeroE"] < ne:
        self.main.etiquetaNumOut.blockSignals(True)
        rmin, rmax = self.OutputList[no]["rango"]

        if (ne - self.OutputList[no]["numeroE"]) == 1:
            ini_range_etiquetas = [
                self.vector_rotacion[self.rotacion_windowOut] * (rmax-rmin) + rmin,
                self.vector_rotacion[self.rotacion_windowOut + 1] * (rmax-rmin) + rmin,
                self.vector_rotacion[self.rotacion_windowOut + 2] * (rmax-rmin) + rmin,
            ]

            self.rotacion_windowOut += 1
            if self.rotacion_windowOut > 4:
                self.rotacion_windowOut = 0
        else:
            step = (rmax-rmin) / ((ne - self.OutputList[no]["numeroE"]) - 1)
            ini_range_etiquetas = np.arange(rmin - step, rmax + step + 1, step).tolist()

        window = 0
        for j in range(self.OutputList[no]["numeroE"], ne):
            self.main.etiquetaNumOut.insertItem(j, str(j + 1))
            self.OutputList[no]["etiquetas"].append(
                EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window + 3])
            )
            window += 1

        self.OutputList[no]["numeroE"] = ne

    self.fuzzController.cambio_etiquetas_output(self, self.OutputList, no)
    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)
    self.main.etiquetaNumOut.blockSignals(False)


def rango_in(self):

    try:
        _ = json.loads(self.main.inputRange.text())
        if len(_) > 2 or len(_) < 2:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Rango no valido, el rango debe estar entre corchetes y los valores separados por coma.\n i.g., [-10, 10]"
        )
        self.error_dialog.exec_()
        self.main.inputRange.setFocus()
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]["rango"] = json.loads(self.main.inputRange.text())
    self.fuzzController.update_rango_input(self, self.InputList, ni)
    self.fuzzController.cambio_etiquetas_input(self, self.InputList, ni)


def rango_out(self):

    try:
        _ = json.loads(self.main.outputRange.text())
        if len(_) > 2 or len(_) < 2:
            raise ValueError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Rango no valido, el rango debe estar entre corchetes y los valores separados por coma.\n i.g., [-10, 10]"
        )
        self.error_dialog.exec_()
        self.main.outputRange.setFocus()
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    no = self.main.outputNumber.currentIndex()
    self.OutputList[no]["rango"] = json.loads(self.main.outputRange.text())
    self.fuzzController.update_rango_output(self, self.OutputList, no)
    self.fuzzController.cambio_etiquetas_output(self, self.OutputList, no)


def defuzz_metodo(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    no = self.main.outputNumber.currentIndex()
    self.OutputList[no]["metodo"] = self.main.defuzzMethodOut.currentText()
    metodo = self.OutputList[no]["metodo"]
    self.fuzzController.cambiar_metodo(self, no, metodo)


def seleccion_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()

    self.main.etiquetaNombreIn.setText(self.InputList[ni]["etiquetas"][ne]["nombre"])
    self.main.etiquetaMfIn.blockSignals(True)
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]["etiquetas"][ne]["mf"])
    self.main.etiquetaDefinicionIn.setText(
        str(self.InputList[ni]["etiquetas"][ne]["definicion"])
    )
    self.main.etiquetaMfIn.blockSignals(False)


def seleccion_etiqueta_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()

    self.main.etiquetaNombreOut.setText(self.OutputList[no]["etiquetas"][ne]["nombre"])
    self.main.etiquetaMfOut.blockSignals(True)
    self.main.etiquetaMfOut.setCurrentText(self.OutputList[no]["etiquetas"][ne]["mf"])
    self.main.etiquetaDefinicionOut.setText(
        str(self.OutputList[no]["etiquetas"][ne]["definicion"])
    )
    self.main.etiquetaMfOut.blockSignals(False)

def nombre_etiqueta_in(self):

    if self.main.etiquetaNombreIn.text().strip() == '':
        self.error_dialog.setInformativeText(
            "El nombre no puede estar vacio")
        self.error_dialog.exec_()
        self.main.etiquetaNombreIn.setFocus()
        return

    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    old_name = self.InputList[ni]["etiquetas"][ne]["nombre"]

    flag = 0

    for i in self.InputList[ni]["etiquetas"]:
        if (
            i["nombre"] == self.main.etiquetaNombreIn.text() and
            old_name != self.main.etiquetaNombreIn.text()
        ):
            flag = 1

    if not flag:
        self.InputList[ni]["etiquetas"][ne]["nombre"] = self.main.etiquetaNombreIn.text()
    else:
        self.InputList[ni]["etiquetas"][ne]["nombre"] = (
            self.main.etiquetaNombreIn.text() + "1"
        )
        self.main.etiquetaNombreIn.setText(self.InputList[ni]["etiquetas"][ne]["nombre"])

    self.fuzzController.cambio_etinombre_input(self, self.InputList, ni, ne, old_name)
    if len(self.RuleList) > 0:
        actualizar_RulesEtiquetas_in(
            self, ni, self.main.etiquetaNombreIn.text(), old_name
        )


def actualizar_RulesEtiquetas_in(self, ni, new_name, old_name):
    for sets in self.RuleEtiquetas:
        for rule in sets[0]:
            if rule[0] == old_name and rule[1] == ni:
                rule[0] = new_name

    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)


def nombre_etiqueta_out(self):

    if self.main.etiquetaNombreOut.text().strip() == '':
        self.error_dialog.setInformativeText(
            "El nombre no puede estar vacio")
        self.error_dialog.exec_()
        self.main.etiquetaNombreOut.setFocus()
        return

    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    old_name = self.OutputList[no]["etiquetas"][ne]["nombre"]

    flag = 0

    for i in self.OutputList[no]["etiquetas"]:
        if (
            i["nombre"] == self.main.etiquetaNombreOut.text() and
            old_name != self.main.etiquetaNombreOut.text()
        ):
            flag = 1

    if not flag:
        self.OutputList[no]["etiquetas"][ne]["nombre"] = self.main.etiquetaNombreOut.text(
        )
    else:
        self.OutputList[no]["etiquetas"][ne]["nombre"] = (
            self.main.etiquetaNombreOut.text() + "1"
        )
        self.main.etiquetaNombreOut.setText(
            self.OutputList[no]["etiquetas"][ne]["nombre"]
        )

    self.fuzzController.cambio_etinombre_output(self, self.OutputList, no, ne, old_name)
    if len(self.RuleList) > 0:
        actualizar_RulesEtiquetas_out(
            self, no, self.main.etiquetaNombreOut.text(), old_name
        )


def actualizar_RulesEtiquetas_out(self, no, new_name, old_name):
    for sets in self.RuleEtiquetas:
        for rule in sets[1]:
            if rule[0] == old_name and rule[1] == no:
                rule[0] = new_name

    self.fuzzController.rulelist = []
    self.RuleList = self.fuzzController.crear_reglas(self.RuleEtiquetas)


def seleccion_mf_in(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    old_mf = self.InputList[ni]["etiquetas"][ne]["mf"]
    definicion = self.InputList[ni]["etiquetas"][ne]["definicion"]
    self.InputList[ni]["etiquetas"][ne]["mf"] = self.main.etiquetaMfIn.currentText()
    new_mf = self.InputList[ni]["etiquetas"][ne]["mf"]
    new_definicion, tooltip = update_definicionmf(self, old_mf, definicion, 'trimf')
    new_definicion, tooltip = update_definicionmf(self, 'trimf', new_definicion, self.main.etiquetaMfIn.currentText())
    new_definicion = round_list(new_definicion)
    self.main.etiquetaDefinicionIn.setText(str(new_definicion))
    self.main.etiquetaDefinicionIn.setToolTip(tooltip)
    definicion_in(self)


def definicion_in(self):

    try:
        deinificion_in_validator(self)
    except AssertionError:
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]["etiquetas"][ne]["definicion"] = json.loads(
        self.main.etiquetaDefinicionIn.text()
    )
    self.fuzzController.update_definicion_input(self, self.InputList, ni, ne)


def deinificion_in_validator(self):
    mf = self.main.etiquetaMfIn.currentText()
    try:
        _ = json.loads(self.main.etiquetaDefinicionIn.text())
        try:
            validacion_mf(self, _, mf)
        except AssertionError:
            self.main.etiquetaDefinicionIn.setFocus()
            raise AssertionError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato de definicion invalido para la funcion de membresia: " + mf +
            "\nDebe estar entre corchetes con valores separados por comas")
        self.error_dialog.exec_()
        self.main.etiquetaDefinicionIn.setFocus()
        raise AssertionError


def seleccion_mf_out(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    old_mf = self.OutputList[no]["etiquetas"][ne]["mf"]
    definicion = self.OutputList[no]["etiquetas"][ne]["definicion"]
    self.OutputList[no]["etiquetas"][ne]["mf"] = self.main.etiquetaMfOut.currentText()
    new_mf = self.OutputList[no]["etiquetas"][ne]["mf"]
    new_definicion, tooltip = update_definicionmf(self, old_mf, definicion, 'trimf')
    new_definicion, tooltip = update_definicionmf(self, 'trimf', new_definicion, self.main.etiquetaMfOut.currentText())
    new_definicion = round_list(new_definicion)
    self.main.etiquetaDefinicionOut.setText(str(new_definicion))
    self.main.etiquetaDefinicionOut.setToolTip(tooltip)
    definicion_out(self)


def definicion_out(self):

    try:
        deinificion_out_validator(self)
    except AssertionError:
        return

    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    self.OutputList[no]["etiquetas"][ne]["definicion"] = json.loads(
        self.main.etiquetaDefinicionOut.text()
    )
    self.fuzzController.update_definicion_output(self, self.OutputList, no, ne)


def deinificion_out_validator(self):
    mf = self.main.etiquetaMfOut.currentText()
    try:
        _ = json.loads(self.main.etiquetaDefinicionOut.text())
        try:
            validacion_mf(self, _, mf)
        except AssertionError:
            self.main.etiquetaDefinicionOut.setFocus()
            raise AssertionError
    except ValueError:
        self.error_dialog.setInformativeText(
            "Formato de definicion invalido para la funcion de membresia: " + mf +
            "\nDebe estar entre corchetes con valores separados por comas")
        self.error_dialog.exec_()
        self.main.etiquetaDefinicionOut.setFocus()
        raise AssertionError


def round_list(lista):
    return list(np.around(np.array(lista), 3))


def rule_list_visualizacion(self):
    if self.main.fuzzyTabWidget.currentIndex() == 3:

        self.main.rulelistWidget.blockSignals(True)

        self.main.rulelistWidget.clear()

        for regla in self.RuleList:
            self.main.rulelistWidget.addItem(str(regla))

        for i, o in zip(self.inframes, self.outframes):
            i.hide()
            o.hide()

        for i, o in zip(self.inlists, self.outlists):
            i.clear()
            o.clear()

        self.main.rulelistWidget.setCurrentRow(0)

        for i, entrada in enumerate(self.InputList):
            self.inframes[i].show()
            self.inlabels[i].setText(entrada["nombre"])
            for etiqueta in entrada["etiquetas"]:
                self.inlists[i].addItem(etiqueta["nombre"])
            self.inlists[i].addItem("None")
            self.inlists[i].setCurrentRow(0)

        for o, salida in enumerate(self.OutputList):
            self.outframes[o].show()
            self.outlabels[o].setText(salida["nombre"])
            for etiqueta in salida["etiquetas"]:
                self.outlists[o].addItem(etiqueta["nombre"])
            self.outlists[o].addItem("None")
            self.outlists[o].setCurrentRow(0)

        self.main.rulelistWidget.blockSignals(False)
        seleccionar_etiquetas(self)


def seleccionar_etiquetas(self):
    if len(self.RuleEtiquetas) > 0:
        ni = len(self.InputList)
        no = len(self.OutputList)

        ruleindex = self.main.rulelistWidget.currentRow()
        Etiquetasin, Etiquetasout, logica = self.RuleEtiquetas[ruleindex]

        if logica:
            self.main.andradioButton.setChecked(True)
        else:
            self.main.orradioButton.setChecked(True)

        for index in range(ni):
            for Etiquetasin2 in Etiquetasin:
                if Etiquetasin2[1] == index:
                    item = self.inlists[index].findItems(
                        Etiquetasin2[0], QtCore.Qt.MatchExactly
                    )
                    self.inlists[index].setCurrentItem(item[-1])
                    if Etiquetasin2[2]:
                        self.innots[index].setChecked(True)
                    else:
                        self.innots[index].setChecked(False)
                    break
            else:
                item = self.inlists[index].findItems("None", QtCore.Qt.MatchExactly)
                self.inlists[index].setCurrentItem(item[-1])
                self.innots[index].setChecked(False)

        for index in range(no):
            for Etiquetasout2 in Etiquetasout:
                if Etiquetasout2[1] == index:
                    item = self.outlists[index].findItems(
                        Etiquetasout2[0], QtCore.Qt.MatchExactly
                    )
                    self.outlists[index].setCurrentItem(item[-1])
                    self.outweights[index].setValue(Etiquetasout2[2])
                    break
            else:
                item = self.outlists[index].findItems("None", QtCore.Qt.MatchExactly)
                self.outlists[index].setCurrentItem(item[-1])


def rule_list_agregar(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    ni = len(self.InputList)
    no = len(self.OutputList)

    Etiquetasin = []
    Etiquetasout = []

    for i, entrada in enumerate(self.InputList):
        if self.inlists[i].currentItem().text() != "None":
            Etiquetasin.append(
                [self.inlists[i].currentItem().text(), i, self.innots[i].isChecked()]
            )

    for o, salida in enumerate(self.OutputList):
        if self.outlists[o].currentItem().text() != "None":
            Etiquetasout.append(
                [self.outlists[o].currentItem().text(), o, self.outweights[o].value()]
            )

    if len(Etiquetasin) > 0 and len(Etiquetasout) > 0:
        self.RuleEtiquetas.append(
            copy.deepcopy(
                [Etiquetasin, Etiquetasout, self.main.andradioButton.isChecked()]
            )
        )
        self.RuleList.append(
            self.fuzzController.agregar_regla(self, ni, no, Etiquetasin, Etiquetasout)
        )
        self.main.rulelistWidget.addItem(str(self.RuleList[-1]))
        self.main.rulelistWidget.setCurrentRow(len(self.RuleList) - 1)
    else:
        self.error_dialog.setInformativeText(
            "Regla no valida, debe contener al menos una entrada y una salida"
        )
        self.error_dialog.exec_()


def rule_list_eliminar(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    if self.main.rulelistWidget.count():
        index_rule = self.main.rulelistWidget.currentRow()
        self.fuzzController.eliminar_regla(index_rule)
        self.main.rulelistWidget.takeItem(self.main.rulelistWidget.currentRow())
        del self.RuleList[index_rule]
        del self.RuleEtiquetas[index_rule]


def rule_list_cambiar(self):
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    index_rule = self.main.rulelistWidget.currentRow()

    ni = len(self.InputList)
    no = len(self.OutputList)

    Etiquetasin = []
    Etiquetasout = []

    for i, entrada in enumerate(self.InputList):
        if self.inlists[i].currentItem().text() != "None":
            Etiquetasin.append(
                [self.inlists[i].currentItem().text(), i, self.innots[i].isChecked()]
            )

    for o, salida in enumerate(self.OutputList):
        if self.outlists[o].currentItem().text() != "None":
            Etiquetasout.append(
                [self.outlists[o].currentItem().text(), o, self.outweights[o].value()]
            )

    if len(Etiquetasin) > 0 and len(Etiquetasout) > 0:
        del self.RuleEtiquetas[index_rule]
        self.RuleEtiquetas.insert(
            index_rule,
            copy.deepcopy(
                [Etiquetasin, Etiquetasout, self.main.andradioButton.isChecked()]
            ),
        )
        regla = self.fuzzController.cambiar_regla(
            self, ni, no, Etiquetasin, Etiquetasout, index_rule
        )
        self.main.rulelistWidget.takeItem(index_rule)
        self.main.rulelistWidget.insertItem(index_rule, str(regla))
        self.main.rulelistWidget.setCurrentRow(index_rule)
        del self.RuleList[index_rule]
        self.RuleList.insert(index_rule, regla)
    else:
        self.error_dialog.setInformativeText(
            "Regla no valida, debe contener al menos una entrada y una salida"
        )
        self.error_dialog.exec_()


def crear_controlador(self):
    if self.main.rulelistWidget.count():
        self.fuzzController = self.fuzzInitController(
            self.InputList, self.OutputList, self.RuleEtiquetas
        )
        self.RuleList = copy.deepcopy(self.fuzzController.rulelist)
        self.main.fuzzyTabWidget.addTab(self.PruebaTab, "Prueba")

        ni = len(self.InputList)
        no = len(self.OutputList)

        for it_f, ot_f, f2d, f3d in zip(
            self.intestframes,
            self.outtestframes,
            self.respuesta2dframes,
            self.respuesta3dframes,
        ):
            it_f.hide()
            ot_f.hide()
            f2d.hide()
            f3d.hide()

        for i, salida in enumerate(self.InputList):
            self.intestframes[i].show()

        for o, salida in enumerate(self.OutputList):
            self.outtestframes[o].show()

        prueba_input(self)

        if ni == 1:
            self.main.fuzzyTabWidget.addTab(self.RespuestaTab, "Respuesta")
            self.main.respuestastackedWidget.setCurrentIndex(0)
            for o, salida in enumerate(self.OutputList):
                self.respuesta2dframes[o].show()
            rimin, rimax = self.InputList[0]["rango"]
            self.fuzzController.graficar_respuesta_2d(self, [rimin, rimax], no)

        if ni == 2:
            self.main.fuzzyTabWidget.addTab(self.RespuestaTab, "Respuesta")
            self.main.respuestastackedWidget.setCurrentIndex(1)
            for o, salida in enumerate(self.OutputList):
                self.respuesta3dframes[o].show()
            rimin1, rimax1 = self.InputList[0]["rango"]
            rimin2, rimax2 = self.InputList[1]["rango"]
            self.fuzzController.graficar_respuesta_3d(
                self, [rimin1, rimax1], [rimin2, rimax2], no
            )


def prueba_input(self):
    ni = len(self.InputList)
    no = len(self.OutputList)

    values = [i.value() for i in self.intestsliders[:ni]]

    for i, entrada in enumerate(self.InputList[:ni]):
        rmin, rmax = entrada["rango"]
        values[i] = values[i] * (rmax-rmin) / 1000 + rmin
        self.intestlabels[i].setText(entrada["nombre"] + f": {np.around(values[i], 3)}")

    self.fuzzController.prueba_de_controlador(self, values, ni, no, pyqtgraph=True)


def crear_vectores_de_widgets(self):

    self.inframes = [
        self.main.inframe1,
        self.main.inframe2,
        self.main.inframe3,
        self.main.inframe4,
        self.main.inframe5,
        self.main.inframe6,
        self.main.inframe7,
        self.main.inframe8,
        self.main.inframe9,
        self.main.inframe10,
    ]

    self.outframes = [
        self.main.outframe1,
        self.main.outframe2,
        self.main.outframe3,
        self.main.outframe4,
        self.main.outframe5,
        self.main.outframe6,
        self.main.outframe7,
        self.main.outframe8,
        self.main.outframe9,
        self.main.outframe10,
    ]

    self.inlists = [
        self.main.inlist1,
        self.main.inlist2,
        self.main.inlist3,
        self.main.inlist4,
        self.main.inlist5,
        self.main.inlist6,
        self.main.inlist7,
        self.main.inlist8,
        self.main.inlist9,
        self.main.inlist10,
    ]

    self.outlists = [
        self.main.outlist1,
        self.main.outlist2,
        self.main.outlist3,
        self.main.outlist4,
        self.main.outlist5,
        self.main.outlist6,
        self.main.outlist7,
        self.main.outlist8,
        self.main.outlist9,
        self.main.outlist10,
    ]

    self.inlabels = [
        self.main.inlabel1,
        self.main.inlabel2,
        self.main.inlabel3,
        self.main.inlabel4,
        self.main.inlabel5,
        self.main.inlabel6,
        self.main.inlabel7,
        self.main.inlabel8,
        self.main.inlabel9,
        self.main.inlabel10,
    ]

    self.outlabels = [
        self.main.outlabel1,
        self.main.outlabel2,
        self.main.outlabel3,
        self.main.outlabel4,
        self.main.outlabel5,
        self.main.outlabel6,
        self.main.outlabel7,
        self.main.outlabel8,
        self.main.outlabel9,
        self.main.outlabel10,
    ]

    self.innots = [
        self.main.innot1,
        self.main.innot2,
        self.main.innot3,
        self.main.innot4,
        self.main.innot5,
        self.main.innot6,
        self.main.innot7,
        self.main.innot8,
        self.main.innot9,
        self.main.innot10,
    ]

    self.intestframes = [
        self.main.intestframe1,
        self.main.intestframe2,
        self.main.intestframe3,
        self.main.intestframe4,
        self.main.intestframe5,
        self.main.intestframe6,
        self.main.intestframe7,
        self.main.intestframe8,
        self.main.intestframe9,
        self.main.intestframe10,
    ]

    self.outtestframes = [
        self.main.outtestframe1,
        self.main.outtestframe2,
        self.main.outtestframe3,
        self.main.outtestframe4,
        self.main.outtestframe5,
        self.main.outtestframe6,
        self.main.outtestframe7,
        self.main.outtestframe8,
        self.main.outtestframe9,
        self.main.outtestframe10,
    ]

    self.intestsliders = [
        self.main.intestslider1,
        self.main.intestslider2,
        self.main.intestslider3,
        self.main.intestslider4,
        self.main.intestslider5,
        self.main.intestslider6,
        self.main.intestslider7,
        self.main.intestslider8,
        self.main.intestslider9,
        self.main.intestslider10,
    ]

    self.ingraphs = [
        self.main.ingraph1,
        self.main.ingraph2,
        self.main.ingraph3,
        self.main.ingraph4,
        self.main.ingraph5,
        self.main.ingraph6,
        self.main.ingraph7,
        self.main.ingraph8,
        self.main.ingraph9,
        self.main.ingraph10,
    ]

    self.outgraphs = [
        self.main.outgraph1,
        self.main.outgraph2,
        self.main.outgraph3,
        self.main.outgraph4,
        self.main.outgraph5,
        self.main.outgraph6,
        self.main.outgraph7,
        self.main.outgraph8,
        self.main.outgraph9,
        self.main.outgraph10,
    ]

    self.intestlabels = [
        self.main.intestlabel1,
        self.main.intestlabel2,
        self.main.intestlabel3,
        self.main.intestlabel4,
        self.main.intestlabel5,
        self.main.intestlabel6,
        self.main.intestlabel7,
        self.main.intestlabel8,
        self.main.intestlabel9,
        self.main.intestlabel10,
    ]

    self.outtestlabels = [
        self.main.outtestlabel1,
        self.main.outtestlabel2,
        self.main.outtestlabel3,
        self.main.outtestlabel4,
        self.main.outtestlabel5,
        self.main.outtestlabel6,
        self.main.outtestlabel7,
        self.main.outtestlabel8,
        self.main.outtestlabel9,
        self.main.outtestlabel10,
    ]

    self.respuesta3dframes = [
        self.main.respuesta3dframe1,
        self.main.respuesta3dframe2,
        self.main.respuesta3dframe3,
        self.main.respuesta3dframe4,
        self.main.respuesta3dframe5,
        self.main.respuesta3dframe6,
        self.main.respuesta3dframe7,
        self.main.respuesta3dframe8,
        self.main.respuesta3dframe9,
        self.main.respuesta3dframe10,
    ]

    self.respuesta2dframes = [
        self.main.respuesta2dframe1,
        self.main.respuesta2dframe2,
        self.main.respuesta2dframe3,
        self.main.respuesta2dframe4,
        self.main.respuesta2dframe5,
        self.main.respuesta2dframe6,
        self.main.respuesta2dframe7,
        self.main.respuesta2dframe8,
        self.main.respuesta2dframe9,
        self.main.respuesta2dframe10,
    ]

    self.respuesta3ds = [
        self.main.respuesta3d1,
        self.main.respuesta3d2,
        self.main.respuesta3d3,
        self.main.respuesta3d4,
        self.main.respuesta3d5,
        self.main.respuesta3d6,
        self.main.respuesta3d7,
        self.main.respuesta3d8,
        self.main.respuesta3d9,
        self.main.respuesta3d10,
    ]

    self.respuesta2ds = [
        self.main.respuesta2d1,
        self.main.respuesta2d2,
        self.main.respuesta2d3,
        self.main.respuesta2d4,
        self.main.respuesta2d5,
        self.main.respuesta2d6,
        self.main.respuesta2d7,
        self.main.respuesta2d8,
        self.main.respuesta2d9,
        self.main.respuesta2d10,
    ]

    self.outweights = [
        self.main.outweight1,
        self.main.outweight2,
        self.main.outweight3,
        self.main.outweight4,
        self.main.outweight5,
        self.main.outweight6,
        self.main.outweight7,
        self.main.outweight8,
        self.main.outweight9,
        self.main.outweight10,
    ]
