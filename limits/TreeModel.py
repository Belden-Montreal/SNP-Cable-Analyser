from PyQt5 import QtCore
from limits.TreeItem import TreeItem
from limits.Limit import Limit
from limits.LimitParser import LimitParser
from collections import OrderedDict
import xmltodict

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, fileUrl = "limits/limits.xml", parent = None):
        QtCore.QAbstractItemModel.__init__(self)
        self.parser = LimitParser(fileUrl)
        self.setupModelFromFile()
        self.header = ["Standard", "RL", "IL", "PropagationDelay", "NEXT", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "ANEXT", "PSANEXT", "AFEXT", "PSAFEXT", "PSAACRF"]

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[section]

        return None

    def setupModelFromFile(self):
        self.rootItem = self.parser.parseFile()
                    
    def writeModelToFile(self):
        self.parser.writeToFile(self.rootItem)
