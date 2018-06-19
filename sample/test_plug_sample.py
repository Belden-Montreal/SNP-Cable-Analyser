import unittest
from sample.test_sample import TestSample
from sample.plug_sample import PlugSample
from parameters.returnloss import ReturnLoss
from parameters.propagationdelay import PropagationDelay

class TestPlugSample(TestSample):
    def setUp(self):
        super(TestPlugSample, self).setUp()
        self._params = [
            "DFShortDelay",
            "DFOpenDelay",
            "PlugOpenDelay",
            "PlugShortDelay",
            "k1",
            "k2",
            "k3",
            "DFDelay",
            "PlugDelay",
            "NEXTDelay",
            "CNEXT",
        ]

    def testParametersBuilding(self):
        rl = ReturnLoss(self._ports, self._freq, self._mm)
        pd = PropagationDelay(self._ports, self._freq, self._mm, rl)
        d = PlugSample(None, pd, pd, pd, pd, 1, 2, 3)
        self.setMockSample(d)
        self.assertEqual(len(d._parameters), len(self._params))
        self.assertListEqual(list(d._parameters.keys()), self._params)
        for param in d._parameters.values():
            self.assertTrue(param)

if __name__ == '__main__':
    unittest.main()