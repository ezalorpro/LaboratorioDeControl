# -*- coding: utf-8 -*-

import functools
import json
import operator

import control as ctrl
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph.exporters import ImageExporter, Matplotlib
from pyqtgraph.graphicsItems import PlotDataItem

import otraventana
from monkeyPatch_fourier import _fourierTransform
from monkeyPatch_image import export
from monkeyPatch_matplotib import MatplotlibExporter
from MonkeyPatch_stepinfo import step_info

ctrl.step_info = step_info
ImageExporter.export = export
PlotDataItem.PlotDataItem._fourierTransform = _fourierTransform
Matplotlib.MatplotlibExporter.cleanAxes = MatplotlibExporter.cleanAxes
Matplotlib.MatplotlibExporter.export = MatplotlibExporter.export


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(772, 395)
        MainWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(10, 20, 751, 331))
        self.widget.setObjectName("widget")

        self.horizontalLayoutMain = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayoutMain.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutMain.setObjectName("horizontalLayoutMain")

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.lineEditNumerador = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEditNumerador.sizePolicy().hasHeightForWidth()
        )
        self.lineEditNumerador.setSizePolicy(sizePolicy)
        self.lineEditNumerador.setObjectName("lineEditNumerador")
        self.lineEditNumerador.setText("[1]")
        self.horizontalLayout.addWidget(self.lineEditNumerador)

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.lineEditDenominador = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.lineEditDenominador.sizePolicy().hasHeightForWidth()
        )
        self.lineEditDenominador.setSizePolicy(sizePolicy)
        self.lineEditDenominador.setObjectName("lineEditDenominador")
        self.lineEditDenominador.setText("[1, 1, 1]")
        self.horizontalLayout_2.addWidget(self.lineEditDenominador)

        self.label_2 = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)

        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.pushButtonStep = QtWidgets.QPushButton(self.widget)
        self.pushButtonStep.setObjectName("pushButtonStep")
        self.horizontalLayout_3.addWidget(self.pushButtonStep)

        self.pushButtonImpulse = QtWidgets.QPushButton(self.widget)
        self.pushButtonImpulse.setObjectName("pushButtonImpulse")
        self.horizontalLayout_3.addWidget(self.pushButtonImpulse)

        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem3)
        self.horizontalLayoutMain.addLayout(self.verticalLayout)

        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setObjectName("tabWidget")

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")

        self.step = QtWidgets.QWidget()
        self.step.setObjectName("step")
        self.graphicsViewStep = pg.PlotWidget(self.step)
        self.graphicsViewStep.setGeometry(QtCore.QRect(10, 10, 351, 291))
        self.graphicsViewStep.setObjectName("graphicsViewStep")
        self.graphicsViewStep.showGrid(x=True, y=True)
        self.stepCurve = self.graphicsViewStep.plot(pen="r")
        self.tabWidget.addTab(self.step, "")

        self.impulse = QtWidgets.QWidget()
        self.impulse.setObjectName("impulse")
        self.graphicsViewImpulse = pg.PlotWidget(self.impulse)
        self.graphicsViewImpulse.setGeometry(QtCore.QRect(10, 10, 351, 291))
        self.graphicsViewImpulse.setObjectName("graphicsViewImpulse")
        self.graphicsViewImpulse.showGrid(x=True, y=True)
        self.impulseCurve = self.graphicsViewImpulse.plot(pen="r")
        self.tabWidget.addTab(self.impulse, "")

        self.horizontalLayoutMain.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 772, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)

        self.pushButtonStep.clicked.connect(self.generateStep)
        self.pushButtonImpulse.clicked.connect(self.generateImpulse)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.lineEditNumerador, self.lineEditDenominador)
        MainWindow.setTabOrder(self.lineEditDenominador, self.pushButtonStep)
        MainWindow.setTabOrder(self.pushButtonStep, self.pushButtonImpulse)
        MainWindow.setTabOrder(self.pushButtonImpulse, self.tabWidget)
        MainWindow.setTabOrder(self.tabWidget, self.graphicsViewStep)
        MainWindow.setTabOrder(self.graphicsViewStep, self.graphicsViewImpulse)
        self.ventana = MainWindow

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Numerador"))
        self.label_2.setText(_translate("MainWindow", "Denominador"))
        self.pushButtonStep.setText(_translate("MainWindow", "Step"))
        self.pushButtonImpulse.setText(_translate("MainWindow", "Impulse"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.step), _translate("MainWindow", "Step")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.impulse), _translate("MainWindow", "Impulse")
        )

    def generateStep(self, rangox=0):

        num = self.lineEditNumerador.text()
        num = json.loads(num)
        dem = self.lineEditDenominador.text()
        dem = json.loads(dem)
        dt = 0.2
        sysc = ctrl.tf(num, dem)
        t, _ = ctrl.impulse_response(sysc)
        T = np.arange(0, max(t), dt)
        U = np.zeros_like(T)
        U[0] = 1

        sysc = ctrl.sample_system(sysc, dt)

        Ti = np.arange(0, 300, dt)
        info = ctrl.step_info(sysc, Ti)
        Ts = int(info["SettlingTime"]) * 2

        # Peak = plt.text(float(info['PeakTime']), float(info['Peak'])*1.03,
        #         f"Peak:{info['Peak']:.3f}", fontsize=6)

        # Risetime = plt.text(float(info['RiseTime']), 0.8,
        #         f"RiseTime:{info['RiseTime']:.3f}s", fontsize=6)

        # Overshoot = plt.text(float(info['PeakTime']), float(info['Peak'])*1.102,
        #         f"Overshoot:{info['Overshoot']:.3f}%", fontsize=6)

        t, y, _ = ctrl.forced_response(sysc, T, U)
        U = np.ones_like(T)

        t, y, _ = ctrl.forced_response(sysc, T, U)

        if ctrl.isdtime(sysc, strict=True):
            y = y[0]

        t_plot = functools.reduce(operator.iconcat, zip(t, t), [])
        y_plot = functools.reduce(operator.iconcat, zip(y, np.zeros_like(y)), [])

        self.tabWidget.setCurrentIndex(0)
        self.stepCurve.setData(t_plot, y_plot, connect="pairs")
        self.graphicsViewStep.setRange(xRange=[0, max(t)], yRange=[min(y), max(y)])

    def generateImpulse(self):
        num = self.lineEditNumerador.text()
        num = json.loads(num)
        dem = self.lineEditDenominador.text()
        dem = json.loads(dem)

        Ts = 10
        sysc = ctrl.tf(num, dem)
        T = np.linspace(0, Ts, 2000)
        Ti = np.linspace(0, Ts * 4, 2000)
        U = np.ones_like(T)
        t, y = ctrl.impulse_response(sysc)
        self.tabWidget.setCurrentIndex(1)
        self.impulseCurve.setData(t, y)
        self.graphicsViewImpulse.setRange(xRange=[0, max(t)], yRange=[min(y), max(y)])

        # self.ventana.close()
        # Dialog = QtWidgets.QDialog()
        # self.NuevaVentana = otraventana.Ui_Dialog()
        # self.NuevaVentana.setupUi(Dialog)
        # Dialog.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
