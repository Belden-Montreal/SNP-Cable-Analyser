# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vna_test.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets




class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(852, 389)
        self.port = None
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sampleConfigVerticalLayout = QtWidgets.QVBoxLayout()
        self.sampleConfigVerticalLayout.setObjectName("sampleConfigVerticalLayout")
        self.groupBox = QtWidgets.QGroupBox(dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.portsLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.portsLineEdit.setObjectName("portsLineEdit")
        self.gridLayout_2.addWidget(self.portsLineEdit, 2, 1, 1, 1)
        self.nameLabel = QtWidgets.QLabel(self.groupBox)
        self.nameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.gridLayout_2.addWidget(self.nameLabel, 0, 0, 1, 1)
        self.limitLabel = QtWidgets.QLabel(self.groupBox)
        self.limitLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.limitLabel.setObjectName("limitLabel")
        self.gridLayout_2.addWidget(self.limitLabel, 3, 0, 1, 1)
        self.limitLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.limitLineEdit.setObjectName("limitLineEdit")
        self.gridLayout_2.addWidget(self.limitLineEdit, 3, 1, 1, 1)
        self.nameLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.gridLayout_2.addWidget(self.nameLineEdit, 0, 1, 1, 1)
        self.portsLabel = QtWidgets.QLabel(self.groupBox)
        self.portsLabel.setObjectName("portsLabel")
        self.gridLayout_2.addWidget(self.portsLabel, 2, 0, 1, 1)
        self.sampleConfigVerticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 210, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.sampleConfigVerticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.sampleConfigVerticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.vna = VNAConfigurationWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vna.sizePolicy().hasHeightForWidth())
        self.vna.setSizePolicy(sizePolicy)
        self.vna.setObjectName("vna")
        self.horizontalLayout.addWidget(self.vna)
        self.horizontalLayout.setStretch(2, 3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.groupBox.setTitle(_translate("dialog", "Sample Configuration"))
        self.nameLabel.setText(_translate("dialog", "Name"))
        self.limitLabel.setText(_translate("dialog", "Limit"))
        self.portsLabel.setText(_translate("dialog", "Number of Ports"))

    def setPort(self,port):
        self.port = port

from snpanalyzer.gui.widget.vna_configuration import VNAConfigurationWidget
