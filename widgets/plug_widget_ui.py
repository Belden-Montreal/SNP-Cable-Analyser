# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIs\plugWidget.ui'
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
        self.gridLayout_3 = QtWidgets.QGridLayout(self.mainTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.dfMeasurementsGroupBox = QtWidgets.QGroupBox(self.mainTab)
        self.dfMeasurementsGroupBox.setObjectName("dfMeasurementsGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dfMeasurementsGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.dfOpenLabel = QtWidgets.QLabel(self.dfMeasurementsGroupBox)
        self.dfOpenLabel.setObjectName("dfOpenLabel")
        self.horizontalLayout_3.addWidget(self.dfOpenLabel)
        self.dfOpenImport = QtWidgets.QPushButton(self.dfMeasurementsGroupBox)
        self.dfOpenImport.setObjectName("dfOpenImport")
        self.horizontalLayout_3.addWidget(self.dfOpenImport)
        self.dfOpenAcquire = QtWidgets.QPushButton(self.dfMeasurementsGroupBox)
        self.dfOpenAcquire.setObjectName("dfOpenAcquire")
        self.horizontalLayout_3.addWidget(self.dfOpenAcquire)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.dfOpenFileName = QtWidgets.QLabel(self.dfMeasurementsGroupBox)
        self.dfOpenFileName.setObjectName("dfOpenFileName")
        self.verticalLayout.addWidget(self.dfOpenFileName)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.dfShortLabel = QtWidgets.QLabel(self.dfMeasurementsGroupBox)
        self.dfShortLabel.setObjectName("dfShortLabel")
        self.horizontalLayout_4.addWidget(self.dfShortLabel)
        self.dfShortImport = QtWidgets.QPushButton(self.dfMeasurementsGroupBox)
        self.dfShortImport.setObjectName("dfShortImport")
        self.horizontalLayout_4.addWidget(self.dfShortImport)
        self.dfShortAcquire = QtWidgets.QPushButton(self.dfMeasurementsGroupBox)
        self.dfShortAcquire.setObjectName("dfShortAcquire")
        self.horizontalLayout_4.addWidget(self.dfShortAcquire)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.dfShortFileName = QtWidgets.QLabel(self.dfMeasurementsGroupBox)
        self.dfShortFileName.setObjectName("dfShortFileName")
        self.verticalLayout.addWidget(self.dfShortFileName)
        self.gridLayout_3.addWidget(self.dfMeasurementsGroupBox, 0, 0, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
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
        self.recalcButton = QtWidgets.QPushButton(self.mainTab)
        self.recalcButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.recalcButton.setObjectName("recalcButton")
        self.verticalLayout_3.addWidget(self.recalcButton)
        self.gridLayout_3.addLayout(self.verticalLayout_3, 0, 2, 1, 1)
        self.matedMeasurementsGroupBox = QtWidgets.QGroupBox(self.mainTab)
        self.matedMeasurementsGroupBox.setObjectName("matedMeasurementsGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.matedMeasurementsGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.openLabel = QtWidgets.QLabel(self.matedMeasurementsGroupBox)
        self.openLabel.setEnabled(True)
        self.openLabel.setObjectName("openLabel")
        self.horizontalLayout_5.addWidget(self.openLabel)
        self.importOpen = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.importOpen.setEnabled(True)
        self.importOpen.setObjectName("importOpen")
        self.horizontalLayout_5.addWidget(self.importOpen)
        self.acquireOpen = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.acquireOpen.setEnabled(True)
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
        self.shortLabel.setEnabled(True)
        self.shortLabel.setObjectName("shortLabel")
        self.horizontalLayout_6.addWidget(self.shortLabel)
        self.importShort = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.importShort.setEnabled(True)
        self.importShort.setObjectName("importShort")
        self.horizontalLayout_6.addWidget(self.importShort)
        self.acquireShort = QtWidgets.QPushButton(self.matedMeasurementsGroupBox)
        self.acquireShort.setEnabled(True)
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
        self.gridLayout_3.addWidget(self.matedMeasurementsGroupBox, 0, 1, 1, 1)
        self.tabWidget.addTab(self.mainTab, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.dfMeasurementsGroupBox.setTitle(_translate("Form", "Direct Fixture measurements"))
        self.dfOpenLabel.setText(_translate("Form", "Open:"))
        self.dfOpenImport.setText(_translate("Form", "Import SNP"))
        self.dfOpenAcquire.setText(_translate("Form", "Acquire"))
        self.dfOpenFileName.setText(_translate("Form", "\"\""))
        self.dfShortLabel.setText(_translate("Form", "Short:"))
        self.dfShortImport.setText(_translate("Form", "Import SNP"))
        self.dfShortAcquire.setText(_translate("Form", "Acquire"))
        self.dfShortFileName.setText(_translate("Form", "\"\""))
        self.groupBox_3.setTitle(_translate("Form", "Constants"))
        self.shortingJack124578Label.setText(_translate("Form", "SJ 12,45,78"))
        self.SJ_124578_LineEdit.setText(_translate("Form", "5e-12"))
        self.sJ36Label.setText(_translate("Form", "SJ 36"))
        self.sJ36LineEdit.setText(_translate("Form", "14e-12"))
        self.thruCalibLabel.setText(_translate("Form", "Thru Calib"))
        self.thruCalibLineEdit.setText(_translate("Form", "20e-12"))
        self.recalcButton.setText(_translate("Form", "Calculate"))
        self.matedMeasurementsGroupBox.setTitle(_translate("Form", "Direct Fixture + Plug measurements"))
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.mainTab), _translate("Form", "main"))

