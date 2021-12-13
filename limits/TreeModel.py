from PyQt5 import QtCore
from limits.TreeItem import TreeItem
from limits.Limit import Limit
from limits.LimitParser import LimitParser
from collections import OrderedDict
import xmltodict

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, fileUrl = "limits/limits.xml", parent = None, type=None):
        QtCore.QAbstractItemModel.__init__(self)
        if type == "Embedding":
            self.header = ["Standard", "Mat. Next", "Mat. Next 1,4", "TPMag 45-36 L", "TPMag 45-36 H", "TPMag 12-36 L", "TPMag 12-36 H", "TPMag 36-78 L", "TPMag 36-78 H", "TPMag 36-78 L", "TPMag 36-78 L", "TPMag 45-12 L", "TPMag 45-12 H", "TPMag 45-78 L", "TPMag 45-78 H", "TPMag 12-78 L", "TPMag 12-78 H", "TPPhase 45-36 L", "TPPhase 45-36 H", "TPPhase 12-36 L", "TPPhase 12-36 H", "TPPhase 36-78 L", "TPPhase 36-78 H", "TPPhase 36-78 L", "TPPhase 36-78 L", "TPPhase 45-12 L", "TPPhase 45-12 H", "TPPhase 45-78 L", "TPPhase 45-78 H", "TPPhase 12-78 L", "TPPhase 12-78 H" ] 
            fileUrl = "limits/limits_embedding.xml"
        else:
            self.header = ["Standard", "RL", "IL", "PropagationDelay", "NEXT", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL", "ANEXT", "PSANEXT", "AVGPSANEXT", "AFEXT", "PSAFEXT", "PSAACRF", "AVGPSAACRF"]
            fileUrl = fileUrl
        self.parser = LimitParser(fileUrl, type=type)
        self.setupModelFromFile()

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
