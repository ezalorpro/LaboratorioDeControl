from rutinas.rutinas_PID import *
import json

def PIDHandler(self):
    
    self.main.tfcalcButton2.clicked.connect(lambda: calcular_PID(self))
    self.main.sscalcButton2.clicked.connect(lambda: calcular_PID(self))

    self.main.tfdiscretocheckBox2.stateChanged.connect(lambda: PID_bool_discreto(self))

    self.main.tfradioButton2.toggled.connect(lambda: PID_stacked_to_tf(self))
    self.main.ssradioButton2.toggled.connect(lambda: PID_stacked_to_ss(self))


def calcular_PID(self):
    pass    


def PID_bool_discreto(self):
    if self.main.tfdiscretocheckBox2.isChecked():
        self.main.tfperiodoEdit2.setEnabled(True)
    else:
        self.main.tfperiodoEdit2.setDisabled(True)


def PID_stacked_to_tf(self):
    self.main.PIDstackedWidget.setCurrentIndex(0)


def PID_stacked_to_ss(self):
    self.main.PIDstackedWidget.setCurrentIndex(1)