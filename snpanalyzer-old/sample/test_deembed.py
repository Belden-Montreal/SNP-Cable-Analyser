from unittest.mock import MagicMock

from snpanalyzer.sample.test_plug import TestPlugSample
from snpanalyzer.sample.deembed import DeembedSample
from snpanalyzer.parameters.type import ParameterType

class TestDeembedSample(TestPlugSample):
    def createSample(self):
        self._cnext = MagicMock()
        self._nextDelay = MagicMock()
        self._cases = MagicMock()
        return DeembedSample(
            "",
            self._cnext,
            self._nextDelay,
            self._cases
        )

    def getExpectedComputedParameters(self):
        return {
            ParameterType.RL,
            ParameterType.NEXT,
            ParameterType.DNEXT,
            ParameterType.CASE,
        }

    def getShouldntRunParameters(self):
        return {
            ParameterType.PC_NEXT,
            ParameterType.NEXT_DELAY,
            ParameterType.CASES,
        }
