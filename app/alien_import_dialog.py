# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs\alienImportDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AlienImportDialog(object):
    def setupUi(self, AlienImportDialog):
        AlienImportDialog.setObjectName("AlienImportDialog")
        AlienImportDialog.resize(400, 357)
        self.buttonBox = QtWidgets.QDialogButtonBox(AlienImportDialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 310, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(AlienImportDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(19, 19, 361, 281))
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
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.end1Button = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.end1Button.setChecked(True)
        self.end1Button.setAutoExclusive(False)
        self.end1Button.setObjectName("end1Button")
        self.gridLayout.addWidget(self.end1Button, 0, 0, 1, 1)
        self.end2Button = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.end2Button.setAutoExclusive(False)
        self.end2Button.setObjectName("end2Button")
        self.gridLayout.addWidget(self.end2Button, 1, 0, 1, 1)
        self.anextButton = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.anextButton.setChecked(True)
        self.anextButton.setAutoExclusive(False)
        self.anextButton.setObjectName("anextButton")
        self.gridLayout.addWidget(self.anextButton, 0, 1, 1, 1)
        self.afextButton = QtWidgets.QRadioButton(self.formLayoutWidget)
        self.afextButton.setAutoExclusive(True)
        self.afextButton.setObjectName("afextButton")
        self.gridLayout.addWidget(self.afextButton, 1, 1, 1, 1)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.SpanningRole, self.gridLayout)

        self.retranslateUi(AlienImportDialog)
        self.buttonBox.accepted.connect(AlienImportDialog.accept)
        self.buttonBox.rejected.connect(AlienImportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AlienImportDialog)

    def retranslateUi(self, AlienImportDialog):
        _translate = QtCore.QCoreApplication.translate
        AlienImportDialog.setWindowTitle(_translate("AlienImportDialog", "Import Alien SNPs"))
        self.disturbersButton.setText(_translate("AlienImportDialog", "Import Disturbers"))
        self.victimButton.setText(_translate("AlienImportDialog", "Import Victim"))
        self.end1Button.setText(_translate("AlienImportDialog", "End 1"))
        self.end2Button.setText(_translate("AlienImportDialog", "End 2"))
        self.anextButton.setText(_translate("AlienImportDialog", "ANEXT"))
        self.afextButton.setText(_translate("AlienImportDialog", "AFEXT"))

