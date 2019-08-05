from matplotlib.backends.backend_qt5agg import (
    FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar,
)
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from PySide2.QtWidgets import QWidget, QGraphicsView
from PySide2.QtWidgets import QVBoxLayout


class MlpWidget(QGraphicsView):
    def __init__(self, parent=None):
        super(MlpWidget, self).__init__(parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        vertical_layout.addWidget(self.toolbar)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()
        self.canvas.axes.grid()
        self.setLayout(vertical_layout)


class MlpWidgetNoToolbar(QGraphicsView):
    def __init__(self, parent=None):
        super(MlpWidgetNoToolbar, self).__init__(parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()
        self.canvas.axes.grid()
        self.setLayout(vertical_layout)

class MlpWidgetSubplot(QGraphicsView):
    def __init__(self, parent=None):
        super(MlpWidgetSubplot, self).__init__(parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        self.toolbar = NavigationToolbar(self.canvas, self)
        vertical_layout.addWidget(self.toolbar)

        self.canvas.axes1 = self.canvas.figure.add_subplot(211)
        self.canvas.axes1.grid()
        self.canvas.axes2 = self.canvas.figure.add_subplot(
            212, sharex=self.canvas.axes1
        )
        self.canvas.axes2.grid()
        self.canvas.figure.tight_layout()
        self.setLayout(vertical_layout)

class MlpWidget3D(QGraphicsView):
    def __init__(self, parent=None):
        super(MlpWidget3D, self).__init__(parent)
        self.canvas = FigureCanvas(Figure(tight_layout=True))

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111, projection='3d')
        self.canvas.figure.tight_layout()
        self.canvas.axes.grid()
        self.colorbar = 0
        self.setLayout(vertical_layout)