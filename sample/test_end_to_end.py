import unittest
from sample.test_sample import TestSample
from sample.end_to_end import EndToEnd

class TestEndToEnd(TestSample):
    def setUp(self):
        super(TestEndToEnd, self).setUp()
        self._params = ["RL", "IL", "NEXT", "Propagation Delay", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]

    def testParametersBuilding(self):
        ee = EndToEnd(None)
        self.setSample(ee)
        self.assertEqual(len(ee._parameters), len(self._params))
        self.assertListEqual(list(ee._parameters.keys()), self._params)


if __name__ == '__main__':
    unittest.main()