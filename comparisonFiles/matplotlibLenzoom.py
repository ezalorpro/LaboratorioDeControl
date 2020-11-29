import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, np.pi*4, 200)
y = np.sin(x)

fig, ax = plt.subplots(figsize=[5, 4])


ax.plot(x, y)

axins = ax.inset_axes([0.55, 0.05, 0.4, 0.4])
axins.plot(x, y, label='hola')
axins.legend()
# sub region of the original image
x1, x2, y1, y2 = np.pi/2, np.pi, 0.8, 1
axins.set_xlim(x1, x2)
axins.set_ylim(y1, y2)
axins.set_xticklabels('')
axins.set_yticklabels('')
ax.indicate_inset_zoom(axins)
plt.show()