# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './ui/presets.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_presetsWidget(object):
    def setupUi(self, presetsWidget):
        presetsWidget.setObjectName("presetsWidget")
        presetsWidget.resize(335, 66)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(presetsWidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.presetsLabel = QtWidgets.QLabel(presetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presetsLabel.sizePolicy().hasHeightForWidth())
        self.presetsLabel.setSizePolicy(sizePolicy)
        self.presetsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.presetsLabel.setObjectName("presetsLabel")
        self.horizontalLayout_2.addWidget(self.presetsLabel)
        self.presetsComboBox = QtWidgets.QComboBox(presetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presetsComboBox.sizePolicy().hasHeightForWidth())
        self.presetsComboBox.setSizePolicy(sizePolicy)
        self.presetsComboBox.setCurrentText("")
        self.presetsComboBox.setObjectName("presetsComboBox")
        self.horizontalLayout_2.addWidget(self.presetsComboBox)
        self.presetsButtonAdd = QtWidgets.QPushButton(presetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presetsButtonAdd.sizePolicy().hasHeightForWidth())
        self.presetsButtonAdd.setSizePolicy(sizePolicy)
        self.presetsButtonAdd.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.presetsButtonAdd.setIcon(icon)
        self.presetsButtonAdd.setFlat(True)
        self.presetsButtonAdd.setObjectName("presetsButtonAdd")
        self.horizontalLayout_2.addWidget(self.presetsButtonAdd)
        self.presetsButtonRemove = QtWidgets.QPushButton(presetsWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.presetsButtonRemove.sizePolicy().hasHeightForWidth())
        self.presetsButtonRemove.setSizePolicy(sizePolicy)
        self.presetsButtonRemove.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/minus-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.presetsButtonRemove.setIcon(icon1)
        self.presetsButtonRemove.setFlat(True)
        self.presetsButtonRemove.setObjectName("presetsButtonRemove")
        self.horizontalLayout_2.addWidget(self.presetsButtonRemove)

        self.retranslateUi(presetsWidget)
        QtCore.QMetaObject.connectSlotsByName(presetsWidget)

    def retranslateUi(self, presetsWidget):
        _translate = QtCore.QCoreApplication.translate
        presetsWidget.setWindowTitle(_translate("presetsWidget", "Form"))
        self.presetsLabel.setText(_translate("presetsWidget", "Presets"))

from gui.ressources import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    presetsWidget = QtWidgets.QWidget()
    ui = Ui_presetsWidget()
    ui.setupUi(presetsWidget)
    presetsWidget.show()
    sys.exit(app.exec_())

