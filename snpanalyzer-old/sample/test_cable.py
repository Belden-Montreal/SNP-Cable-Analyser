from unittest import TestCase

from snpanalyzer.sample.test_sample import TestSample
from snpanalyzer.sample.cable import CableSample
from snpanalyzer.parameters.type import ParameterType

class TestCableSample(TestSample, TestCase):
    def createSample(self):
        return CableSample(self._snp)

    def getNumberOfPorts(self):
        return 16

    def getExpectedComputedParameters(self):
        return {
            ParameterType.RL,
            ParameterType.IL,
            ParameterType.NEXT,
            ParameterType.PROPAGATION_DELAY,
            ParameterType.PSNEXT,
            ParameterType.FEXT,
            ParameterType.PSFEXT,
            ParameterType.ACRF,
            ParameterType.PSACRF,
            ParameterType.LCL,
            ParameterType.LCTL,
            ParameterType.TCL,
            ParameterType.TCTL,
            ParameterType.ELTCTL,
            ParameterType.CMRL,
            ParameterType.CMNEXT,
            ParameterType.CMDMNEXT,
            ParameterType.CMDMRL,
            ParameterType.DMCMNEXT,
            ParameterType.DMCMRL, 
        }

    def getShouldntRunParameters(self):
        return set()

        
        
