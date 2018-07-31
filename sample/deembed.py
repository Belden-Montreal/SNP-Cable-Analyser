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
