from PyQt5 import QtWidgets, QtCore
from limits import Set_Limit_Dialog
from limits.TreeModel import TreeModel
from limits.EditLimitDialog import EditLimitDialog

class LimitDialog(object):
    def __init__(self, limitsFile = "limits/limits.xml"):
        self.dialog = QtWidgets.QDialog()
        self.limitDialog = Set_Limit_Dialog.Ui_LimitDialog()
        self.limitDialog.setupUi(self.dialog)
        self.model = TreeModel(limitsFile)
        self.limitDialog.treeView.setModel(self.model)
        self.resizeColumns(QtCore.QModelIndex())
        button = self.limitDialog.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        button.setDisabled(True)
        self.limitDialog.treeView.clicked.connect(lambda index: self.updateButton(index, button))
        self.limitDialog.treeView.entered.connect(lambda index: self.updateButton(index, button))
        self.limitDialog.treeView.doubleClicked.connect(lambda index: self.doubleClickAccept(index))
        self.limitDialog.treeView.expanded.connect(lambda index: self.resizeColumns(index))
        self.limitDialog.treeView.collapsed.connect(lambda index: self.resizeColumns(index))
        self.limitDialog.editButton.pressed.connect(lambda: self.openLimitEditDialog())

    def resizeColumns(self, index):
        for column in range(self.model.columnCount(index)):
            self.limitDialog.treeView.resizeColumnToContents(column)

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

    def openLimitEditDialog(self):
        editLimitDialog = EditLimitDialog(self.model)

        res = editLimitDialog.showDialog()
    
    def getStandardList(self):
        standards = []
        self.getStandard(self.model.rootItem, standards)
        return standards
        
    def getStandard(self, node, standardList):
        if node.childCount():
            for child in node.children:
                self.getStandard(child, standardList)
        else:
            standardList.append(node.standard)

