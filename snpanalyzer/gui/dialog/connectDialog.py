import datetime

import dateutil
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from snpanalyzer.gui.ui import Set_calSet



class ConnectDialog(object):

    def __init__(self, _vnaManager):
        self.calib = False
        self._vnaManager = _vnaManager
        self.dialog = QtWidgets.QDialog()
        self.newDial = Set_calSet.Ui_CalDialog()
        self.newDial.setupUi(self.dialog)
        self.projectTypes = self._vnaManager.calSet()
        #self.projectTypes=["er","3","4","5"]
        self.newDial.typeBox.addItems(self.projectTypes)
        self.newDial.typeBox.setCurrentIndex(0)
        self.newDial.buttonCal.clicked.connect(lambda index: self.newCalibration(self.dialog))
        self.newDial.buttonBox.accepted.connect(lambda: self.acceptCal(self.dialog))

    def showDialog(self):
        return self.dialog.exec_()
    def newCalibration(self, dialog):
        res = self._vnaManager.calibrateNew()
        if res:
            dialog.accept()
            self.calib = True


    def acceptCal(self,dialog):
        d = datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d") - dateutil.relativedelta.relativedelta(
            months=2)
        if datetime.datetime.strptime(self._vnaManager.getDate()[self.newDial.typeBox.currentIndex()], "%Y-%m-%d") < d:

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("CalSet is expired")
            msg.setInformativeText("Equipment should be used for reference only")
            msg.setWindowTitle("Warning")
            msg.setDetailedText("this CalSet is more that 2 months old")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                dialog.accept()
            else:
                print("cancel")

        else:
            dialog.accept()

        #self.projectTypes=self._vnaManager.calSet()
        #if res:
         #   dialog.accept()
        #self.newDial.typeBox.clear()
        #self.newDial.typeBox.addItems(self.projectTypes)
       # self.newDial.typeBox.setCurrentIndex(0)
