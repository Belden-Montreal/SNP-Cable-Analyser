# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/export/project.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(699, 355)
        self.gridLayout = QtWidgets.QGridLayout(form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.samplesLabel = QtWidgets.QLabel(form)
        self.samplesLabel.setObjectName("samplesLabel")
        self.gridLayout.addWidget(self.samplesLabel, 0, 0, 1, 1)
        self.sampleExportWidget = ExportSampleWidget(form)
        self.sampleExportWidget.setObjectName("sampleExportWidget")
        self.gridLayout.addWidget(self.sampleExportWidget, 0, 1, 2, 1)
        self.samplesListView = QtWidgets.QListView(form)
        self.samplesListView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.samplesListView.setObjectName("samplesListView")
        self.gridLayout.addWidget(self.samplesListView, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.samplesLabel.setText(_translate("form", "Samples"))

from gui.widget.export.sample import ExportSampleWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

