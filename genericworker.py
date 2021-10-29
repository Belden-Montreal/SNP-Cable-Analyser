from PyQt5 import QtCore     
from PyQt5.QtCore import pyqtSignal, pyqtSlot
#https://newbedev.com/how-to-use-qthread-correctly-in-pyqt-with-movetothread
class GenericWorker(QtCore.QRunnable):
   
    finished = pyqtSignal()

    def __init__(self, function, *args, **kwargs):
        ##  Init
        #   @param  Function    function     Function to run on start
        #   @param  List        *args        args to pass to function
        #   @param  Dict        **kwargs     Keyword args to pass to function

        super(GenericWorker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.setAutoDelete(True)
        #self.start.connect(self.run)


    @pyqtSlot()
    def run(self):
        self.function(*self.args, **self.kwargs)
        self.signals.finished.emit()


class WorkerSignals(QtCore.QObject):

    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
        