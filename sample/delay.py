from sample.plug import PlugSample
from parameters.type import ParameterType

class DelaySample(PlugSample):
    def getAvailableParameters(self):
        return [
            ParameterType.RL,
            ParameterType.PROPAGATION_DELAY,
        ]
