from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('svg')
import numpy as np

x = np.linspace(0, 2*np.pi, 10000, dtype='float64')
y = np.sin(x)
z = y + 1e-14

plt.plot(x, y)
plt.plot(x, z)
plt.fill_between(x,y,z)
plt.axis([1.5709534220463992, 1.5709534222199248, 0.999999987660502, 0.9999999876605615])


# # Declare and register callbacks
# def on_xlims_change(axes):
#     print ("updated xlims: ", plt.gca().get_xlim())


# def on_ylims_change(axes):
#     print("updated ylims: ", plt.gca().get_ylim())

# plt.gca().callbacks.connect('xlim_changed', on_xlims_change)
# plt.gca().callbacks.connect('ylim_changed', on_ylims_change)
plt.savefig('wtf.eps')
plt.show()