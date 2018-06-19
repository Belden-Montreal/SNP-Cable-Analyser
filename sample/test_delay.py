import unittest
from sample.test_sample import TestSample
from sample.delay import Delay
from parameters.returnloss import ReturnLoss
from parameters.propagationdelay import PropagationDelay

class TestDelay(TestSample):
    def setUp(self):
        super(TestDelay, self).setUp()
        self._params = ["RL", "Propagation Delay"]

    def testParametersBuilding(self):
        #rl = ReturnLoss(self._ports, self._freq, self._mm)
        #pd = PropagationDelay(self._ports, self._freq, self._mm, rl)
        d = Delay(None)
        self.setMockSample(d)
        self.assertEqual(len(d._parameters), len(self._params))
        self.assertListEqual(list(d._parameters.keys()), self._params)


if __name__ == '__main__':
    unittest.main()