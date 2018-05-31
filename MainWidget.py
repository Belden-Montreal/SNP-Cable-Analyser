# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs\MainWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(1187, 323)
        self.formLayoutWidget = QtWidgets.QWidget(MainWidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1041, 301))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.testNameLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.testNameLabel.setFont(font)
        self.testNameLabel.setObjectName("testNameLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.testNameLabel)
        self.passLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.passLabel.setFont(font)
        self.passLabel.setObjectName("passLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.passLabel)
        self.parametersLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.parametersLabel.setFont(font)
        self.parametersLabel.setObjectName("parametersLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.parametersLabel)
        self.failsLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.failsLabel.setFont(font)
        self.failsLabel.setObjectName("failsLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.failsLabel)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.limitLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.limitLabel.setFont(font)
        self.limitLabel.setText("")
        self.limitLabel.setObjectName("limitLabel")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.limitLabel)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.dateLabel = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.dateLabel.setFont(font)
        self.dateLabel.setText("")
        self.dateLabel.setObjectName("dateLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dateLabel)

        self.retranslateUi(MainWidget)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        _translate = QtCore.QCoreApplication.translate
        MainWidget.setWindowTitle(_translate("MainWidget", "MainWidget"))
        self.testNameLabel.setText(_translate("MainWidget", "Test Name :"))
        self.passLabel.setText(_translate("MainWidget", "Pass"))
        self.parametersLabel.setText(_translate("MainWidget", "Failed Parameters :"))
        self.failsLabel.setText(_translate("MainWidget", "[ Param ]"))
        self.label.setText(_translate("MainWidget", "Limit :"))
        self.label_2.setText(_translate("MainWidget", "Date :"))

