from PyQt5 import QtWidgets, QtCore, Qt
from PyQt5.QtWidgets import QCheckBox, QLabel, QListWidgetItem, QPushButton
from widgets.SmartFlowWidget import SmartFlowWidget

from UI import ParameterWidget as PW
class valueType():
    MARGIN = 0
    VALUE = 1

class ParameterWidget():
    def __init__(self, param, sample):
        self.widget  = QtWidgets.QWidget()
        self.paramWidget = PW.Ui_ParameterWidget()
        self.paramWidget.setupUi(self.widget)
        self.paramWidget.paramLabel.setText(param)
        self.param = param
        self.sample = sample
        self.paramWidget.marginListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.MARGIN))
        self.paramWidget.worstListWidget.currentTextChanged.connect(lambda text: self.pairSelected(text, valueType.VALUE))
        self.setPairsList()
        self.hasPassed = True

        if self.sample.standard is not None:
            print("PARAM WIDGET PARAM : ", self.sample.worstValue)
            values = [self.sample.worstValue[param], self.sample.worstMargin[param]]
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
        self.setResults()

    def setPairsList(self):
        try:
            self.paramWidget.marginListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.marginListWidget.sortItems()
            self.paramWidget.worstListWidget.addItems(getattr(self.sample, self.param))
            self.paramWidget.worstListWidget.sortItems()
        except Exception as e:
            return

    def pairSelected(self, pair, listIndex):
        if self.sample.standard is not None:
            self.setLabels(listIndex, pair)

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


    def setResults(self):

        flowLayout = SmartFlowWidget()

        for label in getattr(self.sample, self.param):

            chkBoxItem = QListWidgetItem()
            chkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            chkBoxItem.setText(label)
            chkBoxItem.setCheckState(QtCore.Qt.CheckState.Checked)
            #checkbox = QCheckBox(label, self.paramWidget.resultsList)
            #checkbox.setChecked(True)  

            self.paramWidget.resultsList.addItem(chkBoxItem)
        



