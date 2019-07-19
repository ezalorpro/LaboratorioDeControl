from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from analisisHandler import AnalisisHandler
import json


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)

        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setText("Error")
        self.error_dialog.setInformativeText('404')
        self.error_dialog.setWindowTitle("Error")

        AnalisisHandler(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
