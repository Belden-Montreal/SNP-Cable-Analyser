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
        Dialog.resize(541, 300)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 521, 241))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(5, 0, 5, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.hardwareEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.hardwareEdit.setObjectName("hardwareEdit")
        self.gridLayout.addWidget(self.hardwareEdit, 2, 1, 1, 1)
        self.categoryEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.categoryEdit.setObjectName("categoryEdit")
        self.gridLayout.addWidget(self.categoryEdit, 1, 1, 1, 1)
        self.standardEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.standardEdit.setObjectName("standardEdit")
        self.gridLayout.addWidget(self.standardEdit, 0, 1, 1, 1)
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
        self.delStandardButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.delStandardButton.setObjectName("delStandardButton")
        self.gridLayout.addWidget(self.delStandardButton, 0, 2, 1, 1)
        self.delCategoryButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.delCategoryButton.setObjectName("delCategoryButton")
        self.gridLayout.addWidget(self.delCategoryButton, 1, 2, 1, 1)
        self.delHardwareButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.delHardwareButton.setObjectName("delHardwareButton")
        self.gridLayout.addWidget(self.delHardwareButton, 2, 2, 1, 1)
        self.parameterEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.parameterEdit.setObjectName("parameterEdit")
        self.gridLayout.addWidget(self.parameterEdit, 3, 1, 1, 2)
        self.gridLayout.setColumnMinimumWidth(0, 100)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(280, 260, 251, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.saveButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout.addWidget(self.saveButton)
        self.okButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.okButton.setObjectName("okButton")
        self.horizontalLayout.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout.addWidget(self.cancelButton)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit Limits"))
        self.delStandardButton.setText(_translate("Dialog", "Delete"))
        self.delCategoryButton.setText(_translate("Dialog", "Delete"))
        self.delHardwareButton.setText(_translate("Dialog", "Delete"))
        self.saveButton.setText(_translate("Dialog", "Save"))
        self.okButton.setText(_translate("Dialog", "Ok"))
        self.cancelButton.setText(_translate("Dialog", "Cancel"))

