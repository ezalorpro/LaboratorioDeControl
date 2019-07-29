from skfuzzy.fuzzymath.fuzzy_ops import interp_membership
from skfuzzy.membership import generatemf
from skfuzzy import control as fuzz
import numpy as np
from matplotlib import pyplot as plt


entrada1 = fuzz.Antecedent(np.linspace(-10, 10, 500), 'entrada1')
entrada2 = fuzz.Antecedent(np.linspace(-10, 10, 500), 'entrada2')

salida1 = fuzz.Consequent(np.linspace(-10, 10, 500), 'salida1', 'centroid')
salida2 = fuzz.Consequent(np.linspace(-10, 10, 500), 'salida1', 'centroid')

entrada1.automf(3, names=["negativo", "cero", "positivo"])
entrada2.automf(3, names=["negativo", "cero", "positivo"])
salida1.automf(3, names=["negativo", "cero", "positivo"])
salida2.automf(3, names=["negativo", "cero", "positivo"])

rule = fuzz.Rule()
rule.antecedent = (entrada1['negativo'] |  ~entrada2['negativo']) | (~entrada2['negativo'])
rule.consequent = (salida1['cero'] | salida2['cero'])

print(rule)