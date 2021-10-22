import visa
import pyvisa
from calWizard import CalWizard

import configparser

import re
import os
import tempfile

class Communication(object):

    def __init__(self):

        #rm = pyvisa.highlevel.ResourceManager()
        #print(rm.list_resources())


        self.vna_settings_file = 'VNA_SETTINGS.ini'

        open(self.vna_settings_file, 'a').close()

        self.config = configparser.ConfigParser()
        self.config.read_file(open(self.vna_settings_file))
        if os.stat(self.vna_settings_file).st_size == 0:

            self.config['comm_settings'] = {}
            self.VNAAddress = "TCPIP0::10.29.48.46::hislip0::INSTR"
            self.IF = 300
            self.min_freq = 10e5
            self.max_freq = 1e9
            self.num_points = 1000
            self.timeout = 500000
            self.ip_address = None
            self.visa_address = None
            self.average = 1
            self.test_name = " "

            self.connected = False

            with open(self.vna_settings_file, 'w') as configfile:
                print("Write to INI")
                self.config.write(configfile)

    def connectToVNA(self, VNA_ADDRESS="TCPIP0::10.29.48.46::hislip0::INSTR"):
        try:
            self.VNAAddress = VNA_ADDRESS
            self.rm = visa.ResourceManager()
            self.session = self.rm.open_resource(self.VNAAddress)
            with open(self.vna_settings_file, 'w') as configfile:
                print("Write to INI")
                self.config.write(configfile)
            self.connected = True
        except Exception as e:
            print(e)

	 
    @property
    def VNAAddress(self):
        try:
            return self.config['comm_settings']['vna_addr']
        except Exception as e:
            return ''
        
    @VNAAddress.setter
    def VNAAddress(self, addr):
        print("Trying to write VNA addr")
        self.config['comm_settings']['vna_addr'] = addr 
        print("Got here")

    @property
    def max_freq(self):
        try:
            return int(float(self.config['comm_settings']['max_freq']))
        except Exception as e:
            return ''

    @max_freq.setter
    def max_freq(self, max_freq):
        self.config['comm_settings']['max_freq'] = str(max_freq)
    
    @property
    def min_freq(self):
        try:
            return int(float(self.config['comm_settings']['min_freq']))
        except Exception as e:
            return ''

    @min_freq.setter
    def min_freq(self, min_freq):
        self.config['comm_settings']['min_freq'] = str(min_freq)
        
    @property
    def average(self):
        try:
            return int(float(self.config['comm_settings']['average']))
        except Exception as e:
            return ''

    @average.setter
    def average(self, avg):
        self.config['comm_settings']['average'] = str(avg) 
        
    @property
    def IF(self):
        try:
            return int(float(self.config['comm_settings']['if']))
        except Exception as e:
            return ''
            
    @IF.setter
    def IF(self, IF):
        print(IF)
        self.config['comm_settings']['if'] = str(IF)
        
    @property
    def num_points(self):
        try:
            return int(float(self.config['comm_settings']['num_points']))
        except Exception as e:
            return ''
        
    @num_points.setter 
    def num_points(self, num_points):
        self.config['comm_settings']['num_points'] = str(num_points)
        
    @property
    def ip_address(self):
        return self._ip

    @num_points.setter
    def ip_address(self, ip):
        self._ip = ip

    @property
    def port_num(self):
        try:
            return int(self.config['comm_settings']['port_num'])
        except Exception as e:
            return ''
        
    @port_num.setter
    def port_num(self, port_num):
        
        self.config['comm_settings']['port_num'] = str(port_num) 

        
    @property
    def test_name(self):
        return self.config['comm_settings']['test_name'] 

    @test_name.setter
    def test_name(self, test_name):
        self.config['comm_settings']['test_name'] = str(test_name) 

    @property
    def timeout(self):
        try:
            return int(float(self.config['comm_settings']['timeout']))
        except Exception as e:
            return ''
        
    @timeout.setter
    def timeout(self, timeout):
        self.config['comm_settings']['timeout'] = str(timeout) 
        
    def getSNP(self):
        pass

    def calibrate(self):
        self.wizard = CalWizard(self)
        self.wizard.show()

    def whoAmI(self):
        return(self.session.query('*IDN?'))

    def aquire(self, testName, portNum):
        try:
            self.test_name = testName
            self.port_num = portNum
            print("Here")
            self.session.timeout = self.timeout

            self.session.write("SENS:BWID " + str(self.IF))
            print("set if")
            self.session.write("SENS:FREQ:STAR " + str(self.min_freq))
            print("set min f")

            self.session.write("SENS:FREQ:STOP " + str(self.max_freq))
            print("set max f")
            print("set avg")
            self.session.write("SENS:SWE:TYPE LIN")
            self.session.write("SENS:SWE:POIN " + str(self.num_points))
            print("ok")
            self.session.write(":SENS:AVER:CLE")
            self.session.write(":ABOR")
            self.session.write("SENS:AVER:COUN {}".format(str(self.average)))
            self.session.write(":INIT1:CONT ON")
            self.session.write(":TRIG:SOUR immediate")
            self.session.write("SENS:SWE:GRO:COUN 4") # "+str(self.average))
            print("ok")

            self.session.write("SENS:SWE:MODE GRO;*OPC?")
            
            self.session.write(":CALC:PAR:SEL 'CH1_S11_1'")
            print(self.session.query(";*OPC?"))
            print("Start")
            self.session.write(":CALC:DATA:SNP:PORT:SAVE '{}', 'Y:\\{}.s{}p'".format(str([i for i in range(1,portNum+1)])[1:-1], testName, portNum))
            print(self.session.query(";*OPC?"))
            snp_data = self.session.query('MMEMory:TRANsfer? "Y:\\{}.s{}p"'.format(testName, portNum)).encode("utf8")
            dirpath = tempfile.mkdtemp()
            temp_file_name = os.path.join(dirpath, testName + "." + "s{}p".format(portNum))
            temp_file = open(temp_file_name, mode = "wb")

            temp_file.write(snp_data)
            #temp_file.seek(0)
            #temp_file.close()

            #rm.list_resources()
            with open(self.vna_settings_file, 'w') as configfile:
                self.config.write(configfile)

            return temp_file_name
            
        except visa.Error as ex:
            print(ex)


    def getLastVNAAddress(self):
        return self.config['comm_settings']['vna_addr']

    def getAcqParams(self):
        params = {'testID'  : self.getNextID(self.testName), 
                  'max_freq': self.max_freq,
                  'min_freq': self.min_freq,
                  'average' : self.average,
                  'IF'      : self.IF,
                  'self'    : self.num_points}

    def getNextID(self, ID):

        #We will first apply a regular expression to find the last integer in a string.
        #If there is an integer, we increment it. Otherwise we will simply append a 2 to the end the test ID.
        #Ex.: cableTest --> cableTest2
        #Ex.: caleTest2 --> cableTest3
        
        currentID = ID
        if currentID.isspace() or len(currentID) < 1 or not currentID:
            print("No CID")
            return "1"
        
        reg = re.compile('\d+$')

        idCount = reg.findall(currentID) #This will return the integer at the end of the testID ... if any.
        
        if idCount :
            idCount = idCount[0]
            IDNoCount = currentID[0: -len(idCount)]
            nextIDCount = str(int(idCount) + 1)

            return IDNoCount + nextIDCount
        
        return currentID + '2'  #If there is no integer at the end of the string, simply append a '2'

    def aquireInterface(self):
        if self.connected :
            try:
                testName, numPorts, IF, start_freq, stop_freq, num_points, average, timeout = Test_Params_Dialog().getParams()
                if testName:
                    try:
                        #comm = Communication(addr)
                        self.IF = IF
                        self.min_freq = start_freq
                        self.max_freq = stop_freq
                        self.num_points = num_points
                        self.average = average
                        print("Aquiring Deembeding")
                        return self.aquire(testName, numPorts)

                    except Exception as e:
                        return None

            except Exception as e:
                print("Cancel")

        raise "You Must be connected to VNA"

    def close(self):
        self.session.close()
        self.rm.close()
        self.connected = False




from decimal import Decimal
from UI import TestParameters
from PyQt5 import QtWidgets, QtGui, QtCore

class Test_Params_Dialog:
    def getParams(self):
        
        comm = Communication()
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

 
if __name__ == '__main__':

    comm = Communication()
    comm.connectToVNA()
    comm.aquire("test4Port", 4)

