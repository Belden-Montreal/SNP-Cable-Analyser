from analysis.parameter import ParameterAnalysis
from analysis.figure import autoscaleY
from analysis.format import formatCaseData
from parameters.dataserie import GenericDataSerie
from overrides import overrides

class CaseAnalysis(ParameterAnalysis):
    def __init__(self, parameter, **kwargs):
        super(CaseAnalysis, self).__init__(parameter, **kwargs)

    @overrides
    def getMaximumNumberOfLines(self):
        n = 0
        for serie in self._parameter.getDataSeries():
            n += len(self._parameter.getParameter()[serie])
        return n

    @overrides
    def _getXData(self, serie):
        return super(CaseAnalysis, self)._getXData(serie)

    @overrides
    def _getYData(self, serie, case):
        if serie.getName() == "limit":
            return self._parameter.getLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True).values()
        if serie.getName() == "limit (Case 1 and 4)":
            lim = self._parameter.getLimit().evaluateDict({'f': self._parameter.getFrequencies()}, len(self._parameter.getFrequencies()), neg=True).values()
            return [y + 1.5 for y in lim]
        return formatCaseData(self._parameter, serie, case, self.getFormat())

    @overrides
    def _getLabel(self, identifier, case):
        if identifier.getName() == "limit" or identifier.getName() == "limit (Case 1 and 4)":
            return identifier.getName()
        return "Case {}".format(case)

    @overrides
    def _getLineStyle(self, identifier):
        if identifier.getName() == "limit (Case 1 and 4)":
            return "--"
        return super(CaseAnalysis, self)._getLineStyle(identifier)
    
    @overrides
    def addSerie(self, serie):
        # make sure the serie isn't already in the figure
        if serie in self._series:
            return

        # add the serie
        for n in self._parameter.getParameter()[serie]: 
            self._addLine(serie, n)
        self._series.add(serie)

    @overrides
    def _addLine(self, identifier, case):
        # make sure the identifier isn't already in the lines
        if case in self._lines:
            return

        # get the color of the line
        color = None
        if case in self._colors:
            color = self._colors[case]
        else:
            color = next(self._colormap)
            self._colors[case] = color

        # get the data
        x = self._getXData(identifier)
        y = self._getYData(identifier, case)
        label = self._getLabel(identifier, case)

        # add the line
        self._lines[case] = self._axis.plot(
            x, y,
            label=label,
            linewidth=0.6,
            c=color,
            linestyle=self._getLineStyle(identifier)
        )
        
        # scale Y axis to fit data
        autoscaleY(self._axis)

        # update the legend
        self._updateLegend()

    @overrides
    def removeSerie(self, serie):
        # make sure the serie is in the figure
        if serie not in self._series:
            return

        # remove the serie
        for n in self._parameter.getParameter()[serie]: 
            self._removeLine(serie, n)
        self._series.discard(serie)

    @overrides
    def _removeLine(self, identifier, case=0):
        # make sure the serie in preset
        if case not in self._lines:
            return

        # remove the line
        {line.remove() for line in self._lines.pop(case)}

        # update the legend
        self._updateLegend()

    @overrides
    def addLimit(self):
        serie = GenericDataSerie("limit")

        if not self._parameter.getLimit():
            return
        self._colors[serie] = (1, 0, 0) # red
        self._addLine(serie, serie)

    @overrides
    def removeLimit(self):
        serie = GenericDataSerie("limit")
        self._removeLine(serie, serie)

    def addSecondLimit(self):
        serie = GenericDataSerie("limit (Case 1 and 4)")

        if not self._parameter.getLimit():
            return
        self._colors[serie] = (0.40, 0.20, 0) # brown
        self._addLine(serie, serie)