import unittest
from sample.test_sample import TestSample
from sample.end_to_end import EndToEnd

class TestEndToEnd(TestSample):
    def setUp(self):
        super(TestEndToEnd, self).setUp()
        self.params = ["RL", "IL", "NEXT", "Propagation Delay", "PSNEXT","FEXT", "PSFEXT", "ACRF", "PSACRF", "LCL", "LCTL", "TCL", "TCTL", "ELTCTL","CMRL", "CMNEXT", "CMDMNEXT", "CMDMRL", "DMCMNEXT", "DMCMRL"]

    def testParametersBuilding(self):
        ee = EndToEnd(None)
        ee._mm = self._mm
        ee._ports = self._ports
        ee._freq = self._freq
        ee.addParameters()
        self.assertEqual(len(ee._parameters), len(self.params))


if __name__ == '__main__':
    unittest.main()