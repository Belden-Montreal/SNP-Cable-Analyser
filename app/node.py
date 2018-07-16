from PyQt5 import QtGui, QtCore

class Node(QtGui.QStandardItem):
    def __init__(self, name):
        super(Node, self).__init__(name)
        self._dataObject = None
        self.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)

    def removeRow(self, row):
        super(Node, self).removeRow(row)
        self.delete()

    def getObject(self):
        return self._dataObject

    def delete(self):
        if self.rowCount() == 0:
            self.parent().removeRow(self.row())

    def hasChild(self, text):
        for i in range(self.rowCount()):
            child = self.child(i)
            if text == child.text():
                return child
        return 0

    def getWidgets(self):
        return dict()