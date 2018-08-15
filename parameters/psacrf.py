from parameters.parameter import Parameter, diffDiffMatrix
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType

class PSACRF(Parameter):
    '''
    PSACRF is calculated using the following formula:

        PSACRF_k = PSFEXT_k - IL_k
        
    where PSFEXT_k is the PSFEXT on wire k and IL_k is the Insertion Loss on wire k
    '''
    def __init__(self, ports, freq, matrices, psfext, il):
        self._psfext = psfext
        self._il = il
        super(PSACRF, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.PSACRF

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSACRF(c, f, m,
            parameters(ParameterType.PSFEXT),
            parameters(ParameterType.IL)
        )

    def computeDataSeries(self):
        # obtains the data series from the dependent parameters
        psfextSeries = self._psfext.getDataSeries()
        ilSeries     = self._il.getDataSeries()

        # create the series for this parameter
        series = set()
        for psfextSerie in psfextSeries:
            p = psfextSerie.getPort()

            # find the corresponding wire
            ilSerie =  [s for s in ilSeries if s.getMainPort() == p]
            if len(ilSerie) != 1:
                raise ValueError

            # create the data serie
            series.add(PortDataSerie.fromSerie(psfextSerie, data=ilSerie[0]))

        return series
    
    def computeParameter(self):
        # initialize the dictionaries for each serie
        dbPSACRF = {serie: list() for serie in self._series}
        cpPSACRF = {serie: list() for serie in self._series}
        
        # get the series frm the dependent parameters
        dbPSFEXT = self._psfext.getParameter()
        dbIL     = self._il.getParameter()

        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                ilSerie = serie.getData()

                # compute the value from the ther parameter
                cpValue = (dbPSFEXT[serie][f][0] - dbIL[ilSerie][f][0])
                dbValue = (dbPSFEXT[serie][f][0] - dbIL[ilSerie][f][0], 0)

                # add the value into the ACRF
                cpPSACRF[serie].append(cpValue)
                dbPSACRF[serie].append(dbValue)

        return (dbPSACRF, cpPSACRF)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getPSFEXT(self):
        return self._psfext

    def getIL(self):
        return self._il

    def getName(self):
        return "PSACRF"
