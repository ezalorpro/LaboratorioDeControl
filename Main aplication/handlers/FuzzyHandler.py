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
        ini_range_etiquetas = np.arange(-10, 11, 20/4).tolist()
        window = 0
        for j in range(self.InputList[i]['numeroE']):
            self.InputList[i]['etiquetas'][j] = inputEtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
            window += 1
            
    self.main.inputNumber.blockSignals(False)
    self.fuzzController = self.fuzzInitController(self.InputList, self.OutputList)
    seleccion_entrada(self)
    self.fuzzController.graficar_mf_in(self, 0)


def inputDic_creator(self, NumeroEntradas, i):
    inputDic = {
        
        'nombre': 'entrada' + str(i+1),
        'numeroE': 3,
        'etiquetas': [0]*3,
        'rango': [-10, 10],        
    }
    return inputDic


def inputEtiquetasDic_creator(self, j, erange):
    etiquetaDic = {
        'nombre': 'etiqueta' + str(j+1),
        'mf': 'trimf',
        'definicion': erange,
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
    return


def nombre_entrada(self):
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]['nombre'] = self.main.inputNombre.text()
    self.fuzzController.cambiar_nombre_input(self, ni, self.InputList[ni]['nombre'] )


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
        self.InputList[ni]['etiquetas'][j] = inputEtiquetasDic_creator(self, j, ini_range_etiquetas[window:window+3])
        window +=1
    
    self.main.etiquetaNombreIn.setText('etiqueta1')
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][0]['definicion']))
    self.main.etiquetaMfIn.setCurrentText('trimf')
    self.fuzzController.cambio_etiquetas_input(self, self.InputList, ni)
    self.main.etiquetaNumIn.blockSignals(False)


def rango_in(self):
    ni = self.main.inputNumber.currentIndex()
    self.InputList[ni]['rango'] = json.loads(self.main.inputRange.text())
    self.fuzzController.update_rango_input(self, self.InputList, ni)
    numero_de_etiquetas_in(self)


def seleccion_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    
    self.main.etiquetaNombreIn.setText(self.InputList[ni]['etiquetas'][ne]['nombre'])
    self.main.etiquetaMfIn.setCurrentText(self.InputList[ni]['etiquetas'][ne]['mf'])
    self.main.etiquetaDefinicionIn.setText(str(self.InputList[ni]['etiquetas'][ne]['definicion']))
    

def nombre_etiqueta_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    old_name = self.InputList[ni]['etiquetas'][ne]['nombre']
    self.InputList[ni]['etiquetas'][ne]['nombre'] = self.main.etiquetaNombreIn.text()
    
    self.fuzzController.cambio_etinombre_input(self, self.InputList, ni, ne, old_name)


def seleccion_mf_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    old_mf = self.InputList[ni]['etiquetas'][ne]['mf']
    definicion = self.InputList[ni]['etiquetas'][ne]['definicion']
    self.InputList[ni]['etiquetas'][ne]['mf'] = self.main.etiquetaMfIn.currentText()
    new_mf = self.InputList[ni]['etiquetas'][ne]['mf']
    new_definicion = update_definicionmf_input(self, old_mf, definicion, new_mf)
    self.main.etiquetaDefinicionIn.setText(new_definicion)
    definicion_in(self)
    
def definicion_in(self):
    ni = self.main.inputNumber.currentIndex()
    ne = self.main.etiquetaNumIn.currentIndex()
    self.InputList[ni]['etiquetas'][ne]['definicion'] = json.loads(self.main.etiquetaDefinicionIn.text())
    self.fuzzController.update_definicion_input(self, self.InputList, ni, ne)


# 100 condiciones if para ayudar al usuario con las formas generales de las funciones de membresia
def update_definicionmf_input(self, old_mf, definicion, new_mf):
    
    if old_mf == 'trimf':
        a, b, c = definicion
        
        if new_mf == 'trimf':
            na, nb, nc = a, b, c 
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na, nd = a, c
            nb = (a+b)/2
            nc = (b+c)/2
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = b
            sigma = (abs(c)+abs(a))/8
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = (a+b)/2
            sigma1 = (abs(c)+abs(a))/16
            mean2 = (b+c)/2
            sigma2 = (abs(c)+abs(a))/16
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = (a+b)/2
            nb = (b+c)/2
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = b 
            nc = 10/(abs(c)+abs(a))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = (a+b)/2
            nc1 = 20/(abs(c)+abs(a))
            nb2 = (b+c)/2 
            nc2 = -20/(abs(c)+abs(a))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na, nd = a, c
            nb = (a+b)/2
            nc = (b+c)/2
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(c) - abs(a)
            nb = 1/(a-b)
            nc = b
            return str([na, nb, nc])
        
    if old_mf == 'trapmf':
        a, b, c, d = definicion
        
        if new_mf == 'trimf':
            na, nc = a, d
            nb = (c+b)/2
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na, nb, nc, nd = a, b, c, d
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = (c+b)/2
            sigma = (abs(d)+abs(a))/8
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = b
            sigma1 = (abs(d)+abs(a))/16
            mean2 = c
            sigma2 = (abs(d)+abs(a))/16
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = b
            nb = c
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = (b+c)/2 
            nc = 10/(abs(d)+abs(a))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = b
            nc1 = 20/(abs(d)+abs(a))
            nb2 = c 
            nc2 = -20/(abs(d)+abs(a))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na, nd = a, d
            nb = b
            nc = c
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(d) - abs(a)
            nb = 1/(a - (b+c)/2)
            nc = (b+c)/2
            return str([na, nb, nc])
        
    if old_mf == 'gaussmf':
        a, b = definicion
        
        if new_mf == 'trimf':
            na = a - b*4
            nc = a + b*4
            nb = a
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na = a - b*4
            nb = a - b*2
            nc = a + b*2
            nd = a + b*4
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = a
            sigma = b
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = a - b*2
            sigma1 = b/2
            mean2 = a + b*2
            sigma2 = b/2
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = a - b*2
            nb = a + b*2
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = a 
            nc = 10/(abs(a + b*4)+abs(a - b*4))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = a - b*2
            nc1 = 20/(abs(a + b*4)+abs(a - b*4))
            nb2 = a + b*2 
            nc2 = -20/(abs(a + b*4)+abs(a - b*4))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na = a - b*4
            nb = a - b*2
            nc = a + b*2
            nd = a + b*4
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(a + b*4) - abs(a - b*4)
            nb = 1/(a - b*4 - a)
            nc = a
            return str([na, nb, nc])
        
        
    if old_mf == 'gauss2mf':
        a, b, c, d = definicion
        
        if new_mf == 'trimf':
            na = a - b*4
            nc = c + d*4
            nb = (a+c)/2
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na = a - b*4
            nb = a
            nc = c
            nd = c + d*4
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = (a+c)/2
            sigma = b*2
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = a
            sigma1 = b
            mean2 = c
            sigma2 = d
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = a
            nb = c
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = (a+c)/2 
            nc = 10/(abs(c + d*4)+abs(a - b*4))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = a
            nc1 = 20/(abs(c + d*4)+abs(a - b*4))
            nb2 = c
            nc2 = -20/(abs(c + d*4)+abs(a - b*4))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na = a - b*4
            nb = a
            nc = c
            nd = c + d*4
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(c + d*4) - abs(a - b*4)
            nb = 1/(a - b*4 - (a+c)/2)
            nc = a
            return str([na, nb, nc])
        
        
    if old_mf == 'smf' or old_mf == 'zmf':
        a, c = definicion
        
        if new_mf == 'trimf':
            na = a - (abs(a)+abs(c))/4
            nc = c  + (abs(a)+abs(c))/4
            nb = (a+c)/2
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na = a - (abs(a)+abs(c))/4
            nb = a
            nc = c
            nd = c  + (abs(a)+abs(c))/4
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = (a+c)/2
            sigma = abs(c-(a+c)/2)/2
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = a
            sigma1 = abs(c-(a+c)/2)/4
            mean2 = c
            sigma2 = abs(c-(a+c)/2)/4
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = a
            nb = c
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = (a+c)/2 
            nc = 10/(abs(c - (abs(a)+abs(c))/4)+abs(a  - (abs(a)+abs(c))/4))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = a
            nc1 = 20/(abs(c - (abs(a)+abs(c))/4)+abs(a  - (abs(a)+abs(c))/4))
            nb2 = c
            nc2 = -20/(abs(c - (abs(a)+abs(c))/4)+abs(a  - (abs(a)+abs(c))/4))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na = a - (abs(a)+abs(c))/4
            nb = a
            nc = c
            nd = c  + (abs(a)+abs(c))/4
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(c - (abs(a)+abs(c))/4) - abs(a  - (abs(a)+abs(c))/4)
            nb = 1/(a - (abs(a)+abs(c))/4 - (a+c)/2)
            nc = a
            return str([na, nb, nc])
        
    
    if old_mf == 'sigmf':
        b, c = definicion
        
        if new_mf == 'trimf':
            na = b - abs(c)*5
            nb = b 
            nc = b + abs(c)*5
            return str([na, nb, nc])
        
        if new_mf == 'trapmf':
            na = b - abs(c)*5
            nb = b - abs(c)*2.5
            nc = b + abs(c)*2.5
            nd = b + abs(c)*5
            return str([na, nb, nc, nd])

        if new_mf == 'gaussmf':
            mean = b
            sigma = (abs(c)+abs(a))/8
            return str([mean, sigma])
        
        if new_mf == 'gauss2mf':
            mean1 = (a+b)/2
            sigma1 = (abs(c)+abs(a))/16
            mean2 = (b+c)/2
            sigma2 = (abs(c)+abs(a))/16
            return str([mean1, sigma1, mean2, sigma2])
        
        if new_mf == 'smf' or new_mf == 'zmf':
            na = (a+b)/2
            nb = (b+c)/2
            return str([na, nb])
        
        if new_mf == 'sigmf':
            nb = b 
            nc = 10/(abs(c)+abs(a))
            return str([nb, nc])
        
        if new_mf == 'psigmf':
            nb1 = (a+b)/2
            nc1 = 20/(abs(c)+abs(a))
            nb2 = (b+c)/2 
            nc2 = -20/(abs(c)+abs(a))
            return str([nb1, nc1, nb2, nc2])
        
        if new_mf == 'pimf':
            na, nd = a, c
            nb = (a+b)/2
            nc = (b+c)/2
            return str([na, nb, nc, nd])
        
        if new_mf == 'gbellmf':
            na = abs(c) - abs(a)
            nb = 1/(a-b)
            nc = b
            return str([na, nb, nc])

