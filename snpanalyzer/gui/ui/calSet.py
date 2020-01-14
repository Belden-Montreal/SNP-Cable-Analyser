# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\LXF09011\Desktop\SNP-Cable-Analyser\snpanalyzer\gui\ui\cal_set.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CalDialog(object):
    def setupUi(self, CalDialog):
        CalDialog.setObjectName("CalDialog")
        CalDialog.resize(600, 400)
        CalDialog.setMinimumSize(QtCore.QSize(600, 400))
        CalDialog.setAutoFillBackground(False)
        CalDialog.setSizeGripEnabled(False)
        CalDialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(CalDialog)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.connectStatus = QtWidgets.QGroupBox(CalDialog)
        self.connectStatus.setObjectName("connectStatus")
        self.gridLayout = QtWidgets.QGridLayout(self.connectStatus)
        self.gridLayout.setObjectName("gridLayout")
        self.vnaAddress = QtWidgets.QLineEdit(self.connectStatus)
        self.vnaAddress.setMinimumSize(QtCore.QSize(400, 0))
        self.vnaAddress.setObjectName("vnaAddress")
        self.gridLayout.addWidget(self.vnaAddress, 0, 0, 1, 1)
        self.statusLabel = QtWidgets.QLabel(self.connectStatus)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 1, 0, 1, 1)
        self.connect = QtWidgets.QCommandLinkButton(self.connectStatus)
        self.connect.setObjectName("connect")
        self.gridLayout.addWidget(self.connect, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.connectStatus)
        self.groupBox_2 = QtWidgets.QGroupBox(CalDialog)
        self.groupBox_2.setEnabled(False)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.typeBox = QtWidgets.QComboBox(self.groupBox_2)
        self.typeBox.setObjectName("typeBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.typeBox)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.buttonCal = QtWidgets.QPushButton(self.groupBox_2)
        self.buttonCal.setObjectName("buttonCal")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.buttonCal)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(CalDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CalDialog)
        self.buttonBox.accepted.connect(CalDialog.accept)
        self.buttonBox.rejected.connect(CalDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CalDialog)

    def retranslateUi(self, CalDialog):
        _translate = QtCore.QCoreApplication.translate
        CalDialog.setWindowTitle(_translate("CalDialog", "Connect to VNA"))
        self.connectStatus.setTitle(_translate("CalDialog", "Set VNA Adress"))
        self.statusLabel.setText(_translate("CalDialog", "Status"))
        self.connect.setText(_translate("CalDialog", "Try connecting"))
        self.groupBox_2.setTitle(_translate("CalDialog", "Chose the calibration setting"))
        self.label.setText(_translate("CalDialog", "CalSet"))
        self.label_2.setText(_translate("CalDialog", "Or"))
        self.label_3.setText(_translate("CalDialog", "Set a new Calibration"))
        self.buttonCal.setText(_translate("CalDialog", "New CalSet"))

