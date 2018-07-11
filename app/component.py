
class Component(object):

    def __init__(self, name):
        self._name = name
        self._date = ""
        self._treeItem = None

    def _generateTreeStructure(self):
        raise NotImplementedError

    def recreateTreeStructure(self):
        raise NotImplementedError

    def showData(self):
        raise NotImplementedError

    def getName(self):
        return self._name

    def getDate(self):
        return self._date

    def getTreeItem(self):
        return self._treeItem