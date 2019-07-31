import json
from collections import deque
import pickle

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

# json.dump(reglas, open("probando.json", 'w'))
# nueva_data2 = json.load(open("probando.json"))
# print(nueva_data2)