import visa
import pyvisa
from calWizard import CalWizard

import configparser

import re
import os

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
            with open(self.vna_settings_file, 'w') as configfile:
                print("Write to INI")
                self.config.write(configfile)

    def connectToVNA(self, VNA_ADDRESS):
        self.VNAAddress = VNA_ADDRESS
        self.rm = visa.ResourceManager()
        self.session = self.rm.open_resource(self.VNAAddress)
        with open(self.vna_settings_file, 'w') as configfile:
            print("Write to INI")
            self.config.write(configfile)
	 
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
            return int(self.config['comm_settings']['max_freq'])
        except Exception as e:
            return ''

    @max_freq.setter
    def max_freq(self, max_freq):
        self.config['comm_settings']['max_freq'] = str(max_freq)
    
    @property
    def min_freq(self):
        try:
            return int(self.config['comm_settings']['min_freq'])
        except Exception as e:
            return ''

    @min_freq.setter
    def min_freq(self, min_freq):
        self.config['comm_settings']['min_freq'] = str(min_freq)
        
    @property
    def average(self):
        try:
            return int(self.config['comm_settings']['average'])
        except Exception as e:
            return ''

    @average.setter
    def average(self, avg):
        self.config['comm_settings']['average'] = str(avg) 
        
    @property
    def IF(self):
        try:
            return int(self.config['comm_settings']['if'])
        except Exception as e:
            return ''
            
    @IF.setter
    def IF(self, IF):
        print(IF)
        self.config['comm_settings']['if'] = str(IF)
        
    @property
    def num_points(self):
        try:
            return int(self.config['comm_settings']['num_points']) 
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
            return int(self.config['comm_settings']['timeout'])
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
            self.session.write(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p'".format(str([i for i in range(1,portNum+1)])[1:-1], "Y:\\"+testName, portNum))
            print(self.session.query(";*OPC?"))
            #rm.list_resources()
            with open(self.vna_settings_file, 'w') as configfile:
                self.config.write(configfile)
            
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


    def close(self):
        self.session.close()
        self.rm.close()


 
if __name__ == '__main__':

    comm = Communication("TCPIP0::10.29.48.46::hislip0::INSTR")
    comm.aquire("123", 8)

