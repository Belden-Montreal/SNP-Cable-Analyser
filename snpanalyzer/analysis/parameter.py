from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
from snpanalyzer.analysis.figure import FigureAnalysis, autoscaleY
from snpanalyzer.analysis.format import DataFormat, formatParameterData
from snpanalyzer.analysis.scale import PlotScale
from snpanalyzer.parameters.dataserie import GenericDataSerie
from overrides import overrides

class ParameterAnalysis(FigureAnalysis):
    def __init__(self, parameter, series=None, **kwargs):
        self._parameter = parameter
        self._series = set()
        super(ParameterAnalysis, self).__init__(**kwargs)

        # set grid
        self._axis.grid(which="both")
        self._axis.xaxis.set_major_formatter(ScalarFormatter())

        # by default, we show all series
        if series is None:
            series = self._parameter.getDataSeries()

        # show the selected series
        for serie in series:
            print(serie)
            self.addSerie(serie)

        # add the limit if it exists
        if self._parameter.getLimit():
            self.addLimit()

    def _getWorstVal(self):
        return self._parameter.getWorstValue()
    def _getWorstMar(self):
        return self._parameter.getWorstMargin()

    def setColorSeries(self,r,g,b):
        for serie in self._series:
            self._colors[serie] = (r, g, b)


    @overrides
    def _getXData(self, serie):
        if serie.getName() == "limit":
            dict_keys = self._parameter.getLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True)
            list_keys = [k for k in dict_keys]
            return list_keys
        if serie is not None:
            return self._parameter.getFrequencies()

    @overrides
    def _getYData(self, serie):
        if serie.getName() == "limit":
            if self._parameter.getName() == "Propagation Delay":
                dict_values = self._parameter.getLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=False).values()
                list_values=[v for v in dict_values]
                return list_values
            dict_values = self._parameter.getLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True).values()
            list_values =[v for v in dict_values]
            return list_values

        return formatParameterData(self._parameter, serie, self.getFormat())

    @overrides
    def _getLineStyle(self, serie):
        if serie.getName() == "limit":
            return "--"
        return "-"
    
    @overrides
    def _getLabel(self, serie):
        return serie.getName()

    @overrides
    def getDefaultTitle(self):
        return self._parameter.getName()

    @overrides
    def getDefaultScale(self):
        return PlotScale.LOGARITHMIC

    @overrides
    def getDefaultFormat(self):
        # we prefer magnitude when available
        formats = self._parameter.getAvailableFormats()
        if DataFormat.MAGNITUDE in formats:
            return DataFormat.MAGNITUDE

        # else choose any format
        return next(iter(formats))

    @overrides
    def getMaximumNumberOfLines(self):
        return len(self._parameter.getDataSeries())

    @overrides
    def getAvailableFormats(self):
        return self._parameter.getAvailableFormats()

    def addSerie(self, serie):
        # make sure the serie isn't already in the figure
       # print("addseries")
        if serie in self._series:

            return

        # add the serie
        self._series.add(serie)
        self._addLine(serie)



    def removeSerie(self, serie):
        # make sure the serie is in the figure
        if serie not in self._series:
            return

        # remove the serie
        self._removeLine(serie)
        self._series.discard(serie)

    def getParameter(self):
        return self._parameter

    def addLimit(self):
        serie = GenericDataSerie("limit")
        if not self._parameter.getLimit():
            return


        self._colors[serie] = (1, 0, 0) # red
        self.addSerie(serie)


    def removeLimit(self):
        serie = GenericDataSerie("limit")
        self.removeSerie(serie)