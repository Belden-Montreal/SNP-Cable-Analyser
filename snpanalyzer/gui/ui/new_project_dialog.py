# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis\NewProjectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewProjectDialog(object):
    def setupUi(self, NewProjectDialog):
        NewProjectDialog.setObjectName("NewProjectDialog")
        NewProjectDialog.resize(400, 136)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewProjectDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 100, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayoutWidget = QtWidgets.QWidget(NewProjectDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 20, 331, 71))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setObjectName("formLayout")
        self.nameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        self.nameLabel.setObjectName("nameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.nameLabel)
        self.nameEdit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.nameEdit.setObjectName("nameEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.nameEdit)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.typeBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.typeBox.setObjectName("typeBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.typeBox)

        self.retranslateUi(NewProjectDialog)
        self.buttonBox.accepted.connect(NewProjectDialog.accept)
        self.buttonBox.rejected.connect(NewProjectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewProjectDialog)

    def retranslateUi(self, NewProjectDialog):
        _translate = QtCore.QCoreApplication.translate
        NewProjectDialog.setWindowTitle(_translate("NewProjectDialog", "New Project"))
        self.nameLabel.setText(_translate("NewProjectDialog", "Project Name : "))
        self.label.setText(_translate("NewProjectDialog", "Project Type : "))

