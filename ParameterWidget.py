from PyQt5 import QtWidgets
import Parameter_Widget
class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget():
    def __init__(self, param, sample):
        self.widget  = QtWidgets.QWidget()
        self.paramWidget = Parameter_Widget.Ui_ParameterWidget()
        self.paramWidget.setupUi(self.widget)
        self.paramWidget.paramLabel.setText(param)
        self.param = param
        self.sample = sample
        self.paramWidget.marginListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.MARGIN))
        self.paramWidget.worstListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.VALUE))
        self.setPairsList()
        self.paramWidget.passLabel.setText("TODO")

    def setPairsList(self):
        self.paramWidget.marginListWidget.addItems(getattr(self.sample, self.param.replace(" ","")).keys())
        self.paramWidget.marginListWidget.sortItems()
        #self.paramWidget.marginListWidget.setCurrentRow(0)
        self.paramWidget.worstListWidget.addItems(getattr(self.sample, self.param.replace(" ","")).keys())
        self.paramWidget.worstListWidget.sortItems()
        #self.paramWidget.worstListWidget.setCurrentRow(0)

    def pairSelected(self, pair, listIndex):
        #TODO: get value of pair
        self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        if listIndex == valueType.MARGIN and False: #Worst margin
            margin = self.sample.getWorstMargin(self.param)[0][pair]
            self.paramWidget.marginValueLabel.setText(margin[0].__str__())
            self.paramWidget.marginFreqLabel.setText(margin[1].__str__())
            self.paramWidget.marginLimitLabel.setText(margin[2].__str__())
            self.paramWidget.marginLabel.setText(margin[3].__str__())
        else: #worst value
            worst = self.sample.getWorstValue(self.param)[0][pair]
            self.paramWidget.worstValueLabel.setText(worst[0].__str__())
            self.paramWidget.worstFreqLabel.setText(worst[1].__str__())
            self.paramWidget.worstLimitLabel.setText(worst[2].__str__())
            self.paramWidget.worstMarginLabel.setText(worst[3].__str__())


