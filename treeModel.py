from PyQt5 import QtCore
from treeItem import TreeItem

class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, parent = None):
        QtCore.QAbstractItemModel.__init__(self)
        self.rootItem = self.setupModelFromFile()

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
        file = open("limits.txt", "r")
        parents = []
        indentations = []
        for line in file:
            position = 0
            while position < len(line):
                if not line[position] == '\t':
                    break
                position += 1
            data = line[position:].strip().split('\t')
            if len(data) > 0:
                if len(parents) > 0:
                    if position > indentations[-1]:
                        if parents[-1].childCount() > 0:
                            parents.append(parents[-1].child(parents[-1].childCount()-1))
                            indentations.append(position)
                    else:
                        while position < indentations[-1] and len(parents) > 0:
                            parents.pop()
                            indentations.pop()
                    parents[-1].addChild(TreeItem(data, parents[-1]))
                else:
                    parents.append(TreeItem(data))
                    indentations.append(position)
        return parents[0]
