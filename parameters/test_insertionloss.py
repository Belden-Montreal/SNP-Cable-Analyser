import unittest
from parameters.parameter import complex2db
from limits.Limit import Limit
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

        parameter = il.getComplexParameter(full=True)

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

    def testWorstMargin(self):
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        l = complex2db(50)
        limit = Limit("IL", ["-"+str(l)])
        il.setLimit(limit)
        worstMargin = il.getWorstMargin()

        #make sure we get a correct tuple
        self.assertEqual(len(worstMargin), 2)

        #margin should not pass
        self.assertFalse(worstMargin[1])

        #check worst margin for port 1
        self.assertAlmostEqual(worstMargin[0][0][0], complex2db(3))
        self.assertAlmostEqual(worstMargin[0][0][1], 100)
        self.assertAlmostEqual(worstMargin[0][0][2], l)
        self.assertAlmostEqual(worstMargin[0][0][3], abs(complex2db(3)-l))

        #check worst margin for port 2
        self.assertAlmostEqual(worstMargin[0][1][0], complex2db(12))
        self.assertAlmostEqual(worstMargin[0][1][1], 100)
        self.assertAlmostEqual(worstMargin[0][1][2], l)
        self.assertAlmostEqual(worstMargin[0][1][3], abs(complex2db(12)-l))

        #check worst margin for port 3
        self.assertAlmostEqual(worstMargin[0][2][0], complex2db(17))
        self.assertAlmostEqual(worstMargin[0][2][1], 100)
        self.assertAlmostEqual(worstMargin[0][2][2], l)
        self.assertAlmostEqual(worstMargin[0][2][3], abs(complex2db(17)-l))

        #check worst margin for port 4
        self.assertAlmostEqual(worstMargin[0][3][0], complex2db(26))
        self.assertAlmostEqual(worstMargin[0][3][1], 100)
        self.assertAlmostEqual(worstMargin[0][3][2], l)
        self.assertAlmostEqual(worstMargin[0][3][3], abs(complex2db(26)-l))

    def testWorstValue(self):
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        l = complex2db(50)
        limit = Limit("IL", ["-"+str(l)])
        il.setLimit(limit)
        worstValue = il.getWorstValue()

        #make sure we get a correct tuple
        self.assertEqual(len(worstValue), 2)

        #margin should not pass
        self.assertFalse(worstValue[1])

        #check worst value for port 1
        self.assertAlmostEqual(worstValue[0][0][0], complex2db(3))
        self.assertAlmostEqual(worstValue[0][0][1], 100)
        self.assertAlmostEqual(worstValue[0][0][2], l)
        self.assertAlmostEqual(worstValue[0][0][3], abs(complex2db(3)-l))

        #check worst value for port 2
        self.assertAlmostEqual(worstValue[0][1][0], complex2db(12))
        self.assertAlmostEqual(worstValue[0][1][1], 100)
        self.assertAlmostEqual(worstValue[0][1][2], l)
        self.assertAlmostEqual(worstValue[0][1][3], abs(complex2db(12)-l))

        #check worst value for port 3
        self.assertAlmostEqual(worstValue[0][2][0], complex2db(17))
        self.assertAlmostEqual(worstValue[0][2][1], 100)
        self.assertAlmostEqual(worstValue[0][2][2], l)
        self.assertAlmostEqual(worstValue[0][2][3], abs(complex2db(17)-l))

        #check worst value for port 4
        self.assertAlmostEqual(worstValue[0][3][0], complex2db(26))
        self.assertAlmostEqual(worstValue[0][3][1], 100)
        self.assertAlmostEqual(worstValue[0][3][2], l)
        self.assertAlmostEqual(worstValue[0][3][3], abs(complex2db(26)-l))

if __name__ == '__main__':
    unittest.main()
