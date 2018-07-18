from sample.test_cable import TestCableSample
from sample.delay import CableDelaySample

class TestCableDelaySample(TestCableSample):
    def createSample(self):
        return CableDelaySample(self._snp)

    def getExpectedComputedParameters(self):
        return {
            "RL",
            "Propagation Delay",
        }
