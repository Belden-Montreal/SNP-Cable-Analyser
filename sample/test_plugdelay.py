from unittest.mock import MagicMock

from sample.test_plug import TestPlugSample
from sample.plugdelay import PlugDelaySample

class TestPlugDelaySample(TestPlugSample):
    def createSample(self):
        self._openDelay = MagicMock()
        self._shortDelay = MagicMock()
        self._dfOpenDelay = MagicMock()
        self._dfShortDelay = MagicMock()
        self._k1 = MagicMock()
        self._k2 = MagicMock()
        self._k3 = MagicMock()
        return PlugDelaySample(
            self._snp,
            self._openDelay,
            self._shortDelay,
            self._dfOpenDelay,
            self._dfShortDelay,
            self._k1,
            self._k2,
            self._k3
        )

    def getExpectedComputedParameters(self):
        return {
            "DFDelay",
            "PlugDelay",
            "NEXTDelay",
            "CNEXT",
        }

    def getShouldntRunParameters(self):
        return {
            "PlugOpenDelay",
            "PlugShortDelay",
            "DFOpenDelay",
            "DFShortDelay",
        }