from unittest import TestCase

from sample.test_sample import TestSample
from sample.cable import CableSample

class TestCableSample(TestSample, TestCase):
    def createSample(self):
        return CableSample(self._snp)

    def getNumberOfPorts(self):
        return 16

    def getExpectedComputedParameters(self):
        return {
            "RL",
            "IL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "FEXT",
            "PSFEXT",
            "ACRF",
            "PSACRF",
            "LCL",
            "LCTL",
            "TCL",
            "TCTL",
            "ELTCTL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL",
        }

    def getShouldntRunParameters(self):
        return set()

        
        
