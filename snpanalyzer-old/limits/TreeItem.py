from snpanalyzer.limits.Standard import Standard

class TreeItem():
    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        current = parent
        standardName = name
        while current and not(current.name == "Standard"):
            standardName = current.name+"|"+standardName
            current = current.parent
        self.standard = Standard(standardName)
        self.children = []

    def addChild(self, item):
        self.children.append(item)

    def removeChild(self, item):
        self.children.remove(item)

    def child(self, row):
        return self.children[row]

    def childCount(self):
        return len(self.children)

    def row(self):
        if self.parent:
            return self.parent.children.index(self)
        return 0
    
    def columnCount(self):
        return len(self.standard.limits) + 1

    def data(self, column):
        if column == 0:
            return self.name
        elif self.standard.limit(column-1).__str__() == "" and not len(self.children):
            return "-"
        else:
            return self.standard.limit(column-1).__str__()