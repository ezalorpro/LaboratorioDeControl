import numpy as np
from skfuzzymdf import control as fuzz
from skfuzzymdf.membership import generatemf
from skfuzzymdf.control.visualization import FuzzyVariableVisualizer
from collections import deque
from matplotlib import pyplot as plt
import matplotlib.ticker as mticker
import json

class FuzzyController():
    
    def __init__(self, inputlist, outputlist, rulelist=None):
        
        self.fuzz_inputs = self.crear_input_output(inputlist)
        self.fuzz_outputs = self.crear_input_output(outputlist)
        self.crear_etiquetas(inputlist, outputlist)
        
        for inp in self.fuzz_inputs:
            fig, ax = FuzzyVariableVisualizer(inp).view()
            plt.show()
            
        
    def crear_input_output(self, inputlist):
        vector = []
        for i, ins in enumerate(inputlist):
            temp_in = fuzz.Antecedent(np.linspace(*ins['rango'], 5*ins['numeroE']), ins['nombre'])
            vector.append(temp_in)
        return vector
    
    def crear_etiquetas(self, inputlist, outputlist):
        
        for n, i in enumerate(inputlist):
            for eti in i['etiquetas']:
                self.fuzz_inputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_inputs[n].universe, eti['definicion'])
                
        for n, i in enumerate(outputlist):
            for eti in i['etiquetas']:
                self.fuzz_outputs[n][eti['nombre']] = getattr(generatemf, eti['mf'])(self.fuzz_outputs[n].universe, eti['definicion'])

                
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