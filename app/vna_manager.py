import VNA_addr_dialog
import TestParameters
from Communication import Communication
from PyQt5 import QtWidgets
from decimal import Decimal

class VNAManager(object):

    def __init__(self):
        self._connected = False
        self._comm = Communication()

    def connect(self):
        addr = Addr_Dialog().getAddr(self._comm)
        if addr:
            try:
                self._comm.connectToVNA(addr)
                self.connected = True
            except Exception as e:
                print(e)

    def disconnect(self):
        while self._connected:
            try:
                self._comm.close()
                self.connected = False
            except Exception as e:
                print(e)

    def whoAmI(self):
        return self._comm.whoAmI()

    def acquire(self):
        if self._comm.connected :
            try:
                testName, numPorts, IF, start_freq, stop_freq, num_points, average, timeout = Test_Params_Dialog().getParams(self._comm)
                if testName:
                    try:
                        self._comm.IF = IF
                        self._comm.min_freq = start_freq
                        self._comm.max_freq = stop_freq
                        self._comm.num_points = num_points
                        self._comm.average = average
                        self._comm.aquire(testName, numPorts)

                        return r"Y:/{}.s{}p".format(testName, numPorts)

                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

        raise "You Must be connected to VNA"

    def calibrate(self):
        self._comm.calibrate()

class Test_Params_Dialog:
    def getParams(self, comm):
        
        print("Connected")
        dialog = QtWidgets.QDialog()
        params_dialog = TestParameters.Ui_TestParameterDialog()
        params_dialog.setupUi(dialog)
        print("Current ID: ", comm.test_name)
        print("NEXT ID: ", comm.getNextID(comm.test_name))
        params_dialog.testNameLineEdit_2.setText(comm.getNextID(comm.test_name)) 
        params_dialog.iFBandwidthLineEdit.setText(str(comm.IF))
        print("Min Freq ", comm.min_freq)
        params_dialog.startFrequencyLineEdit.setText('%E' % Decimal(comm.min_freq))
        params_dialog.stopFrequencyLineEdit.setText('%E' % Decimal(comm.max_freq))
        params_dialog.numberOfPointsLineEdit.setText(str(comm.num_points))
        params_dialog.numberOfPortsLineEdit.setText(str(comm.port_num))
        params_dialog.numberOfAverageLineEdit.setText(str(comm.average))
        params_dialog.timeoutLineEdit.setText('%E' % Decimal(comm.timeout))

        result = dialog.exec_()
        
        if not result:
            return 0
        if result:
            try:
                testName = params_dialog.testNameLineEdit_2.text()
                IF = int(float(params_dialog.iFBandwidthLineEdit.text()))
                start_freq = int(float(params_dialog.startFrequencyLineEdit.text()))
                stop_freq = int(float(params_dialog.stopFrequencyLineEdit.text()))
                num_points = int(float(params_dialog.numberOfPointsLineEdit.text()))
                num_ports = int(float(params_dialog.numberOfPortsLineEdit.text()))
                average = int(float(params_dialog.numberOfAverageLineEdit.text()))
                timeout = int(float(params_dialog.timeoutLineEdit.text()))

                return testName, num_ports, IF, start_freq, stop_freq, num_points, average, timeout
            except Exception as e:
                print("Cancel123")
                return

class Addr_Dialog:
    def getAddr(self, comm):
        dialog = QtWidgets.QDialog()
        addr_dialog = VNA_addr_dialog.Ui_Addr_Dialog()
        addr_dialog.setupUi(dialog)
        addr_dialog.plainTextEdit.setText(comm.VNAAddress)

        result = dialog.exec_()
        print("here")
        if not result:
            return 0
        if result:
            addr =  addr_dialog.plainTextEdit.text()
            print("sent")
            if len(addr) < 1:
                return 0
            return addr