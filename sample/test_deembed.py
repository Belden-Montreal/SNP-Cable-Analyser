from unittest.mock import MagicMock

from sample.test_plug import TestPlugSample
from sample.deembed import DeembedSample

class TestDeembedSample(TestPlugSample):
    def createSample(self):
        self._cnext = MagicMock()
        self._nextDelay = MagicMock()
        self._cases = MagicMock()
        return DeembedSample(
            None,
            self._cnext,
            self._nextDelay,
            self._cases
        )

    def getExpectedComputedParameters(self):
        return {
            "RL",
            "NEXT",
            "DNEXT",
            "Case",
        }

    def getShouldntRunParameters(self):
        return {
            "PCNEXT",
            "NEXTDelay",
            "Cases",
        }
