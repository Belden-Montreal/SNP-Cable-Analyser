from parameters.parameter import Parameter, takeClosest
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

import numpy as np

class PlugDelay(Parameter):
    def __init__(self, ports, freq, matrices, openDelay, shortDelay, dfDelay, k1, k2, k3):
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        self._dfDelay = dfDelay
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        super(PlugDelay, self).__init__(ports, freq, matrices)
        self._visible = False

    @staticmethod
    def getType():
        return ParameterType.PLUG_DELAY

    @staticmethod
    def register(parameters):
        return lambda c, f, m:PlugDelay(c, f, m,
            parameters(ParameterType.PLUG_OPEN_DELAY),
            parameters(ParameterType.PLUG_SHORT_DELAY),
            parameters(ParameterType.DF_DELAY),
            parameters(ParameterType.K1),
            parameters(ParameterType.K2),
            parameters(ParameterType.K3)
        )

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.DELAY,
        }

    def computeDataSeries(self):
        series = {PortDataSerie(port) for port in self._ports.getMainPorts()}

        # make sure all dependent parameters have the same data series
        if series != self._openDelay.getDataSeries():
            raise ValueError
        if series != self._shortDelay.getDataSeries():
            raise ValueError
        if series != self._dfDelay.getDataSeries():
            raise ValueError

        return series

    def computeParameter(self):
        dfDelay    = self._dfDelay.getParameter()
        openDelay  = self._openDelay.getParameter()
        shortDelay = self._shortDelay.getParameter()

        plugDelay = dict()
        for serie in self._series:
            #find the indexes of the points closest to 100 and 500 MHz
            f100, f500 = self.__getFrequenciesIndex(100, 500, self._freq)
            openAvg = np.mean(openDelay[serie][f100:f500])
            shortAvg = np.mean(shortDelay[serie][f100:f500])
            plugDelay[serie] = (openAvg + shortAvg - self._k1 - self._k2)/4.0 - dfDelay[serie] + self._k3
        
        return (plugDelay, None)

    def recalculate(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        (self._parameter, self._complexParameter) = self.computeParameter()

    def chooseMatrices(self, matrices):
        return None

    def getOpenDelay(self):
        return self._openDelay

    def getShortDelay(self):
        return self._shortDelay

    def getDFDelay(self):
        return self._dfDelay

    def getName(self):
        return "PlugDelay"

    def __getFrequenciesIndex(self, f1, f2, f):
        return takeClosest(f1, f), takeClosest(f2, f)+1

class JackDelay(PlugDelay):
    def __init__(self, ports, freq, matrices, openDelay, shortDelay, plugDelay, k1, k2, k3):
        super(JackDelay, self).__init__(ports, freq, matrices, openDelay, shortDelay, plugDelay, k1, k2, k3)

    @staticmethod
    def getType():
        return ParameterType.JACK_DELAY

    @staticmethod
    def register(parameters):
        return lambda c, f, m:PlugDelay(c, f, m,
            parameters(ParameterType.JACK_OPEN_DELAY),
            parameters(ParameterType.JACK_SHORT_DELAY),
            parameters(ParameterType.PLUG_DELAY),
            parameters(ParameterType.K1),
            parameters(ParameterType.K2),
            parameters(ParameterType.K3)
        )

    def getName(self):
        return "JackDelay"
        