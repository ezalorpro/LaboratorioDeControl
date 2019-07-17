from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from rutinas_analisis import *
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        self.main.tfcalcButton1.clicked.connect(self.calcular_analisis)

    def calcular_analisis(self):
        num = json.loads(self.main.tfnumEdit1.text())
        dem = json.loads(self.main.tfdemEdit1.text())
        systema = system_creator(num, dem)
        
        t, y, T = rutina_impulse_plot(self, systema)
        t, y = rutina_step_plot(self, systema, T)
        mag, phase, omega = rutina_bode_plot(self, systema)
        real, imag, freq = rutina_nyquist_plot(self, systema)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
