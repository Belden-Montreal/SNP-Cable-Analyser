from sample.plug import PlugSample

class DeembedSample(PlugSample):
    def __init__(self, snp, plugNext, plugNEXTDelay, cases):
        self._plugNEXT = plugNext
        self._plugNEXTDelay = plugNEXTDelay
        self._cases = cases
        super(DeembedSample, self).__init__(snp)

    def getDefaultParameters(self):
        return {
            "PCNEXT"   : self._plugNEXT,
            "NEXTDelay": self._plugNEXTDelay,
            "Cases"    : self._cases,
        }

    def getAvailableParameters(self):
        return {
            "RL",
            "NEXT",
            "DNEXT",
            "Case",       
        }.union(self.getDefaultParameters().keys())
