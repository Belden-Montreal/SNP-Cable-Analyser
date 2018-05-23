class TreeItem():
    def __init__(self, data, parent=None):
        self.parent = parent
        self._data = data
        self.children = []

    def addChild(self, item):
        self.children.append(item)
        item.parent = self

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    def columnCount(self):
        return len(self._data)

    def data(self, column):
        return self._data[column]