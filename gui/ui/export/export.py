# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/export/export.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(824, 403)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.presetsWidget = PresetsWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presetsWidget.sizePolicy().hasHeightForWidth())
        self.presetsWidget.setSizePolicy(sizePolicy)
        self.presetsWidget.setObjectName("presetsWidget")
        self.verticalLayout.addWidget(self.presetsWidget)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.tempLabel = QtWidgets.QLabel(dialog)
        self.tempLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tempLabel.setObjectName("tempLabel")
        self.gridLayout.addWidget(self.tempLabel, 0, 0, 1, 1)
        self.tempLineEdit = QtWidgets.QLineEdit(dialog)
        self.tempLineEdit.setReadOnly(True)
        self.tempLineEdit.setObjectName("tempLineEdit")
        self.gridLayout.addWidget(self.tempLineEdit, 0, 1, 1, 1)
        self.tempBrowsePushButton = QtWidgets.QPushButton(dialog)
        self.tempBrowsePushButton.setObjectName("tempBrowsePushButton")
        self.gridLayout.addWidget(self.tempBrowsePushButton, 0, 2, 1, 1)
        self.docLabel = QtWidgets.QLabel(dialog)
        self.docLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.docLabel.setObjectName("docLabel")
        self.gridLayout.addWidget(self.docLabel, 1, 0, 1, 1)
        self.docLineEdit = QtWidgets.QLineEdit(dialog)
        self.docLineEdit.setReadOnly(True)
        self.docLineEdit.setObjectName("docLineEdit")
        self.gridLayout.addWidget(self.docLineEdit, 1, 1, 1, 1)
        self.docBrowsePushButton = QtWidgets.QPushButton(dialog)
        self.docBrowsePushButton.setObjectName("docBrowsePushButton")
        self.gridLayout.addWidget(self.docBrowsePushButton, 1, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.projectExportWidget = ExportProjectWidget(dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.projectExportWidget.sizePolicy().hasHeightForWidth())
        self.projectExportWidget.setSizePolicy(sizePolicy)
        self.projectExportWidget.setObjectName("projectExportWidget")
        self.verticalLayout.addWidget(self.projectExportWidget)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem2)
        self.buttonBox = QtWidgets.QDialogButtonBox(dialog)
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
        self.tempLabel.setText(_translate("dialog", "Temporary Folder:"))
        self.tempBrowsePushButton.setText(_translate("dialog", "Browse"))
        self.docLabel.setText(_translate("dialog", "Output Document:"))
        self.docBrowsePushButton.setText(_translate("dialog", "Browse"))

from gui.widget.export.project import ExportProjectWidget
from gui.widget.presets import PresetsWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QDialog()
    ui = Ui_dialog()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec_())

