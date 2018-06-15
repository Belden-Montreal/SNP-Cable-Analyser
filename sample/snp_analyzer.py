from skrf import Network as rf
from os.path import splitext, basename, getctime
import time

class SNPAnalyzer(object):
    def __init__(self, snpFile):
        self._rs = rf()
        self.readFile(snpFile)
        self._freq = self._rs.f #Array containing all the frequencies
        self._se = self._rs.s #single ended
        self.s2mm()
        
    def getFileInfo(self):
        return splitext(basename(self._snpFile)), time.ctime(getctime(self._snpFile))

    def s2mm(self):
        '''
        Convert single ended matrix to mixed mode:
        -------------------|---------------------
        |                  |                    |
        |                  |                    |
        |        DD        |        DC          |
        |                  |                    |
        |                  |                    |
        |------------------|--------------------| 
        |                  |                    |
        |        CD        |        CC          |
        |                  |                    |
        |                  |                    |
        -------------------|---------------------
                                     

        '''
        self._rs.se2gmm(p = int(self._rs.number_of_ports//2))    
        self._mm = self._rs.s #mixed mode

    def readFile(self, snpFile):
        f = open(snpFile, "r")
        self._rs.read_touchstone(f)
        f.close()
        self._snpFile = snpFile

    def getMM(self):
        return self._mm, self._freq, self._rs.number_of_ports//2

    def getFreqUnit(self):
        return self._rs.frequency.unit

    def setFreqUnit(self, unit):

        unit_dict = {"hz" : 1,
                     "khz" : 2,
                     "mhz" : 3,
                     "ghz" : 4}

        current_unit = unit_dict[self._rs.frequency.unit.lower()]
        desired_unit = unit_dict[unit.lower()]

        self._freq = self._freq * (1000 ** (current_unit - desired_unit))
        self._rs.frequency.unit = unit