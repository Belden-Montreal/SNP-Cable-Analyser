from export.configuration import ExportConfiguration
from export.parameter import ParameterExportConfiguration
from document.sample import SampleDocumentObject
from overrides import overrides

class SampleExportConfiguration(ExportConfiguration):
    def __init__(self, sample, **kwargs):
        super(SampleExportConfiguration, self).__init__(**kwargs)
        self._sample     = sample
        self._parameters = dict()

        # by default, we export all parameters
        for (ptype, parameter) in sample.getParameters().items():
            self._parameters[ptype] = ParameterExportConfiguration(parameter)
            self._parameters[ptype].setExport(True)

    def addParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(True)

    def removeParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(False)

    def getParameters(self):
        return self._parameters

    def getSample(self):
        return self._sample

    @overrides
    def generateDocumentObject(self, root, prefix):
        return SampleDocumentObject(root, prefix, self)
        
    
