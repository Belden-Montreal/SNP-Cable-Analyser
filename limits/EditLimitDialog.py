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
    NEW_ITEM = "New"
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
        self.editLimitDialog.standardBox.addItem(self.NEW_ITEM)
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
        if not (self.boxes[boxIndex-1].currentText() == self.NEW_ITEM):
            self.setTextEdit(boxIndex-1)
            if boxIndex < len(self.boxes) - 1:
                self.boxes[boxIndex].clear()
                for item in parent.child(index).children:
                    self.boxes[boxIndex].addItem(item.name, item)
                self.boxes[boxIndex].addItem(self.NEW_ITEM)
                self.setBoxItems(parent.child(index), 0, boxIndex + 1)
            elif boxIndex < len(self.boxes):
                self.boxes[Box.PARAM].setCurrentIndex(0)
                self.setTextLimit(parent.child(index), self.boxes[-1].currentText())
        else:
            self.lineEdits[boxIndex-1].clear()
            self.setBoxesToNew(boxIndex)
        self.boxes[boxIndex].blockSignals(False)


    def setBoxesToNew(self, boxIndex):
        if boxIndex < len(self.boxes) - 1:
            self.boxes[boxIndex].blockSignals(True)
            self.boxes[boxIndex].clear()
            self.boxes[boxIndex].addItem(self.NEW_ITEM)
            self.lineEdits[boxIndex].clear()
            self.setBoxesToNew(boxIndex + 1)
            self.boxes[boxIndex].blockSignals(False)
        elif boxIndex < len(self.boxes):
            self.lineEdits[boxIndex].clear()

    def setTextEdit(self, boxIndex):
        self.lineEdits[boxIndex].setText(self.boxes[boxIndex].currentText())

    def setTextLimit(self, item, param):
        if item:
            if param in item.limits.dict:
                self.lineEdits[Box.PARAM].setText(item.limits.dict[param].__str__())

    def saveLimit(self, closeDialog):
        if self.validateEdits():
            for box in self.boxes:
                box.blockSignals(True)
            parent = self.model.rootItem
            self.model.beginResetModel()
            for i in range(3):
                if not (self.boxes[i].currentText() == self.NEW_ITEM):
                    if i < 1:
                        item = next(x for x in self.model.rootItem.children if x.name == self.boxes[i].currentText())
                    else:
                        item = next(x for x in self.boxes[i-1].currentData().children if x.name == self.boxes[i].currentText())
                    if item:
                        item.name = self.lineEdits[i].text()
                        self.boxes[i].setItemText(self.boxes[i].currentIndex(), item.name)
                        parent = item
                else: #New limit
                    newItem = TreeItem(self.lineEdits[i].text(), parent)
                    self.boxes[i].addItem(newItem.name, newItem)
                    self.boxes[i].setCurrentText(newItem.name)
                    parent.addChild(newItem)
                    parent = newItem
            if not (self.lineEdits[Box.PARAM].text() == ""):
                self.boxes[Box.HARDW].currentData().limits.dict[self.boxes[Box.PARAM].currentText()] = Limit(self.boxes[Box.PARAM].currentText(), self.lineEdits[Box.PARAM].text())
            for box in self.boxes:
                box.blockSignals(False)
            self.model.endResetModel()
            self.model.updateDict()
            if closeDialog:
                self.dialog.accept()
                self.model.writeModelToFIle()

    def validateEdits(self):
        for i in range(3):
            if self.lineEdits[i].text() == "":
                error = QtWidgets.QErrorMessage(self.dialog)
                error.showMessage("Please fill the blanks.", "Empty_Blanks")
                error.exec_()
                return False
        return True

    def showDialog(self):
        return self.dialog.exec_()