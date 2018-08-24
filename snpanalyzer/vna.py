from snpanalyzer.gui.wizard.calibration import CalibrationWizard
from snpanalyzer.config.vna import VNAConfiguration

from visa import Error as VisaError
from pyvisa import ResourceManager

class VNA(object):
    def __init__(self, config=None):
        self._connected = False
        if config is None:
            config = VNAConfiguration()
        self._config = config
        self._manager = None
        self._session = None

    def connect(self):
        self._manager = ResourceManager()
        self._session = self._manager.open_resouce(self._config.getAddress())
        self._connected = True

    def disconnect(self):
        self._session.close()
        self._session = None
        self._manager.close()
        self._manager = None
        self.connected = False

    def acquire(self, name, ports):
        if self._manager is None:
            return

        config = self._config

        self.session.timeout = self._config.getTimeout()
        self.session.write("SENS:BWID "      + str(config.getBandwidth()))
        self.session.write("SENS:FREQ:STAR " + str(config.getMinimumFrequency()))
        self.session.write("SENS:FREQ:STOP " + str(config.getMaximumFrequency()))
        self.session.write("SENS:SWE:TYPE LIN")
        self.session.write("SENS:SWE:POIN "  + str(config.getResolution()))
        self.session.write(":SENS:AVER:CLE")
        self.session.write(":ABOR")
        self.session.write("SENS:AVER:COUN " + str(config.getAverage()))
        self.session.write(":INIT1:CONT ON")
        self.session.write(":TRIG:SOUR immediate")
        self.session.write("SENS:SWE:GRO:COUN 4")
        self.session.write("SENS:SWE:MODE GRO;*OPC?")
        self.session.write(":CALC:PAR:SEL 'CH1_S11_1'")
        self.session.write(":CALC:DATA:SNP:PORT:SAVE '{}', '{}.s{}p'".format(
            str([i for i in range(1,ports+1)])[1:-1], "Y:\\"+name, ports))

    def calibrate(self):
        wizard = CalibrationWizard(self)
        wizard.show()

    def whoAmI(self):
        if self._session is None:
            return "None"
        return self._session.query('*IDN?')

