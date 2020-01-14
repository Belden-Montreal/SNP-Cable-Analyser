import pyvisa
from PyQt5.QtWidgets import QMessageBox
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
        self._sortedCset = list()
        self.useMachineSettings = False
        self._date=list()


    def connect(self, address = None):
        #self._manager = ResourceManager()

        if address == None:
            address = self._config.getAddress()

        try:
            #self._session = self._manager.open_resource(self._config.getAddress())
            self.rm = visa.ResourceManager()
            self.session = self.rm.open_resource(address)

            print(self._config.getAddress())
            self.connection.emit()
            self._connected = True

            self._config.setAddress(address)

            print("Connecting")


        except Exception as e:
            self._connected = False

            '''dialog = QtWidgets.QErrorMessage()
            dialog.showMessage("Error : {}".format(e))
            dialog.exec_()
            print(e)'''


    def disconnect(self):
        try:
            self.session.close()
            self.session = None
            self.rm.close()
            self.rm = None
            self._connected = False
            self.connection.emit()
        except Exception as e:
            dialog = QtWidgets.QErrorMessage()
            dialog.showMessage("Error : {}".format(e))
            dialog.exec_()

    def acquire(self, name = None, ports = None, config = None):
        if config is not None:
            timeOut = self._config.getTimeout()
            bw = config.getBandwidth()
            minFreq = config.getMinimumFrequency()
            print("testing with min freq at ", minFreq)
            maxFreq = config.getMaximumFrequency()
            res = config.getResolution()
            average = config.getAverage()
            noConfig = config.getNoConfig()
        if self.rm is None:
            return
        try:
            self.session.timeout = timeOut
            print("timeout:", self._config.getTimeout())
            
            if noConfig == False:
                self.session.write("SENS:BWID " + str(bw))
                print(self.session.query(";*OPC?"))

                print("set frequence:")
                self.session.write("SENS:FREQ:STAR " + str(minFreq))
                print("min freq setted at "+ str(minFreq))
                self.session.write("SENS:FREQ:STOP " + str(maxFreq))
                print("max freq setted at "+str(maxFreq))

                print("set average:")
                self.session.write("SENS:SWE:TYPE LIN")
                self.session.write("SENS:SWE:POIN " + str(res))
                print("resolution setted at" + str(res))
                self.session.write(":SENS:AVER:CLE")
                self.session.write(":ABOR")
                self.session.write("SENS:AVER:COUN {}".format(str(average)))
                print("average setted at "+str(average))

            print(":INIT1:CONT ON")
            self.session.write(":INIT1:CONT ON")
            print(self.session.query(";*OPC?"))

            print(":TRIG:SOUR immediate")
            self.session.write(":TRIG:SOUR immediate")
            print(self.session.query(";*OPC?"))

            print("SENS:SWE:GRO:COUN 4")
            self.session.write("SENS:SWE:GRO:COUN 4") # "+str(self.average))
            print(self.session.query(";*OPC?"))

            print("SENS:SWE:MODE GRO;*OPC?")
            self.session.write("SENS:SWE:MODE GRO;*OPC?")
            print(self.session.query(";*OPC?"))

            print(":CALC:PAR:SEL 'CH1_S11_1'")
            self.session.write(":CALC:PAR:SEL 'CH1_S11_1'")
            print(self.session.query(";*OPC?"))

            print(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p'")
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

    def calibrateNew(self):
        wizard = CalibrationWizard(self)
        return wizard.exec()
        print("Showing")

    def calSet(self):
        cset = self.session.query("CSET:CAT?")
        cset=cset.replace('"','')
        cset=cset.replace("\n","")
        listCset= cset.split(",")
        CsetDate=list()
        for cal in listCset:
            date=self.session.query("CSET:DATE? '{}'".format(cal))
            for x in range(1,10):
                date=date.replace("+{},".format(x),"+0{},".format(x))
                date=date.replace("+{}\n".format(x),"+0{}\n".format(x))
            date=date.replace("+","")
            date=date.replace(",","-")
            date = date.replace("\n","")
            CsetDate.append("["+date+"] | "+cal)
            self._date.append(date)
            self._date.sort(reverse=True)

        CsetDate.sort(reverse=True)
        for i in CsetDate:
            temp= i.split("] | ")
            self._sortedCset.append(temp[1])
        return CsetDate

    def setCal(self,i):
        print(self._sortedCset[i])
       # self.session.write("SENS1:CORR:CSET:DEAC")
        self.session.write("SENS:CORR:CSET:ACT '{}',1".format(str(self._sortedCset[i])))

    def getDate(self):
        return self._date

    def whoAmI(self):
        start =float(self.session.query("SENS:FREQ:STAR?"))
        end = float(self.session.query("SENS:FREQ:STOP?"))
        type= str(self.session.query("SENS:SWE:TYPE?"))
        res =float(self.session.query("SENS:SWE:POIN?"))
        avg =float(self.session.query("SENS:AVER:COUN?"))
        bwd= float(self.session.query("SENS:BWID?"))
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("\n"+str(self.session.query('*IDN?')))
        msgBox.setInformativeText("CalSet:"+self.session.query('SENS:CORR:CSET:ACT? NAME'))
        msgBox.setDetailedText("Start at: {}\nEnd at: {}\nType: {}Resolution:{}\nAverage: {}\nBandwidth: {}".format(start,end,type,res,avg,bwd))
        msgBox.setWindowTitle("Who am I?")
        msgBox.exec()

    def connected(self):
        return self._connected
