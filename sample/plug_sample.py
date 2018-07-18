from sample.sample import Sample

class PlugSample(Sample):

    def __init__(self, snpFile, openDelay, shortDelay, dfOpenDelay, dfShortDelay, k1, k2, k3):
        self._openDelay = openDelay
        self._shortDelay = shortDelay
        self._dfOpenDelay = dfOpenDelay
        self._dfShortDelay = dfShortDelay
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        super(PlugSample, self).__init__(snpFile)

    def addParameters(self):
        parameters = [
            "RL",
            "DFDelay",
            "PlugDelay",
            "NEXTDelay",
            "CNEXT",
        ]
        self._parameters["DFShortDelay"] = self._dfShortDelay
        self._parameters["DFOpenDelay"] = self._dfOpenDelay
        self._parameters["PlugOpenDelay"] = self._openDelay
        self._parameters["PlugShortDelay"] = self._shortDelay
        self._parameters["k1"] = self._k1
        self._parameters["k2"] = self._k2
        self._parameters["k3"] = self._k3
        for parameter in parameters:
            self._parameters[parameter] = self._factory.getParameter(parameter)

    def recalculate(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._parameters["k1"] = k1
        self._parameters["k2"] = k2
        self._parameters["k3"] = k3
        self._parameters["PlugDelay"].recalculate(self._k1, self._k2, self._k3)
        self._parameters["NEXTDelay"].recalculate(self._parameters["PlugDelay"])
        self._parameters["CNEXT"].recalculate(self._parameters["NEXTDelay"])