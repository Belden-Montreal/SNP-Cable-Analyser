# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/compilation_configuration.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(1311, 732)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.presetsWidget = PresetsWidget(dialog)
        self.presetsWidget.setObjectName("presetsWidget")
        self.verticalLayout.addWidget(self.presetsWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.mainGridLayout = QtWidgets.QGridLayout()
        self.mainGridLayout.setObjectName("mainGridLayout")
        self.parameterLabel = QtWidgets.QLabel(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterLabel.sizePolicy().hasHeightForWidth())
        self.parameterLabel.setSizePolicy(sizePolicy)
        self.parameterLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.parameterLabel.setObjectName("parameterLabel")
        self.mainGridLayout.addWidget(self.parameterLabel, 4, 0, 1, 1)
        self.samplesListView = QtWidgets.QListView(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samplesListView.sizePolicy().hasHeightForWidth())
        self.samplesListView.setSizePolicy(sizePolicy)
        self.samplesListView.setMinimumSize(QtCore.QSize(30, 0))
        self.samplesListView.setBaseSize(QtCore.QSize(30, 0))
        self.samplesListView.setObjectName("samplesListView")
        self.mainGridLayout.addWidget(self.samplesListView, 11, 0, 1, 1)
        self.dataseriesListView = QtWidgets.QListView(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataseriesListView.sizePolicy().hasHeightForWidth())
        self.dataseriesListView.setSizePolicy(sizePolicy)
        self.dataseriesListView.setMinimumSize(QtCore.QSize(30, 0))
        self.dataseriesListView.setBaseSize(QtCore.QSize(30, 0))
        self.dataseriesListView.setObjectName("dataseriesListView")
        self.mainGridLayout.addWidget(self.dataseriesListView, 8, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGridLayout.addItem(spacerItem1, 12, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGridLayout.addItem(spacerItem2, 9, 0, 1, 1)
        self.samplesLabel = QtWidgets.QLabel(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.samplesLabel.sizePolicy().hasHeightForWidth())
        self.samplesLabel.setSizePolicy(sizePolicy)
        self.samplesLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.samplesLabel.setObjectName("samplesLabel")
        self.mainGridLayout.addWidget(self.samplesLabel, 10, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.formatSelection = FormatSelectionWidget(dialog)
        self.formatSelection.setObjectName("formatSelection")
        self.mainGridLayout.addWidget(self.formatSelection, 13, 0, 1, 1)
        self.parameterComboBox = QtWidgets.QComboBox(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.parameterComboBox.sizePolicy().hasHeightForWidth())
        self.parameterComboBox.setSizePolicy(sizePolicy)
        self.parameterComboBox.setMinimumSize(QtCore.QSize(30, 0))
        self.parameterComboBox.setBaseSize(QtCore.QSize(30, 0))
        self.parameterComboBox.setObjectName("parameterComboBox")
        self.mainGridLayout.addWidget(self.parameterComboBox, 5, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGridLayout.addItem(spacerItem4, 6, 0, 1, 1)
        self.titleLabel = QtWidgets.QLabel(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.titleLabel.setObjectName("titleLabel")
        self.mainGridLayout.addWidget(self.titleLabel, 1, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.mainGridLayout.addItem(spacerItem5, 14, 0, 1, 1)
        self.graphicVerticalLayout = QtWidgets.QVBoxLayout()
        self.graphicVerticalLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.graphicVerticalLayout.setContentsMargins(0, -1, 0, -1)
        self.graphicVerticalLayout.setObjectName("graphicVerticalLayout")
        self.mainGridLayout.addLayout(self.graphicVerticalLayout, 1, 1, 16, 1)
        self.titleLineEdit = QtWidgets.QLineEdit(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLineEdit.sizePolicy().hasHeightForWidth())
        self.titleLineEdit.setSizePolicy(sizePolicy)
        self.titleLineEdit.setMinimumSize(QtCore.QSize(30, 0))
        self.titleLineEdit.setBaseSize(QtCore.QSize(30, 0))
        self.titleLineEdit.setObjectName("titleLineEdit")
        self.mainGridLayout.addWidget(self.titleLineEdit, 2, 0, 1, 1)
        self.dataseriesLabel = QtWidgets.QLabel(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataseriesLabel.sizePolicy().hasHeightForWidth())
        self.dataseriesLabel.setSizePolicy(sizePolicy)
        self.dataseriesLabel.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.dataseriesLabel.setObjectName("dataseriesLabel")
        self.mainGridLayout.addWidget(self.dataseriesLabel, 7, 0, 1, 1)
        self.scaleSelection = ScaleSelectionWidget(dialog)
        self.scaleSelection.setObjectName("scaleSelection")
        self.mainGridLayout.addWidget(self.scaleSelection, 15, 0, 1, 1)
        self.mainGridLayout.setColumnStretch(0, 1)
        self.mainGridLayout.setColumnStretch(1, 5)
        self.verticalLayout.addLayout(self.mainGridLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem6)
        self.bottomHorizontalLayout = QtWidgets.QHBoxLayout()
        self.bottomHorizontalLayout.setObjectName("bottomHorizontalLayout")
        self.graphicTextLabel = QtWidgets.QLabel(dialog)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.graphicTextLabel.setFont(font)
        self.graphicTextLabel.setText("")
        self.graphicTextLabel.setObjectName("graphicTextLabel")
        self.bottomHorizontalLayout.addWidget(self.graphicTextLabel)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.bottomHorizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.bottomHorizontalLayout)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "Dialog"))
        self.parameterLabel.setText(_translate("dialog", "Parameter"))
        self.samplesLabel.setText(_translate("dialog", "Samples"))
        self.titleLabel.setText(_translate("dialog", "Title"))
        self.dataseriesLabel.setText(_translate("dialog", "Data Series"))

from snpanalyzer.gui.widget.format import FormatSelectionWidget
from snpanalyzer.gui.widget.presets import PresetsWidget
from snpanalyzer.gui.widget.scale import ScaleSelectionWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

