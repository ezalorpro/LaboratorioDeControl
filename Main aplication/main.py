from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from analisisHandler import AnalisisHandler
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        
        AnalisisHandler(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
