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
        
        self.fuzz_inputs = self.crear_input_output(inputlist)
        # self.fuzz_outputs = self.crear_input_output(outputlist)
        self.crear_etiquetas_input(inputlist)            
        
    def crear_input_output(self, inputlist):
        vector = []
        for i, ins in enumerate(inputlist):
            temp_in = fuzz.Antecedent(np.linspace(*ins['rango'], 100), ins['nombre'])
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
    
    def cambiar_nombre_input(self, window, i, nombre):
        
        self.fuzz_inputs[i].label = nombre

        self.graficar_mf_in(window, i)
    
    def cambio_etiquetas_input(self, window, inputlist, i):
        
        self.fuzz_inputs[i].terms = OrderedDict()
        self.crear_etiquetas_input(inputlist)
        self.graficar_mf_in(window, i)
    
    def cambio_etinombre_input( self, window, inputlist, i, n, old_name):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i].terms.pop(old_name)    
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        
        self.graficar_mf_in(window, i)
    
    def update_definicion_input(self, window, inputlist, i, n):
        eti = inputlist[i]['etiquetas'][n]
        self.fuzz_inputs[i][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[i].universe, *eti['definicion'])
        
        self.graficar_mf_in(window, i)
           
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