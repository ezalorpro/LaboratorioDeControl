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
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.plotwidget)
        self.plotwidget.showGrid(x=True, y=True)
        self.setLayout(vertical_layout)
        