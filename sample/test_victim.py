import unittest
from sample.test_sample import TestSample
from sample.victim import Victim
from parameters.axext import AXEXT
from parameters.insertionloss import InsertionLoss
from parameters.fext import FEXT

class TestVictim(TestSample):
    def setUp(self):
        super(TestVictim, self).setUp()
        self._params = ["IL", "AXEXTD", "PSAXEXT", "PSAACRX"]

    def testParametersBuilding(self):
        il = InsertionLoss(self._e2ePorts, self._freq, self._mm)
        fext = FEXT(self._e2ePorts, self._freq, self._mm)
        axextd = [AXEXT(self._e2ePorts, self._freq, self._mm, fext, il) for i in range(4)]
        v = Victim(None, axextd)
        self.setMockSample(v)
        self.assertEqual(len(v._parameters), len(self._params))
        self.assertListEqual(list(v._parameters.keys()), self._params)


if __name__ == '__main__':
    unittest.main()