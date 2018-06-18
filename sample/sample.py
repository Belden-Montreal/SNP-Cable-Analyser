from sample.snp_analyzer import SNPAnalyzer
from parameters.parameter_factory import ParameterFactory

PORTS_NAME = ["45", "12", "36", "78"]
class Sample(object):
    '''
    The sample class contains the measurements for one object
    '''
    def __init__(self, snpFile):
        self._parameters = dict()
        if snpFile:
            self._snp = SNPAnalyzer(snpFile)
            self._mm, self._freq, self._portsNumber = self._snp.getMM()
            (self._name, self._extension), self._date = self._snp.getFileInfo()
            self._ports = dict()
            self.setPorts()
            self._factory = ParameterFactory(self._ports, self._freq, self._mm, self._parameters)
            self.addParameters()
            self.standard = None

    def addParameters(self):
        raise NotImplementedError

    def setStandard(self, standard):
        for name, parameter in self._parameters.items():
                parameter.setLimit(standard.limits[name])

    def setPorts(self):
        for i in range(self._portsNumber):
            self._ports[i] = PORTS_NAME[i]
    
    def getName(self):
        return self._name

    def getFrequencies(self):
        return self._freq

    def getParameters(self):
        return self._parameters

    def getNumPorts(self):
        return self._portsNumber

