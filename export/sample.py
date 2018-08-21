from export.configuration import ExportConfiguration
from export.parameter import ParameterExportConfiguration
from overrides import overrides

class SampleExportConfiguration(ExportConfiguration):
    def __init__(self, sample):
        self._sample     = sample
        self._parameters = dict()

        # by default, we export all parameters
        for (ptype, parameter) in sample.getParameters().items():
            self._parameters[ptype] = ParameterExportConfiguration(parameter)

    def addParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(True)

    def removeParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(False)

    def getParameters(self):
        return self._parameters

    @overrides
    def generateDocumentObject(self, prefix):
        return SampleDocumentObject(self)
        
    
