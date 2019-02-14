from snpanalyzer.parameters.factory import ParameterFactory
from snpanalyzer.analysis.parameter import ParameterAnalysis
from snpanalyzer.document.sample import SampleDocumentObject

from skrf import Network
from time import ctime
from os.path import getctime, basename

class Sample(object):
    def __init__(self, snp, config=None, standard=None):
        # load the network
        (self._network, self._date) = Sample.loadSNP(snp)

        # get the name of the file
        self._name = basename(snp)
        self._fileName = snp

        # get the network's configuration
        if config:
            self._config = config
        else:
            self._config = self.getDefaultConfiguration()

        # convert the network into mixed mode
        self._network.se2gmm(self.getNumPorts())

        # various initialisation
        self._parameters = self.getDefaultParameters()

        # change frequency unit
        self._network.f = self._network.f * (1000 ** -2)
        self._network.frequency.unit = 'mhz'
        print(len(self._config.getPorts()), self.getNumPorts())

        # config and network should have the same number of ports
        if len(self._config.getPorts()) != self.getNumPorts():
            print(self.getNumPorts())
            raise ValueError

        # create the parameter factory
        self._factory = self.getFactory()

        # create the parameter
        for parameter in self.getAvailableParameters():
            if parameter in self._parameters.keys():
                continue
            self._parameters[parameter] = self._factory.getParameter(parameter)
        
        #self.createAnalyses()

         #  set the standard
        if standard:
            self.setStandard(standard)
        else:
            self._standard = None

    def createAnalyses(self, desiredParam=None):
        self._analyses = dict()
        
        for (ptype, parameter) in self._parameters.items():
            try:
                if parameter.getName() == desiredParam or desiredParam == None:
                    print(str(ptype) + ", " +  str(parameter) + "123")
                    
                    # try:
                    #     del self._analyses[ptype]
                    # except:
                    #     print("Doesnt exist yet !!")
                    self._analyses[ptype] = ParameterAnalysis(parameter)
                    print("doing analysis on : " + parameter.getName())
                    #print(ptype+" Done")

            except:
                continue

    @staticmethod
    def loadSNP(snp):
        # load the touchstone file
        network = Network()
        snpfile = open(snp, 'r')
        network.read_touchstone(snpfile)
        snpfile.close()

        # get the date from the file
        date = ctime(getctime(snp))

        return (network, date)

    @staticmethod
    def getDefaultConfiguration():
        raise NotImplementedError

    @staticmethod
    def getDefaultParameters():
        raise NotImplementedError

    def setStandard(self, standard):
        self._standard = standard
        for (name, parameter) in self._parameters.items():
            if name.name in standard.limits:
                parameter.setLimit(standard.limits[name.name])
                self._analyses[name].addLimit()

    def getStandard(self):
        return self._standard

    def getFactory(self):
        return ParameterFactory(
            self.getConfig(),
            self.getFrequencies(),
            self.getMatrices(),
            self.getParameters(),
        )

    def getConfiguration(self):
        return self._config

    def getAvailableParameters(self):
        raise NotImplementedError

    def getNetwork(self):
        return self._network

    def getMatrices(self):
        return self._network.s

    def getConfig(self):
        return self._config

    def getFrequencies(self):
        return self._network.f

    def getNumPorts(self):
        # we divide by two since we're in mixed mode
        return self._network.number_of_ports//2

    def getParameter(self, name):
        if name not in self._parameters.keys():
            return None
        return self._parameters[name]

    def getParameters(self):
        return self._parameters

    def getAnalysis(self, desiredParam):

        # for ptype, param in self.getParameters().items():
        #     print("Desired = "+str(desiredParam))
        #     print("Param.name = "+str(param.getName()))

        #     if param.visible():
        #         if param.getName() is desiredParam:
        #             print("Found it")
        #             return self._analyses[ptype]   

        # return None

        for (ptype, parameter) in self._parameters.items():
            try:
                #print(str(ptype) + ", " +  str(parameter) + "123")
                if parameter.getName() == desiredParam:
                    print(str(ptype) + " IN getAnalysis")
                    return self._analyses[ptype]                     
            except:
                continue
        print("Analysis non existant")
        return None 

        
        

    def getAnalyses(self):
        return self._analyses

    def getDate(self):
        return self._date

    def getName(self):
        return self._name

    def getFileName(self):
        return self._fileName

    def generateDocumentObject(self, prefix):
        return SampleDocumentObject(prefix, self)

    def getSamples(self):
        return self

#   PORTS_NAME = ["45", "12", "36", "78"]
# class Sample2(object):
#     '''
#     The sample class contains the measurements for one object
#     '''
#     def __init__(self, snpFile, standard=None):
#         self._parameters = dict()
#         if snpFile:
#             self._snp = SNPAnalyzer(snpFile)
#             self._mm, self._freq, self._portsNumber = self._snp.getMM()
#             (self._name, self._extension), self._date = self._snp.getFileInfo()
#             self._ports = dict()
#             self.setPorts()
#             self._factory = ParameterFactory(self._ports, self._freq, self._mm, self._parameters)
#             self.addParameters()
#             if standard:
#                 self.setStandard(standard)
#             else:
#                 self._standard = None

#     def addParameters(self):
#         raise NotImplementedError

#     def setStandard(self, standard):
#         self._standard = standard
#         for name, parameter in self._parameters.items():
#             if name in standard.limits:
#                 parameter.setLimit(standard.limits[name])

#     '''
#     Ports follow the following format: {port_number: (port_name, isRemote)}
#     '''
#     def setPorts(self):
#         for i in range(self._portsNumber):
#             self._ports[i] = (PORTS_NAME[i], False)

#     def getFrequencies(self):
#         return self._freq

#     def getParameters(self):
#         return self._parameters

#     def getNumPorts(self):
#         return self._portsNumber

#     def getStandard(self):
#         return self._standard

#     def getName(self):
#          return self._name

#     def getFileName(self):
#         return self._snp.getFile()

#     def getDate(self):
#         return self._date

from snpanalyzer.app.node import Node
from snpanalyzer.gui.widget.parameter_widget import ParameterWidget
from snpanalyzer.gui.widget.main_widget import MainWidget
from PyQt5 import QtWidgets

class SampleNode(Node):
    def __init__(self, sample, project):
        super(SampleNode, self).__init__(sample.getName())
        self._dataObject = sample
        self._project = project
        self._mainTab = None
        self._paramTabs = dict()

    def delete(self):
        self.parent().removeRow(self.row())
        self._project.removeSample(self._dataObject)

    def getWidgets(self, none):
        widgets = dict()
        
        widgets["main"] = None
        failParams = list()
        for ptype, param in self._dataObject.getParameters().items():
            #try:
            if param.visible():
                if ptype.name not in self._paramTabs:
                    self._paramTabs[ptype.name] = ParameterWidget(param.getName(), param, None)#self._dataObject.getAnalysis(ptype))
                    print("pytpe name: "+ str(ptype.name))

                widgets[param.getName()] = self._paramTabs[ptype.name]
                if not self._paramTabs[ptype.name].hasPassed:
                        failParams.append(ptype.name)
            #except:
                #print("Fail")
                #continue
        if not self._mainTab:
            self._mainTab = MainWidget(self._dataObject, failParams)
        else:
            self._mainTab.updateParams(failParams)
        widgets["main"] = self._mainTab

        return widgets

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)
        self._mainTab = None
        self._paramTabs = dict()
