from sample.plug import PlugSample
from parameters.type import ParameterType

class DeembedSample(PlugSample):
    def __init__(self, snp, plugNext, plugNEXTDelay, cases):
        self._plugNEXT = plugNext
        self._plugNEXTDelay = plugNEXTDelay
        self._cases = cases
        super(DeembedSample, self).__init__(snp)

    def getDefaultParameters(self):
        return {
            ParameterType.PC_NEXT   : self._plugNEXT,
            ParameterType.NEXT_DELAY: self._plugNEXTDelay,
            ParameterType.CASES     : self._cases,
        }

    def getAvailableParameters(self):
        return {
            ParameterType.RL,
            ParameterType.NEXT,
            ParameterType.DNEXT,
            ParameterType.CASE,       
        }.union(self.getDefaultParameters().keys())

    def setStandard(self, standard):
        super(DeembedSample, self).setStandard(standard)
        for name, parameter in self._parameters.items():
            if name == "Case":
                parameter.setLimit(standard.limits["NEXT"])

class ReverseDeembedSample(DeembedSample):
    def __init__(self, snp, plugNext, plugDelay, jackOpenDelay, jackShortDelay, k1, k2, k3, cases):
        self._plugNEXT = plugNext
        self._jackOpenDelay = jackOpenDelay
        self._jackShortDelay = jackShortDelay
        self._plugDelay = plugDelay
        self._cases = cases
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        PlugSample.__init__(self, snp)

    def getDefaultParameters(self):
        return {
            ParameterType.PC_NEXT           : self._plugNEXT,
            ParameterType.PLUG_DELAY        : self._plugDelay,
            ParameterType.JACK_OPEN_DELAY   : self._jackOpenDelay,
            ParameterType.JACK_SHORT_DELAY  : self._jackShortDelay,
            ParameterType.CASES             : self._cases,
            ParameterType.K1                : self._k1,
            ParameterType.K2                : self._k2,
            ParameterType.K3                : self._k3,
        }

    def getAvailableParameters(self):
        return {
            ParameterType.RL,
            ParameterType.NEXT,
            ParameterType.JACK_DELAY,
            ParameterType.JACK_NEXT_DELAY,
            ParameterType.RDNEXT,
            ParameterType.RCASE,       
        }.union(self.getDefaultParameters().keys())