# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\PC\Documents\Descargas chrome\NO TOCAR MALDITO IDIOTA!! ZZZZ\kleiver\Tesis\Nueva tesis\LaboratorioDeControl\VentanaPrincipal.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(900, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("")
        MainWindow.setDocumentMode(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.principalTab = QtWidgets.QTabWidget(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        self.principalTab.setPalette(palette)
        self.principalTab.setTabPosition(QtWidgets.QTabWidget.North)
        self.principalTab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.principalTab.setElideMode(QtCore.Qt.ElideNone)
        self.principalTab.setDocumentMode(True)
        self.principalTab.setTabsClosable(False)
        self.principalTab.setTabBarAutoHide(True)
        self.principalTab.setObjectName("principalTab")
        self.analisisTab = QtWidgets.QWidget()
        self.analisisTab.setObjectName("analisisTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.analisisTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.demLabel1 = QtWidgets.QLabel(self.analisisTab)
        self.demLabel1.setObjectName("demLabel1")
        self.gridLayout_3.addWidget(self.demLabel1, 3, 0, 1, 1)
        self.numEdit1 = QtWidgets.QLineEdit(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numEdit1.sizePolicy().hasHeightForWidth())
        self.numEdit1.setSizePolicy(sizePolicy)
        self.numEdit1.setObjectName("numEdit1")
        self.gridLayout_3.addWidget(self.numEdit1, 2, 1, 1, 1)
        self.analisisGraficaTab = QtWidgets.QTabWidget(self.analisisTab)
        self.analisisGraficaTab.setAutoFillBackground(True)
        self.analisisGraficaTab.setDocumentMode(False)
        self.analisisGraficaTab.setMovable(True)
        self.analisisGraficaTab.setTabBarAutoHide(False)
        self.analisisGraficaTab.setObjectName("analisisGraficaTab")
        self.stepTab = QtWidgets.QWidget()
        self.stepTab.setObjectName("stepTab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.stepTab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.stepGraphicsView1 = QtWidgets.QGraphicsView(self.stepTab)
        self.stepGraphicsView1.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stepGraphicsView1.setInteractive(True)
        self.stepGraphicsView1.setObjectName("stepGraphicsView1")
        self.gridLayout_2.addWidget(self.stepGraphicsView1, 0, 0, 1, 1)
        self.analisisGraficaTab.addTab(self.stepTab, "")
        self.impulseTab = QtWidgets.QWidget()
        self.impulseTab.setObjectName("impulseTab")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.impulseTab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.impulseGraphicsView = QtWidgets.QGraphicsView(self.impulseTab)
        self.impulseGraphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.impulseGraphicsView.setObjectName("impulseGraphicsView")
        self.gridLayout_4.addWidget(self.impulseGraphicsView, 0, 0, 1, 1)
        self.analisisGraficaTab.addTab(self.impulseTab, "")
        self.bodeTab = QtWidgets.QWidget()
        self.bodeTab.setObjectName("bodeTab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.bodeTab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.magBodeGraphicsView = QtWidgets.QGraphicsView(self.bodeTab)
        self.magBodeGraphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.magBodeGraphicsView.setObjectName("magBodeGraphicsView")
        self.gridLayout_5.addWidget(self.magBodeGraphicsView, 0, 0, 1, 1)
        self.phaBodeGraphicsView = QtWidgets.QGraphicsView(self.bodeTab)
        self.phaBodeGraphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.phaBodeGraphicsView.setObjectName("phaBodeGraphicsView")
        self.gridLayout_5.addWidget(self.phaBodeGraphicsView, 1, 0, 1, 1)
        self.analisisGraficaTab.addTab(self.bodeTab, "")
        self.nyquistTab = QtWidgets.QWidget()
        self.nyquistTab.setObjectName("nyquistTab")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.nyquistTab)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.NyquistGraphicsView = QtWidgets.QGraphicsView(self.nyquistTab)
        self.NyquistGraphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.NyquistGraphicsView.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.NyquistGraphicsView.setObjectName("NyquistGraphicsView")
        self.gridLayout_6.addWidget(self.NyquistGraphicsView, 0, 0, 1, 1)
        self.analisisGraficaTab.addTab(self.nyquistTab, "")
        self.rlocusTab = QtWidgets.QWidget()
        self.rlocusTab.setObjectName("rlocusTab")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.rlocusTab)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.rlocusGraphicsView = QtWidgets.QGraphicsView(self.rlocusTab)
        self.rlocusGraphicsView.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.rlocusGraphicsView.setObjectName("rlocusGraphicsView")
        self.gridLayout_7.addWidget(self.rlocusGraphicsView, 0, 0, 1, 1)
        self.analisisGraficaTab.addTab(self.rlocusTab, "")
        self.gridLayout_3.addWidget(self.analisisGraficaTab, 0, 2, 8, 1)
        self.numLabel1 = QtWidgets.QLabel(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numLabel1.sizePolicy().hasHeightForWidth())
        self.numLabel1.setSizePolicy(sizePolicy)
        self.numLabel1.setObjectName("numLabel1")
        self.gridLayout_3.addWidget(self.numLabel1, 2, 0, 1, 1)
        self.demEdit1 = QtWidgets.QLineEdit(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.demEdit1.sizePolicy().hasHeightForWidth())
        self.demEdit1.setSizePolicy(sizePolicy)
        self.demEdit1.setObjectName("demEdit1")
        self.gridLayout_3.addWidget(self.demEdit1, 3, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem, 6, 1, 1, 1)
        self.datosTextEdit1 = QtWidgets.QPlainTextEdit(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datosTextEdit1.sizePolicy().hasHeightForWidth())
        self.datosTextEdit1.setSizePolicy(sizePolicy)
        self.datosTextEdit1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.datosTextEdit1.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.datosTextEdit1.setReadOnly(True)
        self.datosTextEdit1.setPlainText("")
        self.datosTextEdit1.setBackgroundVisible(True)
        self.datosTextEdit1.setObjectName("datosTextEdit1")
        self.gridLayout_3.addWidget(self.datosTextEdit1, 4, 1, 1, 1)
        self.datosLabel1 = QtWidgets.QLabel(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datosLabel1.sizePolicy().hasHeightForWidth())
        self.datosLabel1.setSizePolicy(sizePolicy)
        self.datosLabel1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.datosLabel1.setScaledContents(False)
        self.datosLabel1.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.datosLabel1.setWordWrap(False)
        self.datosLabel1.setObjectName("datosLabel1")
        self.gridLayout_3.addWidget(self.datosLabel1, 4, 0, 1, 1)
        self.calcButton1 = QtWidgets.QPushButton(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calcButton1.sizePolicy().hasHeightForWidth())
        self.calcButton1.setSizePolicy(sizePolicy)
        self.calcButton1.setObjectName("calcButton1")
        self.gridLayout_3.addWidget(self.calcButton1, 5, 1, 1, 1)
        self.coefLabel1 = QtWidgets.QLabel(self.analisisTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coefLabel1.sizePolicy().hasHeightForWidth())
        self.coefLabel1.setSizePolicy(sizePolicy)
        self.coefLabel1.setObjectName("coefLabel1")
        self.gridLayout_3.addWidget(self.coefLabel1, 1, 0, 1, 2)
        self.principalTab.addTab(self.analisisTab, "")
        self.PIDTab = QtWidgets.QWidget()
        self.PIDTab.setObjectName("PIDTab")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.PIDTab)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.numEdit2 = QtWidgets.QLineEdit(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numEdit2.sizePolicy().hasHeightForWidth())
        self.numEdit2.setSizePolicy(sizePolicy)
        self.numEdit2.setObjectName("numEdit2")
        self.gridLayout_8.addWidget(self.numEdit2, 3, 1, 1, 1)
        self.demEdit2 = QtWidgets.QLineEdit(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.demEdit2.sizePolicy().hasHeightForWidth())
        self.demEdit2.setSizePolicy(sizePolicy)
        self.demEdit2.setObjectName("demEdit2")
        self.gridLayout_8.addWidget(self.demEdit2, 4, 1, 1, 1)
        self.demLabel2 = QtWidgets.QLabel(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.demLabel2.sizePolicy().hasHeightForWidth())
        self.demLabel2.setSizePolicy(sizePolicy)
        self.demLabel2.setObjectName("demLabel2")
        self.gridLayout_8.addWidget(self.demLabel2, 4, 0, 1, 1)
        self.datosLabel2 = QtWidgets.QLabel(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datosLabel2.sizePolicy().hasHeightForWidth())
        self.datosLabel2.setSizePolicy(sizePolicy)
        self.datosLabel2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.datosLabel2.setScaledContents(False)
        self.datosLabel2.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.datosLabel2.setWordWrap(False)
        self.datosLabel2.setObjectName("datosLabel2")
        self.gridLayout_8.addWidget(self.datosLabel2, 5, 0, 1, 1)
        self.numLabel2 = QtWidgets.QLabel(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.numLabel2.sizePolicy().hasHeightForWidth())
        self.numLabel2.setSizePolicy(sizePolicy)
        self.numLabel2.setObjectName("numLabel2")
        self.gridLayout_8.addWidget(self.numLabel2, 3, 0, 1, 1)
        self.kdHSlider2 = QtWidgets.QSlider(self.PIDTab)
        self.kdHSlider2.setEnabled(False)
        self.kdHSlider2.setMaximum(200)
        self.kdHSlider2.setSliderPosition(0)
        self.kdHSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.kdHSlider2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.kdHSlider2.setTickInterval(2)
        self.kdHSlider2.setObjectName("kdHSlider2")
        self.gridLayout_8.addWidget(self.kdHSlider2, 9, 2, 1, 1)
        self.kiHSlider2 = QtWidgets.QSlider(self.PIDTab)
        self.kiHSlider2.setEnabled(False)
        self.kiHSlider2.setMaximum(1000)
        self.kiHSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.kiHSlider2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.kiHSlider2.setTickInterval(10)
        self.kiHSlider2.setObjectName("kiHSlider2")
        self.gridLayout_8.addWidget(self.kiHSlider2, 8, 2, 1, 1)
        self.kpHSlider2 = QtWidgets.QSlider(self.PIDTab)
        self.kpHSlider2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.kpHSlider2.sizePolicy().hasHeightForWidth())
        self.kpHSlider2.setSizePolicy(sizePolicy)
        self.kpHSlider2.setMaximum(1000)
        self.kpHSlider2.setSingleStep(1)
        self.kpHSlider2.setProperty("value", 1)
        self.kpHSlider2.setTracking(True)
        self.kpHSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.kpHSlider2.setInvertedAppearance(False)
        self.kpHSlider2.setInvertedControls(False)
        self.kpHSlider2.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.kpHSlider2.setTickInterval(10)
        self.kpHSlider2.setObjectName("kpHSlider2")
        self.gridLayout_8.addWidget(self.kpHSlider2, 7, 2, 1, 1)
        self.datosTextEdit2 = QtWidgets.QPlainTextEdit(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.datosTextEdit2.sizePolicy().hasHeightForWidth())
        self.datosTextEdit2.setSizePolicy(sizePolicy)
        self.datosTextEdit2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.datosTextEdit2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.datosTextEdit2.setReadOnly(True)
        self.datosTextEdit2.setPlainText("")
        self.datosTextEdit2.setBackgroundVisible(True)
        self.datosTextEdit2.setObjectName("datosTextEdit2")
        self.gridLayout_8.addWidget(self.datosTextEdit2, 5, 1, 1, 1)
        self.kiCheckBox2 = QtWidgets.QCheckBox(self.PIDTab)
        self.kiCheckBox2.setTristate(False)
        self.kiCheckBox2.setObjectName("kiCheckBox2")
        self.gridLayout_8.addWidget(self.kiCheckBox2, 8, 3, 1, 1)
        self.kpCheckBox2 = QtWidgets.QCheckBox(self.PIDTab)
        self.kpCheckBox2.setChecked(True)
        self.kpCheckBox2.setObjectName("kpCheckBox2")
        self.gridLayout_8.addWidget(self.kpCheckBox2, 7, 3, 1, 1)
        self.kdCheckBox2 = QtWidgets.QCheckBox(self.PIDTab)
        self.kdCheckBox2.setObjectName("kdCheckBox2")
        self.gridLayout_8.addWidget(self.kdCheckBox2, 9, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_8.addItem(spacerItem1, 6, 1, 1, 1)
        self.stepGraphicsView2 = QtWidgets.QGraphicsView(self.PIDTab)
        self.stepGraphicsView2.setObjectName("stepGraphicsView2")
        self.gridLayout_8.addWidget(self.stepGraphicsView2, 0, 2, 7, 2)
        self.coefLabel2 = QtWidgets.QLabel(self.PIDTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coefLabel2.sizePolicy().hasHeightForWidth())
        self.coefLabel2.setSizePolicy(sizePolicy)
        self.coefLabel2.setObjectName("coefLabel2")
        self.gridLayout_8.addWidget(self.coefLabel2, 2, 0, 1, 2)
        self.principalTab.addTab(self.PIDTab, "")
        self.fuzzyTab = QtWidgets.QWidget()
        self.fuzzyTab.setObjectName("fuzzyTab")
        self.principalTab.addTab(self.fuzzyTab, "")
        self.gridLayout.addWidget(self.principalTab, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionpelado = QtWidgets.QAction(MainWindow)
        self.actionpelado.setObjectName("actionpelado")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.retranslateUi(MainWindow)
        self.principalTab.setCurrentIndex(0)
        self.analisisGraficaTab.setCurrentIndex(0)
        self.kiCheckBox2.clicked['bool'].connect(self.kiHSlider2.setEnabled)
        self.kpCheckBox2.clicked['bool'].connect(self.kpHSlider2.setEnabled)
        self.kdCheckBox2.clicked['bool'].connect(self.kdHSlider2.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.principalTab, self.numEdit1)
        MainWindow.setTabOrder(self.numEdit1, self.demEdit1)
        MainWindow.setTabOrder(self.demEdit1, self.datosTextEdit1)
        MainWindow.setTabOrder(self.datosTextEdit1, self.calcButton1)
        MainWindow.setTabOrder(self.calcButton1, self.analisisGraficaTab)
        MainWindow.setTabOrder(self.analisisGraficaTab, self.stepGraphicsView1)
        MainWindow.setTabOrder(self.stepGraphicsView1, self.impulseGraphicsView)
        MainWindow.setTabOrder(self.impulseGraphicsView, self.magBodeGraphicsView)
        MainWindow.setTabOrder(self.magBodeGraphicsView, self.phaBodeGraphicsView)
        MainWindow.setTabOrder(self.phaBodeGraphicsView, self.NyquistGraphicsView)
        MainWindow.setTabOrder(self.NyquistGraphicsView, self.rlocusGraphicsView)
        MainWindow.setTabOrder(self.rlocusGraphicsView, self.numEdit2)
        MainWindow.setTabOrder(self.numEdit2, self.demEdit2)
        MainWindow.setTabOrder(self.demEdit2, self.datosTextEdit2)
        MainWindow.setTabOrder(self.datosTextEdit2, self.stepGraphicsView2)
        MainWindow.setTabOrder(self.stepGraphicsView2, self.kpHSlider2)
        MainWindow.setTabOrder(self.kpHSlider2, self.kpCheckBox2)
        MainWindow.setTabOrder(self.kpCheckBox2, self.kiHSlider2)
        MainWindow.setTabOrder(self.kiHSlider2, self.kiCheckBox2)
        MainWindow.setTabOrder(self.kiCheckBox2, self.kdHSlider2)
        MainWindow.setTabOrder(self.kdHSlider2, self.kdCheckBox2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Laboratorio de sistemas de control"))
        self.demLabel1.setText(_translate("MainWindow", "Denominador"))
        self.numEdit1.setText(_translate("MainWindow", "[1]"))
        self.analisisGraficaTab.setTabText(self.analisisGraficaTab.indexOf(self.stepTab), _translate("MainWindow", "Step"))
        self.analisisGraficaTab.setTabText(self.analisisGraficaTab.indexOf(self.impulseTab), _translate("MainWindow", "Impulso"))
        self.analisisGraficaTab.setTabText(self.analisisGraficaTab.indexOf(self.bodeTab), _translate("MainWindow", "Bode"))
        self.analisisGraficaTab.setTabText(self.analisisGraficaTab.indexOf(self.nyquistTab), _translate("MainWindow", "Nyquist"))
        self.analisisGraficaTab.setTabText(self.analisisGraficaTab.indexOf(self.rlocusTab), _translate("MainWindow", "root locus"))
        self.numLabel1.setText(_translate("MainWindow", "Numerador"))
        self.demEdit1.setText(_translate("MainWindow", "[1, 1, 1]"))
        self.datosLabel1.setText(_translate("MainWindow", "Datos"))
        self.calcButton1.setText(_translate("MainWindow", "Calcular"))
        self.coefLabel1.setText(_translate("MainWindow", "Coeficientes de la funcion de transferencia"))
        self.principalTab.setTabText(self.principalTab.indexOf(self.analisisTab), _translate("MainWindow", "Analisis"))
        self.numEdit2.setText(_translate("MainWindow", "[1]"))
        self.demEdit2.setText(_translate("MainWindow", "[1, 1, 1]"))
        self.demLabel2.setText(_translate("MainWindow", "Denominador"))
        self.datosLabel2.setText(_translate("MainWindow", "Datos"))
        self.numLabel2.setText(_translate("MainWindow", "Numerador"))
        self.kiCheckBox2.setText(_translate("MainWindow", "Ki"))
        self.kpCheckBox2.setText(_translate("MainWindow", "Kp"))
        self.kdCheckBox2.setText(_translate("MainWindow", "Kd"))
        self.coefLabel2.setText(_translate("MainWindow", "Coeficientes de la funcion de transferencia"))
        self.principalTab.setTabText(self.principalTab.indexOf(self.PIDTab), _translate("MainWindow", "PID Tuning"))
        self.principalTab.setTabText(self.principalTab.indexOf(self.fuzzyTab), _translate("MainWindow", "Logica difusa"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionpelado.setText(_translate("MainWindow", "pelado"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ventana = Ui_MainWindow()
    ventana.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())