from snpanalyzer.gui.widget.tab_widget import TabWidget
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from snpanalyzer.gui.widget.navbar import NavigationToolbar
from canvas import Canvas
from snpanalyzer.analysis.parameter import ParameterAnalysis
from copy import deepcopy

class CNEXTTab(TabWidget):
    def __init__(self, serie, parameter, parent=None):
        super(CNEXTTab, self).__initWidgetOnly__(parent)
        self._name = serie.getName()
        self._serie = serie
        self._parameter = parameter
        self._analysis = ParameterAnalysis(parameter)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._figure = self._analysis.getFigure()
        self._graphicsView = Canvas(self._figure, self)
        self._navBar = NavigationToolbar(self._graphicsView, self._analysis, self)
        self._layout.addWidget(self._graphicsView)
        self._layout.addWidget(self._navBar)
        self.setupPlot()
        self._graphicsView.draw()

    def setupPlot(self):
        series = self._parameter.getDataSeries()
        for serie in series:
            self._analysis.removeSerie(serie) 
        self._analysis.addSerie(self._serie)
        