from sample.plug import PlugSample

class PlugDelaySample(PlugSample):
    def __init__(self, snp, openDelay, shortDelay, dfOpenDelay, dfShortDelay, k1, k2, k3, config=None):
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        self._dfOpenDelay = dfOpenDelay
        self._dfShortDelay = dfShortDelay
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        super(PlugDelaySample, self).__init__(snp, config=config)

    def getDefaultParameters(self):
        return {
            "PlugOpenDelay" : self._openDelay,
            "PlugShortDelay": self._shortDelay,
            "DFOpenDelay"   : self._dfOpenDelay,
            "DFShortDelay"  : self._dfShortDelay,
        }

    def getAvailableParameters(self):
        return {
            "DFDelay",
            "PlugDelay",
            "NEXTDelay",
            "CNEXT",
        }
