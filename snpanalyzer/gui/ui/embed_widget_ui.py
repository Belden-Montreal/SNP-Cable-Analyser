# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs\embedWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(858, 420)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.mainTab)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plugVerticalLayout = QtWidgets.QVBoxLayout()
        self.plugVerticalLayout.setObjectName("plugVerticalLayout")
        self.plugGroupBox = QtWidgets.QGroupBox(self.mainTab)
        self.plugGroupBox.setObjectName("plugGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.plugGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.importPlug = QtWidgets.QPushButton(self.plugGroupBox)
        self.importPlug.setObjectName("importPlug")
        self.verticalLayout.addWidget(self.importPlug)
        self.plugLabel = QtWidgets.QLabel(self.plugGroupBox)
        self.plugLabel.setText("")
        self.plugLabel.setObjectName("plugLabel")
        self.verticalLayout.addWidget(self.plugLabel)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.label = QtWidgets.QLabel(self.plugGroupBox)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.dnext12_36 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext12_36.setObjectName("dnext12_36")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.dnext12_36)
        self.label_3 = QtWidgets.QLabel(self.plugGroupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.dnext45_12 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext45_12.setObjectName("dnext45_12")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.dnext45_12)
        self.label_5 = QtWidgets.QLabel(self.plugGroupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.dnext12_78 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext12_78.setObjectName("dnext12_78")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dnext12_78)
        self.label_7 = QtWidgets.QLabel(self.plugGroupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.dnext45_36 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext45_36.setObjectName("dnext45_36")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.dnext45_36)
        self.label_9 = QtWidgets.QLabel(self.plugGroupBox)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.dnext36_78 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext36_78.setObjectName("dnext36_78")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.dnext36_78)
        self.label_11 = QtWidgets.QLabel(self.plugGroupBox)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.dnext45_78 = QtWidgets.QLabel(self.plugGroupBox)
        self.dnext45_78.setObjectName("dnext45_78")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.dnext45_78)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.plugVerticalLayout.addWidget(self.plugGroupBox)
        self.horizontalLayout.addLayout(self.plugVerticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.reverseLayoutBox = QtWidgets.QHBoxLayout()
        self.reverseLayoutBox.setObjectName("reverseLayoutBox")
        self.reverseCheckBox = QtWidgets.QCheckBox(self.mainTab)
        self.reverseCheckBox.setObjectName("reverseCheckBox")
        self.reverseLayoutBox.addWidget(self.reverseCheckBox)
        self.verticalLayout_2.addLayout(self.reverseLayoutBox)
        self.matedMeasurementsVerticalLayout = QtWidgets.QVBoxLayout()
        self.matedMeasurementsVerticalLayout.setObjectName("matedMeasurementsVerticalLayout")
        self.matedMeasurementsGroupBox = QtWidgets.QGroupBox(self.mainTab)
        self.matedMeasurementsGroupBox.setObjectName("matedMeasurementsGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.matedMeasurementsGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openLabel = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        self.openLabel.setEnabled(False)
        self.openLabel.setObjectName("openLabel")
        self.horizontalLayout_5.addWidget(self.openLabel)
        self.importOpen = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.importOpen.setEnabled(False)
        self.importOpen.setObjectName("importOpen")
        self.horizontalLayout_5.addWidget(self.importOpen)
        self.acquireOpen = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.acquireOpen.setEnabled(False)
        self.acquireOpen.setObjectName("acquireOpen")
        self.horizontalLayout_5.addWidget(self.acquireOpen)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.openFileName = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.openFileName.setFont(font)
        self.openFileName.setObjectName("openFileName")
        self.verticalLayout_4.addWidget(self.openFileName)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.shortLabel = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        self.shortLabel.setEnabled(False)
        self.shortLabel.setObjectName("shortLabel")
        self.horizontalLayout_6.addWidget(self.shortLabel)
        self.importShort = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.importShort.setEnabled(False)
        self.importShort.setObjectName("importShort")
        self.horizontalLayout_6.addWidget(self.importShort)
        self.acquireShort = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.acquireShort.setEnabled(False)
        self.acquireShort.setObjectName("acquireShort")
        self.horizontalLayout_6.addWidget(self.acquireShort)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.shortFileName = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.shortFileName.setFont(font)
        self.shortFileName.setObjectName("shortFileName")
        self.verticalLayout_4.addWidget(self.shortFileName)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.loadLabel = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        self.loadLabel.setObjectName("loadLabel")
        self.horizontalLayout_7.addWidget(self.loadLabel)
        self.importLoad = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.importLoad.setObjectName("importLoad")
        self.horizontalLayout_7.addWidget(self.importLoad)
        self.acquireLoad = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.acquireLoad.setObjectName("acquireLoad")
        self.horizontalLayout_7.addWidget(self.acquireLoad)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.loadFileName = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.loadFileName.setFont(font)
        self.loadFileName.setObjectName("loadFileName")
        self.verticalLayout_4.addWidget(self.loadFileName)
        self.matedMeasurementsVerticalLayout.addWidget(self.matedMeasurementsGroupBox)
        self.verticalLayout_2.addLayout(self.matedMeasurementsVerticalLayout)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.categoryLayout = QtWidgets.QVBoxLayout()
        self.categoryLayout.setObjectName("categoryLayout")
        self.categoryGroupBox = QtWidgets.QGroupBox(self.mainTab)
        self.categoryGroupBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.categoryGroupBox.setObjectName("categoryGroupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.categoryGroupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.embedCat5 = QtWidgets.QRadioButton(self.categoryGroupBox)
        self.embedCat5.setObjectName("embedCat5")
        self.gridLayout_3.addWidget(self.embedCat5, 2, 0, 1, 1)
        self.embedCat6 = QtWidgets.QRadioButton(self.categoryGroupBox)
        self.embedCat6.setChecked(True)
        self.embedCat6.setObjectName("embedCat6")
        self.gridLayout_3.addWidget(self.embedCat6, 1, 0, 1, 1)
        self.categoryLayout.addWidget(self.categoryGroupBox)
        self.verticalLayout_3.addLayout(self.categoryLayout)
        self.groupBox_3 = QtWidgets.QGroupBox(self.mainTab)
        self.groupBox_3.setMaximumSize(QtCore.QSize(200, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.shortingJack124578Label = QtWidgets.QLabel(self.groupBox_3)
        self.shortingJack124578Label.setObjectName("shortingJack124578Label")
        self.gridLayout.addWidget(self.shortingJack124578Label, 0, 0, 1, 1)
        self.SJ_124578_LineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.SJ_124578_LineEdit.setObjectName("SJ_124578_LineEdit")
        self.gridLayout.addWidget(self.SJ_124578_LineEdit, 0, 1, 1, 1)
        self.sJ36Label = QtWidgets.QLabel(self.groupBox_3)
        self.sJ36Label.setObjectName("sJ36Label")
        self.gridLayout.addWidget(self.sJ36Label, 1, 0, 1, 1)
        self.sJ36LineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.sJ36LineEdit.setObjectName("sJ36LineEdit")
        self.gridLayout.addWidget(self.sJ36LineEdit, 1, 1, 1, 1)
        self.thruCalibLabel = QtWidgets.QLabel(self.groupBox_3)
        self.thruCalibLabel.setObjectName("thruCalibLabel")
        self.gridLayout.addWidget(self.thruCalibLabel, 2, 0, 1, 1)
        self.thruCalibLineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.thruCalibLineEdit.setObjectName("thruCalibLineEdit")
        self.gridLayout.addWidget(self.thruCalibLineEdit, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.reembedButton = QtWidgets.QPushButton(self.mainTab)
        self.reembedButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.reembedButton.setObjectName("reembedButton")
        self.verticalLayout_3.addWidget(self.reembedButton)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.tabWidget.addTab(self.mainTab, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.plugGroupBox.setTitle(_translate("Form", "Plug"))
        self.importPlug.setText(_translate("Form", "Import Plug"))
        self.label.setText(_translate("Form", "DNEXT 12-36:"))
        self.dnext12_36.setText(_translate("Form", "\"\""))
        self.label_3.setText(_translate("Form", "DNEXT 45-12:"))
        self.dnext45_12.setText(_translate("Form", "\"\""))
        self.label_5.setText(_translate("Form", "DNEXT 12-78:"))
        self.dnext12_78.setText(_translate("Form", "\"\""))
        self.label_7.setText(_translate("Form", "DNEXT 45-36:"))
        self.dnext45_36.setText(_translate("Form", "\"\""))
        self.label_9.setText(_translate("Form", "DNEXT 36-78:"))
        self.dnext36_78.setText(_translate("Form", "\"\""))
        self.label_11.setText(_translate("Form", "DNEXT 45-78:"))
        self.dnext45_78.setText(_translate("Form", "\"\""))
        self.reverseCheckBox.setText(_translate("Form", "Reverse"))
        self.matedMeasurementsGroupBox.setTitle(_translate("Form", "Mated measurements"))
        self.openLabel.setText(_translate("Form", "Open:"))
        self.importOpen.setText(_translate("Form", "Import SNP"))
        self.acquireOpen.setText(_translate("Form", "Acquire"))
        self.openFileName.setText(_translate("Form", "\"\""))
        self.shortLabel.setText(_translate("Form", "Short:"))
        self.importShort.setText(_translate("Form", "Import SNP"))
        self.acquireShort.setText(_translate("Form", "Acquire"))
        self.shortFileName.setText(_translate("Form", "\"\""))
        self.loadLabel.setText(_translate("Form", "Load:"))
        self.importLoad.setText(_translate("Form", "Import SNP"))
        self.acquireLoad.setText(_translate("Form", "Acquire"))
        self.loadFileName.setText(_translate("Form", "\"\""))
        self.categoryGroupBox.setTitle(_translate("Form", "Category"))
        self.embedCat5.setText(_translate("Form", "Cat 5"))
        self.embedCat6.setText(_translate("Form", "Cat 6/6A"))
        self.groupBox_3.setTitle(_translate("Form", "Constants"))
        self.shortingJack124578Label.setText(_translate("Form", "SJ 12,45,78"))
        self.sJ36Label.setText(_translate("Form", "SJ 36"))
        self.thruCalibLabel.setText(_translate("Form", "Thru Calib"))
        self.reembedButton.setText(_translate("Form", "Reembed"))

