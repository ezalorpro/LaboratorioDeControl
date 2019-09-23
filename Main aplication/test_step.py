import controlmdf as ctrl
import numpy as np
from numpy import real as REAL
from numpy import imag as IMAG
from matplotlib import pyplot as plt

a = np.asarray([-1, 0, 2, 0, -1, 2, 3, 4])
crossHack1 = np.diff(1 * (a > -190) != 0)
crossHack2 = np.diff(1 * (a > -170) != 0)
crossHack = ~crossHack1 * ~crossHack2
gg = np.diff(1 * (a <= 0) != 0)
print(~crossHack1)
print(~crossHack2)
print(crossHack)
gg = gg * crossHack
print(gg)
print(a[:-1][gg])
# system = ctrl.TransferFunction([25], [1, 55.1, 0])
# w = np.linspace(0, 100 * np.pi, 5000)
# mag, phase, omega = ctrl.bode(system, w, Plot=True)
# plt.show()

# if np.any(phase * 180.0 / np.pi >= 180):
#     phase = phase - 2 * np.pi

# gainDb = 20 * np.log10(mag)
# degPhase = phase * 180.0 / np.pi

# indPhase = np.diff(1 * (gainDb > 0) != 0)
# indGain = np.diff(1 * (degPhase > -180) != 0)

# print(omega[:-1][indPhase])
# print(omega[:-1][indGain])

# if len(omega[:-1][indGain]) > 0 and len(omega[:-1][indGain]) < 2:
#     omegaGain = omega[:-1][indGain][0]
#     GainMargin = -gainDb[:-1][indGain][0]
# elif len(omega[:-1][indGain]) > 0:
#     newGainIndex = min(range(len(gainDb[:-1][indGain])),
#                       key=lambda i: abs(gainDb[:-1][indGain][i] - 0))
#     omegaGain = omega[:-1][indGain][newGainIndex]
#     GainMargin = -gainDb[:-1][indGain][newGainIndex]
# else:
#     omegaGain = np.nan
#     GainMargin = np.infty

# if len(omega[:-1][indPhase]) > 0 and len(omega[:-1][indPhase]) < 2:
#     omegaPhase = omega[:-1][indPhase][0]
#     PhaseMargin = 180 + degPhase[:-1][indPhase][0]
# elif len(omega[:-1][indPhase]) > 0:
#     newPhaIndex = min(range(len(degPhase[:-1][indPhase])),
#                       key=lambda i: abs(degPhase[:-1][indPhase][i] + 180))
#     omegaPhase = omega[:-1][indPhase][newPhaIndex]
#     PhaseMargin = 180 + degPhase[:-1][indPhase][newPhaIndex]
# else:
#     omegaPhase = np.nan
#     PhaseMargin = np.infty


# print(omegaPhase, PhaseMargin, omegaGain, GainMargin)

# plt.style.use("seaborn-dark-palette")

# plt.rcParams["font.family"] = "serif"
# plt.rcParams["font.serif"] = "Times New Roman"

# plt.rcParams["mathtext.rm"] = "serif"
# plt.rcParams["mathtext.it"] = "serif:italic"
# plt.rcParams["mathtext.bf"] = "serif:bold"
# plt.rcParams["mathtext.fontset"] = "custom"

# plt.rc("text", usetex=True)
# plt.rcParams["text.latex.preamble"] = [
#     r"\usepackage{mathptmx} \usepackage{newtxmath} \usepackage{amsmath}"
# ]

# w = np.logspace(-np.pi, 2 * np.pi, 5000)

# GsS = ctrl.TransferFunction([1, 2], [1, 2, 3])

# GsI = ctrl.TransferFunction([3, -1.5], [1, -2, 3])

# real, imag, freq = ctrl.nyquist_plot(GsS, w, Plot=False)
# poles, zeros = ctrl.pzmap(GsS, Plot=False)

# plt.scatter(REAL(poles),
#             IMAG(poles),
#             s=50,
#             marker='x',
#             facecolors="r",
#             edgecolors='k')
# plt.scatter(REAL(zeros),
#             IMAG(zeros),
#             s=50,
#             marker='o',
#             facecolors="r",
#             edgecolors='k')

# plt.plot([-1], [0], color="#12711C", marker='+')

# plt.arrow(real[0],
#           imag[0], (real[1] - real[0]) / 2, (imag[1] - imag[0]) / 2,
#           width=0.02,
#           facecolor='r',
#           edgecolor='k')

# mindex = int(len(real) / 2.5)

# plt.arrow(
#     real[mindex],
#     imag[mindex],
#     (real[mindex + 1] - real[mindex]) / 2,
#     (imag[mindex + 1] - imag[mindex]) / 2,
#     width=0.02,
#     facecolor='r',
#     edgecolor='k'
# )


# plt.plot(real, imag, "r", label=r'$G_1(s) = \frac{s + 2}{s^2 + 2s + 3}$')
# plt.plot(real, -imag, "r")

# real, imag, freq = ctrl.nyquist_plot(GsI, w, Plot=False)
# poles, zeros = ctrl.pzmap(GsI, Plot=False)

# plt.scatter(REAL(poles),
#             IMAG(poles),
#             s=50,
#             marker='x',
#             facecolors="#001C7F",
#             edgecolors='k')
# plt.scatter(REAL(zeros),
#             IMAG(zeros),
#             s=50,
#             marker='o',
#             facecolors="#001C7F",
#             edgecolors='k')

# plt.arrow(real[0],
#           imag[0], (real[1] - real[0]) / 2, (imag[1] - imag[0]) / 2,
#           width=0.02,
#           facecolor='#001C7F',
#           edgecolor='k')
# plt.arrow(real[-1],
#           imag[-1], (real[-1] - real[-2]) / 2, (imag[-1] - imag[-2]) / 2,
#           width=0.02,
#           facecolor='#001C7F',
#           edgecolor='k')

# mindex = int(len(real) / 2)

# plt.plot(real, imag, "#001C7F", label=r'$G_2(s) = \frac{3s - 1.5}{s^2 - 2s + 3}$')
# plt.plot(real, -imag, "#001C7F")

# plt.legend()
# plt.grid()
# plt.gcf().tight_layout()
# plt.show()

# N = 0
# kp = 5
# ki = 5
# kd = 5

# pid1 = ctrl.tf2ss(ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

# pid2 = ctrl.tf2ss(
#     ctrl.TransferFunction([1], [0.1, 1]) *
#     ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

# # pid3 = ctrl.tf2ss(
# #     ctrl.TransferFunction([1], [10 / (N*kd), 1]) *
# #     ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

# pid4 = ctrl.tf2ss(
#     ctrl.TransferFunction([
#         10 * kp,
#         N**2 * kd**2 + N*kd*kp + 10*N*kp + 10*ki,
#         N**2*kd * kp + kd*N*ki + 10*N*ki,
#         N**2 * kd * ki
#     ], [10, 10*N + N*kd, N**2 * kd, 0]))

# ctrl.bode(pid1)
# ctrl.bode(pid2)
# # ctrl.bode(pid3)
# ctrl.bode(pid4)
# plt.show()

# N = 100
# kd1 = 1
# kd2 = 10

# derivativa1 = ctrl.TransferFunction([N * kd1, 0], [1, N])
# derivativa2 = ctrl.TransferFunction([N * kd2, 0], [1, N])
# ctrl.bode(derivativa1)
# ctrl.bode(derivativa2)
# plt.show()

# filtro1 = ctrl.TransferFunction([1], [1 / (N), 1])
# filtro2 = ctrl.TransferFunction([1], [1 / (N*kd2), 1])
# ctrl.bode(filtro1)
# ctrl.bode(filtro2)
# plt.show()

# ctrl.bode(derivativa1 * filtro1)
# ctrl.bode(derivativa1 * filtro1)
# ctrl.bode(derivativa2 * filtro1)
# ctrl.bode(derivativa2 * filtro2)
# plt.show()

# from skfuzzy import control as fuzz
# from skfuzzy.membership import generatemf as mf
# from matplotlib import pyplot as plt
# import numpy as np

# input1 = fuzz.Antecedent(np.linspace(-10, 10, 100), 'input1')

# input1['label1'] = mf.dsigmf(input1.universe, *[-5, 1, 5, -1])
# input1.view()
# plt.show()

# from __future__ import division
# import sys
# from parse import parse
# from time import time
# import ast
# import pprint
# import copy
# import json
# import re


# class FISParser:

#     def __init__(self, file, InputList=None, OutputList=None, RuleEtiquetas=None):
#         if InputList is None and OutputList is None and RuleEtiquetas is None:
#             with open(file, 'r') as infis:
#                 self.rawlines = infis.readlines()
#             self.systemList = 0
#             self.InputList = []
#             self.OutputList = []
#             self.RuleList = []
#             self.get_system()
#             self.get_vars()
#             self.get_rules()
#         else:
#             self.file = file
#             self.InputList = InputList
#             self.OutputList = OutputList
#             self.RuleEtiquetas = RuleEtiquetas
#             self.json_to_fis()

#     def get_system(self):
#         end_sysblock = self.rawlines.index('\n')
#         systemblock = self.rawlines[1:end_sysblock]
#         fisargs = map(lambda x: parse('{arg}={val}', x), systemblock)
#         fissys = {f['arg'].lower(): f['val'].strip("'") for f in fisargs}
#         self.numinputs = int(fissys['numinputs'])
#         self.numoutputs = int(fissys['numoutputs'])
#         self.numrules = int(fissys['numrules'])
#         self.start_varblocks = end_sysblock + 1
#         self.systemList = fissys

#     def get_var(self, vartype, varnum, start_line, end_line):
#         varblock = self.rawlines[start_line:end_line]
#         fisargs = map(lambda x: parse('{arg}={val}', x), varblock)
#         fisvar = {f['arg'].lower(): f['val'].strip("'") for f in fisargs}

#         if 'input' in vartype:
#             self.InputList.append(fisvar)
#         elif 'output' in vartype:
#             self.OutputList.append(fisvar)

#     def get_vars(self):
#         start_ruleblock = self.rawlines.index('[Rules]\n')
#         var_lines = []
#         var_types = []
#         flag = 0
#         for i, line in enumerate(self.rawlines[self.start_varblocks - 1:start_ruleblock]):
#             if flag:
#                 flag = 0
#                 vt = parse('[{type}{num:d}]', line)
#                 var_types.append((vt['type'].lower(), vt['num']))
#             if line == '\n':
#                 var_lines.append(i + self.start_varblocks - 1)
#                 flag = 1
#         for i, l in enumerate(var_lines[:-1]):
#             if 'input' in var_types[i][0]:
#                 self.get_var('input', var_types[i][1] - 1, l + 2, var_lines[i + 1])
#             elif 'output' in var_types[i][0]:
#                 self.get_var('output', var_types[i][1] - 1, l + 2, var_lines[i + 1])

#     def get_rules(self):
#         start_ruleblock = self.rawlines.index('[Rules]\n')
#         ruleblock = self.rawlines[start_ruleblock + 1:]
#         antecedents = (('{a%d:d} ' * self.numinputs) %
#                        tuple(range(self.numinputs))).strip()
#         consequents = ('{c%d:d} ' * self.numoutputs) % tuple(range(self.numoutputs))
#         p = antecedents + ', ' + consequents + '({w:d}) : {c:d}'
#         for rule in ruleblock:
#             try:
#                 p = antecedents + ', ' + consequents + '({w:d}) : {c:d}'
#                 rp = parse(p, rule)
#                 r = []
#                 for inp in range(self.numinputs):
#                     rpar = rp['a%d' % inp]
#                     rval = rpar if rpar != 0 else None
#                     r.append(rval)
#                 for outp in range(self.numoutputs):
#                     rpar = rp['c%d' % outp]
#                     rval = rpar if rpar != 0 else None
#                     r.append(rval)
#                 r += [rp['w'], rp['c'] - 1]
#                 self.RuleList.append(r)
#             except:
#                 p = antecedents + ', ' + consequents + '({w:f}) : {c:d}'
#                 rp = parse(p, rule)
#                 r = []
#                 for inp in range(self.numinputs):
#                     rpar = rp['a%d' % inp]
#                     rval = rpar if rpar != 0 else None
#                     r.append(rval)
#                 for outp in range(self.numoutputs):
#                     rpar = rp['c%d' % outp]
#                     rval = rpar if rpar != 0 else None
#                     r.append(rval)
#                 r += [rp['w'], rp['c'] - 1]
#                 self.RuleList.append(r)

#     def fis_to_json(self):
#         ni = int(self.systemList['numinputs'])
#         no = int(self.systemList['numoutputs'])
#         nr = int(self.systemList['numrules'])

#         InputList = [0] * ni
#         OutputList = [0] * no
#         RuleEtiquetas = []

#         for i in range(ni):
#             InputList[i] = {
#                 "nombre": self.InputList[i]['name'],
#                 "numeroE": int(self.InputList[i]['nummfs']),
#                 "etiquetas": [0] * int(self.InputList[i]['nummfs']),
#                 "rango": ast.literal_eval(re.sub("\s+", ",", self.InputList[i]['range'].strip()))
#             }

#             for ne in range(int(self.InputList[i]['nummfs'])):
#                 temp_etiqueta = self.InputList[0]['mf' + str(ne + 1)].replace(
#                     "'", '').split(':')
#                 temp2 = temp_etiqueta[1].split(',')
#                 InputList[i]['etiquetas'][ne] = {
#                     "nombre": temp_etiqueta[0],
#                     "mf": temp2[0],
#                     "definicion": ast.literal_eval(re.sub("\s+", ",", temp2[1].strip()))
#                 }

#         for i in range(no):
#             OutputList[i] = {
#                 "nombre":
#                     self.OutputList[i]['name'],
#                 "numeroE":
#                     int(self.OutputList[i]['nummfs']),
#                 "etiquetas": [0] * int(self.OutputList[i]['nummfs']),
#                 "rango":
#                     ast.literal_eval(
#                         re.sub("\s+", ",", self.OutputList[i]['range'].strip())),
#                 "metodo":
#                     self.systemList['defuzzmethod']
#             }

#             for ne in range(int(self.OutputList[i]['nummfs'])):
#                 temp_etiqueta = self.OutputList[i]['mf' + str(ne + 1)].replace(
#                     "'", '').split(':')
#                 temp2 = temp_etiqueta[1].split(',')
#                 OutputList[i]['etiquetas'][ne] = {
#                     "nombre": temp_etiqueta[0],
#                     "mf": temp2[0],
#                     "definicion": ast.literal_eval(re.sub("\s+", ",", temp2[1].strip()))
#                 }
#         for numeror, i in enumerate(self.RuleList):
#             ril = []
#             rol = []

#             for j in range(ni):
#                 if i[j] is not None:
#                     nombre = InputList[j]['etiquetas'][abs(i[j]) - 1]['nombre']
#                     numero = j
#                     negacion = False if i[j] > 0 else True
#                     ril.append([nombre, numero, negacion])

#             for j in range(ni, no + ni):
#                 if i[j] is not None:
#                     if i[j] < 0:
#                         raise TypeError('No se permiten salidas negadas')
#                     nombre = OutputList[j - ni]['etiquetas'][abs(i[j]) - 1]['nombre']
#                     numero = j - ni
#                     peso = float(i[no + ni])
#                     rol.append([nombre, numero, peso])

#             and_condition = True if i[ni + no + 1] == 0 else False
#             RuleEtiquetas.append(copy.deepcopy([ril, rol, and_condition]))

#         return copy.deepcopy(InputList), copy.deepcopy(OutputList), copy.deepcopy(RuleEtiquetas)

#     def json_to_fis(self):
#         ni = len(self.InputList)
#         no = len(self.OutputList)
#         nr = len(self.RuleEtiquetas)

#         with open(self.file, 'w') as f:
#             f.write(f"[System]\n")
#             f.write(f"Name='{self.file.split('/')[-1].split('.')[0]}'\n")
#             f.write(f"Type='mamdani'\n")
#             f.write(f"Version=2.0\n")
#             f.write(f"NumInputs={ni}\n")
#             f.write(f"NumOutputs={no}\n")
#             f.write(f"NumRules={nr}\n")
#             f.write(f"AndMethod='min'\n")
#             f.write(f"OrMethod='max'\n")
#             f.write(f"ImpMethod='min'\n")
#             f.write(f"AggMethod='max'\n")
#             f.write(f"DefuzzMethod='{self.OutputList[0]['metodo']}'\n")
#             f.write(f"\n")

#             for i in range(ni):
#                 f.write(f"[Input"+str(i+1)+"]\n")
#                 f.write(f"Name='{self.InputList[i]['nombre']}'\n")
#                 string_temp = re.sub('\s+', '', str(self.InputList[i]['rango'])).replace(',', ' ')
#                 f.write(f"Range={string_temp}\n")
#                 f.write(f"NumMFs={self.InputList[i]['numeroE']}\n")

#                 for ne in range(self.InputList[i]['numeroE']):
#                     string_temp = re.sub(
#                         '\s+', '',
#                         str(self.InputList[i]['etiquetas'][ne]['definicion'])).replace(
#                             ',', ' ')
#                     f.write(
#                         f"MF{ne+1}='{self.InputList[i]['etiquetas'][ne]['nombre']}':'{self.InputList[i]['etiquetas'][ne]['mf']}',{string_temp}\n"
#                     )

#                 f.write(f"\n")

#             for i in range(no):
#                 f.write(f"[Output" + str(i + 1) + "]\n")
#                 f.write(f"Name='{self.OutputList[i]['nombre']}'\n")
#                 string_temp = re.sub('\s+', '',str(self.OutputList[i]['rango'])).replace(',', ' ')
#                 f.write(f"Range={string_temp}\n")
#                 f.write(f"NumMFs={self.OutputList[i]['numeroE']}\n")

#                 for ne in range(self.OutputList[i]['numeroE']):
#                     string_temp = re.sub(
#                         '\s+', '',
#                         str(self.OutputList[i]['etiquetas'][ne]['definicion'])).replace(
#                             ',', ' ')
#                     f.write(
#                         f"MF{ne+1}='{self.OutputList[i]['etiquetas'][ne]['nombre']}':'{self.OutputList[i]['etiquetas'][ne]['mf']}',{string_temp}\n"
#                     )

#                 f.write(f"\n")

#             rules_no_format = []
#             for i, rule in enumerate(self.RuleEtiquetas):

#                 inner_rules = []
#                 for nir in range(ni):
#                     for inputrule in rule[0]:
#                         if nir == inputrule[1]:
#                             if  not inputrule[2]:
#                                 for ner, etiqueta in enumerate(self.InputList[nir]['etiquetas']):
#                                     if etiqueta['nombre'] == inputrule[0]:
#                                         inner_rules.append(ner+1)
#                                         break
#                             else:
#                                 for ner, etiqueta in enumerate(self.InputList[nir]['etiquetas']):
#                                     if etiqueta['nombre'] == inputrule[0]:
#                                         inner_rules.append(-ner-1)
#                                         break

#                             break
#                         else:
#                             continue
#                     else:
#                         inner_rules.append(0)
#                         break

#                 for nor in range(no):
#                     for outputtrule in rule[1]:
#                         if nor == outputtrule[1]:
#                             for ner, etiqueta in enumerate(self.OutputList[nor]['etiquetas']):
#                                 if etiqueta['nombre'] == outputtrule[0]:
#                                     inner_rules.append(ner+1)
#                                     break
#                             break
#                         else:
#                             continue
#                     else:
#                         inner_rules.append(0)

#                 inner_rules.append(rule[1][0][2])

#                 if rule[2]:
#                     inner_rules.append(1)
#                 else:
#                     inner_rules.append(2)

#                 rules_no_format.append(copy.deepcopy(inner_rules))

#             f.write(f"[Rules]\n")

#             for i in range(nr):
#                 rule_str = ""
#                 for j in range(ni):
#                     rule_str += str(rules_no_format[i][j]) + " "
#                 rule_str += ","
#                 for j in range(ni, ni+no):
#                     rule_str += str(rules_no_format[i][j]) + " "
#                 rule_str += f"({str(rules_no_format[i][ni+no])})" + " "
#                 rule_str += f": {str(rules_no_format[i][ni+no+1])}\n"
#                 f.write(rule_str)


# if __name__ == "__main__":
#     Parsing = FISParser('controladorcompleto.fis')
#     lista1, lista2, lista3 = Parsing.fis_to_json()
#     print(lista2)
#     Parsing = FISParser('gainshedulerTest.fis', lista1, lista2, lista3)
#     Parsing.json_to_fis()

#     stringboletoso = '[10,    10]'
#     print(re.sub("\s+", "", str([-10, 10])).replace(',', ' '))




# from qtconsole.qt import QtGui
# from qtconsole.rich_jupyter_widget import RichJupyterWidget
# from qtconsole.inprocess import QtInProcessKernelManager


# def show():
#     global ipython_widget  # Prevent from being garbage collected

#     # Create an in-process kernel
#     kernel_manager = QtInProcessKernelManager()
#     kernel_manager.start_kernel(show_banner=False)
#     kernel = kernel_manager.kernel
#     kernel.gui = 'qt'

#     kernel_client = kernel_manager.client()
#     kernel_client.start_channels()

#     ipython_widget = RichJupyterWidget()
#     ipython_widget.kernel_manager = kernel_manager
#     ipython_widget.kernel_client = kernel_client
#     ipython_widget.show()


# if __name__ == "__main__":
#     app = QtGui.QApplication([])
#     show()
#     app.exec_()

# # import json
# # from collections import deque
# # # import pickle
# import controlmdf as ctrl
# # from skfuzzymdf import control as fuzz
# from matplotlib import pyplot as plt
# # from matplotlib import figure
# # from mpl_toolkits.mplot3d import Axes3D
# # import time
# # import pyqtgraph as pg
# # import sys
# # from PySide2 import QtWidgets, QtCore, QtGui
# import numpy as np
# # import pyvista as pv
# # from scipy import signal
# from scipy.integrate import RK45
# from scipy import signal
# # from multiprocessing import Queue
# # import math

# sistema = signal.StateSpace(signal.TransferFunction([1], [1, 1, 1]))
# print(sistema.A)
# a = np.asarray([[1, 2, 3], [2, 3, 4]])
# b = np.asarray([3, 4])
# print(len(a))
# print(a**2)
# print(np.linalg.matrix_power(a, 2))
# N = 100
# kp = 1
# kd = 1
# ki = 1

# derivadaf = ctrl.tf2ss(ctrl.TransferFunction([1], [0.1, 1])*
#     ctrl.TransferFunction([N*kd + kp, N*kp + ki, N * ki], [1, N, 0]))

# sistema = ctrl.tf2ss(ctrl.TransferFunction([1], [1, 1, 1]))
# vstadosB = np.zeros_like(sistema.B)


# def state_space(t, y, A, B, U, y_vect):
#     ydot = A*y_vect.reshape([-1, 1]) + B*U
#     return np.squeeze(np.asarray(ydot))


# def runge_kutta(ss, x, h, inputValue):
#     k1 = h * (ss.A * x + ss.B * inputValue)
#     k2 = h * (ss.A * (x + k1/2) + ss.B * (inputValue))
#     k3 = h * (ss.A * (x + k2/2) + ss.B * (inputValue))
#     k4 = h * (ss.A * (x+k3) + ss.B * (inputValue))

#     x = x + (1/6) * (k1 + k2*2 + k3*2 + k4)
#     y = ss.C * x + ss.D * inputValue
#     return y.item(), x


# A1 = derivadaf.A
# B1 = derivadaf.B
# C1 = derivadaf.C
# D1 = derivadaf.D

# x_vect = np.asarray(np.zeros_like(B1))
# x_vect = x_vect.flatten()
# print(x_vect)
# salida = [0]
# tiempo = [0]
# tiempo2 = 0
# error = 0
# output = 0
# sc_t = 0
# counter = 0

# solution = RK45(lambda t,
#                 y: state_space(t, y, A1, B1, error, x_vect),
#                 t0=0,
#                 y0=x_vect,
#                 max_step=0.1,
#                 rtol=1e-3,
#                 atol=1e-6,
#                 t_bound=30)

# while solution.status is not 'finished' and solution.status is not 'failed':
#     error = 1 - output
#     counter +=1
#     solution.step()
#     print(solution.t)
#     x_vect = solution.y
#     sc_t = (C1 * x_vect.reshape([-1, 1]) + D1*1).item()
#     output, vstadosB = runge_kutta(sistema, vstadosB, solution.step_size, sc_t)
#     salida.append(output)
#     tiempo.append(solution.t)

# print(counter)
# plt.plot(tiempo, salida)
# plt.show()
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


# class Lowpassfilter:
#     """ Filtro pasa-bajo con ventaja Hamming"""

#     def __init__(self, order, fsampling, fpaso):

#         self.order = order
#         self.samples0 = order*[0]
#         self.fsampling = fsampling
#         self.fpaso = fpaso
#         self.h_n = signal.firwin(self.order,
#                                  self.fpaso,
#                                  fs=self.fsampling) * 30
#         self.h_n = self.h_n.tolist()
#         print(self.h_n)

#     def filtrar(self, entrada):

#         self.samples0.append(entrada)
#         self.samples0 = self.samples0[1:]
#         salida = sum(a * b for a, b in zip(self.samples0, self.h_n))
#         return salida
# # [-0.3664505514016285, -4.578068971937084, 21.576763158929094, -4.578068971937084, -0.3664505514016285]

# fs = 30
# nyq = fs / 2

# filtro = Lowpassfilter(5, fs, N/(2*np.pi))
# # b, a = signal.butter(3, omega)
# w, h = signal.freqz(filtro.h_n)

# plt.figure(figsize=(11, 8))
# plt.semilogx(w * nyq / np.pi, 20 * np.log10(abs(h)))
# plt.title('Respuesta del filtro Butterworth')
# plt.xlabel('Frequency [Hz]')
# plt.ylabel('Amplitude [dB]')
# plt.grid(which='both', axis='both')
# plt.axvline(N * nyq / np.pi, color='green')  # Frecuencia de corte

# # plt.savefig("Filtro Bode.png", bbox_inches='tight', pad_inches=0.1)
# plt.show()

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