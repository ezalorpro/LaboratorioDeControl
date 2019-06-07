from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.exporters.Exporter import Exporter
from pyqtgraph import PlotItem
from pyqtgraph import functions as fn

def cleanAxes(self, axl):
    if type(axl) is not list:
        axl = [axl]
    for ax in axl:
        if ax is None:
            continue
        for loc, spine in ax.spines.items():
            if loc in ['left', 'bottom']:
                pass
            elif loc in ['right', 'top']:
                spine.set_color('none')
                # do not draw the spine
            else:
                raise ValueError('Unknown spine location: %s' % loc)
            # turn off ticks when there is no spine
            ax.xaxis.set_ticks_position('bottom')