from snpanalyzer.sample.plug import PlugSample
from snpanalyzer.parameters.type import ParameterType

class DelaySample(PlugSample):
    def getAvailableParameters(self):
        return [
            ParameterType.RL,
            ParameterType.PROPAGATION_DELAY,
        ]
    def getAvailableExport(self):
        return self.getAvailableParameters()
