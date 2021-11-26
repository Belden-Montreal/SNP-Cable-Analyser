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
            if sample.selected:
                s.setCheckState(0, Qt.Checked)

            s.setData(0, Qt.UserRole, sample)   #Set the tree node data to QT Node
            params = PreOrderIter(sample, maxlevel=2)
            next(params) #skip sample
            for param in params:
                p = QtWidgets.QTreeWidgetItem(s)
                p.setFlags(p.flags()| Qt.ItemIsTristate  | Qt.ItemIsUserCheckable)
                p.setText(0, param.name)

                if param.selected:
                    p.setCheckState(0, Qt.Checked)
                if param.hasComplex:
                    if param.complex:
                        p.setText(1, "Re/Im")
                    else:
                        p.setText(1, "Mag")


                    p.setData(1, Qt.UserRole, param)   #Set the tree node data to QT Node

                p.setData(0, Qt.UserRole, param)   #Set the tree node data to QT Node
                
                series = PreOrderIter(param, maxlevel=2)
                next(series) #skip param
                for ser in series:
                    l = QtWidgets.QTreeWidgetItem(p)
                    l.setFlags(l.flags() | Qt.ItemIsUserCheckable)
                    l.setText(0, ser.name)
                    if ser.selected:
                        l.setCheckState(0, Qt.Checked)
                    l.setData(0, Qt.UserRole, ser)   #Set the tree node data to QT Node
            
        tree.itemClicked.connect(self.updateConfig)   
        tree.itemChanged.connect(self.updateConfig)            
         
        tree.show()
         
    def getNewConfig(self):
        print("NEW CONFIG !")
        self.dialog.close()
        return self.config


    def updateConfig(self, item, column):
        print(item.text(column), column, type(column))
        tree    = self.configDialog.dataTree
        #print(item.data(0, Qt.UserRole) )
        try:
            node = item.data(column, Qt.UserRole) 
            node.selected = True

            if item.checkState(0) == Qt.Unchecked:
                node.selected = False
            if column == 1:
                tree.blockSignals( True )
                node.complex ^= 1
                if node.complex:
                    item.setText(1,"Re/Im")
                else:
                    item.setText(1,"Mag")
                tree.blockSignals( False )

            print("complex : ", node.complex)

        
            
            #print(node.name, node.selected)
        except:
            pass
    
    
    def showState(self):
        print("HERE")
        print(self.config.children)

    def cancel(self):
        self.dialog.close()
