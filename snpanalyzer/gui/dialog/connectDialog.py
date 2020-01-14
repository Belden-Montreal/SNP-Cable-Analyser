import datetime

import dateutil
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

#from snpanalyzer.gui.ui import calSets
from snpanalyzer.gui.ui import calSet


class ConnectDialog(object):

    def __init__(self, _vnaManager):
        self.calib = False
        self._vnaManager = _vnaManager
        self.dialog = QtWidgets.QDialog()
        self.newDial = calSet.Ui_CalDialog()
        self.newDial.setupUi(self.dialog)
        #self.projectTypes=["er","3","4","5"]

        
        #self.projectTypes = self._vnaManager.calSet()
        #self.newDial.typeBox.addItems(self.projectTypes)
        self.newDial.typeBox.setCurrentIndex(0)
        self.newDial.buttonCal.clicked.connect(lambda index: self.newCalibration(self.dialog))
        
        self.newDial.connect.clicked.connect(self.connect)
        self.newDial.buttonBox.accepted.connect(lambda: self.acceptCal(self.dialog))
        self.newDial.statusLabel.setText("Not Connected")
        self.newDial.vnaAddress.setText(self._vnaManager._config.getAddress())

    
    def connect(self):
        addr =  self.newDial.vnaAddress.text()
        self._vnaManager.connect(addr)
        print("Connect status ", self._vnaManager._connected)
        if self._vnaManager._connected:
            self.newDial.statusLabel.setText("Connected")
            self.newDial.groupBox_2.setEnabled(True)
            self.projectTypes = self._vnaManager.calSet()
            self.newDial.typeBox.addItems(self.projectTypes)
        
        if not self._vnaManager._connected:
            self.newDial.statusLabel.setText("Not Connected")
            self.newDial.groupBox_2.setEnabled(False)



    def showDialog(self):
        return self.dialog.exec_()
    def newCalibration(self, dialog):
        res = self._vnaManager.calibrateNew()
        if res:
            dialog.accept()
            self.calib = True


    def acceptCal(self,dialog):
        if self._vnaManager._connected:
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
