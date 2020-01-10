# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis\NewProjectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!
import datetime

import dateutil
from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_CalDialog(object):
    def setupUi(self, NewCalDialog):
        NewCalDialog.setObjectName("NewCalDialog")
        NewCalDialog.resize(400, 310)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewCalDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 120, 341, 310))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vLayoutWidget = QtWidgets.QWidget(NewCalDialog)
        self.vLayoutWidget.setGeometry(QtCore.QRect(30, 25, 331, 200))
        self.vLayoutWidget.setObjectName("vLayoutWidget")
        self.VLayout = QtWidgets.QVBoxLayout(self.vLayoutWidget)
        self.HLayout = QtWidgets.QHBoxLayout(self.vLayoutWidget)
        self.VLayout.setContentsMargins(0, 0, 0, 0)
        self.VLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(self.vLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.VLayout.addWidget(self.nameLabel)
        self.label = QtWidgets.QLabel(self.vLayoutWidget)
        self.label.setObjectName("label")
        self.HLayout.addWidget(self.label)
        self.typeBox = QtWidgets.QComboBox(self.vLayoutWidget)
        self.typeBox.setObjectName("typeBox")
        self.HLayout.addWidget(self.typeBox)
        self.VLayout.addLayout(self.HLayout)
        self.orLabel = QtWidgets.QLabel(self.vLayoutWidget)
        self.newCalLabel = QtWidgets.QLabel(self.vLayoutWidget)
        self.buttonCal = QtWidgets.QPushButton(self.vLayoutWidget)
        self.VLayout.addWidget(self.orLabel)
        self.VLayout.addWidget(self.newCalLabel)
        self.VLayout.addWidget(self.buttonCal)
        self.retranslateUi(NewCalDialog)

        self.buttonBox.rejected.connect(NewCalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewCalDialog)
    def retranslateUi(self, NewCalDialog):
        _translate = QtCore.QCoreApplication.translate
        NewCalDialog.setWindowTitle(_translate("NewCalDialog", "CalSet"))
        self.nameLabel.setText(_translate("NewCalDialog", "Choose the Calibration setting"))
        self.label.setText(_translate("NewCalDialog", "CalSet: "))
        self.orLabel.setText(_translate("NewCalDialog", "OR"))
        self.newCalLabel.setText(_translate("NewCalDialog","Set a new calibration"))
        self.buttonCal.setText(_translate("NewCalDialog"," New CalSet "))

