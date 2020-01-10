# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/unitinput.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(400, 106)
        form.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.horizontalLayout = QtWidgets.QHBoxLayout(form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.valueLineEdit = QtWidgets.QLineEdit(form)
        self.valueLineEdit.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.valueLineEdit.setText("")
        self.valueLineEdit.setObjectName("valueLineEdit")
        self.horizontalLayout.addWidget(self.valueLineEdit)
        self.unitComboBox = QtWidgets.QComboBox(form)
        self.unitComboBox.setObjectName("unitComboBox")
        self.horizontalLayout.addWidget(self.unitComboBox)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

