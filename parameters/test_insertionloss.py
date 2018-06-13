import unittest

from parameters.test_parameter import TestParameter
from parameters.insertionloss import InsertionLoss

class TestInsertionLoss(TestParameter):
    def testComputeParameter(self):
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        parameter = il.getComplexParameter()

        # there should be a parameter for half the ports
        self.assertEqual(len(parameter), len(self._ports)//2)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[0][0], self._matrices[0, 0, len(self._ports)//2])
        self.assertEqual(parameter[0][1], self._matrices[1, 0, len(self._ports)//2])
        self.assertEqual(parameter[0][2], self._matrices[2, 0, len(self._ports)//2])
        self.assertEqual(parameter[0][3], self._matrices[3, 0, len(self._ports)//2])

        # check the values of the port 2
        self.assertEqual(parameter[1][0], self._matrices[0, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[1][1], self._matrices[1, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[1][2], self._matrices[2, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[1][3], self._matrices[3, 1, 1+len(self._ports)//2])

        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True)
        parameter = il.getComplexParameter()

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 3
        self.assertEqual(parameter[2][0], self._matrices[0, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[2][1], self._matrices[1, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[2][2], self._matrices[2, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[2][3], self._matrices[3, 0+len(self._ports)//2, 0])

        # check the values of the port 4
        self.assertEqual(parameter[3][0], self._matrices[0, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[3][1], self._matrices[1, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[3][2], self._matrices[2, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[3][3], self._matrices[3, 1+len(self._ports)//2, 1])

if __name__ == '__main__':
    unittest.main()
