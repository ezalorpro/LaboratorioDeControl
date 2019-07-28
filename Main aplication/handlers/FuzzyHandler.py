from rutinas.rutinas_fuzzy import *
import json
import pprint


def FuzzyHandler(self):
    
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)
    
    self.main.generarFuzzyButton.clicked.connect(lambda: crear_tabs(self))
    
    self.main.inputNumber.currentIndexChanged.connect(lambda: seleccion_entrada(self))
    self.main.inputNombre.editingFinished.connect(lambda: nombre_entrada(self))
    self.main.inputEtiquetasNum.editingFinished.connect(lambda: numero_de_etiquetas_in(self))
    self.main.inputRange.editingFinished.connect(lambda: rango_in(self))
    
    self.main.etiquetaNumIn.currentIndexChanged.connect(lambda: seleccion_etiqueta_in(self))
    self.main.etiquetaNombreIn.editingFinished.connect(lambda: nombre_etiqueta_in(self))
    self.main.etiquetaMfIn.currentIndexChanged.connect(lambda: seleccion_mf_in(self))
    self.main.etiquetaDefinicionIn.editingFinished.connect(lambda: definicion_in(self))


def crear_tabs(self):
    self.main.inputNumber.blockSignals(True)
    self.InputList = []

    self.main.fuzzyTabWidget.addTab(self.EntradasTab, 'Entradas')
    self.main.fuzzyTabWidget.addTab(self.SalidasTab, 'Salidas')
    self.main.fuzzyTabWidget.addTab(self.ReglasTab, 'Reglas')
    self.main.fuzzyTabWidget.addTab(self.PruebaTab, 'Prueba')
    NumeroEntradas = int(self.main.estrucNumberInputs.currentText())
    NumeroSalidas = int(self.main.estrucNumberOutputs.currentText())
    
    self.main.inputNumber.clear()
    # self.main.outputNumber.clear()

    for i in range(NumeroEntradas):
        self.main.inputNumber.insertItem(i, str(i+1))
        temp_dic = inputDic_creator(self, NumeroEntradas, i)
        self.InputList.append(temp_dic)
        for j in range(self.InputList[i]['numeroE']):
            self.InputList[i]['etiquetas'][j] = inputEtiquetasDic_creator(self, j)
            
    self.main.inputNumber.blockSignals(False)
    seleccion_entrada(self)


def inputDic_creator(self, NumeroEntradas, i):
    inputDic = {
        
        'nombre': 'entrada' + str(i+1),
        'numeroE': 3,
        'etiquetas': [0]*3,
        'rango': [-10, 10],        
    }
    return inputDic


def inputEtiquetasDic_creator(self, j):
    etiquetaDic = {
        'nombre': 'etiqueta' + str(j+1),
        'mf': self.main.etiquetaMfIn.currentText(),
        'definicion': json.loads(self.main.etiquetaDefinicionIn.text()),
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
    return


def nombre_entrada(self):
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]['nombre'] = self.main.inputNombre.text()


def numero_de_etiquetas_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = int(self.main.inputEtiquetasNum.text())
    self.InputList[ni]['etiquetas'] = [0]*ne
    self.InputList[ni]['numeroE'] = ne
    self.main.etiquetaNumIn.blockSignals(True)
    self.main.etiquetaNumIn.clear()
    
    for j in range(self.InputList[ni]['numeroE']):
        self.main.etiquetaNumIn.insertItem(j, str(j+1))
        self.InputList[ni]['etiquetas'][j] = inputEtiquetasDic_creator(self, j)
    
    self.main.etiquetaNumIn.blockSignals(False)


def rango_in(self):
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]['rango'] = json.loads(self.main.inputRange.text())


def seleccion_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    
    self.main.etiquetaNombreIn.setText(self.InputList[ni]['etiquetas'][ne]['nombre'])
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]['etiquetas'][ne]['mf'])
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][ne]['definicion']))
    

def nombre_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreIn.text()


def seleccion_mf_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]['etiquetas'][ne]['mf'] = self.main.etiquetaMfIn.currentText()


def definicion_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]['etiquetas'][ne]['definicion'] = json.loads(self.main.etiquetaDefinicionIn.text())

# def etiquetasDic_creator(self, j):
    
#     etiquetaDic = {
#         'nombre': self.main.etiquetaNombreIn.text() + str(j),
#         'mf': self.main.etiquetaMfIn.currentText(),
#         'definicion': json.loads(self.main.etiquetaDefinicionIn.text()),
#     }
    
#     return etiquetaDic
    
    
# def inputDic_creator(self, NumeroEntradas, i):
    
#     inputDic = {
        
#         'nombre': self.main.inputNombre.text() + str(i),
#         'numeroE': int(self.main.inputEtiquetasNum.text()),
#         'etiquetas': [0]*int(self.main.inputEtiquetasNum.text()),
#         'rango': json.loads(self.main.inputRange.text()),        
#     }
    
#     return inputDic