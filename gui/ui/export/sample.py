# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/export/sample.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(566, 307)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.parametersLabel = QtWidgets.QLabel(form)
        self.parametersLabel.setObjectName("parametersLabel")
        self.gridLayout.addWidget(self.parametersLabel, 0, 0, 1, 1)
        self.parametersListView = QtWidgets.QListView(form)
        self.parametersListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.parametersListView.setObjectName("parametersListView")
        self.gridLayout.addWidget(self.parametersListView, 1, 0, 1, 1)
        self.parameterExportWidget = ExportParameterWidget(form)
        self.parameterExportWidget.setObjectName("parameterExportWidget")
        self.gridLayout.addWidget(self.parameterExportWidget, 0, 1, 2, 1)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.parametersLabel.setText(_translate("form", "Parameters"))

from gui.widget.export.parameter import ExportParameterWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

