from rutinas.rutinas_fuzzy import *
from handlers.modificadorMf import update_definicionmf
from rutinas.rutinas_fuzzy import FuzzyController
from PySide2 import QtCore, QtGui, QtWidgets
from collections import deque
import pickle
import json
import pprint


def FuzzyHandler(self):
    self.EntradasTab = self.main.fuzzyTabWidget.widget(1)
    self.SalidasTab = self.main.fuzzyTabWidget.widget(2)
    self.ReglasTab = self.main.fuzzyTabWidget.widget(3)
    self.PruebaTab = self.main.fuzzyTabWidget.widget(4)
    self.RespuestaTab = self.main.fuzzyTabWidget.widget(5)
    
    self.main.guardarFuzzButton.setDisabled(True)
    self.main.guardarComoFuzzButton.setDisabled(True)
    
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)
    
    self.InputList = []
    self.OutputList = []
    self.RuleList = []
    self.RuleEtiquetas = []
    
    self.fuzzInitController = FuzzyController
    
    crear_vectores_de_widgets(self)
        
    for i_f, o_f, it_f, ot_f, f2d, f3d in zip(self.inframes, self.outframes, self.intestframes, 
                                              self.outtestframes, self.respuesta2dframes, self.respuesta3dframes):
        i_f.hide()
        o_f.hide()
        it_f.hide()
        ot_f.hide()
        f2d.hide()
        f3d.hide()
        
    self.main.generarFuzzyButton.clicked.connect(lambda: crear_tabs(self))
    self.main.guardarFuzzButton.clicked.connect(lambda: guardar_controlador(self))
    self.main.cargarFuzzButton.clicked.connect(lambda: cargar_controlador(self))
    self.main.guardarComoFuzzButton.clicked.connect(lambda: guardarcomo_controlador(self))
    
    self.main.inputNumber.currentIndexChanged.connect(lambda: seleccion_entrada(self))
    self.main.inputNombre.returnPressed.connect(lambda: nombre_entrada(self))
    self.main.inputEtiquetasNum.returnPressed.connect(lambda: numero_de_etiquetas_in(self))
    self.main.inputRange.returnPressed.connect(lambda: rango_in(self))
    
    self.main.etiquetaNumIn.currentIndexChanged.connect(lambda: seleccion_etiqueta_in(self))
    self.main.etiquetaNombreIn.returnPressed.connect(lambda: nombre_etiqueta_in(self))
    self.main.etiquetaMfIn.currentIndexChanged.connect(lambda: seleccion_mf_in(self))
    self.main.etiquetaDefinicionIn.returnPressed.connect(lambda: definicion_in(self))
    
    
    self.main.outputNumber.currentIndexChanged.connect(lambda: seleccion_salida(self))
    self.main.outputNombre.returnPressed.connect(lambda: nombre_salida(self))
    self.main.outputEtiquetasNum.returnPressed.connect(lambda: numero_de_etiquetas_out(self))
    self.main.outputRange.returnPressed.connect(lambda: rango_out(self))
    self.main.defuzzMethodOut.currentIndexChanged.connect(lambda: defuzz_metodo(self))
    
    self.main.etiquetaNumOut.currentIndexChanged.connect(lambda: seleccion_etiqueta_out(self))
    self.main.etiquetaNombreOut.returnPressed.connect(lambda: nombre_etiqueta_out(self))
    self.main.etiquetaMfOut.currentIndexChanged.connect(lambda: seleccion_mf_out(self))
    self.main.etiquetaDefinicionOut.returnPressed.connect(lambda: definicion_out(self))
    
    self.main.fuzzyTabWidget.currentChanged.connect(lambda: rule_list_visualizacion(self))
    self.main.ruleAgregarButton.clicked.connect(lambda: rule_list_agregar(self))
    self.main.ruleEliminarButton.clicked.connect(lambda: rule_list_eliminar(self))
    self.main.ruleCambiarButton.clicked.connect(lambda: rule_list_cambiar(self))
    self.main.ruleCrearButton.clicked.connect(lambda: crear_controlador(self))
    
    for slider in self.intestsliders:
        slider.valueChanged.connect(lambda: prueba_input(self))


def crear_tabs(self):
    self.main.inputNumber.blockSignals(True)
    self.main.outputNumber.blockSignals(True)
    
    self.current_file = ''
    self.InputList = []
    self.OutputList = []
    self.RuleList = []
    self.RuleEtiquetas = []
    
    self.main.guardarFuzzButton.setEnabled(True)
    self.main.guardarComoFuzzButton.setEnabled(True)
    
    self.main.fuzzyTabWidget.removeTab(5)
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)
    
    self.main.fuzzyTabWidget.addTab(self.EntradasTab, 'Entradas')
    self.main.fuzzyTabWidget.addTab(self.SalidasTab, 'Salidas')
    self.main.fuzzyTabWidget.addTab(self.ReglasTab, 'Reglas')
    
    NumeroEntradas = int(self.main.estrucNumberInputs.currentText())
    NumeroSalidas = int(self.main.estrucNumberOutputs.currentText())
    
    self.main.inputNumber.clear()
    self.main.outputNumber.clear()

    for i in range(NumeroEntradas):
        self.main.inputNumber.insertItem(i, str(i+1))
        temp_dic = inputDic_creator(self, NumeroEntradas, i)
        self.InputList.append(temp_dic)
        ini_range_etiquetas = np.arange(-10, 11, 20/4).tolist()
        window = 0
        for j in range(self.InputList[i]['numeroE']):
            self.InputList[i]['etiquetas'][j] = EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
            window += 1
    
    for i in range(NumeroSalidas):
        self.main.outputNumber.insertItem(i, str(i+1))
        temp_dic = outputDic_creator(self, NumeroSalidas, i)
        self.OutputList.append(temp_dic)
        ini_range_etiquetas = np.arange(-10, 11, 20/4).tolist()
        window = 0
        for j in range(self.OutputList[i]['numeroE']):
            self.OutputList[i]['etiquetas'][j] = EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
            window += 1
                    
    self.main.inputNumber.blockSignals(False)
    self.main.outputNumber.blockSignals(False)
    
    self.fuzzController = self.fuzzInitController(self.InputList, self.OutputList)
    
    seleccion_entrada(self)
    seleccion_salida(self)
    
    self.fuzzController.graficar_mf_in(self, 0)
    self.fuzzController.graficar_mf_out(self, 0)


def inputDic_creator(self, NumeroEntradas, i):
    inputDic = {
        
        'nombre': 'entrada' + str(i+1),
        'numeroE': 3,
        'etiquetas': [0]*3,
        'rango': [-10, 10],        
    }
    return inputDic


def outputDic_creator(self, NumeroSalidas, i):
    outputDic = {
        
        'nombre': 'salida' + str(i+1),
        'numeroE': 3,
        'etiquetas': [0]*3,
        'rango': [-10, 10],
        'metodo': 'centroid',        
    }
    return outputDic


def EtiquetasDic_creator(self, j, erange):
    etiquetaDic = {
        'nombre': 'etiqueta' + str(j+1),
        'mf': 'trimf',
        'definicion': round_list(erange),
    }
    return etiquetaDic


def guardar_controlador(self):
    
    if len(self.current_file) > 0:
        with open(self.current_file, 'wb', ) as f:
            pickle.dump([self.InputList, self.OutputList, self.RuleList, self.RuleEtiquetas], f)
    else:
        guardarcomo_controlador(self)

def guardarcomo_controlador(self):
    path_guardar = QtWidgets.QFileDialog.getSaveFileName(selectedFilter='*.pkl')
    if len(path_guardar[0]) > 1:
        self.current_file = path_guardar[0]
        with open(path_guardar[0], 'wb', ) as f:
            pickle.dump([self.InputList, self.OutputList, self.RuleList, self.RuleEtiquetas], f)
                       

def cargar_controlador(self):
    self.path_cargar = QtWidgets.QFileDialog.getOpenFileName(selectedFilter='*.pkl')
    if len(self.path_cargar[0]) > 1:
        with open(self.path_cargar[0], 'rb', ) as f:
            self.InputList, self.OutputList, self.RuleList, self.RuleEtiquetas = pickle.load(f) 
        
        self.main.guardarFuzzButton.setEnabled(True)
        self.main.guardarComoFuzzButton.setEnabled(True)
    
        self.current_file = copy.deepcopy(self.path_cargar[0])
        
        self.main.inputNumber.blockSignals(True)
        self.main.outputNumber.blockSignals(True)
    
        self.main.fuzzyTabWidget.removeTab(5)
        self.main.fuzzyTabWidget.removeTab(4)
        self.main.fuzzyTabWidget.removeTab(3)
        self.main.fuzzyTabWidget.removeTab(2)
        self.main.fuzzyTabWidget.removeTab(1)
        
        self.main.fuzzyTabWidget.addTab(self.EntradasTab, 'Entradas')
        self.main.fuzzyTabWidget.addTab(self.SalidasTab, 'Salidas')
        self.main.fuzzyTabWidget.addTab(self.ReglasTab, 'Reglas')

        self.main.inputNumber.clear()
        self.main.outputNumber.clear()
        
        for i in range(len(self.InputList)):
            self.main.inputNumber.insertItem(i, str(i+1))
        
        for i in range(len(self.OutputList)):
            self.main.outputNumber.insertItem(i, str(i+1))
        
        self.main.inputNumber.blockSignals(False)
        self.main.outputNumber.blockSignals(False)
    
        self.fuzzController = self.fuzzInitController(self.InputList, self.OutputList, self.RuleEtiquetas)
        
        seleccion_entrada(self)
        seleccion_salida(self)
        
        self.fuzzController.graficar_mf_in(self, 0)
        self.fuzzController.graficar_mf_out(self, 0)
    
    
def seleccion_entrada(self):
    ni = self.main.inputNumber.currentIndex()
    self.main.inputNombre.setText(self.InputList[ni]['nombre'])
    self.main.inputEtiquetasNum.setText(str(self.InputList[ni]['numeroE']))
    self.main.inputRange.setText(str(self.InputList[ni]['rango']))
    self.main.etiquetaNumIn.clear()
    
    for j in range(self.InputList[ni]['numeroE']):
        self.main.etiquetaNumIn.insertItem(j, str(j+1))
    
    self.main.etiquetaNombreIn.setText(self.InputList[ni]['etiquetas'][0]['nombre'])
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]['etiquetas'][0]['mf'])
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][0]['definicion']))
    
    self.fuzzController.graficar_mf_in(self, ni)


def seleccion_salida(self):
    no = self.main.outputNumber.currentIndex()
    self.main.outputNombre.setText(self.OutputList[no]['nombre'])
    self.main.outputEtiquetasNum.setText(str(self.OutputList[no]['numeroE']))
    self.main.outputRange.setText(str(self.OutputList[no]['rango']))
    self.main.defuzzMethodOut.setCurrentText(self.OutputList[no]['metodo'])
    self.main.etiquetaNumOut.clear()
    
    for j in range(self.OutputList[no]['numeroE']):
        self.main.etiquetaNumOut.insertItem(j, str(j+1))
    
    self.main.etiquetaNombreOut.setText(self.OutputList[no]['etiquetas'][0]['nombre'])
    self.main.etiquetaMfOut.setCurrentText(self.OutputList[no]['etiquetas'][0]['mf'])
    self.main.etiquetaDefinicionOut.setText(str(self.OutputList[no]['etiquetas'][0]['definicion']))
    
    self.fuzzController.graficar_mf_out(self, no)


def nombre_entrada(self):
    ni = self.main.inputNumber.currentIndex()
    old_name = self.InputList[ni]['nombre']
    flag = 0
    
    for i in self.InputList:
        if i['nombre'] == self.main.inputNombre.text() and old_name != self.main.inputNombre.text() :
            flag = 1
    
    if not flag:
        self.InputList[ni]['nombre'] = self.main.inputNombre.text()
    else:
        self.InputList[ni]['nombre'] = self.main.inputNombre.text() + '1'
        self.main.inputNombre.setText(self.InputList[ni]['nombre'])
    
    self.fuzzController.cambiar_nombre_input(self, ni, self.InputList[ni]['nombre'])


def nombre_salida(self):
    no = self.main.outputNumber.currentIndex()
    old_name = self.OutputList[no]['nombre']
    flag = 0
    
    for o in self.OutputList:
        if o['nombre'] == self.main.outputNombre.text() and old_name != self.main.outputNombre.text() :
            flag = 1
    
    if not flag:
        self.OutputList[no]['nombre'] = self.main.outputNombre.text()
    else:
        self.OutputList[no]['nombre'] = self.main.outputNombre.text() + '1'
        self.main.outputNombre.setText(self.OutputList[no]['nombre'])
        
    self.fuzzController.cambiar_nombre_output(self, no, self.OutputList[no]['nombre'] )
    

def numero_de_etiquetas_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = int(self.main.inputEtiquetasNum.text())
    self.InputList[ni]['etiquetas'] = [0]*ne
    self.InputList[ni]['numeroE'] = ne
    self.main.etiquetaNumIn.blockSignals(True)
    self.main.etiquetaNumIn.clear()
    rmin, rmax = self.InputList[ni]['rango']
    ini_range_etiquetas = np.arange(rmin, rmax+1, (rmax-rmin)/(ne+1)).tolist()
    window = 0
    for j in range(self.InputList[ni]['numeroE']):
        self.main.etiquetaNumIn.insertItem(j, str(j+1))
        self.InputList[ni]['etiquetas'][j] = EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
        window +=1
    
    self.main.etiquetaNombreIn.setText('etiqueta1')
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][0]['definicion']))
    self.main.etiquetaMfIn.setCurrentText('trimf')
    self.fuzzController.cambio_etiquetas_input(self, self.InputList, ni)
    self.main.etiquetaNumIn.blockSignals(False)


def numero_de_etiquetas_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = int(self.main.outputEtiquetasNum.text())
    self.OutputList[no]['etiquetas'] = [0]*ne
    self.OutputList[no]['numeroE'] = ne
    self.main.etiquetaNumOut.blockSignals(True)
    self.main.etiquetaNumOut.clear()
    rmin, rmax = self.OutputList[no]['rango']
    ini_range_etiquetas = np.arange(rmin, rmax+1, (rmax-rmin)/(ne+1)).tolist()
    window = 0
    for j in range(self.OutputList[no]['numeroE']):
        self.main.etiquetaNumOut.insertItem(j, str(j+1))
        self.OutputList[no]['etiquetas'][j] = EtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
        window +=1
    
    self.main.etiquetaNombreOut.setText('etiqueta1')
    self.main.etiquetaDefinicionOut.setText(str(self.OutputList[no]['etiquetas'][0]['definicion']))
    self.main.etiquetaMfOut.setCurrentText('trimf')
    self.fuzzController.cambio_etiquetas_output(self, self.OutputList, no)
    self.main.etiquetaNumOut.blockSignals(False)
    

def rango_in(self):
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]['rango'] = json.loads(self.main.inputRange.text())
    self.fuzzController.update_rango_input(self, self.InputList, ni)
    self.fuzzController.cambio_etiquetas_input(self, self.InputList, ni)


def rango_out(self):
    no = self.main.outputNumber.currentIndex()
    self.OutputList[no]['rango'] = json.loads(self.main.outputRange.text())
    self.fuzzController.update_rango_output(self, self.OutputList, no)
    self.fuzzController.cambio_etiquetas_output(self, self.OutputList, no)


def defuzz_metodo(self):
    no = self.main.outputNumber.currentIndex()
    self.OutputList[no]['metodo'] = self.main.defuzzMethodOut.currentText()
    metodo = self.OutputList[no]['metodo']
    self.fuzzController.cambiar_metodo(self, no, metodo)   


def seleccion_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    
    self.main.etiquetaNombreIn.setText(self.InputList[ni]['etiquetas'][ne]['nombre'])
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]['etiquetas'][ne]['mf'])
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][ne]['definicion']))


def seleccion_etiqueta_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    
    self.main.etiquetaNombreOut.setText(self.OutputList[no]['etiquetas'][ne]['nombre'])
    self.main.etiquetaMfOut.setCurrentText(self.OutputList[no]['etiquetas'][ne]['mf'])
    self.main.etiquetaDefinicionOut.setText(str(self.OutputList[no]['etiquetas'][ne]['definicion']))
      

def nombre_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    old_name = self.InputList[ni]['etiquetas'][ne]['nombre']
    
    flag = 0
    
    for i in self.InputList[ni]['etiquetas']:
        if i['nombre'] == self.main.etiquetaNombreIn.text() and old_name != self.main.etiquetaNombreIn.text() :
            flag = 1
    
    if not flag:
        self.InputList[ni]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreIn.text()
    else:
        self.InputList[ni]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreIn.text() + '1'
        self.main.etiquetaNombreIn.setText(self.InputList[ni]['etiquetas'][ne]['nombre'])
        
    self.fuzzController.cambio_etinombre_input(self, self.InputList, ni, ne, old_name)


def nombre_etiqueta_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    old_name = self.OutputList[no]['etiquetas'][ne]['nombre']
    
    flag = 0
    
    for i in self.OutputList[no]['etiquetas']:
        if i['nombre'] == self.main.etiquetaNombreOut.text() and old_name != self.main.etiquetaNombreOut.text() :
            flag = 1
    
    if not flag:
        self.OutputList[no]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreOut.text()
    else:
        self.OutputList[no]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreOut.text() + '1'
        self.main.etiquetaNombreOut.setText(self.OutputList[no]['etiquetas'][ne]['nombre'])
        
    self.fuzzController.cambio_etinombre_output(self, self.OutputList, no, ne, old_name)
    

def seleccion_mf_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    old_mf = self.InputList[ni]['etiquetas'][ne]['mf']
    definicion = self.InputList[ni]['etiquetas'][ne]['definicion']
    self.InputList[ni]['etiquetas'][ne]['mf'] = self.main.etiquetaMfIn.currentText()
    new_mf = self.InputList[ni]['etiquetas'][ne]['mf']
    new_definicion = update_definicionmf(self, old_mf, definicion, new_mf)
    new_definicion = round_list(new_definicion)
    self.main.etiquetaDefinicionIn.setText(str(new_definicion))
    definicion_in(self)
 
    
def definicion_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]['etiquetas'][ne]['definicion'] = json.loads(self.main.etiquetaDefinicionIn.text())
    self.fuzzController.update_definicion_input(self, self.InputList, ni, ne)


def seleccion_mf_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    old_mf = self.OutputList[no]['etiquetas'][ne]['mf']
    definicion = self.OutputList[no]['etiquetas'][ne]['definicion']
    self.OutputList[no]['etiquetas'][ne]['mf'] = self.main.etiquetaMfOut.currentText()
    new_mf = self.OutputList[no]['etiquetas'][ne]['mf']
    new_definicion = update_definicionmf(self, old_mf, definicion, new_mf)
    new_definicion = round_list(new_definicion)
    self.main.etiquetaDefinicionOut.setText(str(new_definicion))
    definicion_out(self)


def definicion_out(self):
    no = self.main.outputNumber.currentIndex()
    ne = self.main.etiquetaNumOut.currentIndex()
    self.OutputList[no]['etiquetas'][ne]['definicion'] = json.loads(self.main.etiquetaDefinicionOut.text())
    self.fuzzController.update_definicion_output(self, self.OutputList, no, ne)
    
    
def round_list(lista):
    return list(np.around(np.array(lista),2))


def rule_list_visualizacion(self):
    if self.main.fuzzyTabWidget.currentIndex() == 3:
        
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
            self.inlabels[i].setText(entrada['nombre'])
            for etiqueta in entrada['etiquetas']:
                self.inlists[i].addItem(etiqueta['nombre'])
            self.inlists[i].addItem('None')
            self.inlists[i].setCurrentRow(0)
                
        for o, salida in enumerate(self.OutputList):
            self.outframes[o].show()
            self.outlabels[o].setText(salida['nombre'])
            for etiqueta in salida['etiquetas']:
                self.outlists[o].addItem(etiqueta['nombre'])
            self.outlists[o].addItem('None')
            self.outlists[o].setCurrentRow(0)


def rule_list_agregar(self):
    ni = len(self.InputList)
    no = len(self.OutputList)
    
    Etiquetasin = deque([])
    Etiquetasout = deque([])
    
    for i, entrada in enumerate(self.InputList):
        Etiquetasin.append(self.inlists[i].currentItem().text())
    
    for o, salida in enumerate(self.OutputList):
        Etiquetasout.append(self.outlists[o].currentItem().text())
    
    self.RuleEtiquetas.append(copy.deepcopy([Etiquetasin, Etiquetasout, self.main.andradioButton.isChecked()]))
    self.RuleList.append(self.fuzzController.agregar_regla(self, ni, no, Etiquetasin, Etiquetasout))
    self.main.rulelistWidget.addItem(str(self.RuleList[-1]))
    self.main.rulelistWidget.setCurrentRow(len(self.RuleList) - 1)


def rule_list_eliminar(self):
    if self.main.rulelistWidget.count():
        index_rule = self.main.rulelistWidget.currentRow()
        self.fuzzController.eliminar_regla(index_rule)
        self.main.rulelistWidget.takeItem(self.main.rulelistWidget.currentRow())
        del self.RuleList[index_rule]
        del self.RuleEtiquetas[index_rule]
    

def rule_list_cambiar(self):
    index_rule = self.main.rulelistWidget.currentRow()
    
    ni = len(self.InputList)
    no = len(self.OutputList)
    
    Etiquetasin = deque([])
    Etiquetasout = deque([])
    
    for i, entrada in enumerate(self.InputList):
        Etiquetasin.append(self.inlists[i].currentItem().text())
    
    for o, salida in enumerate(self.OutputList):
        Etiquetasout.append(self.outlists[o].currentItem().text())
    
    del self.RuleEtiquetas[index_rule]
    self.RuleEtiquetas.insert(index_rule, copy.deepcopy([Etiquetasin, Etiquetasout, self.main.andradioButton.isChecked()]))
    regla = self.fuzzController.cambiar_regla(self, ni, no, Etiquetasin, Etiquetasout, index_rule)
    self.main.rulelistWidget.takeItem(index_rule)
    self.main.rulelistWidget.insertItem(index_rule, str(regla))
    self.main.rulelistWidget.setCurrentRow(index_rule)
    del self.RuleList[index_rule]
    self.RuleList.insert(index_rule, regla)
    

def crear_controlador(self):
    if self.main.rulelistWidget.count():
        self.fuzzController = self.fuzzInitController(self.InputList, self.OutputList, self.RuleEtiquetas)
        self.main.fuzzyTabWidget.addTab(self.PruebaTab, 'Prueba')
        
        ni = len(self.InputList)
        no = len(self.OutputList)
        
        for it_f, ot_f, f2d, f3d in zip(self.intestframes, self.outtestframes, self.respuesta2dframes, self.respuesta3dframes):
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
            self.main.fuzzyTabWidget.addTab(self.RespuestaTab, 'Respuesta')
            self.main.respuestastackedWidget.setCurrentIndex(0)
            for o, salida in enumerate(self.OutputList):
                self.respuesta2dframes[o].show()      
            rimin, rimax = self.InputList[0]['rango']
            self.fuzzController.graficar_respuesta_2d(self, [rimin, rimax], no)
        
        if ni == 2:
            self.main.fuzzyTabWidget.addTab(self.RespuestaTab, 'Respuesta')
            self.main.respuestastackedWidget.setCurrentIndex(1)
            for o, salida in enumerate(self.OutputList):
                self.respuesta3dframes[o].show()     
            rimin1, rimax1 = self.InputList[0]['rango']
            rimin2, rimax2 = self.InputList[1]['rango']
            self.fuzzController.graficar_respuesta_3d(self, [rimin1, rimax1], [rimin2, rimax2], no)

def prueba_input(self):
    ni = len(self.InputList)
    no = len(self.OutputList)
        
    values = [i.value() for i in self.intestsliders[:ni]]
    
    for i, entrada in  enumerate(self.InputList[:ni]):
        rmin, rmax = entrada['rango']
        values[i] = values[i]*(rmax - rmin)/1000 + rmin
        self.intestlabels[i].setText(entrada['nombre'] + f': {np.around(values[i], 3)}')
    
    for o, salida in  enumerate(self.OutputList[:no]):
        self.outtestlabels[o].setText(salida['nombre'])
    
    self.fuzzController.prueba_de_controlador(self, values, ni, no)
    

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
    
    
