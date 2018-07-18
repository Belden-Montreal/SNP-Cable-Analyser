from unittest import TestCase

from sample.test_sample import TestSample
from sample.plug import PlugSample

class TestPlugSample(TestSample, TestCase):
    def createSample(self):
        return PlugSample(self._snp)
        
    def getNumberOfPorts(self):
        return 8

    def getExpectedComputedParameters(self):
        return {
            "RL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "LCL",
            "TCL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL",
        }

    def getShouldntRunParameters(self):
        return set()
