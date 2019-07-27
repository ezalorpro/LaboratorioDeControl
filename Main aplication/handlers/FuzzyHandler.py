from rutinas.rutinas_fuzzy import *
import json
import pprint


def FuzzyHandler(self):
    
    self.main.fuzzyTabWidget.removeTab(4)
    self.main.fuzzyTabWidget.removeTab(3)
    self.main.fuzzyTabWidget.removeTab(2)
    self.main.fuzzyTabWidget.removeTab(1)
    
    self.main.crearFuzzyButton.clicked.connect(lambda: crear_tabs(self))
    
    self.main.inputNumber.currentIndexChanged.connect(lambda: seleccion_entrada(self))
    self.main.inputNombre.editingFinished.connect(lambda: nombre_entrada(self))
    self.main.inputEtiquetasNum.editingFinished.connect(lambda: numero_de_etiquetas(self))
    
    
    
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

def inputEtiquetasDic_creator(self, j):
    
    etiquetaDic = {
        'nombre': 'etiqueta' + str(j+1),
        'mf': self.main.etiquetaMf.currentText(),
        'definicion': json.loads(self.main.etiquetaDefinicion.text()),
    }
    
    return etiquetaDic
    
    
def inputDic_creator(self, NumeroEntradas, i):
    
    inputDic = {
        
        'nombre': 'entrada' + str(i+1),
        'numeroE': int(self.main.inputEtiquetasNum.text()),
        'etiquetas': [0]*int(self.main.inputEtiquetasNum.text()),
        'rango': json.loads(self.main.inputRange.text()),        
    }
    
    return inputDic

    
def seleccion_entrada(self):
    numero_input = self.main.inputNumber.currentIndex()
    self.main.inputNombre.setText(self.InputList[numero_input]['nombre'])
    self.main.inputEtiquetasNum.setText(str(self.InputList[numero_input]['numeroE']))
    self.main.inputRange.setText(str(self.InputList[numero_input]['rango']))
    
    self.main.etiquetaNum.clear()
    
    for j in range(self.InputList[numero_input]['numeroE']):
        self.main.etiquetaNum.insertItem(j, str(j+1))
    
    self.main.etiquetaNombre.setText(self.InputList[numero_input]['etiquetas'][0]['nombre'])
    self.main.etiquetaMf.setCurrentText(self.InputList[numero_input]['etiquetas'][0]['mf'])
    self.main.etiquetaDefinicion.setText(str(self.InputList[numero_input]['etiquetas'][0]['definicion']))
    return


def nombre_entrada(self):
    numero_input = self.main.inputNumber.currentIndex()
    self.InputList[numero_input]['nombre'] = self.main.inputNombre.text()

def numero_de_etiquetas(self):
    
    numero_input = self.main.inputNumber.currentIndex()
    Numero_Etiquetas = int(self.main.inputEtiquetasNum.text())
    
    self.InputList[numero_input]['etiquetas'] = [0]*Numero_Etiquetas
    self.InputList[numero_input]['numeroE'] = Numero_Etiquetas
    
    self.main.etiquetaNum.clear()
    
    for j in range(self.InputList[numero_input]['numeroE']):
        self.main.etiquetaNum.insertItem(j, str(j+1))
        self.InputList[numero_input]['etiquetas'][j] = inputEtiquetasDic_creator(self, j)






# def etiquetasDic_creator(self, j):
    
#     etiquetaDic = {
#         'nombre': self.main.etiquetaNombre.text() + str(j),
#         'mf': self.main.etiquetaMf.currentText(),
#         'definicion': json.loads(self.main.etiquetaDefinicion.text()),
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