# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/export/parameter.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_form(object):
    def setupUi(self, form):
        form.setObjectName("form")
        form.resize(261, 342)
        self.verticalLayout = QtWidgets.QVBoxLayout(form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dataSeriesLabel = QtWidgets.QLabel(form)
        self.dataSeriesLabel.setObjectName("dataSeriesLabel")
        self.verticalLayout.addWidget(self.dataSeriesLabel)
        self.dataSeriesListView = QtWidgets.QListView(form)
        self.dataSeriesListView.setObjectName("dataSeriesListView")
        self.verticalLayout.addWidget(self.dataSeriesListView)
        self.scaleSelection = ScaleSelectionWidget(form)
        self.scaleSelection.setObjectName("scaleSelection")
        self.verticalLayout.addWidget(self.scaleSelection)
        self.formatSelection = FormatSelectionWidget(form)
        self.formatSelection.setObjectName("formatSelection")
        self.verticalLayout.addWidget(self.formatSelection)

        self.retranslateUi(form)
        QtCore.QMetaObject.connectSlotsByName(form)

    def retranslateUi(self, form):
        _translate = QtCore.QCoreApplication.translate
        form.setWindowTitle(_translate("form", "Form"))
        self.dataSeriesLabel.setText(_translate("form", "Data Series"))

from gui.widget.format import FormatSelectionWidget
from gui.widget.scale import ScaleSelectionWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = Ui_form()
    ui.setupUi(form)
    form.show()
    sys.exit(app.exec_())

