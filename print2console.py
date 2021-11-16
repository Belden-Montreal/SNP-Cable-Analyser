from PyQt5 import QtCore     
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject

class EmittingStream(QObject):  # test
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

