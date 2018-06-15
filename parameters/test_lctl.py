import unittest

from parameters.test_parameter import TestParameter
from parameters.lctl import LCTL
from parameters.parameter import complex2db

class TestLCTL(TestParameter):
    def createParameter(self):
        return LCTL(self._ports, self._freq, self._matrices)


    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], complex2db(self._matrices[0, 0, 6]))
        self.assertAlmostEqual(parameter[0][1], complex2db(self._matrices[1, 0, 6]))
        self.assertAlmostEqual(parameter[0][2], complex2db(self._matrices[2, 0, 6]))
        self.assertAlmostEqual(parameter[0][3], complex2db(self._matrices[3, 0, 6]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], complex2db(self._matrices[0, 1, 7]))
        self.assertAlmostEqual(parameter[1][1], complex2db(self._matrices[1, 1, 7]))
        self.assertAlmostEqual(parameter[1][2], complex2db(self._matrices[2, 1, 7]))
        self.assertAlmostEqual(parameter[1][3], complex2db(self._matrices[3, 1, 7]))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[0][0], self._matrices[0, 0, 6])
        self.assertEqual(parameter[0][1], self._matrices[1, 0, 6])
        self.assertEqual(parameter[0][2], self._matrices[2, 0, 6])
        self.assertEqual(parameter[0][3], self._matrices[3, 0, 6])

        # check the values of the port 2
        self.assertEqual(parameter[1][0], self._matrices[0, 1, 7])
        self.assertEqual(parameter[1][1], self._matrices[1, 1, 7])
        self.assertEqual(parameter[1][2], self._matrices[2, 1, 7])
        self.assertEqual(parameter[1][3], self._matrices[3, 1, 7])

if __name__ == '__main__':
    unittest.main()
