import json
from collections import deque
import pickle
import numpy as np
import controlmdf as ctrl
from skfuzzymdf import control as fuzz
from matplotlib import pyplot as plt
from matplotlib import figure
from mpl_toolkits.mplot3d import Axes3D
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
import time 


# colors = [
#     '#1f77b4',
#     '#ff7f0e',
#     '#2ca02c',
#     '#d62728',
#     '#9467bd',
#     '#8c564b',
#     '#e377c2',
#     '#7f7f7f',
#     '#bcbd22',
#     '#17becf'
# ]
# a, b, c = json.load(open("datosFill"))
# print(int('6A', 16))
# pg.setConfigOption('background', 'w')
# pg.setConfigOption('foreground', 'k')

# #QtGui.QApplication.setGraphicsSystem('raster')
# app = QtGui.QApplication([])
# mw = QtGui.QMainWindow()
# mw.setWindowTitle('pyqtgraph example: PlotWidget')
# mw.resize(800,800)
# cw = QtGui.QWidget()
# mw.setCentralWidget(cw)
# l = QtGui.QVBoxLayout()
# cw.setLayout(l)

# pw = pg.PlotWidget(name='Plot1')  ## giving the plots names allows us to link their axes together
# l.addWidget(pw)

# mw.show()

# c1 = pw.plot(np.asarray([0, 5, 10]),np.asarray([0, 1, 0]), pen={'width': 2, 'color':pg.mkColor(colors[0])})
# c2 = pw.plot(np.asarray([-5, 0, 5]),np.asarray([0, 1, 0]), pen={'width': 2, 'color':pg.mkColor(colors[1])})
# c3 = pw.plot(np.asarray([1.2, 1.2]), [0, 0.235], pen={'width': 6, 'color':'k'})
# top1 = pw.plot(np.array(a), np.array(b), pen={'width': 5, 'color':pg.mkColor(colors[0]+'6A')})
# top2 = pw.plot(np.array(a), np.array(c), pen={'width': 5, 'color':pg.mkColor(colors[0]+'6A')})

# fill = pg.FillBetweenItem(top1, top2, brush=pg.mkColor(colors[0]+'6A'))

# pw.addItem(fill)

# pw.enableMouse(False)


# c1.setData(np.asarray([-1, 5, 10]),np.asarray([0, 1, 0]))
# c2.setData(np.asarray([-6, 0, 5]),np.asarray([0, 1, 0]))

# QtGui.QApplication.instance().exec_()

# path = "c:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication\\main.py"
# print(path)
# file = path.split('\\')[-1]
# print(file)

# salidas = [
#         {
#             'nombre': 'output1',
#             'numeroE': 3,
#             'etiquetas': [
#                 {
#                     'nombre': 'bajo',
#                     'mf': 'trimf',
#                     'definicion': [-11, -10, 0],
#                 },
#                 {
#                     'nombre': 'medio',
#                     'mf': 'trimf',
#                     'definicion': [-10, 0, 10],
#                 },
#                 {
#                     'nombre': 'alto',
#                     'mf': 'trimf',
#                     'definicion': [0, 10, 11],
#                 },
#                 ],
#             'rango': [-10, 10],
#             'metodo': True
#         }
#     ]


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

input1 = fuzz.Antecedent(np.linspace(-10, 10 + 20/5000, 5000), 'input1')
input2 = fuzz.Antecedent(np.linspace(-10, 10 + 20/5000, 5000), 'input2')
output1 = fuzz.Consequent(np.linspace(-10, 10 + 20/5000, 5000), 'output1', defuzzify_method='som')
output2 = fuzz.Consequent(np.linspace(-10, 10 + 20/5000, 5000), 'output2', defuzzify_method='som')

input1.automf(3, names=['label1', 'label2', 'label3'])
input2.automf(3, names=['label1', 'label2', 'label3'])
output1.automf(3, names=['label1', 'label2', 'label3'])
output2.automf(3, names=['label1', 'label2', 'label3'])

rule1 = fuzz.Rule(input1['label1'] & input2['label1'],
                   consequent=[output1['label1']%1.0, output2['label1']%1.0])

rule2 = fuzz.Rule(input1['label1'] | input2['label2'],
                   consequent=[output1['label2']%1.0, output2['label2']%1.0])

rule3 = fuzz.Rule(input1['label1'] | input2['label3'],
                   consequent=[output1['label3']%0.5, output2['label3']%0.5])

rule4 = fuzz.Rule(input1['label2'] | ~input2['label1'],
                   consequent=[output1['label3']%0.5, output2['label1']%0.5])

rule5 = fuzz.Rule(input1['label2'] & ~input2['label2'],
                   consequent=[output1['label2']%0.5, output2['label2']%0.5])

rule6 = fuzz.Rule(~input1['label2'] & input2['label3'],
                   consequent=[output1['label1']%0.5, output2['label3']%0.5])

rule7 = fuzz.Rule(input1['label3'] & input2['label1'],
                   consequent=[output1['label1']%0.25, output2['label3']%0.25])

rule8 = fuzz.Rule(~input1['label3'] & ~input2['label2'],
                   consequent=[output1['label1']%0.25, output2['label3']%0.25])

rule9 = fuzz.Rule(input1['label3'] & input2['label3'],
                   consequent=[output2['label3']%0.25])


temp = fuzz.ControlSystem([rule1, rule2, rule3, rule4, rule5,
                           rule6, rule7, rule8, rule9])


controlador = fuzz.ControlSystemSimulation(temp)

controlador.input['input1'] = 10
controlador.input['input2'] = -10

controlador.compute()

out1 = controlador.output['output1']
out2 = controlador.output['output2']

print(out1)
print(out2)

output1.view(sim=controlador)
output2.view(sim=controlador)
plt.show()

print(np.around(2.5, 0))