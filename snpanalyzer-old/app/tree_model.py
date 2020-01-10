from PyQt5 import QtGui, QtCore
from snpanalyzer.app.node import Node

class TreeModel(QtGui.QStandardItemModel):
    def __init__(self, parent = None):
        super(TreeModel, self).__init__()
        self.setHorizontalHeaderLabels(["name"])

    def getRootFromIndex(self, index):
        item = index
        while self.parent(item) != QtCore.QModelIndex():
            item = self.parent(item)
        return item