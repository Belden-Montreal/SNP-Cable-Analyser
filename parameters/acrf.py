from parameters.parameter import Parameter, diffDiffMatrix
from parameters.dataserie import PortPairDataSerie
from parameters.type import ParameterType

from math import sqrt, floor

class ACRF(Parameter):
    '''
        ACRF is calculated using the following formula : 

        ACRF_k = FEXT_k - IL_k
    '''
    def __init__(self, ports, freq, matrices, fext, il):
        self._fext = fext
        self._il   = il
        super(ACRF, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.ACRF

    @staticmethod
    def register(parameters):
        return lambda c, f, m: ACRF(c, f, m,
            parameters(ParameterType.FEXT),
            parameters(ParameterType.IL)
        )

    def computeDataSeries(self):
        # obtains data series from the dependent parameters
        fextSeries = self._fext.getDataSeries()
        ilSeries   = self._il.getDataSeries()

        # create the series for this parameter
        series = set()
        for fextSerie in fextSeries:
            (p1,p2) = fextSerie.getPorts()

            # find the corresponding wire
            ilSerie = [s for s in ilSeries if s.getPorts()[0] is p1]
            if len(ilSerie) != 1:
                raise ValueError

            # create the data serie
            series.add(PortPairDataSerie.fromSerie(fextSerie, ilSerie[0]))

        return series

    def computeParameter(self):
        # initialize the dictionaries for each series
        dbACRF = {serie: list() for serie in self._series}
        cpACRF = {serie: list() for serie in self._series}

        # get the series from the dependent parameters
        dbFEXT = self._fext.getParameter()
        dbIL   = self._il.getParameter()

        # compute the ACRF values from the other parameters
        wires = self._il.getDataSeries()
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                ilSerie = serie.getData()

                # compute the value from the other parameter
                cpValue = (dbFEXT[serie][f][0] - dbIL[ilSerie][f][0])
                dbValue = (dbFEXT[serie][f][0] - dbIL[ilSerie][f][0], 0)

                # add the value into the ACRF
                cpACRF[serie].append(cpValue)
                dbACRF[serie].append(dbValue)

        return (dbACRF, cpACRF)
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getFEXT(self):
        return self._fext

    def getIL(self):
        return self._il

    def getName(self):
        return "ACRF"
