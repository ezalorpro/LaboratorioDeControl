from skfuzzy.fuzzymath.fuzzy_ops import interp_membership
from skfuzzy.membership import generatemf
import numpy as np
from matplotlib import pyplot as plt


x = np.linspace(-10, 10, 500)
y = generatemf.trimf(x, [-2, 0, 2])

h = np.linspace(-10, 10, 1000)
y2 = interp_membership(x, y, h)

plt.plot(x, y)
plt.show()

plt.plot(h, y2)
plt.show()