from unittest import TestCase
from sample.test_alien import TestAlienSample
from sample.disturber import DisturberSample
from parameters.type import ParameterType

class TestDisturberRemoteSample(TestAlienSample, TestCase):
    def createSample(self):
        return DisturberSample(self._snp, remote=True)

    def getExpectedComputedParameters(self):
        return {ParameterType.AFEXT}

    def getShouldntRunParameters(self):
        return {ParameterType.ANEXT}

class TestDisturberMainSample(TestAlienSample, TestCase):
    def createSample(self):
        return DisturberSample(self._snp)

    def getExpectedComputedParameters(self):
        return {ParameterType.ANEXT}

    def getShouldntRunParameters(self):
        return {ParameterType.AFEXT}
