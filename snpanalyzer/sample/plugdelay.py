from snpanalyzer.sample.plug import PlugSample
from snpanalyzer.parameters.type import ParameterType

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
            ParameterType.PLUG_OPEN_DELAY : self._openDelay,
            ParameterType.PLUG_SHORT_DELAY: self._shortDelay,
            ParameterType.DF_OPEN_DELAY   : self._dfOpenDelay,
            ParameterType.DF_SHORT_DELAY  : self._dfShortDelay,
            ParameterType.K1 : self._k1,
            ParameterType.K2 : self._k2,
            ParameterType.K3 : self._k3,
        }

    def getAvailableParameters(self):
        return [
            ParameterType.DF_DELAY,
            ParameterType.PLUG_DELAY,
            ParameterType.NEXT_DELAY,
            ParameterType.CORRECTED_NEXT,
        ]

    def recalculate(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        #re-create the parameters
        self._parameters = self.getDefaultParameters()
        for parameter in self.getAvailableParameters():
            if parameter in self._parameters.keys():
                continue
            self._parameters[parameter] = self._factory.getParameter(parameter)
