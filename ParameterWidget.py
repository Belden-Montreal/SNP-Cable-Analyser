from PyQt5 import QtWidgets
import Parameter_Widget
class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget():
    def __init__(self, param, sample, values):
        self.widget  = QtWidgets.QWidget()
        self.paramWidget = Parameter_Widget.Ui_ParameterWidget()
        self.paramWidget.setupUi(self.widget)
        self.paramWidget.paramLabel.setText(param)
        self.param = param
        self.sample = sample
        self.paramWidget.marginListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.MARGIN))
        self.paramWidget.worstListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.VALUE))
        self.setPairsList()
        if values[0] and values[1]:
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
        try:
            self.paramWidget.marginListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.marginListWidget.sortItems()
            #self.paramWidget.marginListWidget.setCurrentRow(0)
            self.paramWidget.worstListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.worstListWidget.sortItems()
            #self.paramWidget.worstListWidget.setCurrentRow(0)
        except Exception as e:
            return

    def pairSelected(self, pair, listIndex):
        self.setLabels(listIndex, pair)
        print(self.worstValue[0][pair][0].__str__())

    def setLabels(self, listIndex, pair):
        if self.worstMargin and listIndex == valueType.MARGIN: #Worst margin
            self.paramWidget.marginValueLabel.setText(self.worstMargin[0][pair][0].__str__())
            self.paramWidget.marginFreqLabel.setText(self.worstMargin[0][pair][1].__str__())
            self.paramWidget.marginLimitLabel.setText(self.worstMargin[0][pair][2].__str__())
            self.paramWidget.marginLabel.setText(self.worstMargin[0][pair][3].__str__())
        elif self.worstValue: #worst value
            self.paramWidget.worstValueLabel.setText(self.worstValue[0][pair][0].__str__())
            self.paramWidget.worstFreqLabel.setText(self.worstValue[0][pair][1].__str__())
            self.paramWidget.worstLimitLabel.setText(self.worstValue[0][pair][2].__str__())
            self.paramWidget.worstMarginLabel.setText(self.worstValue[0][pair][3].__str__())


