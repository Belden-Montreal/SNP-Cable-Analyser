from limits.limitParameters import ParameterDict

class TreeItem():
    def __init__(self, name, parent=None, header=False):
        self.parent = parent
        self.name = name
        self.limits = ParameterDict(header)
        self.children = []

    def addChild(self, item):
        self.children.append(item)

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    def columnCount(self):
        return len(self.limits.dict) + 1

    def data(self, column):
        if column == 0:
            return self.name
        else:
            return list(self.limits.dict.values())[column-1].__str__()