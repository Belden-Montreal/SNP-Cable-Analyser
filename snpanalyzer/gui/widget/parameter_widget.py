from snpanalyzer.gui.widget.tab_widget import TabWidget 
from snpanalyzer.gui.ui import parameter_widget_ui
from snpanalyzer.gui.widget.canvas import Canvas
from PyQt5 import QtWidgets
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from snpanalyzer.gui.widget.navbar import NavigationToolbar

class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget(TabWidget, parameter_widget_ui.Ui_ParameterWidget):
    def __init__(self, paramName, parameter, analysis):
        super(ParameterWidget, self).__init__(self)
        self.paramLabel.setText(paramName)
        self.paramName = paramName
        self.parameter = parameter
        self.hasPassed = True
        worstVal, worstMarg = parameter.getWorstValue(), parameter.getWorstMargin()
        self.marginListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.MARGIN))
        self.worstListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.VALUE))
        self.setPairsList()
        self.analysis = analysis
        self.graphicsView = Canvas(analysis.getFigure())
        self.verticalLayout.insertWidget(0, self.graphicsView)
        self.navBar = NavigationToolbar(self.graphicsView, self.analysis, self)
        self.verticalLayout.insertWidget(1, self.navBar)
        if worstVal.hasData():
            self.worstValue = worstVal
            self.worstMargin = worstMarg
            if (self.worstValue.passed and self.worstMargin.passed) or not self.worstMargin.hasData():
                self.passLabel.setText("Pass")
                self.hasPassed = True
            if self.worstValue.hasData():
                worst = self.worstValue.getWorstPairValue()
                item = PairItem.getItemFromPair(worst, [self.worstListWidget.item(i) for i in range(self.worstListWidget.count())])
                self.worstListWidget.setCurrentItem(item)
            if self.worstMargin.hasData():
                worst = self.worstMargin.getWorstPairMargin()
                item = PairItem.getItemFromPair(worst, [self.marginListWidget.item(i) for i in range(self.marginListWidget.count())])
                self.marginListWidget.setCurrentItem(item)
            else:
                self.passLabel.setText("Fail")
                self.hasPassed = False

    def setPairsList(self):
        for serie in self.parameter.getDataSeries():
            self.marginListWidget.addItem(PairItem(serie.getName(), serie))
            self.worstListWidget.addItem(PairItem(serie.getName(), serie))
        self.marginListWidget.sortItems()            
        self.worstListWidget.sortItems()


    def pairSelected(self, pair, listIndex):
        self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        try:
            if self.worstMargin.hasData() and listIndex == valueType.MARGIN: #Worst margin
                self.marginValueLabel.setText("{0:.2f}".format(self.worstMargin.pairs[pair.number].value))
                self.marginFreqLabel.setText("{0:.2f}".format(self.worstMargin.pairs[pair.number].freq))
                self.marginLimitLabel.setText("{0:.2f}".format(self.worstMargin.pairs[pair.number].limit))
                self.marginLabel.setText("{0:.2f}".format(abs(self.worstMargin.pairs[pair.number].margin)))
            elif self.worstValue.hasData() and listIndex == valueType.VALUE: #worst value
                self.worstValueLabel.setText("{0:.2f}".format(self.worstValue.pairs[pair.number].value))
                self.worstFreqLabel.setText("{0:.2f}".format(self.worstValue.pairs[pair.number].freq))
                self.worstLimitLabel.setText("{0:.2f}".format(self.worstValue.pairs[pair.number].limit))
                self.worstMarginLabel.setText("{0:.2f}".format(abs(self.worstValue.pairs[pair.number].margin)))
        except:
            return
            
class PairItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, number, parent = None, type = QtWidgets.QListWidgetItem.Type):
        super(PairItem, self).__init__(text, parent, type)
        self.number = number

    @staticmethod
    def getItemFromPair(pair, items):
        for item in items:
            if pair is not None:
                if pair == item.number:
                    return item
