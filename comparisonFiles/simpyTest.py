from matplotlib import pyplot as plt
import sympy as sm
import numpy as np
from tqdm import tqdm
from sympy.utilities.lambdify import lambdify

s = sm.symbols('s')
t = sm.symbols('t', positive=True)

N = 100
kp = 1
ki = 0
kd = 0

Gp = 1/(s**2 + s + 1)
Gc = kp + ki/s + kd*s
Gs = Gp*Gc
Gsh = (Gs / (1+ Gs))*(1/s)

y = sm.inverse_laplace_transform(sm.expand(Gsh), s, t)
y = sm.simplify(y)

tiempo = np.linspace(0, 20, 500)

func = lambdify(t, y, modules=['numpy'])
yt = func(tiempo)

plt.plot(tiempo, np.abs(yt))
plt.grid()
plt.show()
