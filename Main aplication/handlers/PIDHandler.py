from rutinas.rutinas_PID import *
import json

def PIDHandler(self):
    
    self.main.tfcalcButton2.clicked.connect(lambda: calcular_PID(self))
    self.main.sscalcButton2.clicked.connect(lambda: calcular_PID(self))

    self.main.tfdiscretocheckBox2.stateChanged.connect(lambda: PID_bool_discreto(self))

    self.main.tfradioButton2.toggled.connect(lambda: PID_stacked_to_tf(self))
    self.main.ssradioButton2.toggled.connect(lambda: PID_stacked_to_ss(self))


def calcular_PID(self):
    if (self.main.tfdiscretocheckBox2.isChecked()
        and self.main.PIDstackedWidget.currentIndex() == 0):
        try:
            self.dt = json.loads(self.main.tfperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    elif (self.main.ssdiscretocheckBox2.isChecked() 
          and self.main.PIDstackedWidget.currentIndex() == 1):
        try:
            self.dt = json.loads(self.main.ssperiodoEdit2.text())
        except ValueError:
            self.error_dialog.setInformativeText("Periodo de muestreo no valido")
            self.error_dialog.exec_()
            return
    else:
        self.dt = None

    if self.main.PIDstackedWidget.currentIndex() == 0:
        num = json.loads(self.main.tfnumEdit2.text())
        dem = json.loads(self.main.tfdemEdit2.text())
        system_op, T = system_creator_tf(self, num, dem)
    else:
        A = json.loads(self.main.ssAEdit2.text())
        B = json.loads(self.main.ssBEdit2.text())
        C = json.loads(self.main.ssCEdit2.text())
        D = json.loads(self.main.ssDEdit2.text())
        system_op, T = system_creator_ss(self, A, B, C, D)
    
    
    print(system_)


def PID_bool_discreto(self):
    if self.main.tfdiscretocheckBox2.isChecked():
        self.main.tfperiodoEdit2.setEnabled(True)
    else:
        self.main.tfperiodoEdit2.setDisabled(True)


def PID_stacked_to_tf(self):
    self.main.PIDstackedWidget.setCurrentIndex(0)


def PID_stacked_to_ss(self):
    self.main.PIDstackedWidget.setCurrentIndex(1)