from app.component import Component
from app.component_tree_item import ComponentTreeItem

class Subproject(Component):

    def __init__(self, name):
        super(Subproject, self).__init__(name)
        self._components = list()
        self._treeItem = ComponentTreeItem(self)
        self._generateTreeStructure()

    def getComponents(self):
        return self._components

    def setComponents(self, components):
        self._components = components
        self._generateTreeStructure()
    
    def addComponent(self, component):
        self._components.append(component)
        self._generateTreeStructure()

    def _generateTreeStructure(self):
        self._treeItem.children = list()
        for component in self._components:
            self._treeItem.addChild(component.getTreeItem())