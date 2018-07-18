from widgets.tab_widget import TabWidget 
from widgets import parameter_widget_ui
from canvas import Canvas
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget(TabWidget, parameter_widget_ui.Ui_ParameterWidget):
    def __init__(self, paramName, parameter):
        super(ParameterWidget, self).__init__(self)
        self.paramLabel.setText(paramName)
        self.paramName = paramName
        self.parameter = parameter
        self.hasPassed = False
        values = (parameter.getWorstValue(), parameter.getWorstMargin())
        self.marginListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.MARGIN))
        self.worstListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.VALUE))
        self.setPairsList()
        self.graphicsView = Canvas(parameter.getPlot().getFigure())
        self.verticalLayout.insertWidget(0, self.graphicsView)
        self.navBar = NavigationToolbar(self.graphicsView, self)
        self.verticalLayout.insertWidget(1, self.navBar)
        if values[0][0] and values[1]:
            self.worstValue = values[0]
            self.worstMargin = values[1]
            if self.worstValue[1] and self.worstMargin[1]:
                self.passLabel.setText("Pass")
                self.hasPassed = True
            else:
                self.passLabel.setText("Fail")
                self.hasPassed = False
        else:
            self.worstMargin = (dict(),None)
            self.worstValue = (dict(),None)
            self.passLabel.setText("Fail")
            self.hasPassed = False

    def setPairsList(self):
        for num, (port, isRemote) in self.parameter.getPorts().items():
            self.marginListWidget.addItem(PairItem(port, num, isRemote))
            self.worstListWidget.addItem(PairItem(port, num, isRemote))
        self.marginListWidget.sortItems()            
        self.worstListWidget.sortItems()


    def pairSelected(self, pair, listIndex):
        self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        if self.worstMargin[0] and listIndex == valueType.MARGIN: #Worst margin
            self.marginValueLabel.setText(self.worstMargin[0][pair.number][0].__str__())
            self.marginFreqLabel.setText(self.worstMargin[0][pair.number][1].__str__())
            self.marginLimitLabel.setText(self.worstMargin[0][pair.number][2].__str__())
            self.marginLabel.setText(self.worstMargin[0][pair.number][3].__str__())
        elif self.worstValue and listIndex == valueType.VALUE: #worst value
            self.worstValueLabel.setText(self.worstValue[0][pair.number][0].__str__())
            self.worstFreqLabel.setText(self.worstValue[0][pair.number][1].__str__())
            self.worstLimitLabel.setText(self.worstValue[0][pair.number][2].__str__())
            self.worstMarginLabel.setText(self.worstValue[0][pair.number][3].__str__())
            
class PairItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, number, isRemote, parent = None, type = QtWidgets.QListWidgetItem.Type):
        super(PairItem, self).__init__(text, parent, type)
        self.number = number
        self.isRemote = isRemote

