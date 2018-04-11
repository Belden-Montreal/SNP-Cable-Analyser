# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VNA_addr_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Addr_Dialog(object):
    def setupUi(self, Addr_Dialog):
        Addr_Dialog.setObjectName("Addr_Dialog")
        Addr_Dialog.resize(400, 194)
        self.buttonBox = QtWidgets.QDialogButtonBox(Addr_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Addr_Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 80, 361, 31))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(Addr_Dialog)
        self.label.setGeometry(QtCore.QRect(20, 50, 161, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Addr_Dialog)
        self.buttonBox.accepted.connect(Addr_Dialog.accept)
        self.buttonBox.rejected.connect(Addr_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Addr_Dialog)

    def retranslateUi(self, Addr_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Addr_Dialog.setWindowTitle(_translate("Addr_Dialog", "VNA Address"))
        self.label.setText(_translate("Addr_Dialog", "VNA Address:"))

