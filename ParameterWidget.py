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
        self.worstMargin = self.sample.getWorstMargin(self.param)#[0][pair][0].__str__()
        self.worstValue  = self.sample.getWorstValue(self.param)#[0][pair][0].__str__()
        self.setPairsList()
        self.paramWidget.passLabel.setText("TODO")
        if sample.standard and param in sample.standard.limits:
            self.margin = None#self.sample.getWorstMargin(self.param)[0]
            self.worst = self.sample.getWorstValue(self.param)[0]
        else:
            self.worst = None
            self.margin = None




    def setPairsList(self):
        try:
            self.paramWidget.marginListWidget.addItems(self.worstMargin[0].keys())
            self.paramWidget.marginListWidget.sortItems()
            #self.paramWidget.marginListWidget.setCurrentRow(0)
            self.paramWidget.worstListWidget.addItems(self.worstValue[0].keys())
            self.paramWidget.worstListWidget.sortItems()
            #self.paramWidget.worstListWidget.setCurrentRow(0)
        except Exception as e:
            return

    def pairSelected(self, pair, listIndex):
        #TODO: get value of pair
        self.setLabels(listIndex, pair)

    def setLabels(self, listIndex, pair):
        if self.margin and listIndex == valueType.MARGIN: #Worst margin
            pass
            # self.paramWidget.marginValueLabel.setText(self.margin[pair][0].__str__())
            # self.paramWidget.marginFreqLabel.setText(self.margin[pair][1].__str__())
            # self.paramWidget.marginLimitLabel.setText(self.margin[pair][2].__str__())
            # self.paramWidget.marginLabel.setText(self.margin[pair][3].__str__())
        elif self.worst: #worst value
            self.paramWidget.worstValueLabel.setText(self.worst[pair][0].__str__())
            self.paramWidget.worstFreqLabel.setText(self.worst[pair][1].__str__())
            self.paramWidget.worstLimitLabel.setText(self.worst[pair][2].__str__())
            self.paramWidget.worstMarginLabel.setText(self.worst[pair][3].__str__())


