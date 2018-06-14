import unittest
from sample.test_sample import TestSample
from sample.single_ended import SingleEnded

class TestSingleEnded(TestSample):
    def setUp(self):
        super(TestSingleEnded, self).setUp()
        self._params = ["RL", "NEXT", "Propagation Delay", "PSNEXT", "LCL", "TCL", "CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]

    def testParametersBuilding(self):
        se = SingleEnded(None)
        self.setSample(se)
        self.assertEqual(len(se._parameters), len(self._params))
        self.assertListEqual(list(se._parameters.keys()), self._params)


if __name__ == '__main__':
    unittest.main()