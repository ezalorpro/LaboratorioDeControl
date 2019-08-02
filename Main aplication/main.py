from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from handlers.analisisHandler import AnalisisHandler
from handlers.PIDHandler import PIDHandler
from handlers.FuzzyHandler import FuzzyHandler
import json
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
        
        self.flag0 = 0
        self.flag1 = 0
        self.flag2 = 0
        self.flag3 = 0
        
        self.main.principalTab.currentChanged.connect(self.principalTab_visuliazation)
        
    def principalTab_visuliazation(self):
        if self.main.principalTab.currentIndex() == 0 and not self.flag0:
            self.flag0 = 1
            AnalisisHandler(self)
        if self.main.principalTab.currentIndex() == 1 and not self.flag1:
            self.flag1 = 1
            PIDHandler(self)    
        if self.main.principalTab.currentIndex() == 2 and not self.flag2:
            self.flag2 = 1    
            FuzzyHandler(self)
        if self.main.principalTab.currentIndex() == 3 and not self.flag3:
            pass
            # self.flag3 = 1   
            # SimulacionHandler(self)
    
    def resource_path(self, relative_path):
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
