from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from canvas import Canvas

class CaseTab(QtWidgets.QWidget):
    def __init__(self, name, freq, parameter, parent=None):
        super(CaseTab, self).__init__(parent)
        self._name = name
        self._freq = freq
        self._parameter = parameter
        self._figure = Figure()
        self._graphicsView = Canvas(self._figure, self)
        self.drawFigure()

    def drawFigure(self):
        self._figure.clear()
        ax = self._figure.add_subplot(111)
        for n, data in self._parameter.items():
            plotData = list(map(lambda val: val[0], data))

            # draw the data
            ax.semilogx(
                self._freq,
                plotData,
                label="Case "+str(n),
            )
        ax.set_title(self._name)
        ax.set_xlabel('Frequency (TODO)')
        ax.set_ylabel('dB')
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.grid(which="both")
        ax.legend(loc="best")

    def showTab(self):
        self._graphicsView.draw()