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
            self._standard = None

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

    def getName(self):
         return self._name

    def getDate(self):
        return self._date

from app.node import Node
from widgets.parameter_widget import ParameterWidget
from widgets.main_widget import MainWidget
from PyQt5 import QtWidgets
class SampleNode(Node):
    def __init__(self, sample, project):
        super(SampleNode, self).__init__(sample.getName())
        self._dataObject = sample
        self._project = project

    def delete(self):
        self.parent().removeRow(self.row())
        self._project.removeSample(self._dataObject)

    def getWidgets(self):
        widgets = dict()
        widgets["main"] = None
        failParams = list()
        for name, param in self._dataObject.getParameters().items():
            try:
                if param.visible():
                    tab = ParameterWidget(name, param)
                    widgets[name] = tab
                    if not tab.hasPassed:
                        failParams.append(name)
            except:
                continue
        widgets["main"] = MainWidget(self._dataObject, failParams)
        return widgets

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)
