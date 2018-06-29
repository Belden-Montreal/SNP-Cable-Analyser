from parameters.parameter import PairedParameter, takeClosest
import numpy as np

class DFDelay(PairedParameter):

    def __init__(self, ports, freq, matrices, openDelay, shortDelay):
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        super(DFDelay, self).__init__(ports, freq, matrices)
        self._visible = False

    def computePairs(self, ports):
        pairs = dict()
        for i in range(len(ports)):
            port,isRemote = ports[i]
            pairs[(i,i)] = (port,isRemote)
        return pairs

    def computeParameter(self):
        openDelay = self._openDelay.getParameter()
        shortDelay = self._shortDelay.getParameter()
        dfDelay = dict()
        for port in self._ports:
            #find the indexes of the points closest to 100 and 500 MHz
            f100, f500 = self.__getFrequenciesIndex(100, 500, self._freq)
            openAvg = np.mean(openDelay[port][f100:f500])
            shortAvg = np.mean(shortDelay[port][f100:f500])
            dfDelay[port] = (openAvg + shortAvg)/4.0
        return dfDelay,None

    def chooseMatrices(self, matrices):
        return None

    def getOpenDelay(self):
        return self._openDelay

    def getShortDelay(self):
        return self._shortDelay

    def getName(self):
        return "DFDelay"

    def __getFrequenciesIndex(self, f1, f2, f):
        return takeClosest(f1, f), takeClosest(f2, f)+1