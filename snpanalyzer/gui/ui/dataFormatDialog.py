# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs\dataFormatDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DataFormatDialog(object):
    def setupUi(self, DataFormatDialog):
        DataFormatDialog.setObjectName("DataFormatDialog")
        DataFormatDialog.resize(400, 95)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DataFormatDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formatBox = QtWidgets.QComboBox(DataFormatDialog)
        self.formatBox.setObjectName("formatBox")
        self.verticalLayout.addWidget(self.formatBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(DataFormatDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(DataFormatDialog)
        self.buttonBox.accepted.connect(DataFormatDialog.accept)
        self.buttonBox.rejected.connect(DataFormatDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DataFormatDialog)

    def retranslateUi(self, DataFormatDialog):
        _translate = QtCore.QCoreApplication.translate
        DataFormatDialog.setWindowTitle(_translate("DataFormatDialog", "Change Data Format"))

