from PySide2 import QtCore, QtWidgets


class FocusLineEdit(QtWidgets.QLineEdit):
    focusIn = QtCore.Signal()

    def focusInEvent(self, event):
        super(FocusLineEdit, self).focusInEvent(event)
        self.focusIn.emit()