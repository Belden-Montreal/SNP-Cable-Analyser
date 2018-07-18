from unittest import TestCase
from sample.test_alien import TestAlienSample
from sample.disturber import DisturberSample

class TestDisturberRemoteSample(TestAlienSample, TestCase):
    def createSample(self):
        return DisturberSample(self._snp, remote=True)

    def getExpectedComputedParameters(self):
        return {"AFEXT"}

    def getShouldntRunParameters(self):
        return {"ANEXT"}

class TestDisturberMainSample(TestAlienSample, TestCase):
    def createSample(self):
        return DisturberSample(self._snp)

    def getExpectedComputedParameters(self):
        return {"ANEXT"}

    def getShouldntRunParameters(self):
        return {"AFEXT"}
