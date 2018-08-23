# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/scale.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(240, 63)
        self.verticalLayout = QtWidgets.QVBoxLayout(form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.linearRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.linearRadioButton.setObjectName("linearRadioButton")
        self.gridLayout.addWidget(self.linearRadioButton, 0, 0, 1, 1)
        self.logarithmicRadioButton = QtWidgets.QRadioButton(self.groupBox)
        self.logarithmicRadioButton.setObjectName("logarithmicRadioButton")
        self.gridLayout.addWidget(self.logarithmicRadioButton, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.groupBox.setTitle(_translate("form", "Scale"))
        self.linearRadioButton.setText(_translate("form", "Linear"))
        self.logarithmicRadioButton.setText(_translate("form", "Logarithmic"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

