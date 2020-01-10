from snpanalyzer.sample.test_cable import TestCableSample
from snpanalyzer.sample.delay import CableDelaySample

class TestCableDelaySample(TestCableSample):
    def createSample(self):
        return CableDelaySample(self._snp)

    def getExpectedComputedParameters(self):
        return {
            "RL",
            "Propagation Delay",
        }
