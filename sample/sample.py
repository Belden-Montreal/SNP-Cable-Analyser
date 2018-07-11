from sample.snp_analyzer import SNPAnalyzer
from parameters.parameter_factory import ParameterFactory
from app.component import Component
from app.component_tree_item import ComponentTreeItem

PORTS_NAME = ["45", "12", "36", "78"]
class Sample(Component):
    '''
    The sample class contains the measurements for one object
    '''
    def __init__(self, snpFile):
        self._parameters = dict()
        self._snp = SNPAnalyzer(snpFile)
        self._mm, self._freq, self._portsNumber = self._snp.getMM()
        (name, self._extension), date = self._snp.getFileInfo()
        super(Sample, self).__init__(name)
        self._date = date
        self._ports = dict()
        self.setPorts()
        self._factory = ParameterFactory(self._ports, self._freq, self._mm, self._parameters)
        self.addParameters()
        self._standard = None
        self._generateTreeStructure()

    def addParameters(self):
        raise NotImplementedError

    def setStandard(self, standard):
        self._standard = standard
        for name, parameter in self._parameters.items():
            if name in standard.limits:
                parameter.setLimit(standard.limits[name])

    '''
    Ports follow the following format: {port_number: (port_name, isRemote)}
    '''
    def setPorts(self):
        for i in range(self._portsNumber):
            self._ports[i] = (PORTS_NAME[i], False)

    def getFrequencies(self):
        return self._freq

    def getParameters(self):
        return self._parameters

    def getNumPorts(self):
        return self._portsNumber

    def getStandard(self):
        return self._standard

    def _generateTreeStructure(self):
        self._treeItem = ComponentTreeItem(self)
