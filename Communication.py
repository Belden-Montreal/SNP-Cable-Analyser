import visa
import pyvisa
from calWizard import CalWizard

class Communication(object):

    def __init__(self, VNA_ADDRESS):
        self.VNA_ADDRESS = VNA_ADDRESS
        self.IF = 300
        self.min_freq = 10e5
        self.max_freq = 1e9
        self.num_points = 1000
        self.timeout = 500000
        self.ip_address = None
        self.visa_address = None
        self.average = 1
        
        #rm = pyvisa.highlevel.ResourceManager()
        #print(rm.list_resources())
        self.rm = visa.ResourceManager()
        self.session = self.rm.open_resource(self.VNA_ADDRESS)
        self.session.timeout = self.timeout
        

    @property
    def max_freq(self):
        return self._max_freq

    @max_freq.setter
    def max_freq(self, max_freq):
        self._max_freq = int(max_freq)
    
    @property
    def min_freq(self):
        return self._min_freq

    @min_freq.setter
    def min_freq(self, min_freq):
        self._min_freq = int(min_freq)
        
    @property
    def average(self):
        return self._avg

    @average.setter
    def average(self, avg):
        self._avg = avg

    @property
    def IF(self):
        return self._IF

    @IF.setter
    def IF(self, IF):
        self._IF = int(IF)


    @property
    def num_points(self):
        return self._num_points

    @num_points.setter 
    def num_points(self, num_points):
        self._num_points = num_points

    @property
    def ip_address(self):
        return self._ip

    @num_points.setter
    def ip_address(self, ip):
        self._ip = ip


    def getSNP(self):
        pass


    def calibrate(self):
        self.wizard = CalWizard(self)
        self.wizard.show()

    def whoAmI(self):
        return(self.session.query('*IDN?'))

    def aquire(self, testName, portNum):
        try:
            self.session.write("SENS:BWID " + str(self.IF))
            print("set if")
            self.session.write("SENS:FREQ:STAR "+str(self.min_freq))
            print("set min f")

            self.session.write("SENS:FREQ:STOP "+str(self.max_freq))
            print("set max f")
            self.session.write("SENS:SWE:TYPE LIN")
            self.session.write("SENS:SWE:POIN "+str(self.num_points))
            print("ok")
            self.session.write(":SENS:AVER:CLE")
            self.session.write(":ABOR")
            self.session.write(":INIT1:CONT ON")
            self.session.write(":TRIG:SOUR immediate")
            self.session.write("SENS:SWE:GRO:COUN 4") #{}".format(str(self.average))) # "+str(self.average))
            print("ok")
            

            self.session.write("SENS:SWE:MODE GRO;*OPC?")

            self.session.write(":CALC:PAR:SEL 'CH1_S11_1'")
            print("Start")
            print(self.session.query(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p';*OPC?".format(str([i for i in range(1,portNum+1)])[1:-1], "Y:\\"+testName, portNum)))

            #rm.list_resources()


        except visa.Error as ex:
            print(ex)

    def close(self):
        self.session.close()
        self.rm.close()

 
if __name__ == '__main__':

    comm = Communication("TCPIP0::10.29.48.46::hislip0::INSTR")
    comm.aquire("123",8)

