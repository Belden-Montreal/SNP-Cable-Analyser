import unittest
from sample.test_sample import TestSample
from sample.disturber import Disturber

class TestDisturber(TestSample):
    def setUp(self):
        super(TestDisturber, self).setUp()
        self._params = ["IL","FEXT", "AXEXT"]

    def testParametersBuilding(self):
        d = Disturber(None)
        self.setMockSample(d)
        self.assertEqual(len(d._parameters), len(self._params))
        self.assertListEqual(list(d._parameters.keys()), self._params)


if __name__ == '__main__':
    unittest.main()