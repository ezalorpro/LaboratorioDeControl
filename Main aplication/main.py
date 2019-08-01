from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from handlers.analisisHandler import AnalisisHandler
from handlers.PIDHandler import PIDHandler
from handlers.FuzzyHandler import FuzzyHandler
import json
from pyvista import QtInteractor
import os

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        self.showMaximized()
        icon = QtGui.QIcon()
        image_path = self.resource_path("icono.ico")
        icon.addPixmap(QtGui.QPixmap(image_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        
        self.error_dialog = QtWidgets.QMessageBox()
        self.error_dialog.setIcon(QtWidgets.QMessageBox.Critical)
        self.error_dialog.setText("Error")
        self.error_dialog.setInformativeText('404')
        self.error_dialog.setWindowTitle("Error")
        
        AnalisisHandler(self)
        PIDHandler(self)        
        FuzzyHandler(self)

    def resource_path(self, relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
