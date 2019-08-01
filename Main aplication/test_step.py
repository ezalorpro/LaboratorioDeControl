import json
from collections import deque
import pickle
import numpy as np
from skfuzzy import control as fuzz

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
            'metodo': True
        }
    ]


def guardar_archivo(lista):
    with open('probando.pkl', 'wb', ) as f:
        pickle.dump([salidas, lista], f)
        
def cargar_archivo():
    with open('probando.pkl', 'rb') as f:
        data1, data2 = pickle.load(f)
    return data1, data2

a = deque(['hola', 'andate', True])
b = deque(['hola', 'andate', True])
c = deque(['hola', 'andate', True])
reglas = [a, b, c]

guardar_archivo(reglas)
nueva_data1, nueva_data2 = cargar_archivo()

print(reglas)
print(nueva_data2)

print(salidas)
print(nueva_data1)

json.dump([['hola', 'chao'], [True, False], [1, 0.2]], open("probando.json", 'w'))
a, b, c= json.load(open("probando.json"))

print(a)
print(b)
print(c)

entrada = fuzz.Antecedent(np.linspace(-10, 10, 100), 'entrada')
salida = fuzz.Consequent(np.linspace(-10, 10, 100), 'entrada')

entrada.automf(3, names=['hola', 'hola2', 'hola3'])
salida.automf(3, names=['hola', 'hola2', 'hola3'])

rule = fuzz.Rule()

rule.antecedent = ~entrada['hola']
rule.consequent = salida['hola']
print(rule)