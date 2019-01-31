from snpanalyzer.gui.wizard.calibration import CalibrationWizard
from snpanalyzer.config.vna import VNAConfiguration
from PyQt5 import QtWidgets, QtCore
import visa
import time

from visa import Error as VisaError
from pyvisa import ResourceManager

class VNA(QtCore.QObject):
    connection = QtCore.pyqtSignal()

    def __init__(self):
        super(QtCore.QObject, self).__init__()
        self._connected = False
        self._config = VNAConfiguration()
        self._manager = None
        #self._session = None
        self.session = None
    def connect(self):
        #self._manager = ResourceManager()
        try:
            #self._session = self._manager.open_resource(self._config.getAddress())
            self.rm = visa.ResourceManager()
            self.session = self.rm.open_resource(self._config.getAddress())
            print(self._config.getAddress())
            #print(self._config.getAddress())
            self.connection.emit()
            self._connected = True
            print("Connecting")

        except Exception as e:
            dialog = QtWidgets.QErrorMessage()
            dialog.showMessage("Error : {}".format(e))
            dialog.exec_()
            print(e)

    def disconnect(self):
        try:
            self.session.close()
            self.session = None
            self.rm.close()
            self.rm = None
            self.connected = False
            self.connection.emit()
        except Exception as e:
            dialog = QtWidgets.QErrorMessage()
            dialog.showMessage("Error : {}".format(e))
            dialog.exec_()

    def acquire(self, name, ports):
        config = self._config

        timeOut = self._config.getTimeout()
        bw = config.getBandwidth()
        minFreq = config.getMinimumFrequency()
        maxFreq = config.getMaximumFrequency()
        res = config.getResolution()
        average = config.getAverage()
        if self.rm is None:
            return


        try:
            self.session.timeout = timeOut
            print(self._config.getTimeout())

            self.session.write("SENS:BWID " + str(bw))
            print(self.session.query(";*OPC?"))

            print("set if")
            self.session.write("SENS:FREQ:STAR " + str(minFreq))
            print("set min f")

            self.session.write("SENS:FREQ:STOP " + str(maxFreq))
            print("set max f:"+str(maxFreq))
            print("set avg")
            self.session.write("SENS:SWE:TYPE LIN")
            self.session.write("SENS:SWE:POIN " + str(res))
            print("res " + str(res))
            self.session.write(":SENS:AVER:CLE")
            self.session.write(":ABOR")
            self.session.write("SENS:AVER:COUN {}".format(str(average)))
            self.session.write(":INIT1:CONT ON")
            self.session.write(":TRIG:SOUR immediate")
            self.session.write("SENS:SWE:GRO:COUN 4") # "+str(self.average))
            print("ok")

            self.session.write("SENS:SWE:MODE GRO;*OPC?")
            
            self.session.write(":CALC:PAR:SEL 'CH1_S11_1'")
            print(self.session.query(";*OPC?"))
            self.session.write(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p'".format(str([i for i in range(1,int(ports)+1)])[1:-1], "Y:\\"+name, str(int(ports)) ))
            print(self.session.query(";*OPC?"))
            #rm.list_resources()
            
            return (r"Y:/{}.s{}p".format(name, str(int(ports))))
            
        except VisaError as ex:
            print(ex)
        


        '''self._session.timeout = self._config.getTimeout()
        print(self._config.getTimeout())
        self._session.write("SENS:BWID "      + str(config.getBandwidth()))
        print("SENS:BWID "      + str(config.getBandwidth()))
        self._session.write("SENS:FREQ:STAR " + str(config.getMinimumFrequency()))
        print("SENS:FREQ:STAR " + str(config.getMinimumFrequency()))
        self._session.write("SENS:FREQ:STOP " + str(config.getMaximumFrequency()))
        print("SENS:FREQ:STOP " + str(config.getMaximumFrequency()))
        self._session.write("SENS:SWE:TYPE LIN")
        print("SENS:SWE:TYPE LIN")
        self._session.write("SENS:SWE:POIN "  + str(config.getResolution()))
        print("SENS:SWE:POIN "  + str(config.getResolution()))
        self._session.write(":SENS:AVER:CLE")
        print(":SENS:AVER:CLE")
        self._session.write(":ABOR")
        print("ABOR")
        self._session.write("SENS:AVER:COUN " + str(config.getAverage()))
        print("SENS:AVER:COUN " + str(config.getAverage()))
        self._session.write(":INIT1:CONT ON")
        self._session.write(":TRIG:SOUR immediate")
        self._session.write("SENS:SWE:GRO:COUN 4")
        self._session.write("SENS:SWE:MODE GRO;*OPC?")
        self._session.write(":CALC:PAR:SEL 'CH1_S11_1'")
        print(self._session.query(";*OPC?"))

        print(":CALC:PAR:SEL 'CH1_S11_1")
        self._session.write(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p'".format(
            str([i for i in range(1,int(ports)+1)])[1:-1], "Y:\\"+name, ports))
        return'''

    def calibrate(self):
        wizard = CalibrationWizard(self)
        wizard.exec()
        print("Showing")
        

    def whoAmI(self):
        print("wAi")
        if self.session is None:
            return "None"
            print("wAi2")

        print(self.session.query('*IDN?'))
        return self.session.query('*IDN?')

    def connected(self):
        return self._connected
