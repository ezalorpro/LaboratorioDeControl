from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pyvista as pv
import numpy as np
import pickle

print(pv.Report())

# Data from my app
with open('probando.pkl', 'rb') as f:
    x, y, z = pickle.load(f)

print('generic Data')
print(type(z))
print(np.shape(z))

# # Matplotlib -----
fig1 = plt.figure(1)
ax1 = fig1.add_subplot(projection='3d')
surface = ax1.plot_surface(x, y, z, cmap='viridis')
fig1.colorbar(surface)
plt.show()

# PyVista -----
grid = pv.StructuredGrid(x, y, z)
plotter = pv.Plotter()
plotter.add_mesh(grid, scalars=z, cmap='viridis', lighting=False)

plotter.set_scale(xscale=(np.max(z)/np.max(x)),
                  yscale=(np.max(z)/np.max(y)))
plotter.add_scalar_bar()
plotter.show_bounds(grid='back',
                    location='outer',
                    ticks='both',
                    bounds=[np.min(x), np.max(x),
                            np.min(y), np.max(y),
                            np.min(z), np.max(z)])
plotter.show()


# # Known data
# x_samp = np.linspace(-10, 10, 20)
# y_samp = np.linspace(-10, 10, 20)
# x, y = np.meshgrid(x_samp, y_samp)
# a = -0.0001
# z = a*(np.abs(np.sin(x)*np.sin(y)*np.exp(np.abs(100-np.sqrt(x**2 + y**2)/np.pi))) + 1)**0.1

# print(type(z))
# print(np.shape(z))

# # Matplotlib -----
# fig2 = plt.figure(2)
# ax2 = fig2.add_subplot(projection='3d')
# surface = ax2.plot_surface(x, y, z, cmap='viridis')
# fig2.colorbar(surface)
# plt.show()

# # PyVista -----
# grid = pv.StructuredGrid(x, y, z)
# plotter = pv.Plotter()
# plotter.add_mesh(grid, scalars=z, cmap='viridis', lighting=False)

# plotter.set_scale(xscale=(np.max(z)/np.max(x)),
#                   yscale=(np.max(z)/np.max(y)))
# plotter.add_scalar_bar()
# plotter.show_bounds(grid='back',
#                     location='outer',
#                     ticks='both',
#                     bounds=[np.min(x), np.max(x),
#                             np.min(y), np.max(y),
#                             np.min(z), np.max(z)])
# plotter.show()

