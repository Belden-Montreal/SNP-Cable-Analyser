from PyQt5 import QtWidgets, QtCore
from limits import Edit_Limit_Dialog
from limits.limitParameters import PARAMETERS
from limits.TreeItem import TreeItem
from limits.Limit import Limit

class Box():
    STAND = 0
    CAT = 1
    HARDW = 2
    PARAM = 3

class EditLimitDialog():

    def __init__(self, model):
        self.model = model
        self.dialog = QtWidgets.QDialog()
        self.editLimitDialog = Edit_Limit_Dialog.Ui_Dialog()
        self.editLimitDialog.setupUi(self.dialog)
        self.boxes = [self.editLimitDialog.standardBox, self.editLimitDialog.categoryBox, self.editLimitDialog.hardwareBox, self.editLimitDialog.parameterBox]
        self.lineEdits = [self.editLimitDialog.standardEdit, self.editLimitDialog.categoryEdit, self.editLimitDialog.hardwareEdit, self.editLimitDialog.parameterEdit]
        self.editLimitDialog.parameterBox.addItems(PARAMETERS)
        for item in self.model.rootItem.children:
            self.editLimitDialog.standardBox.addItem(item.name, item)
        self.setBoxItems(self.model.rootItem, 0, Box.CAT)
        self.setBoxItems(self.model.rootItem.child(0), 0, Box.HARDW)
        self.editLimitDialog.standardBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.model.rootItem, index, Box.CAT))
        self.editLimitDialog.categoryBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.editLimitDialog.standardBox.currentData(), index, Box.HARDW))
        self.editLimitDialog.hardwareBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.editLimitDialog.categoryBox.currentData(), index, Box.PARAM))
        self.editLimitDialog.parameterBox.currentTextChanged.connect(lambda text: self.setTextLimit(self.editLimitDialog.hardwareBox.currentData(), text))
        self.editLimitDialog.okButton.pressed.connect(lambda: self.saveLimit(True))
        self.editLimitDialog.cancelButton.pressed.connect(self.dialog.reject)
        self.editLimitDialog.saveButton.pressed.connect(lambda: self.saveLimit(False))

    def setBoxItems(self, parent, index, boxIndex):
        self.boxes[boxIndex].blockSignals(True)
        self.setTextEdit(boxIndex-1)
        if boxIndex < len(self.boxes) - 1:
            self.boxes[boxIndex].clear()
            for item in parent.child(index).children:
                self.boxes[boxIndex].addItem(item.name, item)
            self.setBoxItems(parent.child(index), 0, boxIndex + 1)
        elif boxIndex < len(self.boxes):
            self.boxes[Box.PARAM].setCurrentIndex(0)
            self.setTextLimit(parent.child(index), self.boxes[-1].currentText())
        self.boxes[boxIndex].blockSignals(False)


    def setTextEdit(self, boxIndex):
        self.lineEdits[boxIndex].setText(self.boxes[boxIndex].currentText())

    def setTextLimit(self, item, param):
        if param in item.limits.dict:
            self.lineEdits[Box.PARAM].setText(item.limits.dict[param].__str__())

    def saveLimit(self, closeDialog):
        if closeDialog:
            self.dialog.accept()
        #TODO: save to xml file and model
        for i in range(3):
            if i < 1:
                item = [x for x in self.model.rootItem.children if x.name == self.boxes[i].currentText()]
            else:
                item = [x for x in self.boxes[i-1].currentData().children if x.name == self.boxes[i].currentText()]
            if len(item) > 0:
                item[0].name = self.lineEdits[i].text()
                self.boxes[i].setItemText(self.boxes[i].currentIndex(), item[0].name)
        self.boxes[Box.HARDW].currentData().limits.dict[self.boxes[Box.PARAM].currentText()] = Limit(self.boxes[Box.PARAM].currentText(), self.lineEdits[Box.PARAM].text())

    def showDialog(self):
        return self.dialog.exec_()