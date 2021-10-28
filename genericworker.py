from PyQt5 import QtCore     
from PyQt5.QtCore import pyqtSignal, pyqtSlot
#https://newbedev.com/how-to-use-qthread-correctly-in-pyqt-with-movetothread
class GenericWorker(QtCore.QObject):

    start = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    #@pyqtSlot()
    def __del__(self):
        self.wait()

    @pyqtSlot()
    def run(self, *args, **kwargs):
        self.function(*self.args, **self.kwargs)
        self.finished.emit()