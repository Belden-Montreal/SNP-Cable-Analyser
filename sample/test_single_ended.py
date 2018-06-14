import unittest
from sample.test_sample import TestSample
from sample.single_ended import SingleEnded

class TestSingleEnded(TestSample):
    def setUp(self):
        super(TestSingleEnded, self).setUp()
        self.params = ["RL", "NEXT", "Propagation Delay", "PSNEXT", "LCL", "TCL", "CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]

    def testParametersBuilding(self):
        se = SingleEnded(None)
        se._mm = self._mm
        se._ports = self._ports
        se._freq = self._freq
        se.addParameters()
        self.assertEqual(len(se._parameters), len(self.params))


if __name__ == '__main__':
    unittest.main()