from PyQt5 import QtWidgets, QtCore
from limits import Set_Limit_Dialog
from limits.TreeModel import TreeModel

class LimitDialog(object):
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.limitDialog = Set_Limit_Dialog.Ui_LimitDialog()
        self.limitDialog.setupUi(self.dialog)
        self.model = TreeModel()
        self.limitDialog.treeView.setModel(self.model)
        button = self.limitDialog.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        button.setDisabled(True)
        self.limitDialog.treeView.clicked.connect(lambda index: self.updateButton(index, button))
        self.limitDialog.treeView.doubleClicked.connect(lambda index: self.doubleClickAccept(index))

    def getSelection(self):
        return self.limitDialog.treeView.selectedIndexes()[0]

    def showDialog(self):
        return self.dialog.exec_()
    
    def updateButton(self, index, button):
        if index:
            if self.isValidSelection(index):
                button.setEnabled(True)
                return
        button.setDisabled(True)

    def doubleClickAccept(self, index):
        if index:
            if self.isValidSelection(index):
                self.dialog.accept()

    def isValidSelection(self, index):
        return not (self.model.parent(index) == QtCore.QModelIndex() or index.internalPointer().children)