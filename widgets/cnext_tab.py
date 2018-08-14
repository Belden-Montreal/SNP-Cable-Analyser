from widgets.tab_widget import TabWidget
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from canvas import Canvas

class CNEXTTab(TabWidget):
    def __init__(self, name, freq, parameter, parent=None):
        super(CNEXTTab, self).__initWidgetOnly__(parent)
        self._name = name
        self._freq = freq
        self._parameter = parameter
        self._layout = QtWidgets.QVBoxLayout(self)
        self._figure = Figure()
        self._graphicsView = Canvas(self._figure, self)
        self._navBar = NavigationToolbar(self._graphicsView, self)
        self._layout.addWidget(self._graphicsView)
        self._layout.addWidget(self._navBar)
        self.drawFigure()

    def drawFigure(self):
        self._figure.clear()
        ax = self._figure.add_subplot(121)
        axp = self._figure.add_subplot(122)
        magData = list(map(lambda val: val[0], self._parameter))

        # draw the data
        ax.semilogx(
            self._freq,
            magData,
        )

        phaseData = list(map(lambda val: val[1], self._parameter))

        axp.semilogx(
            self._freq,
            phaseData,
        )
        self._figure.suptitle(self._name)
        ax.set_title("Magnitude")
        axp.set_title("Phase")
        ax.set_xlabel('Frequency')
        axp.set_xlabel('Frequency')
        ax.set_ylabel('dB')
        axp.set_ylabel(u"\u00B0")
        ax.xaxis.set_major_formatter(ScalarFormatter())
        axp.xaxis.set_major_formatter(ScalarFormatter())
        ax.grid(which="both")
        axp.grid(which="both")