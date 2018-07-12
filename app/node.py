
class Node(object):
    def __init__(self, name, parent=None):
        self.parent = parent
        if parent:
            parent.addChild(self)
        self._name = name
        self.children = []
        self._dataObject = None

    def addChild(self, item):
        self.children.append(item)
        item.parent = self

    def removeChild(self, item):
        self.children.remove(item)
        self.delete()

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    def columnCount(self):
        return 1

    def data(self, column):
        return self._name

    def getName(self):
        return self._name

    def getObject(self):
        return self._dataObject

    def delete(self):
        if self.childCount() == 0:
            self.parent.removeChild(self)