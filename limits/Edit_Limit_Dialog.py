# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditLimitGui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(542, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 0, 5, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.categoryBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.categoryBox.setObjectName("categoryBox")
        self.gridLayout.addWidget(self.categoryBox, 1, 0, 1, 1)
        self.standardBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.standardBox.setObjectName("standardBox")
        self.gridLayout.addWidget(self.standardBox, 0, 0, 1, 1)
        self.hardwareBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.hardwareBox.setObjectName("hardwareBox")
        self.gridLayout.addWidget(self.hardwareBox, 2, 0, 1, 1)
        self.parameterBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.parameterBox.setObjectName("parameterBox")
        self.gridLayout.addWidget(self.parameterBox, 3, 0, 1, 1)
        self.parameterEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.parameterEdit.setObjectName("parameterEdit")
        self.gridLayout.addWidget(self.parameterEdit, 3, 1, 1, 1)
        self.standardEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.standardEdit.setObjectName("standardEdit")
        self.gridLayout.addWidget(self.standardEdit, 0, 1, 1, 1)
        self.categoryEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.categoryEdit.setObjectName("categoryEdit")
        self.gridLayout.addWidget(self.categoryEdit, 1, 1, 1, 1)
        self.hardwareEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.hardwareEdit.setObjectName("hardwareEdit")
        self.gridLayout.addWidget(self.hardwareEdit, 2, 1, 1, 1)
        self.gridLayout.setColumnMinimumWidth(0, 100)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(15, 260, 511, 23))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Limits"))

