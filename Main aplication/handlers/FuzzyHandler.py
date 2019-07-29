from rutinas.rutinas_fuzzy import *
from handlers.modificadorMf import update_definicionmf
import json
import pprint


def FuzzyHandler(self):
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)
    
    self.main.generarFuzzyButton.clicked.connect(lambda: crear_tabs(self))
    
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


def crear_tabs(self):
    self.main.inputNumber.blockSignals(True)
    self.main.outputNumber.blockSignals(True)
    self.InputList = []
    self.OutputList = []

    self.main.fuzzyTabWidget.addTab(self.EntradasTab, 'Entradas')
    self.main.fuzzyTabWidget.addTab(self.SalidasTab, 'Salidas')
    self.main.fuzzyTabWidget.addTab(self.ReglasTab, 'Reglas')
    self.main.fuzzyTabWidget.addTab(self.PruebaTab, 'Prueba')
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
    # self.fuzzController.graficar_mf_out(self, 0)


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
    self.InputList[ni]['nombre'] = self.main.inputNombre.text()
    self.fuzzController.cambiar_nombre_input(self, ni, self.InputList[ni]['nombre'])


def nombre_salida(self):
    no = self.main.outputNumber.currentIndex()
    self.OutputList[no]['nombre'] = self.main.outputNombre.text()
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
