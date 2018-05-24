# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SetLimitGui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LimitDialog(object):
    def setupUi(self, LimitDialog):
        LimitDialog.setObjectName("LimitDialog")
        LimitDialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(LimitDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.treeView = QtWidgets.QTreeView(LimitDialog)
        self.treeView.setGeometry(QtCore.QRect(10, 10, 381, 221))
        self.treeView.setObjectName("treeView")

        self.retranslateUi(LimitDialog)
        self.buttonBox.accepted.connect(LimitDialog.accept)
        self.buttonBox.rejected.connect(LimitDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LimitDialog)

    def retranslateUi(self, LimitDialog):
        _translate = QtCore.QCoreApplication.translate
        LimitDialog.setWindowTitle(_translate("LimitDialog", "Set Limit"))

