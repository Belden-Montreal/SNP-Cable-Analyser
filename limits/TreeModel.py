from PyQt5 import QtCore
from limits.TreeItem import TreeItem
from limits.Limit import Limit
import xmltodict

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self)
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
            return self.rootItem.data(section)

        return None

    def setupModelFromFile(self):
        file = open("limits/limits.xml", "r")
        data = xmltodict.parse(file.read())
        self.rootItem = TreeItem(data["Root"]["@name"], None, True)
        self.parseProperty("Standard", self.rootItem, data["Root"])

    def parseProperty(self, name, parent, data):
        if not isinstance(data[name], list):
            properties = [data[name]]
        else:
            properties = data[name]
        for prop in properties:
            if "@name" in prop:
                item = TreeItem(prop["@name"], parent)
                parent.addChild(item)
                for nextName in prop:
                    if not nextName == "@name":
                        self.parseProperty(nextName, item, prop)
            else:
                parent.limits.dict[prop["@param"]] = Limit(prop["@param"], prop["@function"])
                

