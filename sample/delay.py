from sample.cable import CableSample

class CableDelaySample(CableSample):
    def getAvailableParameters(self):
        return {
            "RL",
            "Propagation Delay",
        }
