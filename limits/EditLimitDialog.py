from PyQt5 import QtWidgets, QtCore
from limits import Edit_Limit_Dialog
from limits.limitParameters import PARAMETERS
from limits.TreeItem import TreeItem

class EditLimitDialog():
    def __init__(self, model):
        self.model = model
        self.dialog = QtWidgets.QDialog()
        self.editLimitDialog = Edit_Limit_Dialog.Ui_Dialog()
        self.editLimitDialog.setupUi(self.dialog)
        self.boxes = [self.editLimitDialog.standardBox, self.editLimitDialog.categoryBox, self.editLimitDialog.hardwareBox, self.editLimitDialog.parameterBox]
        for item in self.model.rootItem.children:
            self.editLimitDialog.standardBox.addItem(item.name)
        self.setBoxItems(self.model.rootItem, 0, 1)
        self.setBoxItems(self.model.rootItem.child(0), 0, 2)
        self.editLimitDialog.parameterBox.addItems(PARAMETERS)
        self.editLimitDialog.standardBox.activated.connect(lambda index: self.setBoxItems(self.model.rootItem, index, 1))
        self.editLimitDialog.categoryBox.activated.connect(lambda index: self.setBoxItems(self.model.rootItem.child(self.editLimitDialog.standardBox.currentIndex()), index, 2))


    def setBoxItems(self, parent, index, boxIndex):
        if boxIndex < len(self.boxes) - 1:
            self.boxes[boxIndex].clear()
            for item in parent.child(index).children:
                self.boxes[boxIndex].addItem(item.name)
            self.setBoxItems(parent.child(index), 0, boxIndex + 1)
        elif boxIndex < len(self.boxes):
            self.boxes[boxIndex].setCurrentIndex(0)

    

    def showDialog(self):
        return self.dialog.exec_()