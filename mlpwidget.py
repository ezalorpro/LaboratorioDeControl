from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QGraphicsView
from PySide2.QtWidgets import QVBoxLayout

class MlpWidget(QGraphicsView):
    def __init__(self, parent = None):
        super(MlpWidget, self).__init__(parent)
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        
        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.setLayout(vertical_layout)
        
class MlpWidgetSubplot(QGraphicsView):
    def __init__(self, parent = None):
        super(MlpWidgetSubplot, self).__init__(parent)
        self.canvas = FigureCanvas(Figure())
        
        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(NavigationToolbar(self.canvas, self))
        
        self.canvas.axes1 = self.canvas.figure.add_subplot(211)
        self.canvas.axes1 = self.canvas.figure.add_subplot(212)
        self.setLayout(vertical_layout)