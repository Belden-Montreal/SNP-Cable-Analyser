import unittest
from sample.test_sample import TestSample
from sample.deembed import Deembed
from parameters.returnloss import ReturnLoss
from parameters.propagationdelay import PropagationDelay
from parameters.nextdelay import NEXTDelay
from parameters.correctednext import CorrectedNEXT
from parameters.plugdelay import PlugDelay
from parameters.dfdelay import DFDelay

class TestPlugSample(TestSample):
    def setUp(self):
        super(TestPlugSample, self).setUp()
        self._params = [
            "PCNEXT",
            "NEXTDelay",
            "DNEXT",
        ]

    def testParametersBuilding(self):
        rl = ReturnLoss(self._ports, self._freq, self._mm)
        pd = PropagationDelay(self._ports, self._freq, self._mm, rl)
        dfDelay = DFDelay(self._ports, self._freq, self._mm, pd, pd)
        plugDelay = PlugDelay(self._ports, self._freq, self._mm, pd, pd, dfDelay, 1, 2, 3)
        nextDelay = NEXTDelay(self._ports, self._freq, self._mm, plugDelay)
        cnext = CorrectedNEXT(self._ports, self._freq, self._mm, nextDelay)
        d = Deembed(None, cnext, nextDelay)
        self.setMockSample(d)
        self.assertEqual(len(d._parameters), len(self._params))
        self.assertListEqual(list(d._parameters.keys()), self._params)
        for param in d._parameters.values():
            self.assertTrue(param)

if __name__ == '__main__':
    unittest.main()