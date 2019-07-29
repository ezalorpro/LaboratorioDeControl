import numpy as np
from skfuzzymdf import control as fuzz
from skfuzzymdf.membership import generatemf
from skfuzzymdf.control.visualization import FuzzyVariableVisualizer
from collections import deque
from collections import OrderedDict
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import json


class FuzzyController():
    
    def __init__(self, inputlist, outputlist, rulelist=None): 
        self.fuzz_inputs = self.crear_input(inputlist)
        self.fuzz_outputs = self.crear_output(outputlist)
        self.crear_etiquetas_input(inputlist)
        self.crear_etiquetas_output(outputlist)           
        
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
        FuzzyVariableVisualizer(self.fuzz_inputs[i], window.main.inputgraphicsView, window.main.inputgraphicsView.canvas.axes).view()
        window.main.inputgraphicsView.canvas.draw()
        window.main.inputgraphicsView.toolbar.update()
    
    def graficar_mf_out(self, window, o):
        window.main.outputgraphicsView.canvas.axes.clear()
        FuzzyVariableVisualizer(self.fuzz_outputs[o], window.main.outputgraphicsView, window.main.outputgraphicsView.canvas.axes).view()
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
            'rango': [-10, 10],
            'metadata': None
        },
        {
            'nombre': 'd_error',
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
            'metadata': None
        }
    ]
    
    salidas = [
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
            'rango': [-10, 10],
            'metadata': None
        },
        {
            'nombre': 'd_error',
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
            'metadata': None
        }
    ]
    
    FuzzyController(entradas, salidas)