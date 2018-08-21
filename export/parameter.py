from document.parameter import ParameterDocumentObject
from export.configuration import ExportConfiguration
from analysis.scale import PlotScale
from analysis.format import DataFormat
from overrides import overrides

class ParameterExportConfiguration(ExportConfiguration):
    def __init__(self, parameter, **kwargs):
        super(ParameterExportConfiguration, self).__init__(**kwargs)

        self._parameter = parameter
        self._series    = dict()
        self._margins   = dict()

        # by default, we want magnitude if possible
        if DataFormat.MAGNITUDE in parameter.getAvailableFormats():
            self._format = DataFormat.MAGNITUDE
        else:
            self._format = next(iter(parameter.getAvailableFormats()))

        # by default, we use logarithmic scale
        self._scale = PlotScale.LOGARITHMIC

        # by default, we export everything
        for serie in parameter.getDataSeries():
            self._series[serie]  = True
            self._margins[serie] = True

    def addDataSerie(self, serie):
        if serie in self._series:
            self._series[serie] = True

    def removeDataSerie(self, serie):
        if serie in self._series:
            self._series[serie] = False

    def getDataSeries(self):
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

    def getParameter(self):
        return self._parameter

    @overrides
    def generateDocumentObject(self, prefix):
        return ParameterDocumentObject(prefix, self)
