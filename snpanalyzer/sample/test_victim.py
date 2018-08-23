from unittest import TestCase
from sample.test_alien import TestAlienSample
from sample.disturber import DisturberSample
from sample.victim import VictimSample
from parameters.type import ParameterType

class TestVictimSample(TestAlienSample):
    def isRemote(self):
        raise NotImplementedError

    def createSample(self):
        self._samples = {
            DisturberSample("disturber1.snp", remote=self.isRemote()),
            DisturberSample("disturber2.snp", remote=self.isRemote()),
            DisturberSample("disturber3.snp", remote=self.isRemote()),
            DisturberSample("disturber4.snp", remote=self.isRemote()),
        }
        return VictimSample(self._snp, self._samples)

class TestVictimRemoteSample(TestVictimSample, TestCase):
    def isRemote(self):
        return True

    def getExpectedComputedParameters(self):
        return {ParameterType.PSAFEXT, ParameterType.PSAACRF}

    def getShouldntRunParameters(self):
        return {ParameterType.AFEXTD}

class TestVictimMainSample(TestVictimSample, TestCase):
    def isRemote(self):
        return False

    def getExpectedComputedParameters(self):
        return {ParameterType.PSANEXT, ParameterType.PSAACRN}

    def getShouldntRunParameters(self):
        return {ParameterType.ANEXTD} 
