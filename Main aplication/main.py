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
        self.main.tfdiscretocheckBox1.stateChanged.connect(self.bool_discreto)

    def calcular_analisis(self):
        num = json.loads(self.main.tfnumEdit1.text())
        dem = json.loads(self.main.tfdemEdit1.text())
        
        if self.main.tfdiscretocheckBox1.isChecked():
            self.dt = json.loads(self.main.tfperiodoEdit1.text())
        else:
            self.dt = None
            
        system, T = system_creator(self, num, dem)
        
        t1, y1 = rutina_impulse_plot(self, system, T)
        t2, y2 = rutina_step_plot(self, system, T)
        mag, phase, omega = rutina_bode_plot(self, system)
        real, imag, freq = rutina_nyquist_plot(self, system)
        rutina_root_locus_plot(self, system)

    def bool_discreto(self):
        if self.main.tfdiscretocheckBox1.isChecked():
            self.main.tfperiodoEdit1.setEnabled(True)
        else:
            self.main.tfperiodoEdit1.setDisabled(True)
        


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
