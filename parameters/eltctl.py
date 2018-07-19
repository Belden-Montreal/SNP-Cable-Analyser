from parameters.parameter import Parameter
from parameters.type import ParameterType

class ELTCTL(Parameter):
    '''
    ELTCTL (Equal Level Transverse Conversion Transfer Loss) is calculated
    using the following formula:

        ELTCTL_k = TCTL_k - IL_k
    '''
    def __init__(self, ports, freq, matrices, il, tctl):
        self._il = il
        self._tctl = tctl
        super(ELTCTL, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.ELTCTL

    @staticmethod
    def register(parameters):
        return lambda c, f, m: DNEXT(c, f, m,
            parameters(ParameterType.IL),
            parameters(ParameterType.TCTL)
        )

    def computeDataSeries(self):
        # make sure all dependent parameters have the same data series
        if self._il.getDataSeries() != self._tctl.getDataSeries():
            raise ValueError

        # use either IL or TCTL series
        return self._il.getDataSeries()

    def computeParameter(self):
        dbELTCTL = {serie: list() for serie in self._series}
        cpELTCTL = {serie: list() for serie in self._series}

        dbIL   = self._il.getParameter()
        dbTCTL = self._tctl.getParameter()

        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                dbValue = (dbTCTL[serie][f][0] - dbIL[serie][f][0], 0)
                cpValue = (dbTCTL[serie][f][0] - dbIL[serie][f][0])

                dbELTCTL[serie].append(dbValue)
                cpELTCTL[serie].append(cpValue)

        return (dbELTCTL, cpELTCTL)

    def chooseMatrices(self, matrices):
        return None

    def getIL(self):
        return self._il

    def getTCTL(self):
        return self._tctl

    def getName(self):
        return "ELTCTL"
