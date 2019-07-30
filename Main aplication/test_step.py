from skfuzzy.fuzzymath.fuzzy_ops import interp_membership
from skfuzzy.membership import generatemf
from skfuzzy import control as fuzz
import numpy as np
from matplotlib import pyplot as plt
from collections import deque
import copy

entrada1 = fuzz.Antecedent(np.linspace(-10, 10, 500), 'entrada1')
entrada2 = fuzz.Antecedent(np.linspace(-10, 10, 500), 'entrada2')
entrada3 = fuzz.Antecedent(np.linspace(-10, 10, 500), 'entrada3')

salida1 = fuzz.Consequent(np.linspace(-10, 10, 500), 'salida1', 'centroid')
salida2 = fuzz.Consequent(np.linspace(-10, 10, 500), 'salida2', 'centroid')
salida3 = fuzz.Consequent(np.linspace(-10, 10, 500), 'salida3', 'centroid')

entrada1.automf(3, names=["negativo", "cero", "positivo"])
entrada2.automf(3, names=["negativo", "cero", "positivo"])
entrada3.automf(3, names=["negativo", "cero", "positivo"])

salida1.automf(3, names=["negativo", "cero", "positivo"])
salida2.automf(3, names=["negativo", "cero", "positivo"])
salida3.automf(3, names=["negativo", "cero", "positivo"])

rule = fuzz.Rule(antecedent=None, consequent=None)

reglain = deque(['cero', 'negativo', 'None'])
reglaout = deque(['cero', 'None', 'negativo'])

Entradas = deque([entrada1, entrada2, entrada3])
Salidas = deque([salida1, salida2, salida3])

ni = 3
no = 3

for i, etiqueta in enumerate(copy.copy(reglain)):
    reglain.popleft()
    if etiqueta is not 'None':
        rule.antecedent = Entradas[0][etiqueta]
        Entradas.popleft()
        break
    Entradas.popleft()
else:
    raise TypeError('Regla no valida')

peso = 0.3

for i, etiqueta in enumerate(copy.copy(reglaout)):
    reglaout.popleft()
    if etiqueta is not 'None':
        rule.consequent = Salidas[0][etiqueta] % peso
        Salidas.popleft()
        break
    Salidas.popleft()
else:
    raise TypeError('Regla no valida')

peso = 0.3

for i, etiqueta in enumerate(reglain):
    if etiqueta is not 'None':
        rule.antecedent = rule.antecedent & Entradas[i][etiqueta] 

for i, etiqueta in enumerate(reglaout):
    if etiqueta is not 'None':
        rule.consequent.append(Salidas[i][etiqueta]%peso)
        
print(rule)