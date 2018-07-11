
class ProjectTreeItem():
    def __init__(self, project, parent=None):
        self.parent = parent
        if parent:
            parent.addChild(self)
        self._project = project
        self.children = []

    def addChild(self, item):
        self.children.append(item)
        item.parent = self

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
        return 2

    def data(self, column):
        if column == 0:
            return self._project.getName()
        else:
            try:
                return self._project.getDate()
            except:
                return ""

    def getProject(self):
        return self._project