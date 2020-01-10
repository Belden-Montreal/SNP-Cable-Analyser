# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/format.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(248, 135)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.realRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.realRadioButton.setObjectName("realRadioButton")
        self.gridLayout_2.addWidget(self.realRadioButton, 1, 0, 1, 1)
        self.magnitudeRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.magnitudeRadioButton.setObjectName("magnitudeRadioButton")
        self.gridLayout_2.addWidget(self.magnitudeRadioButton, 0, 0, 1, 1)
        self.delayRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.delayRadioButton.setObjectName("delayRadioButton")
        self.gridLayout_2.addWidget(self.delayRadioButton, 2, 0, 1, 1)
        # self.phaseRadioButton = QtWidgets.QRadioButton(self.groupBox)
        # self.phaseRadioButton.setObjectName("phaseRadioButton")
        # self.gridLayout_2.addWidget(self.phaseRadioButton, 0, 1, 1, 1)
        # self.imaginaryRadioButton = QtWidgets.QRadioButton(self.groupBox)
        # self.imaginaryRadioButton.setObjectName("imaginaryRadioButton")
        # self.gridLayout_2.addWidget(self.imaginaryRadioButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.groupBox.setTitle(_translate("form", "Format"))
        self.realRadioButton.setText(_translate("form", "Real/Imaginary"))
        self.magnitudeRadioButton.setText(_translate("form", "Magnitude/Phase"))
        self.delayRadioButton.setText(_translate("form", "Delay"))
        # self.phaseRadioButton.setText(_translate("form", "Phase"))
        # self.imaginaryRadioButton.setText(_translate("form", "Imaginary"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

