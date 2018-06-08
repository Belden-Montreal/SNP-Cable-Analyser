from PyQt5 import QtWidgets, QtCore
from limits import Edit_Limit_Dialog
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
        self.lineEdits = [self.editLimitDialog.standardEdit, self.editLimitDialog.categoryEdit, self.editLimitDialog.hardwareEdit]
        self.editLimitDialog.limitsTable.setHorizontalHeaderLabels(["Min", "Max", "Limit"])
        self.editLimitDialog.limitsTable.setColumnWidth(0, 50)
        self.editLimitDialog.limitsTable.setColumnWidth(1, 50)
        self.editLimitDialog.parameterBox.addItems(self.model.header[1:])
        self.editLimitDialog.exampleTable.setHorizontalHeaderLabels(["1","4","8","10","16","20","62.5","100","200","250","400"])
        for item in self.model.rootItem.children:
            self.editLimitDialog.standardBox.addItem(item.name, item)
        self.editLimitDialog.standardBox.addItem(self.NEW_ITEM)
        self.setBoxItems(self.model.rootItem.child(0), 0, Box.CAT)
        self.updateExampleTable()
        self.editLimitDialog.standardBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.editLimitDialog.standardBox.currentData(), index, Box.CAT))
        self.editLimitDialog.categoryBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.editLimitDialog.categoryBox.currentData(), index, Box.HARDW))
        self.editLimitDialog.hardwareBox.currentIndexChanged.connect(lambda index: self.setBoxItems(self.editLimitDialog.hardwareBox.currentData(), index, Box.PARAM))
        self.editLimitDialog.parameterBox.currentTextChanged.connect(lambda text: self.setTextLimit(self.editLimitDialog.hardwareBox.currentData(), text))
        self.editLimitDialog.okButton.pressed.connect(lambda: self.saveLimit(True))
        self.editLimitDialog.cancelButton.pressed.connect(self.dialog.reject)
        self.editLimitDialog.saveButton.pressed.connect(lambda: self.saveLimit(False))
        self.editLimitDialog.delStandardButton.pressed.connect(lambda: self.deleteItem(Box.STAND))
        self.editLimitDialog.delCategoryButton.pressed.connect(lambda: self.deleteItem(Box.CAT))
        self.editLimitDialog.delHardwareButton.pressed.connect(lambda: self.deleteItem(Box.HARDW))
        self.editLimitDialog.addButton.pressed.connect(lambda: self.addLimit(self.editLimitDialog.limitsTable.selectedIndexes()))
        self.editLimitDialog.removeButton.pressed.connect(lambda: self.removeLimit(self.editLimitDialog.limitsTable.selectedIndexes()))


    def setBoxItems(self, parent, index, boxIndex):
        self.boxes[boxIndex].blockSignals(True)
        if not (self.boxes[boxIndex-1].currentText() == self.NEW_ITEM):
            self.setTextEdit(boxIndex-1)
            if boxIndex < len(self.boxes) - 1:
                self.boxes[boxIndex].clear()
                for item in parent.children:
                    self.boxes[boxIndex].addItem(item.name, item)
                self.boxes[boxIndex].addItem(self.NEW_ITEM)
                if parent.childCount() > 0:
                    self.setBoxItems(parent.child(0), 0, boxIndex + 1)
                else:
                    self.setBoxesToNew(boxIndex)
            elif boxIndex < len(self.boxes):
                self.boxes[Box.PARAM].setCurrentIndex(0)
                self.setTextLimit(parent, self.boxes[-1].currentText())
                self.updateExampleTable()

        else:
            self.setBoxesToNew(boxIndex-1)
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
            self.editLimitDialog.limitsTable.clearContents()
            self.editLimitDialog.limitsTable.setRowCount(1)
            self.editLimitDialog.limitsTable.setItem(0, 0, QtWidgets.QTableWidgetItem('-'))
            self.editLimitDialog.limitsTable.setItem(0, 1, QtWidgets.QTableWidgetItem('-'))
            self.editLimitDialog.limitsTable.setItem(0, 2, QtWidgets.QTableWidgetItem(''))


    def setTextEdit(self, boxIndex):
        self.lineEdits[boxIndex].setText(self.boxes[boxIndex].currentText())

    def setTextLimit(self, item, param):
        if item:
            if param in item.standard.limits:
                self.editLimitDialog.limitsTable.clearContents()
                self.editLimitDialog.limitsTable.setRowCount(len(item.standard.limits[param].clauses))
                for i, clause in enumerate(item.standard.limits[param].clauses):
                    minimum = item.standard.limits[param].bounds[i]
                    if minimum == float('-inf'):
                        minimum = "-"
                    maximum = item.standard.limits[param].bounds[i+1]
                    if maximum == float('inf'):
                        maximum = "-"
                    self.editLimitDialog.limitsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(minimum.__str__()))
                    self.editLimitDialog.limitsTable.setItem(i, 1, QtWidgets.QTableWidgetItem(maximum.__str__()))
                    self.editLimitDialog.limitsTable.setItem(i, 2, QtWidgets.QTableWidgetItem(clause))
                    self.editLimitDialog.limitsTable.resizeColumnToContents(2)
                self.updateExampleTable()

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
            limits = []
            bounds = []
            for x in range(0,self.editLimitDialog.limitsTable.rowCount()):
                limits.append(self.editLimitDialog.limitsTable.item(x, 2).text())
                if x == 0:
                    if self.editLimitDialog.limitsTable.item(x, 0).text() == '-':
                        bounds.append(float('-inf'))
                    else:
                        bounds.append(float(self.editLimitDialog.limitsTable.item(x, 0).text()))
                if self.editLimitDialog.limitsTable.item(x, 1).text() == '-':
                        bounds.append(float('inf'))
                else:
                    bounds.append(float(self.editLimitDialog.limitsTable.item(x, 1).text()))
            self.boxes[Box.HARDW].currentData().standard.limits[self.boxes[Box.PARAM].currentText()] = Limit(self.boxes[Box.PARAM].currentText(), limits, bounds)
            for box in self.boxes:
                box.blockSignals(False)
            self.model.endResetModel()
            self.updateExampleTable()
            if closeDialog:
                self.dialog.accept()
                self.model.writeModelToFile()

    def validateEdits(self):
        for i in range(3):
            if self.lineEdits[i].text() == "":
                error = QtWidgets.QErrorMessage(self.dialog)
                error.showMessage("Please fill the blanks.", "Empty_Blanks")
                error.exec_()
                return False
        return True

    def updateExampleTable(self):
        self.editLimitDialog.exampleTable.clearContents()
        limit = self.boxes[Box.HARDW].currentData().standard.limits[self.boxes[Box.PARAM].currentText()]
        for y in range(0, self.editLimitDialog.exampleTable.columnCount()):
            try:
                self.editLimitDialog.exampleTable.setItem(0, y, QtWidgets.QTableWidgetItem("{0:.2f}".format(limit.evaluate({'f': float(self.editLimitDialog.exampleTable.horizontalHeaderItem(y).text())}))))
            except:
                self.editLimitDialog.exampleTable.setItem(0, y, QtWidgets.QTableWidgetItem("{0}".format(limit.evaluate({'f': float(self.editLimitDialog.exampleTable.horizontalHeaderItem(y).text())}))))

    def deleteItem(self, buttonIndex):
        itemToDelete = self.boxes[buttonIndex].currentData()
        if itemToDelete:
            res = QtWidgets.QMessageBox.question(self.dialog, "Deletion", "Are you sure you want to delete "+itemToDelete.name+"?", QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if res == QtWidgets.QMessageBox.Yes:
                itemToDelete.parent.removeChild(itemToDelete)
                self.setBoxItems(itemToDelete.parent, 0, buttonIndex)

    def addLimit(self, rows):
        if len(rows) == 0:
            self.editLimitDialog.limitsTable.insertRow(self.editLimitDialog.limitsTable.rowCount())
        else:
            self.editLimitDialog.limitsTable.insertRow(rows[0].row())


    def removeLimit(self, rows):
        if len(rows) == 0:
            self.editLimitDialog.limitsTable.removeRow(self.editLimitDialog.limitsTable.rowCount()-1)
        else:
            for row in rows:
                self.editLimitDialog.limitsTable.removeRow(row.row())

    def showDialog(self):
        return self.dialog.exec_()