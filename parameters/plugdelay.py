from parameters.parameter import PairedParameter, takeClosest
import numpy as np

class PlugDelay(PairedParameter):

    def __init__(self, ports, freq, matrices, openDelay, shortDelay, dfDelay, k1, k2, k3):
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        self._dfDelay = dfDelay
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        super(PlugDelay, self).__init__(ports, freq, matrices)
        self._visible = False

    def computePairs(self, ports):
        pairs = dict()
        for i in range(len(ports)):
            port,isRemote = ports[i]
            pairs[(i,i)] = (port, isRemote)
        return pairs

    def computeParameter(self):
        dfDelay = self._dfDelay.getParameter()
        openDelay = self._openDelay.getParameter()
        shortDelay = self._shortDelay.getParameter()
        plugDelay = dict()
        for port in self._ports:
            #find the indexes of the points closest to 100 and 500 MHz
            f100, f500 = self.__getFrequenciesIndex(100, 500, self._freq)
            openAvg = np.mean(openDelay[port][f100:f500])
            shortAvg = np.mean(shortDelay[port][f100:f500])
            plugDelay[port] = (openAvg + shortAvg - self._k1 - self._k2)/4.0 - dfDelay[port] + self._k3
        
        return plugDelay,None

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