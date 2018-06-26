from PyQt5 import QtWidgets
import Parameter_Widget
class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget():
    def __init__(self, param, parameter):
        self.widget  = QtWidgets.QWidget()
        self.paramWidget = Parameter_Widget.Ui_ParameterWidget()
        self.paramWidget.setupUi(self.widget)
        self.paramWidget.paramLabel.setText(param)
        self.param = param
        self.parameter = parameter
        values = (parameter.getWorstValue(), parameter.getWorstMargin())
        self.paramWidget.marginListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.MARGIN))
        self.paramWidget.worstListWidget.currentItemChanged.connect(lambda current: self.pairSelected(current, valueType.VALUE))
        self.setPairsList()
        if values[0][0] and values[1]:
            self.worstValue = values[0]
            self.worstMargin = values[1]
            if self.worstValue[1] == "Pass" and self.worstMargin[1] == "Pass":
                self.paramWidget.passLabel.setText("Pass")
                self.hasPassed = True
            else:
                self.paramWidget.passLabel.setText("Fail")
                self.hasPassed = False
        else:
            self.worstMargin = None
            self.worstValue = None
            self.paramWidget.passLabel.setText("Fail")
            self.hasPassed = False




    def setPairsList(self):
        for num, port in self.parameter.getPorts().items():
            self.paramWidget.marginListWidget.addItem(PairItem(port, num))
            self.paramWidget.worstListWidget.addItem(PairItem(port, num))
        self.paramWidget.marginListWidget.sortItems()            
        self.paramWidget.worstListWidget.sortItems()


    def pairSelected(self, pair, listIndex):
        self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        if self.worstMargin and listIndex == valueType.MARGIN: #Worst margin
            self.paramWidget.marginValueLabel.setText(self.worstMargin[0][pair.number][0].__str__())
            self.paramWidget.marginFreqLabel.setText(self.worstMargin[0][pair.number][1].__str__())
            self.paramWidget.marginLimitLabel.setText(self.worstMargin[0][pair.number][2].__str__())
            self.paramWidget.marginLabel.setText(self.worstMargin[0][pair.number][3].__str__())
        elif self.worstValue: #worst value
            self.paramWidget.worstValueLabel.setText(self.worstValue[0][pair.number][0].__str__())
            self.paramWidget.worstFreqLabel.setText(self.worstValue[0][pair.number][1].__str__())
            self.paramWidget.worstLimitLabel.setText(self.worstValue[0][pair.number][2].__str__())
            self.paramWidget.worstMarginLabel.setText(self.worstValue[0][pair.number][3].__str__())

class PairItem(QtWidgets.QListWidgetItem):
    def __init__(self, text, number, parent = None, type = QtWidgets.QListWidgetItem.Type):
        super(PairItem, self).__init__(text, parent, type)
        self.number = number

