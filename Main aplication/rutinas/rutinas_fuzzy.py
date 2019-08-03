import numpy as np
from skfuzzymdf import control as fuzz
from skfuzzymdf.membership import generatemf
from skfuzzymdf.control.visualization import FuzzyVariableVisualizer
from collections import deque
from collections import OrderedDict
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import copy


class FuzzyController():
    
    def __init__(self, inputlist, outputlist, rulelist=[]):
        self.fuzz_inputs = self.crear_input(inputlist)
        self.fuzz_outputs = self.crear_output(outputlist)
        self.rulelist = []
        self.crear_etiquetas_input(inputlist)
        self.crear_etiquetas_output(outputlist)
        
        if len(rulelist) > 0:
            self.crear_reglas(rulelist)
            self.crear_controlador()     
        
    def crear_input(self, inputlist):
        vector = []
        for i, ins in enumerate(inputlist):
            temp_in = fuzz.Antecedent(np.linspace(*ins['rango'], 500), ins['nombre'])
            vector.append(temp_in)
        return vector
    
    def crear_output(self, outputlist):
        vector = []
        for i, ins in enumerate(outputlist):
            temp_in = fuzz.Consequent(np.linspace(*ins['rango'], 500), ins['nombre'], ins['metodo'])
            vector.append(temp_in)
        return vector
    
    def crear_etiquetas_input(self, inputlist):
        
        for n, i in enumerate(inputlist):
            for eti in i['etiquetas']:
                self.fuzz_inputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[n].universe, *eti['definicion'])

    def crear_etiquetas_output(self, outputlist):
        for n, i in enumerate(outputlist):
            for eti in i['etiquetas']:
                self.fuzz_outputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[n].universe, *eti['definicion'])

    def graficar_mf_in(self, window, i):
        window.main.inputgraphicsView.canvas.axes.clear()
        FuzzyVariableVisualizer(self.fuzz_inputs[i], 
                                window.main.inputgraphicsView, 
                                window.main.inputgraphicsView.canvas.axes).view()
        window.main.inputgraphicsView.canvas.axes.grid(color="lightgray")
        window.main.inputgraphicsView.canvas.draw()
        window.main.inputgraphicsView.toolbar.update()
    
    def graficar_mf_out(self, window, o):
        window.main.outputgraphicsView.canvas.axes.clear()
        FuzzyVariableVisualizer(self.fuzz_outputs[o], 
                                window.main.outputgraphicsView, 
                                window.main.outputgraphicsView.canvas.axes).view()
        window.main.outputgraphicsView.canvas.axes.grid(color="lightgray")
        window.main.outputgraphicsView.canvas.draw()
        window.main.outputgraphicsView.toolbar.update()
        
    def cambiar_nombre_input(self, window, i, nombre):
        self.fuzz_inputs[i].label = nombre
        self.graficar_mf_in(window, i)
    
    def cambiar_nombre_output(self, window, o, nombre):
        self.fuzz_outputs[o].label = nombre
        self.graficar_mf_out(window, o)
        
    def cambio_etiquetas_input(self, window, inputlist, i):
        self.fuzz_inputs[i].terms = OrderedDict()
        self.crear_etiquetas_input(inputlist)
        self.graficar_mf_in(window, i)
    
    def cambio_etiquetas_output(self, window, outputlist, o):
        self.fuzz_outputs[o].terms = OrderedDict()
        self.crear_etiquetas_output(outputlist)
        self.graficar_mf_out(window, o)
    
    def update_rango_input(self, window, inputlist, i):
        self.fuzz_inputs[i].universe = np.asarray(np.linspace(*inputlist[i]['rango'], 500))
        self.graficar_mf_in(window, i)
    
    def update_rango_output(self, window, outputlist, o):
        self.fuzz_outputs[o].universe = np.asarray(np.linspace(*outputlist[o]['rango'], 500))
        self.graficar_mf_out(window, o)
    
    def cambiar_metodo(self, window, o, metodo):
        self.fuzz_inputs[o].defuzzify_method = metodo
             
    def cambio_etinombre_input( self, window, inputlist, i, n, old_name):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i].terms.pop(old_name)    
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)
    
    def cambio_etinombre_output( self, window, outputlist, o, n, old_name):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o].terms.pop(old_name)    
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[o].universe, *eti['definicion'])
        self.graficar_mf_out(window, o)
        
    def update_definicion_input(self, window, inputlist, i, n):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        self.graficar_mf_in(window, i)
        
    def update_definicion_output(self, window, outputlist, o, n):
        eti = outputlist[o]['etiquetas'][n]
        self.fuzz_outputs[o][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[o].universe, *eti['definicion'])
        self.graficar_mf_out(window, o)

    def crear_reglas(self, rulelistC):
        for sets in rulelistC:
            Etiquetasin, Etiquetasout, logica = copy.deepcopy(sets)
            
            self.rulelist.append(fuzz.Rule())
         
            inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
            
            if not negacion_ini:
                self.rulelist[-1].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
            else:
                self.rulelist[-1].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
                
            outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
            
            self.rulelist[-1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
            
            for i in Etiquetasin[1:len(Etiquetasin)]:
                if logica:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
                else:
                    if not i[2]:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                    else:
                        self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
            
            for o in Etiquetasout[1:len(Etiquetasout)]:
                self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])
    
    def agregar_regla(self, window, ni, no, Etiquetasin, Etiquetasout):
        
        self.rulelist.append(fuzz.Rule())
         
        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
        
        if not negacion_ini:
            self.rulelist[-1].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
        else:
            self.rulelist[-1].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
            
        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
        
        self.rulelist[-1].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
        
        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[-1].antecedent = self.rulelist[-1].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
        
        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[-1].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])

        return self.rulelist[-1]
    
    def eliminar_regla(self, index_rule):
        del self.rulelist[index_rule]
    
    def cambiar_regla(self, window, ni, no, Etiquetasin, Etiquetasout, index_rule):
        del self.rulelist[index_rule]
        self.rulelist.insert(index_rule, fuzz.Rule())
        
        inetiqueta_ini, ni_ini, negacion_ini = Etiquetasin[0]
        
        if not negacion_ini:
            self.rulelist[index_rule].antecedent = self.fuzz_inputs[ni_ini][inetiqueta_ini]
        else:
            self.rulelist[index_rule].antecedent = ~self.fuzz_inputs[ni_ini][inetiqueta_ini]
            
        outetiqueta_oni, no_ini, weight_ini = Etiquetasout[0]
        
        self.rulelist[index_rule].consequent = self.fuzz_outputs[no_ini][outetiqueta_oni]%weight_ini
        
        for i in Etiquetasin[1:len(Etiquetasin)]:
            if window.main.andradioButton.isChecked():
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent & self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent & ~self.fuzz_inputs[i[1]][i[0]]
            else:
                if not i[2]:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent | self.fuzz_inputs[i[1]][i[0]]
                else:
                    self.rulelist[index_rule].antecedent = self.rulelist[index_rule].antecedent | ~self.fuzz_inputs[i[1]][i[0]]
        
        for o in Etiquetasout[1:len(Etiquetasout)]:
            self.rulelist[index_rule].consequent.append(self.fuzz_outputs[o[1]][o[0]]%o[2])

        return self.rulelist[index_rule]
    
    def crear_controlador(self):
        temp = fuzz.ControlSystem(self.rulelist)
        self.Controlador = fuzz.ControlSystemSimulation(temp, flush_after_run=20000)
        
    def prueba_de_controlador(self, window, values, ni, no):
        for i in range(ni):
            self.Controlador.input[self.fuzz_inputs[i].label] = values[i]
            
        self.Controlador.compute()
        self.graficar_prueba(window, ni, no)
    
    def graficar_prueba(self, window, ni, no):
        for i, grafica in enumerate(window.ingraphs[:ni]):
            grafica.canvas.axes.clear()
            FuzzyVariableVisualizer(self.fuzz_inputs[i], 
                                    grafica, 
                                    grafica.canvas.axes).view(self.Controlador, legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()
            
        for o, grafica in enumerate(window.outgraphs[:no]):
            grafica.canvas.axes.clear()
            value = FuzzyVariableVisualizer(self.fuzz_outputs[o], 
                                    grafica, 
                                    grafica.canvas.axes).view(self.Controlador, legend=False)
            grafica.canvas.axes.grid(color="lightgray")
            grafica.canvas.draw()
            
            window.outtestlabels[o].setText(window.OutputList[o]['nombre'] + f': {np.around(value, 3)}')
    
    def graficar_respuesta_2d(self, window, inrange, no):
        entrada = np.linspace(*inrange, 500)
        
        entradas = []
        salidas = [[] for i in range(no)]
        
        for value in entrada :
            self.Controlador.input[self.fuzz_inputs[0].label] = value
            try:
                self.Controlador.compute()
                entradas.append(value)
                for i in range(no):
                    salidas[i].append(self.Controlador.output[self.fuzz_outputs[i].label])
            except:
                pass
        
        for i in range(no):
            window.respuesta2ds[i].canvas.axes.clear()
            window.respuesta2ds[i].canvas.axes.plot(entradas, salidas[i])
            window.respuesta2ds[i].canvas.axes.grid(color="lightgray")
            window.respuesta2ds[i].canvas.axes.set_xlabel(self.fuzz_inputs[0].label)
            window.respuesta2ds[i].canvas.axes.set_ylabel(self.fuzz_outputs[i].label)
            window.respuesta2ds[i].canvas.draw()
            window.respuesta2ds[i].toolbar.update()
            
    def graficar_respuesta_3d(self, window, inrange1, inrange2, no):
        n_puntos = 20
        entrada1 = np.linspace(*inrange1, n_puntos)
        entrada2 = np.linspace(*inrange2, n_puntos)
        entrada1, entrada2 = np.meshgrid(entrada1, entrada2)
        
        entrada11 = [np.zeros_like(entrada1) for i in range(no)]
        entrada22 = [np.zeros_like(entrada1) for i in range(no)]
        
        salidas = [np.zeros_like(entrada1) for i in range(no)]
		
        for i in range(n_puntos) :
            for j in range(n_puntos):
                self.Controlador.input[self.fuzz_inputs[0].label] = entrada1[i, j]
                self.Controlador.input[self.fuzz_inputs[1].label] = entrada2[i, j]
                try:
                    self.Controlador.compute()
                    for o in range(no):
                        entrada11[o][i, j] =  entrada1[i, j]
                        entrada22[o][i, j] = entrada2[i, j]
                        salidas[o][i, j] = self.Controlador.output[self.fuzz_outputs[o].label]
                except:
                    pass
                     
        for o in range(no):
            window.respuesta3ds[o].canvas.axes.clear()
            surface = window.respuesta3ds[o].canvas.axes.plot_surface(entrada11[o], entrada22[o], salidas[o], 
                                                            rstride=1, cstride=1, cmap='viridis', linewidth=0.4, antialiased=True)
           
            window.respuesta3ds[o].canvas.figure.colorbar(surface)
            
            window.respuesta3ds[o].canvas.axes.view_init(30, 200)
            window.respuesta3ds[o].canvas.axes.set_xlabel(self.fuzz_inputs[0].label)
            window.respuesta3ds[o].canvas.axes.set_ylabel(self.fuzz_inputs[1].label)
            window.respuesta3ds[o].canvas.axes.set_zlabel(self.fuzz_outputs[o].label)
            window.respuesta3ds[o].canvas.draw() 

if __name__ == "__main__":
    
    entradas = [
        {
            'nombre': 'error',
            'numeroE': 3,
            'etiquetas': [
                {
                    'nombre': 'bajo',
                    'mf': 'trimf',
                    'definicion': [-11, -10, 0],
                },
                {
                    'nombre': 'medio',
                    'mf': 'trimf',
                    'definicion': [-10, 0, 10],
                },
                {
                    'nombre': 'alto',
                    'mf': 'trimf',
                    'definicion': [0, 10, 11],
                },
                ],
            'rango': [-10, 10]
        }
    ]
    
    salidas = [
        {
            'nombre': 'salida1',
            'numeroE': 3,
            'etiquetas': [
                {
                    'nombre': 'bajo',
                    'mf': 'trimf',
                    'definicion': [-11, -10, 0],
                },
                {
                    'nombre': 'medio',
                    'mf': 'trimf',
                    'definicion': [-10, 0, 10],
                },
                {
                    'nombre': 'alto',
                    'mf': 'trimf',
                    'definicion': [0, 10, 11],
                },
                ],
            'rango': [-10, 10],
            'metodo': 'centroid'
        }
    ]
    
    rulelist = []
    Etiquetasin = [['bajo'], ['medio'], ['alto']]
    Etiquetasout = [['alto'], ['bajo'], ['bajo']]
    controlador = FuzzyController(entradas, salidas)
    for i in range(3):
        rulelist.append(controlador.agregar_regla(None, 1, 1, Etiquetasin[i], Etiquetasout[i]))
        
    controlador.rulelist = rulelist
    controlador.crear_controlador()
    
    fig, ax = plt.subplots()
    FuzzyVariableVisualizer(controlador.fuzz_inputs[0], 
                                    fig, 
                                    ax).view(controlador.Controlador, legend=False)