import unittest

from parameters.test_parameter import TestParameter
from parameters.tctl import TCTL

class TestTCTL(TestParameter):
    def createParameter(self):
        return TCTL(self._ports, self._freq, self._matrices)

    def testComputeParameter(self):
        parameter = self._parameter.getComplexParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports)//2)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[0][0], self._matrices[0, 4, 2])
        self.assertEqual(parameter[0][1], self._matrices[1, 4, 2])
        self.assertEqual(parameter[0][2], self._matrices[2, 4, 2])
        self.assertEqual(parameter[0][3], self._matrices[3, 4, 2])

        # check the values of the port 2
        self.assertEqual(parameter[1][0], self._matrices[0, 5, 3])
        self.assertEqual(parameter[1][1], self._matrices[1, 5, 3])
        self.assertEqual(parameter[1][2], self._matrices[2, 5, 3])
        self.assertEqual(parameter[1][3], self._matrices[3, 5, 3])

if __name__ == '__main__':
    unittest.main()
