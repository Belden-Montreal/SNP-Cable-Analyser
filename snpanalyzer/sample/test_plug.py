from unittest import TestCase

from snpanalyzer.sample.test_sample import TestSample
from snpanalyzer.sample.plug import PlugSample
from snpanalyzer.parameters.type import ParameterType

class TestPlugSample(TestSample, TestCase):
    def createSample(self):
        return PlugSample(self._snp)
        
    def getNumberOfPorts(self):
        return 8

    def getExpectedComputedParameters(self):
        return {
            ParameterType.RL,
            ParameterType.NEXT,
            ParameterType.PROPAGATION_DELAY,
            ParameterType.PSNEXT,
            ParameterType.LCL,
            ParameterType.TCL,
            ParameterType.CMRL,
            ParameterType.CMNEXT,
            ParameterType.CMDMNEXT,
            ParameterType.CMDMRL,
            ParameterType.DMCMNEXT,
            ParameterType.DMCMRL, 
        }

    def getShouldntRunParameters(self):
        return set()
