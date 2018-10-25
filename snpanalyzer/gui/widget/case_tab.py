from snpanalyzer.gui.widget.tab_widget import TabWidget
from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
from snpanalyzer.gui.widget.navbar import NavigationToolbar
from canvas import Canvas
from snpanalyzer.analysis.case import CaseAnalysis

class CaseTab(TabWidget):
    def __init__(self, serie, parameter,  parent=None, limit=None):
        super(CaseTab, self).__initWidgetOnly__(parent)
        self._name = serie.getName()
        self._serie = serie
        self._parameter = parameter
        self._analysis = CaseAnalysis(parameter)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._figure = self._analysis.getFigure()
        self._graphicsView = Canvas(self._figure, self)
        self._navBar = NavigationToolbar(self._graphicsView, self._analysis, self)
        self._layout.addWidget(self._graphicsView)
        self._layout.addWidget(self._navBar)
        self._limit = limit
        self.setupPlot()
        self._graphicsView.draw()

    def setupPlot(self):
        for serie in self._parameter.getDataSeries():
            self._analysis.removeSerie(serie)
        self._analysis.addSerie(self._serie)
        param = self._parameter.getParameter()[self._serie]
        if 1 in param or 4 in param:
            if self._parameter.getLimit():
                self._analysis.addSecondLimit()
