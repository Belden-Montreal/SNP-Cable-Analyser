# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParameterWidget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ParameterWidget(object):
    def setupUi(self, ParameterWidget):
        ParameterWidget.setObjectName("ParameterWidget")
        ParameterWidget.resize(1237, 687)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(ParameterWidget)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_7.addLayout(self.verticalLayout_3)
        self.canvasLayout = QtWidgets.QVBoxLayout()
        self.canvasLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.canvasLayout.setObjectName("canvasLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ResultsFrame = QtWidgets.QFrame(ParameterWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultsFrame.sizePolicy().hasHeightForWidth())
        self.ResultsFrame.setSizePolicy(sizePolicy)
        self.ResultsFrame.setMinimumSize(QtCore.QSize(246, 0))
        self.ResultsFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.ResultsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ResultsFrame.setObjectName("ResultsFrame")
        self.label = QtWidgets.QLabel(self.ResultsFrame)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.paramLabel = QtWidgets.QLabel(self.ResultsFrame)
        self.paramLabel.setGeometry(QtCore.QRect(10, 70, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.paramLabel.setFont(font)
        self.paramLabel.setText("")
        self.paramLabel.setObjectName("paramLabel")
        self.passLabel = QtWidgets.QLabel(self.ResultsFrame)
        self.passLabel.setGeometry(QtCore.QRect(10, 140, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.passLabel.setFont(font)
        self.passLabel.setText("")
        self.passLabel.setObjectName("passLabel")
        self.horizontalLayout_2.addWidget(self.ResultsFrame)
        self.groupBox = QtWidgets.QGroupBox(ParameterWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(-1, 5, -1, -1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.marginListWidget = QtWidgets.QListWidget(self.groupBox_3)
        self.marginListWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.marginListWidget.setObjectName("marginListWidget")
        self.horizontalLayout_4.addWidget(self.marginListWidget)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_5.addWidget(self.label_2)
        self.marginValueLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.marginValueLabel.setFont(font)
        self.marginValueLabel.setText("")
        self.marginValueLabel.setObjectName("marginValueLabel")
        self.verticalLayout_5.addWidget(self.marginValueLabel)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.marginFreqLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.marginFreqLabel.setFont(font)
        self.marginFreqLabel.setText("")
        self.marginFreqLabel.setObjectName("marginFreqLabel")
        self.verticalLayout_5.addWidget(self.marginFreqLabel)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.marginLimitLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.marginLimitLabel.setFont(font)
        self.marginLimitLabel.setText("")
        self.marginLimitLabel.setObjectName("marginLimitLabel")
        self.verticalLayout_5.addWidget(self.marginLimitLabel)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.marginLabel = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.marginLabel.setFont(font)
        self.marginLabel.setText("")
        self.marginLabel.setObjectName("marginLabel")
        self.verticalLayout_5.addWidget(self.marginLabel)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(ParameterWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, 5, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.worstListWidget = QtWidgets.QListWidget(self.groupBox_4)
        self.worstListWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.worstListWidget.setObjectName("worstListWidget")
        self.horizontalLayout_6.addWidget(self.worstListWidget)
        self.horizontalLayout_3.addWidget(self.groupBox_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_6.addWidget(self.label_6)
        self.worstValueLabel = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.worstValueLabel.setFont(font)
        self.worstValueLabel.setText("")
        self.worstValueLabel.setObjectName("worstValueLabel")
        self.verticalLayout_6.addWidget(self.worstValueLabel)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.worstFreqLabel = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.worstFreqLabel.setFont(font)
        self.worstFreqLabel.setText("")
        self.worstFreqLabel.setObjectName("worstFreqLabel")
        self.verticalLayout_6.addWidget(self.worstFreqLabel)
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.worstLimitLabel = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.worstLimitLabel.setFont(font)
        self.worstLimitLabel.setText("")
        self.worstLimitLabel.setObjectName("worstLimitLabel")
        self.verticalLayout_6.addWidget(self.worstLimitLabel)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_6.addWidget(self.label_9)
        self.worstMarginLabel = QtWidgets.QLabel(self.groupBox_2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.worstMarginLabel.setFont(font)
        self.worstMarginLabel.setText("")
        self.worstMarginLabel.setObjectName("worstMarginLabel")
        self.verticalLayout_6.addWidget(self.worstMarginLabel)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addWidget(self.groupBox_2)
        self.canvasLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_7.addLayout(self.canvasLayout)

        self.retranslateUi(ParameterWidget)
        QtCore.QMetaObject.connectSlotsByName(ParameterWidget)

    def retranslateUi(self, ParameterWidget):
        _translate = QtCore.QCoreApplication.translate
        ParameterWidget.setWindowTitle(_translate("ParameterWidget", "ParameterWidget"))
        self.label.setText(_translate("ParameterWidget", "Results"))
        self.groupBox.setTitle(_translate("ParameterWidget", "Worst Margin"))
        self.groupBox_3.setTitle(_translate("ParameterWidget", "Pair"))
        self.label_2.setText(_translate("ParameterWidget", "Value :"))
        self.label_3.setText(_translate("ParameterWidget", "Freq : "))
        self.label_4.setText(_translate("ParameterWidget", "Limit : "))
        self.label_5.setText(_translate("ParameterWidget", "Margin : "))
        self.groupBox_2.setTitle(_translate("ParameterWidget", "Worst Value"))
        self.groupBox_4.setTitle(_translate("ParameterWidget", "Pair"))
        self.label_6.setText(_translate("ParameterWidget", "Value :"))
        self.label_7.setText(_translate("ParameterWidget", "Freq : "))
        self.label_8.setText(_translate("ParameterWidget", "Limit : "))
        self.label_9.setText(_translate("ParameterWidget", "Margin : "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ParameterWidget = QtWidgets.QWidget()
    ui = Ui_ParameterWidget()
    ui.setupUi(ParameterWidget)
    ParameterWidget.show()
    sys.exit(app.exec_())
