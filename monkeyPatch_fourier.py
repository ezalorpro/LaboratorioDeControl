""" Monkey patch para arreglar un bug que no permitia transformar la señal a frecuencia"""

import numpy as np
from pyqtgraph.metaarray import MetaArray as metaarray
from pyqtgraph.Qt import QtCore
from pyqtgraph.graphicsItems.GraphicsObject import GraphicsObject
from pyqtgraph.graphicsItems.PlotCurveItem import PlotCurveItem
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem
from pyqtgraph import functions as fn
from pyqtgraph import debug as debug
from pyqtgraph import getConfigOption

def _fourierTransform(self, x, y):
    ## Perform fourier transform. If x values are not sampled uniformly,
    ## then use np.interp to resample before taking fft.
    dx = np.diff(x)
    uniform = not np.any(np.abs(dx-dx[0]) > (abs(dx[0]) / 1000.))
    if not uniform:
        x2 = np.linspace(x[0], x[-1], len(x))
        y = np.interp(x2, x, y)
        x = x2
    f = np.fft.fft(y) / len(y)

    # linea cambiada - se agrego la funcion int()
    y = abs(f[1:int(len(f)/2)])
    # -------------------------------------------------

    dt = x[-1] - x[0]
    x = np.linspace(0, 0.5*len(x)/dt, len(y))
    return x, y
