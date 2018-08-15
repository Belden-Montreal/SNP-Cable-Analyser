from parameters.parameter import Parameter, takeClosest
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

import numpy as np

class DFDelay(Parameter):
    def __init__(self, ports, freq, matrices, openDelay, shortDelay):
        self._openDelay  = openDelay
        self._shortDelay = shortDelay
        self._visible    = False
        super(DFDelay, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.DF_DELAY

    @staticmethod
    def register(parameters):
        return lambda c, f, m: DFDelay(c, f, m,
            parameters(ParameterType.DF_OPEN_DELAY),
            parameters(ParameterType.DF_SHORT_DELAY)
        )

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.DELAY,
        }

    def computeDataSeries(self):
        return {PortDataSerie(port) for port in self._ports.getPorts()}

    def computeParameter(self):
        openDelay  = self._openDelay.getParameter()
        shortDelay = self._shortDelay.getParameter()

        dfDelay = dict()
        for serie in self._series:
            # find the indexes of the points closest to 100 and 500 MHz
            (f100, f500) = self.__getFrequenciesIndex(100, 500, self._freq)

            openAvg  = np.mean(openDelay[serie][f100:f500])
            shortAvg = np.mean(shortDelay[serie][f100:f500])
            dfDelay[serie] = (openAvg + shortAvg)/4.0
        return (dfDelay, None)

    def chooseMatrices(self, matrices):
        return None

    def getOpenDelay(self):
        return self._openDelay

    def getShortDelay(self):
        return self._shortDelay

    def getName(self):
        return "DFDelay"

    def __getFrequenciesIndex(self, f1, f2, f):
        return (takeClosest(f1, f), takeClosest(f2, f)+1)
