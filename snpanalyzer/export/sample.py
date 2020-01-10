from snpanalyzer.export.configuration import ExportConfiguration
from snpanalyzer.export.parameter import ParameterExportConfiguration
from snpanalyzer.document.sample import SampleDocumentObject
from snpanalyzer.parameters.type import ParameterType
from overrides import overrides


class SampleExportConfiguration(ExportConfiguration):
    def __init__(self, sample, cnext=False, case = False, **kwargs):
        super(SampleExportConfiguration, self).__init__(**kwargs)
        self._sample = sample
        self._parameters = dict()
        self.name = sample.getName()

        # by default, we export all parameters
        if cnext or case:
            print(self._sample)
            series = self._sample.getDataSeries()
            for serie in series:
                self._parameters[serie]= ParameterExportConfiguration(self._sample, serie= serie, cnext= cnext, case=case)
                self._parameters[serie].setExport(True)

        else:
            for (ptype, parameter) in sample.getParam().items():
                if ptype in (ParameterType.CASE, ParameterType.CORRECTED_NEXT):
                    continue
                if type(parameter) is list:
                    for p in parameter:
                        self._parameters[ptype] = ParameterExportConfiguration(p)
                else:
                    self._parameters[ptype] = ParameterExportConfiguration(parameter)
                self._parameters[ptype].setExport(True)

    def addParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(True)

    def setName(self, name):
        self.name= name

    def removeParameter(self, parameter):
        if parameter in self._parameters:
            self._parameters[parameter].setExport(False)

    def getParameters(self):
        return self._parameters

    def getName(self):
        return self.name

    def getSample(self):
        return self._sample

    @overrides
    def generateDocumentObject(self, root, prefix):
        return SampleDocumentObject(root, prefix, self)


