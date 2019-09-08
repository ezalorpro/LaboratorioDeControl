from PySide2 import QtCore, QtGui, QtWidgets
from Ui_VentanaPrincipal import Ui_MainWindow
from handlers.analisisHandler import AnalisisHandler
from handlers.TuningHandler import TuningHandler
from handlers.FuzzyHandler import FuzzyHandler
from handlers.simulacionHandler import SimulacionHandler
from handlers.jupyterConsoleHandler import jupyterConsoleHandler
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
        TuningHandler(self)
        FuzzyHandler(self)
        SimulacionHandler(self)
        # jupyterConsoleHandler(self)

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def closeEvent(self, event):
        error_dialog = QtWidgets.QMessageBox.question(
            self,
            "Laboratorio Virtual",
            '¿Cerrar el programa? Los cambios no guardados se perderan',
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        )

        event.ignore()
        if error_dialog == QtWidgets.QMessageBox.Ok:
            self.main.jupyterWidget.jupyter_widget.kernel_client.stop_channels()
            self.main.jupyterWidget.jupyter_widget.kernel_manager.shutdown_kernel()
            event.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    frame = MainWindow()
    frame.show()
    app.exec_()
