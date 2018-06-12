import unittest

from parameters.test_parameter import TestParameter
from parameters.returnloss import ReturnLoss

class TestReturnLoss(TestParameter):
    def testComputeParameter(self):
        rl = ReturnLoss(self._ports, self._freq, self._matrices)
        parameter = rl.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._ports[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[3]]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[self._ports[0]][0], self._matrices[0, 0, 0])
        self.assertEqual(parameter[self._ports[0]][1], self._matrices[1, 0, 0])
        self.assertEqual(parameter[self._ports[0]][2], self._matrices[2, 0, 0])
        self.assertEqual(parameter[self._ports[0]][3], self._matrices[3, 0, 0])

        # check the values of the port 2
        self.assertEqual(parameter[self._ports[1]][0], self._matrices[0, 1, 1])
        self.assertEqual(parameter[self._ports[1]][1], self._matrices[1, 1, 1])
        self.assertEqual(parameter[self._ports[1]][2], self._matrices[2, 1, 1])
        self.assertEqual(parameter[self._ports[1]][3], self._matrices[3, 1, 1])

        # check the values of the port 3
        self.assertEqual(parameter[self._ports[2]][0], self._matrices[0, 2, 2])
        self.assertEqual(parameter[self._ports[2]][1], self._matrices[1, 2, 2])
        self.assertEqual(parameter[self._ports[2]][2], self._matrices[2, 2, 2])
        self.assertEqual(parameter[self._ports[2]][3], self._matrices[3, 2, 2])

        # check the values of the port 4
        self.assertEqual(parameter[self._ports[3]][0], self._matrices[0, 3, 3])
        self.assertEqual(parameter[self._ports[3]][1], self._matrices[1, 3, 3])
        self.assertEqual(parameter[self._ports[3]][2], self._matrices[2, 3, 3])
        self.assertEqual(parameter[self._ports[3]][3], self._matrices[3, 3, 3])

if __name__ == '__main__':
    unittest.main()
