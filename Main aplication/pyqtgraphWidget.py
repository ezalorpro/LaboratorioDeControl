from PySide2.QtWidgets import QGraphicsView
from PySide2.QtWidgets import QVBoxLayout
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class PgraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(PgraphWidget, self).__init__(parent)
        
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
                
        self.plotwidget = PlotWidget()
        self.plotwidget.setMouseEnabled(False, False)
        self.plotwidget.setYRange(0, 1)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.plotwidget)
        self.plotwidget.showGrid(x=True, y=True)
        self.setLayout(vertical_layout)

class PgraphWidgetpid(QGraphicsView):
    def __init__(self, parent=None):
        super(PgraphWidgetpid, self).__init__(parent)
        
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        self.plotwidget = PlotWidget()
        self.plotwidget.setMouseEnabled(False, False)
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.plotwidget)
        self.plotwidget.showGrid(x=True, y=True)
        self.curva = self.plotwidget.plot(pen={'color': pg.mkColor('#1f77b4'), 'width': 3})
        self.setLayout(vertical_layout)