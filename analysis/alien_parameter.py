from analysis.parameter import ParameterAnalysis
from parameters.dataserie import GenericDataSerie
from overrides import overrides

class AlienParameterAnalysis(ParameterAnalysis):
    def __init__(self, parameter, series=None, **kwargs):
        super(AlienParameterAnalysis, self).__init__(parameter, series, **kwargs)

        # add avg value
        self._average = list()
        self.addAverage()

        # add avg limit if it exists
        if self._parameter.getAverageLimit():
            self.addAverageLimit()

    @overrides
    def _getXData(self, serie):
        if serie.getName() == "average limit":
            return self._parameter.getAverageLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True).keys()
        return super(AlienParameterAnalysis, self)._getXData(serie)

    @overrides
    def _getYData(self, serie):
        if serie.getName() == "average limit":
            return self._parameter.getAverageLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True).values()
        if serie.getName() == "average":
            return self._average
        return super(AlienParameterAnalysis, self)._getYData(serie)

    @overrides
    def _getLineStyle(self, serie):
        if serie.getName() == "average limit":
            return "--"
        return super(AlienParameterAnalysis, self)._getLineStyle(serie)

    @overrides
    def getMaximumNumberOfLines(self):
        return len(self._parameter.getDataSeries())+1
    
    def addAverage(self):
        if len(self._parameter.getDataSeries()) == 0:
            return
        # calculate average value
        self._average = list()
        p = self._parameter.getParameter()
        for (f,_) in enumerate(self._parameter.getFrequencies()):
            value = 0
            for serie in p:
                value += p[serie][f][0]
            value /= len(self._parameter.getDataSeries())
            self._average.append(value)

        if len(self._average):
            serie = GenericDataSerie("average")
            self.removeSerie(serie)
            self.addSerie(serie)

    def removeAverage(self):
        serie = GenericDataSerie("average")
        self.removeSerie(serie)

    def addAverageLimit(self):
        serie = GenericDataSerie("average limit")

        if serie in self._series or not self._parameter.getAverageLimit():
            return
        self._colors[serie] = (0.40, 0.20, 0) # brown
        self.addSerie(serie)

    def removeAverageLimit(self):
        serie = GenericDataSerie("average limit")
        self.removeSerie(serie)