from snpanalyzer.export.configuration import ExportConfiguration
from snpanalyzer.document.parameter import ParameterDocumentObject
from snpanalyzer.analysis.scale import PlotScale
from snpanalyzer.analysis.format import DataFormat
from overrides import overrides

from snpanalyzer.document.case import caseDocumentObject
from snpanalyzer.document.cnext import cnextDocumentObject


class ParameterExportConfiguration(ExportConfiguration):
    def __init__(self, parameter, serie=None, cnext=False,case=False, **kwargs):
        super(ParameterExportConfiguration, self).__init__(**kwargs)

        self._parameter = parameter
        self._name = self._parameter.getName()
        self._series = dict()
        self._margins = dict()
        self._serie=serie
        self._cnext = cnext
        self._case = case
        self._exportFormat = dict()

        # Set the format for the PDF export
        self._exportFormat[DataFormat.MAGNITUDE] = [DataFormat.MAGNITUDE, DataFormat.PHASE]
        self._exportFormat[DataFormat.REAL] = [DataFormat.REAL,DataFormat.IMAGINARY]
        self._exportFormat[DataFormat.DELAY] = [DataFormat.DELAY]

        # by default, we want magnitude if possible
        if DataFormat.MAGNITUDE in parameter.getAvailableFormats():
            self._format = DataFormat.MAGNITUDE
        else:
            self._format = next(iter(parameter.getAvailableFormats()))

        # by default, we use logarithmic scale
        self._scale = PlotScale.LOGARITHMIC

        # by default, we export everything
        if serie:
            self._series[serie]=True
            self._margins[serie]=True
            self._name=serie.getName()
        else:
            for s in parameter.getDataSeries():
                self._series[s] = True
                self._margins[s] = True

    def addDataSerie(self, serie):
        if serie in self._series:
            self._series[serie] = True

    def removeDataSerie(self, serie):
        if serie in self._series:
            self._series[serie] = False

    def getDataSeries(self, limit=False):
        # print("Getting Data Series (Export")
        return self._series

    def addMargin(self, serie):
        if serie in self._margins:
            self._margins[serie] = True

    def removeMargin(self, serie):
        if serie in self._margins:
            self._margins[serie] = False

    def getMargins(self):
        return self._margins

    def setScale(self, scale):
        self._scale = scale

    def getScale(self):
        return self._scale

    def setFormat(self, pformat):
        self._format = pformat

    def getFormat(self):
        return self._format

    def getFormatExport(self):
        return self._exportFormat[self._format]

    def getParameter(self):
        return self._parameter

    def getName(self):
        return self._name

    def isCnext(self):
        return self._cnext

    def isEmb(self):
        return self._case
    @overrides
    def generateDocumentObject(self, root, prefix,plug=False,emb=False):
        if plug:
            return cnextDocumentObject(root, prefix, self)
        if emb:
            return caseDocumentObject(root, prefix, self)
        else:
            return ParameterDocumentObject(root, prefix, self)


