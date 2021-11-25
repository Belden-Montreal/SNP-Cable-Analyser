#from settings import Settings

from UI import CompilationConfiguration_2 as CC


from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLineEdit, QMessageBox, QTableWidgetItem, QFileDialog, QCheckBox
from PyQt5.Qt import Qt

from anytree import AnyNode, RenderTree, PreOrderIter
import sys


class ReportConfig:

    def __init__(self, configTree):
        
        self.config = configTree

        self.dialog = QtWidgets.QDialog()
        self.configDialog = CC.Ui_ConfigDialog()
        self.configDialog.setupUi(self.dialog)
        
        self.configDialog.selectFileButton.clicked.connect(self.showState)
        self.configDialog.accept.clicked.connect(self.getNewConfig)
        self.configDialog.reject.clicked.connect(self.cancel)

        self.displayTree()
        self.dialog.exec_()

    def displayTree(self):
        tree    = self.configDialog.dataTree
        samples = PreOrderIter(self.config, maxlevel=2)
        next(samples) #skip root
        for sample in samples:
            s = QtWidgets.QTreeWidgetItem(tree) 
            s.setText(0, sample.name)
            s.setFlags(s.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            s.setCheckState(0, Qt.Checked)

            s.setData(0, Qt.UserRole, sample)   #Set the tree node data to QT Node
            params = PreOrderIter(sample, maxlevel=2)
            next(params) #skip sample
            for param in params:
                p = QtWidgets.QTreeWidgetItem(s)
                p.setFlags(p.flags() | Qt.ItemIsUserCheckable)
                p.setText(0, param.name)
                p.setCheckState(0, Qt.Checked)
                p.setData(0, Qt.UserRole, param)   #Set the tree node data to QT Node

            
        tree.itemClicked.connect(self.updateConfig)   
        tree.itemChanged.connect(self.updateConfig)            
         
        tree.show()
         
    def getNewConfig(self):
        self.dialog.close()
        return self.config


    def updateConfig(self, item, column):
        #print(item.text(column), column)
        #print(item.data(0, Qt.UserRole) )
        try:
            node = item.data(column, Qt.UserRole) 
            node.selected = True
            if item.checkState(0) == Qt.Unchecked:
                node.selected = False
            
            print(node.name, node.selected)
        except:
            pass
    
    
    def showState(self):
        print("HERE")
        print(self.config.children)

    def cancel(self):
        self.dialog.close()
