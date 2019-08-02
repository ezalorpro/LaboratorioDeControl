import json
from collections import deque
import pickle
import numpy as np
from skfuzzy import control as fuzz
from matplotlib import pyplot as plt

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


# def guardar_archivo(lista):
#     with open('probando.pkl', 'wb', ) as f:
#         pickle.dump([salidas, lista], f)
        
# def cargar_archivo():
#     with open('probando.pkl', 'rb') as f:
#         data1, data2 = pickle.load(f)
#     return data1, data2

# a = deque(['hola', 'andate', True])
# b = deque(['hola', 'andate', True])
# c = deque(['hola', 'andate', True])
# reglas = [a, b, c]

# guardar_archivo(reglas)
# nueva_data1, nueva_data2 = cargar_archivo()

# print(reglas)
# print(nueva_data2)

# print(salidas)
# print(nueva_data1)

# json.dump([['hola', 'chao'], [True, False], [1, 0.2]], open("probando.json", 'w'))
# a, b, c= json.load(open("probando.json"))

# print(a)
# print(b)
# print(c)

entrada1 = fuzz.Antecedent(np.linspace(-10, 10 + 20/500, 500), 'entrada1')
entrada2 = fuzz.Antecedent(np.linspace(-10, 10 + 20/500, 500), 'entrada2')
salida1 = fuzz.Consequent(np.linspace(-10, 10 + 20/500, 500), 'salida1', defuzzify_method='som')
salida2 = fuzz.Consequent(np.linspace(-10, 10 + 20/500, 500), 'salida2', defuzzify_method='som')

entrada1.automf(3, names=['etiqueta1', 'etiqueta2', 'etiqueta3'])
entrada2.automf(3, names=['etiqueta1', 'etiqueta2', 'etiqueta3'])
salida1.automf(3, names=['etiqueta1', 'etiqueta2', 'etiqueta3'])
salida2.automf(3, names=['etiqueta1', 'etiqueta2', 'etiqueta3'])

rule1 = fuzz.Rule(entrada1['etiqueta1'] & entrada2['etiqueta1'],
                   consequent=[salida1['etiqueta1']%1.0, salida2['etiqueta1']%1.0])

rule2 = fuzz.Rule(entrada1['etiqueta1'] | entrada2['etiqueta2'],
                   consequent=[salida1['etiqueta2']%1.0, salida2['etiqueta2']%1.0])

rule3 = fuzz.Rule(entrada1['etiqueta1'] | entrada2['etiqueta3'],
                   consequent=[salida1['etiqueta3']%0.5, salida2['etiqueta3']%0.5])

rule4 = fuzz.Rule(entrada1['etiqueta2'] | ~entrada2['etiqueta1'],
                   consequent=[salida1['etiqueta3']%0.5, salida2['etiqueta1']%0.5])

rule5 = fuzz.Rule(entrada1['etiqueta2'] & ~entrada2['etiqueta2'],
                   consequent=[salida1['etiqueta2']%0.5, salida2['etiqueta2']%0.5])

rule6 = fuzz.Rule(~entrada1['etiqueta2'] & entrada2['etiqueta3'],
                   consequent=[salida1['etiqueta1']%0.5, salida2['etiqueta3']%0.5])

rule7 = fuzz.Rule(entrada1['etiqueta3'] & entrada2['etiqueta1'],
                   consequent=[salida1['etiqueta1']%0.25, salida2['etiqueta3']%0.25])

rule8 = fuzz.Rule(~entrada1['etiqueta3'] & ~entrada2['etiqueta2'],
                   consequent=[salida1['etiqueta1']%0.25, salida2['etiqueta3']%0.25])

rule9 = fuzz.Rule(entrada1['etiqueta3'] & entrada2['etiqueta3'],
                   consequent=[salida2['etiqueta3']%0.25])


temp = fuzz.ControlSystem([rule1, rule2, rule3, rule4, rule5,
                           rule6, rule7, rule8, rule9])


controlador = fuzz.ControlSystemSimulation(temp)

controlador.input['entrada1'] = 10
controlador.input['entrada2'] = -10

controlador.compute()

out1 = controlador.output['salida1']
out2 = controlador.output['salida2']

print(out1)
print(out2)

salida1.view(sim=controlador)
salida2.view(sim=controlador)
plt.show()
