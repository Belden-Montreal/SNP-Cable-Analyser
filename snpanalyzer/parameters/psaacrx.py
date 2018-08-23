from parameters.parameter import Parameter, diffDiffMatrix
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

class PSAACRX(Parameter):
    '''
    PSAACRX represents both PSAACRN and PSAACRF.

    This parameter assumes that the PSAXEXT (PSANEXT or PSAFEXT) as been
    calculated prior to this one (see :class: `parameters.psaxext.PSAXEXT`).

    This parameter requires the insertion loss of the entire cable and is
    calculated using the following formula:

        PSAACRX_k = PSAXEXT_k - IL_k

    where PSAXEXT is either the PSANEXT or the PSAFEXT on the disturbed pair k
    and IL_k is the Insertion Loss on the disturbed pair k.
    '''
    def __init__(self, ports, freq, matrices, psaxext, il):
        self._psaxext = psaxext
        self._il      = il
        super(PSAACRX, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.PSAACRX

    # @staticmethod
    # def register(parameters):
    #     return lambda c, f, m: PSAACRX(c, f, m,

    #         parameters(ParameterType.IL)
    #     )

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        # obtains the data series from the dependent parameters
        psaxextSeries = self._psaxext.getDataSeries()
        ilSeries      = self._il.getDataSeries()

        # create the series for this parameter
        series = set()
        for psaxextSerie in psaxextSeries:
            port = psaxextSerie.getPort()

            # find the corresponding wire
            ilSerie = [s for s in ilSeries if s.getMainPort() == port]
            if len(ilSerie) != 1:
                raise ValueError

            # create the data serie
            series.add(PortDataSerie.fromSerie(psaxextSerie, data=ilSerie[0]))

        return series
    
    def computeParameter(self):
        # initialize the dictionaries for each serie
        dbPSAACRX = {serie: list() for serie in self._series}
        cpPSAACRX = {serie: list() for serie in self._series}

        # get the series from the dependent parameters
        dbPSAXEXT = self._psaxext.getParameter()
        dbIL      = self._il.getParameter()

        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                ilSerie = serie.getData()

                # compute the value from the other parameters
                cpValue = (dbPSAXEXT[serie][f][0] - dbIL[ilSerie][f][0])
                dbValue = (dbPSAXEXT[serie][f][0] - dbIL[ilSerie][f][0], 0)

                # add the value into the PSAACRX
                cpPSAACRX[serie].append(cpValue)
                dbPSAACRX[serie].append(dbValue)

        return (dbPSAACRX, cpPSAACRX)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getPSAXEXT(self):
        return self._psaxext

    def getIL(self):
        return self._il

    def getName(self):
        return "PSAACRX"

    def recalculate(self, psaxext):
        self._psaxext = psaxext
        (self._parameter, self._complexParameter) = self.computeParameter()

class PSAACRN(PSAACRX):
    @staticmethod
    def getType():
        return ParameterType.PSAACRN

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSAACRN(c, f, m,
            parameters(ParameterType.PSANEXT),
            parameters(ParameterType.IL)
        )

    def getName(self):
        return "PSAACRN"

class PSAACRF(PSAACRX):
    @staticmethod
    def getType():
        return ParameterType.PSAACRF

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSAACRF(c, f, m,
            parameters(ParameterType.PSAFEXT),
            parameters(ParameterType.IL)
        )

    def getName(self):
        return "PSAACRF"

