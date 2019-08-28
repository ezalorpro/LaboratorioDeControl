import json
from collections import deque
# import pickle
import controlmdf as ctrl
from skfuzzymdf import control as fuzz
from matplotlib import pyplot as plt
from matplotlib import figure
from mpl_toolkits.mplot3d import Axes3D
import time
import pyqtgraph as pg
import sys
from PySide2 import QtWidgets, QtCore, QtGui
import numpy as np
import pyvista as pv
from scipy import signal
from multiprocessing import Queue
import math
N = 30
derivadaf = ctrl.tf2ss(ctrl.TransferFunction([N, 0], [1, N]))
print(derivadaf)
ctrl.bode(derivadaf, dB=True, Hz=True)

# class Lowpassfilter:
#     """ Filtro pasa-bajo con ventaja Hamming"""

#     def __init__(self, order, fsampling, fpaso, coeficiente):

#         self.order = order
#         self.samples0 = [0]*order
#         self.fsampling = fsampling
#         self.fpaso = fpaso
#         self.h_n = signal.firwin(self.order, self.fpaso, fs=self.fsampling)*coeficiente
#         self.h_n = self.h_n.tolist()

#     def filtrar(self, entrada):

#         self.samples0.append(entrada)
#         self.samples0 = self.samples0[1:]
#         salida = sum(a * b for a, b in zip(self.samples0, self.h_n))
#         return salida


class Lowpassfilter:
    """ Filtro pasa-bajo con ventaja Hamming"""

    def __init__(self, order, fsampling, fpaso):

        self.order = order
        self.samples0 = order*[0]
        self.fsampling = fsampling
        self.fpaso = fpaso
        self.h_n = signal.firwin(self.order,
                                 self.fpaso,
                                 fs=self.fsampling) * 30
        self.h_n = self.h_n.tolist()
        print(self.h_n)

    def filtrar(self, entrada):

        self.samples0.append(entrada)
        self.samples0 = self.samples0[1:]
        salida = sum(a * b for a, b in zip(self.samples0, self.h_n))
        return salida
# [-0.3664505514016285, -4.578068971937084, 21.576763158929094, -4.578068971937084, -0.3664505514016285]

fs = 30
nyq = fs / 2

filtro = Lowpassfilter(5, fs, N/(2*np.pi))
# b, a = signal.butter(3, omega)
w, h = signal.freqz(filtro.h_n)

plt.figure(figsize=(11, 8))
plt.semilogx(w * nyq / np.pi, 20 * np.log10(abs(h)))
plt.title('Respuesta del filtro Butterworth')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.grid(which='both', axis='both')
plt.axvline(N * nyq / np.pi, color='green')  # Frecuencia de corte

# plt.savefig("Filtro Bode.png", bbox_inches='tight', pad_inches=0.1)
plt.show()

# fs = 1000 / 3
# nyq = fs / 2
# omega = 0.05

# b, a = signal.butter(3, omega)
# w, h = signal.freqz(b, a)

# plt.figure(figsize=(11, 8))
# plt.semilogx(w * nyq / np.pi, 20 * np.log10(abs(h)))
# plt.title('Respuesta del filtro Butterworth')
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude [dB]')
# plt.grid(which='both', axis='both')
# plt.axvline(omega * nyq, color='green')  # Frecuencia de corte

# plt.savefig("Filtro Bode.png", bbox_inches='tight', pad_inches=0.1)
# plt.show()

# start = 0.0001
# end = 30
# base = 1.2
# logs = np.geomspace(start, end, 200)
# t = np.linspace(0, 30, 2000)
# t_log = np.log(np.linspace(base**0, base**30, 2000))/np.log(base)
# plt.plot(t, t_log)
# plt.show()
# gs = ctrl.tf2ss(ctrl.tf([1], [1, 1, 1]))
# print(gs.returnScipySignalLTI()[0][0])
# pid = ctrl.tf([0, 7, 0], [1, 1])

# feed = ctrl.feedback(pid*gs)
# print(feed)

#          7 s
# ---------------------
# s^3 + 2 s^2 + 9 s + 1

# T = np.arange(0, 40, 0.1)
# lista = [1, 2, 0.5, 5, 0.25, 10, 1, 15, 0.3, 26, 0.7, 32]
# it = iter(lista)
# u = np.zeros_like(T)
# for i, x in enumerate(it):
#     ini = int(next(it) / 0.1)
#     u[ini:] = x

# plt.plot(T, u)
# plt.show()
# kp, ki, kd = map(float, ['3.7', '2', ''])

# print([kp, ki, kd])
# class ResultObj(QtCore.QObject):

#     def __init__(self, val):
#         self.val = val


# class SimpleThread(QtCore.QThread):
#     finished = QtCore.Signal(object)

#     def __init__(self, queue, callback, parent=None):
#         QtCore.QThread.__init__(self, parent)
#         self.queue = queue
#         self.finished.connect(callback)

#     def run(self):
#         while True:
#             arg = self.queue.get()
#             if arg is None:  # None means exit
#                 print("Shutting down")
#                 return
#             self.fun(arg)

#     def fun(self, arg):
#         for i in range(3):
#             print ('fun: %s' % i)
#             self.sleep(1)
#         self.finished.emit(ResultObj(arg + 1))


# class AppWindow(QtGui.QMainWindow):

#     def __init__(self):
#         super(AppWindow, self).__init__()
#         mainWidget = QtGui.QWidget()
#         self.setCentralWidget(mainWidget)
#         mainLayout = QtGui.QVBoxLayout()
#         mainWidget.setLayout(mainLayout)
#         button = QtGui.QPushButton('Process')
#         button.clicked.connect(self.process)
#         mainLayout.addWidget(button)

#     def handle_result(self, result):
#         val = result.val
#         print("got val {}".format(val))
#         # You can update the UI from here.

#     def process(self):
#         MAX_CORES = 1
#         self.queue = Queue()
#         self.threads = []
#         for i in range(MAX_CORES):
#             thread = SimpleThread(self.queue, self.handle_result)
#             self.threads.append(thread)
#             thread.start()

#         for arg in [1, 2, 3]:
#             self.queue.put(arg)

#         for _ in range(MAX_CORES):  # Tell the workers to shut down
#             self.queue.put(None)


# app = QtGui.QApplication([])
# window = AppWindow()
# window.show()
# sys.exit(app.exec_())

# class MainWindow(QtWidgets.QMainWindow):

#     def __init__(self, parent=None, show=True):
#         super(MainWindow, self).__init__(parent)

#         # create the frame
#         self.frame = QtWidgets.QFrame()
#         vlayout = QtWidgets.QVBoxLayout()

#         # add the pyvista interactor object
#         self.vtk_widget = pv.QtInteractor(self.frame)
#         vlayout.addWidget(self.vtk_widget)

#         self.frame.setLayout(vlayout)
#         self.setCentralWidget(self.frame)

#         # simple menu to demo functions
#         mainMenu = self.menuBar()
#         fileMenu = mainMenu.addMenu('File')
#         exitButton = QtWidgets.QAction('Exit', self)
#         exitButton.setShortcut('Ctrl+Q')
#         exitButton.triggered.connect(self.close)
#         fileMenu.addAction(exitButton)

#         # allow adding a sphere
#         meshMenu = mainMenu.addMenu('Mesh')
#         self.add_sphere_action = QtWidgets.QAction('Add Sphere', self)
#         self.add_sphere_action.triggered.connect(self.add_sphere)
#         meshMenu.addAction(self.add_sphere_action)
#         self.range = 2
#         if show:
#             self.show()

#     def add_sphere(self):
#         """ add a sphere to the pyqt frame """
#         self.vtk_widget.clear()

#         x_samp = np.logspace(-self.range, self.range, 200)
#         y_samp = np.logspace(-self.range, self.range, 200)
#         x, y = np.meshgrid(x_samp, y_samp)
#         a = -0.0001
#         z = a * (
#             np.abs(
#                 np.sin(x) * np.sin(y) *
#                 np.exp(np.abs(100 - np.sqrt(x**2 + y**2) / np.pi))
#             ) + 1
#         )**0.1

#         grid = pv.StructuredGrid(x, y, z)
#         grid['scalars'] = z.ravel('F')

#         xscale = (np.max(z) - np.min(z)) / (np.max(x) - np.min(x))
#         yscale = (np.max(z) - np.min(z)) / (np.max(y) - np.min(y))

#         self.vtk_widget.set_scale(xscale=xscale, yscale=yscale)
#         self.vtk_widget.add_mesh(
#             grid,
#             scalars='scalars',
#             cmap='viridis',
#             style='surface',
#             scalar_bar_args={'vertical': True}
#         )

#         self.vtk_widget.show_bounds(
#             grid='back',
#             location='outer',
#             ticks='both',
#             bounds=[np.min(x), np.max(x), np.min(y), np.max(y), np.min(z), np.max(z)]
#         )

#         self.vtk_widget.reset_camera()
#         self.range -= 1

# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())

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

# #QtWidgetsGui.QApplication.setGraphicsSystem('raster')
# app = QtWidgetsGui.QApplication([])
# mw = QtWidgetsGui.QMainWindow()
# mw.setWindowTitle('pyQtWidgetsgraph example: PlotWidget')
# mw.resize(800,800)
# cw = QtWidgetsGui.QWidget()
# mw.setCentralWidget(cw)
# l = QtWidgetsGui.QVBoxLayout()
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

# QtWidgetsGui.QApplication.instance().exec_()

# path = "c:\\Users\\PC\\Documents\\Descargas chrome\\NO TOCAR MALDITO IDIOTA!! ZZZZ\\kleiver\\Tesis\\Nueva tesis\\LaboratorioDeControl\\Main aplication\\main.py"
# print(path)
# file = path.split('\\')[-1]
# print(file)

# salidas = [
#     {
#         'nombre': 'output1',
#         'numeroE': 3,
#         'etiquetas':
#             [
#                 {
#                     'nombre': 'bajo',
#                     'mf': 'trimf',
#                     'definicion': [-11, -10, 0],},
#                 {
#                     'nombre': 'medio',
#                     'mf': 'trimf',
#                     'definicion': [-10, 0, 10],},
#                 {
#                     'nombre': 'alto',
#                     'mf': 'trimf',
#                     'definicion': [0, 10, 11],},
#             ],
#         'rango': [-10, 10],
#         'metodo': True
#     }
# ]

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

# json.dump([np.asarray([1, 2, 3, 4])], open("probando.json", 'w'))
# a, b, c= json.load(open("probando.json"))

# print(a)
# print(b)
# print(c)

# input1 = fuzz.Antecedent(np.linspace(-10, 10 + 20/5000, 5000), 'input1')
# input2 = fuzz.Antecedent(np.linspace(-10, 10 + 20/5000, 5000), 'input2')
# output1 = fuzz.Consequent(np.linspace(-10, 10 + 20/5000, 5000), 'output1', defuzzify_method='som')
# output2 = fuzz.Consequent(np.linspace(-10, 10 + 20/5000, 5000), 'output2', defuzzify_method='som')

# input1.automf(3, names=['label1', 'label2', 'label3'])
# input2.automf(3, names=['label1', 'label2', 'label3'])
# output1.automf(3, names=['label1', 'label2', 'label3'])
# output2.automf(3, names=['label1', 'label2', 'label3'])

# rule1 = fuzz.Rule(input1['label1'] & input2['label1'],
#                    consequent=[output1['label1']%1.0, output2['label1']%1.0])

# rule2 = fuzz.Rule(input1['label1'] | input2['label2'],
#                    consequent=[output1['label2']%1.0, output2['label2']%1.0])

# rule3 = fuzz.Rule(input1['label1'] | input2['label3'],
#                    consequent=[output1['label3']%0.5, output2['label3']%0.5])

# rule4 = fuzz.Rule(input1['label2'] | ~input2['label1'],
#                    consequent=[output1['label3']%0.5, output2['label1']%0.5])

# rule5 = fuzz.Rule(input1['label2'] & ~input2['label2'],
#                    consequent=[output1['label2']%0.5, output2['label2']%0.5])

# rule6 = fuzz.Rule(~input1['label2'] & input2['label3'],
#                    consequent=[output1['label1']%0.5, output2['label3']%0.5])

# rule7 = fuzz.Rule(input1['label3'] & input2['label1'],
#                    consequent=[output1['label1']%0.25, output2['label3']%0.25])

# rule8 = fuzz.Rule(~input1['label3'] & ~input2['label2'],
#                    consequent=[output1['label1']%0.25, output2['label3']%0.25])

# rule9 = fuzz.Rule(input1['label3'] & input2['label3'],
#                    consequent=[output2['label3']%0.25])

# temp = fuzz.ControlSystem([rule1, rule2, rule3, rule4, rule5,
#                            rule6, rule7, rule8, rule9])

# controlador = fuzz.ControlSystemSimulation(temp)

# controlador.input['input1'] = 10
# controlador.input['input2'] = -10

# controlador.compute()

# out1 = controlador.output['output1']
# out2 = controlador.output['output2']

# print(out1)
# print(out2)

# output1.view(sim=controlador)
# output2.view(sim=controlador)
# plt.show()

# print(np.around(2.5, 0))