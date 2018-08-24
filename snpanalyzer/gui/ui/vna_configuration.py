# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/vna_configuration.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(400, 310)
        self.verticalLayout = QtWidgets.QVBoxLayout(form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.addressLabel = QtWidgets.QLabel(self.groupBox)
        self.addressLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.addressLabel.setObjectName("addressLabel")
        self.gridLayout.addWidget(self.addressLabel, 0, 0, 1, 1)
        self.addressLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.addressLineEdit.setObjectName("addressLineEdit")
        self.gridLayout.addWidget(self.addressLineEdit, 0, 1, 1, 1)
        self.bandwidthLabel = QtWidgets.QLabel(self.groupBox)
        self.bandwidthLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bandwidthLabel.setObjectName("bandwidthLabel")
        self.gridLayout.addWidget(self.bandwidthLabel, 1, 0, 1, 1)
        self.bandwidthInput = UnitInputWidget(self.groupBox)
        self.bandwidthInput.setObjectName("bandwidthInput")
        self.gridLayout.addWidget(self.bandwidthInput, 1, 1, 1, 1)
        self.startFreqLabel = QtWidgets.QLabel(self.groupBox)
        self.startFreqLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.startFreqLabel.setObjectName("startFreqLabel")
        self.gridLayout.addWidget(self.startFreqLabel, 2, 0, 1, 1)
        self.startFreqInput = UnitInputWidget(self.groupBox)
        self.startFreqInput.setObjectName("startFreqInput")
        self.gridLayout.addWidget(self.startFreqInput, 2, 1, 1, 1)
        self.stopFreqLabel = QtWidgets.QLabel(self.groupBox)
        self.stopFreqLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.stopFreqLabel.setObjectName("stopFreqLabel")
        self.gridLayout.addWidget(self.stopFreqLabel, 3, 0, 1, 1)
        self.stopFreqInput = UnitInputWidget(self.groupBox)
        self.stopFreqInput.setObjectName("stopFreqInput")
        self.gridLayout.addWidget(self.stopFreqInput, 3, 1, 1, 1)
        self.resolutionLabel = QtWidgets.QLabel(self.groupBox)
        self.resolutionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.resolutionLabel.setObjectName("resolutionLabel")
        self.gridLayout.addWidget(self.resolutionLabel, 4, 0, 1, 1)
        self.resolutionLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.resolutionLineEdit.setObjectName("resolutionLineEdit")
        self.gridLayout.addWidget(self.resolutionLineEdit, 4, 1, 1, 1)
        self.averageLabel = QtWidgets.QLabel(self.groupBox)
        self.averageLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.averageLabel.setObjectName("averageLabel")
        self.gridLayout.addWidget(self.averageLabel, 5, 0, 1, 1)
        self.averageLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.averageLineEdit.setObjectName("averageLineEdit")
        self.gridLayout.addWidget(self.averageLineEdit, 5, 1, 1, 1)
        self.portsLabel = QtWidgets.QLabel(self.groupBox)
        self.portsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.portsLabel.setObjectName("portsLabel")
        self.gridLayout.addWidget(self.portsLabel, 6, 0, 1, 1)
        self.portsLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.portsLineEdit.setObjectName("portsLineEdit")
        self.gridLayout.addWidget(self.portsLineEdit, 6, 1, 1, 1)
        self.timeoutLabel = QtWidgets.QLabel(self.groupBox)
        self.timeoutLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeoutLabel.setObjectName("timeoutLabel")
        self.gridLayout.addWidget(self.timeoutLabel, 7, 0, 1, 1)
        self.timeoutLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.timeoutLineEdit.setObjectName("timeoutLineEdit")
        self.gridLayout.addWidget(self.timeoutLineEdit, 7, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.groupBox.setTitle(_translate("form", "VNA Configuration"))
        self.addressLabel.setText(_translate("form", "Address"))
        self.bandwidthLabel.setText(_translate("form", "Bandwidth"))
        self.startFreqLabel.setText(_translate("form", "Start Frequency"))
        self.stopFreqLabel.setText(_translate("form", "Stop Frequency"))
        self.resolutionLabel.setText(_translate("form", "Resolution"))
        self.averageLabel.setText(_translate("form", "Number of Averages"))
        self.portsLabel.setText(_translate("form", "Number of Ports"))
        self.timeoutLabel.setText(_translate("form", "Timeout"))

from snpanalyzer.gui.widget.unitinput import UnitInputWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

