# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis\alienImportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlienImportDialog(object):
    def setupUi(self, AlienImportDialog):
        AlienImportDialog.setObjectName("AlienImportDialog")
        AlienImportDialog.resize(400, 298)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlienImportDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(AlienImportDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(19, 19, 361, 221))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.disturbersButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.disturbersButton.setObjectName("disturbersButton")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.disturbersButton)
        self.disturbersList = QtWidgets.QListWidget(self.formLayoutWidget)
        self.disturbersList.setObjectName("disturbersList")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.disturbersList)
        self.victimButton = QtWidgets.QPushButton(self.formLayoutWidget)
        self.victimButton.setObjectName("victimButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.victimButton)
        self.victimLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.victimLabel.setText("")
        self.victimLabel.setObjectName("victimLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.victimLabel)

        self.retranslateUi(AlienImportDialog)
        self.buttonBox.accepted.connect(AlienImportDialog.accept)
        self.buttonBox.rejected.connect(AlienImportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AlienImportDialog)

    def retranslateUi(self, AlienImportDialog):
        _translate = QtCore.QCoreApplication.translate
        AlienImportDialog.setWindowTitle(_translate("AlienImportDialog", "Import Alien SNPs"))
        self.disturbersButton.setText(_translate("AlienImportDialog", "Import Disturbers"))
        self.victimButton.setText(_translate("AlienImportDialog", "Import Victim"))

