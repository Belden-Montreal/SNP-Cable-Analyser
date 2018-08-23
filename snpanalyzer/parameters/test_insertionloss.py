import unittest
from limits.Limit import Limit
from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.insertionloss import InsertionLoss
from parameters.dataserie import WireDataSerie

class TestInsertionLoss(TestParameter):
    def setUp(self):
        super(TestInsertionLoss, self).setUp()
        self._series = {
            0: WireDataSerie(self._wires[0]),
            1: WireDataSerie(self._wires[1]),
            2: WireDataSerie(self._wires[2]),
            3: WireDataSerie(self._wires[3]),
        }

    def createParameter(self):
        return InsertionLoss(self._config, self._freq, self._matrices)

    def testComputeDataSeries(self):
        series = self._parameter.getDataSeries()
        self.assertEqual(len(series), 4)
        self.assertEqual(self._series[0] in series, True)
        self.assertEqual(self._series[1] in series, True)
        self.assertEqual(self._series[2] in series, True)
        self.assertEqual(self._series[3] in series, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each wires
        self.assertEqual(len(parameter), len(self._wires))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._series[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[3]]), len(self._freq))

        # check the values of the wire 1
        self.assertComplexAlmostEqual(parameter[self._series[0]][0], self._matrices[0, 0, len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[0]][1], self._matrices[1, 0, len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[0]][2], self._matrices[2, 0, len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[0]][3], self._matrices[3, 0, len(self._ports)//2])

        # check the values of the wire 2
        self.assertComplexAlmostEqual(parameter[self._series[1]][0], self._matrices[0, 1, 1+len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[1]][1], self._matrices[1, 1, 1+len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[1]][2], self._matrices[2, 1, 1+len(self._ports)//2])
        self.assertComplexAlmostEqual(parameter[self._series[1]][3], self._matrices[3, 1, 1+len(self._ports)//2])

        # check the values of the wire 3
        self.assertComplexAlmostEqual(parameter[self._series[2]][0], self._matrices[0, 0+len(self._ports)//2, 0])
        self.assertComplexAlmostEqual(parameter[self._series[2]][1], self._matrices[1, 0+len(self._ports)//2, 0])
        self.assertComplexAlmostEqual(parameter[self._series[2]][2], self._matrices[2, 0+len(self._ports)//2, 0])
        self.assertComplexAlmostEqual(parameter[self._series[2]][3], self._matrices[3, 0+len(self._ports)//2, 0])

        # check the values of the wire 4
        self.assertComplexAlmostEqual(parameter[self._series[3]][0], self._matrices[0, 1+len(self._ports)//2, 1])
        self.assertComplexAlmostEqual(parameter[self._series[3]][1], self._matrices[1, 1+len(self._ports)//2, 1])
        self.assertComplexAlmostEqual(parameter[self._series[3]][2], self._matrices[2, 1+len(self._ports)//2, 1])
        self.assertComplexAlmostEqual(parameter[self._series[3]][3], self._matrices[3, 1+len(self._ports)//2, 1])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # there should be a parameter for each wire
        self.assertEqual(len(parameter), len(self._wires))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._series[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._series[3]]), len(self._freq))

        # check the values of the wire 1
        self.assertEqual(parameter[self._series[0]][0], self._matrices[0, 0, len(self._ports)//2])
        self.assertEqual(parameter[self._series[0]][1], self._matrices[1, 0, len(self._ports)//2])
        self.assertEqual(parameter[self._series[0]][2], self._matrices[2, 0, len(self._ports)//2])
        self.assertEqual(parameter[self._series[0]][3], self._matrices[3, 0, len(self._ports)//2])

        # check the values of the wire 2
        self.assertEqual(parameter[self._series[1]][0], self._matrices[0, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[self._series[1]][1], self._matrices[1, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[self._series[1]][2], self._matrices[2, 1, 1+len(self._ports)//2])
        self.assertEqual(parameter[self._series[1]][3], self._matrices[3, 1, 1+len(self._ports)//2])

        # check the values of the wire 3
        self.assertEqual(parameter[self._series[2]][0], self._matrices[0, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[self._series[2]][1], self._matrices[1, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[self._series[2]][2], self._matrices[2, 0+len(self._ports)//2, 0])
        self.assertEqual(parameter[self._series[2]][3], self._matrices[3, 0+len(self._ports)//2, 0])

        # check the values of the wire 4
        self.assertEqual(parameter[self._series[3]][0], self._matrices[0, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[self._series[3]][1], self._matrices[1, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[self._series[3]][2], self._matrices[2, 1+len(self._ports)//2, 1])
        self.assertEqual(parameter[self._series[3]][3], self._matrices[3, 1+len(self._ports)//2, 1])

    def testWorstMargin(self):
        l = complex2db(50)
        limit = Limit("IL", ["-"+str(l)])
        self._parameter.setLimit(limit)
        worstMargin = self._parameter.getWorstMargin()

        # make sure we get a correct tuple
        self.assertEqual(len(worstMargin), 2)

        # margin should not pass
        self.assertFalse(worstMargin[1])

        # check worst margin for wire 1
        self.assertAlmostEqual(worstMargin[0][self._series[0]][0], complex2db(3))
        self.assertAlmostEqual(worstMargin[0][self._series[0]][1], 100)
        self.assertAlmostEqual(worstMargin[0][self._series[0]][2], l)
        self.assertAlmostEqual(worstMargin[0][self._series[0]][3], abs(complex2db(3)-l))

        # check worst margin for wire 2
        self.assertAlmostEqual(worstMargin[0][self._series[1]][0], complex2db(12))
        self.assertAlmostEqual(worstMargin[0][self._series[1]][1], 100)
        self.assertAlmostEqual(worstMargin[0][self._series[1]][2], l)
        self.assertAlmostEqual(worstMargin[0][self._series[1]][3], abs(complex2db(12)-l))

        # check worst margin for wire 3
        self.assertAlmostEqual(worstMargin[0][self._series[2]][0], complex2db(17))
        self.assertAlmostEqual(worstMargin[0][self._series[2]][1], 100)
        self.assertAlmostEqual(worstMargin[0][self._series[2]][2], l)
        self.assertAlmostEqual(worstMargin[0][self._series[2]][3], abs(complex2db(17)-l))

        # check worst margin for wire 4
        self.assertAlmostEqual(worstMargin[0][self._series[3]][0], complex2db(26))
        self.assertAlmostEqual(worstMargin[0][self._series[3]][1], 100)
        self.assertAlmostEqual(worstMargin[0][self._series[3]][2], l)
        self.assertAlmostEqual(worstMargin[0][self._series[3]][3], abs(complex2db(26)-l))

    def testWorstValue(self):
        l = complex2db(50)
        limit = Limit("IL", ["-"+str(l)])
        self._parameter.setLimit(limit)
        worstValue = self._parameter.getWorstValue()

        # make sure we get a correct tuple
        self.assertEqual(len(worstValue), 2)

        # margin should not pass
        self.assertFalse(worstValue[1])

        # check worst value for wire 1
        self.assertAlmostEqual(worstValue[0][self._series[0]][0], complex2db(3))
        self.assertAlmostEqual(worstValue[0][self._series[0]][1], 100)
        self.assertAlmostEqual(worstValue[0][self._series[0]][2], l)
        self.assertAlmostEqual(worstValue[0][self._series[0]][3], abs(complex2db(3)-l))

        # check worst value for wire 2
        self.assertAlmostEqual(worstValue[0][self._series[1]][0], complex2db(12))
        self.assertAlmostEqual(worstValue[0][self._series[1]][1], 100)
        self.assertAlmostEqual(worstValue[0][self._series[1]][2], l)
        self.assertAlmostEqual(worstValue[0][self._series[1]][3], abs(complex2db(12)-l))

        # check worst value for wire 3
        self.assertAlmostEqual(worstValue[0][self._series[2]][0], complex2db(17))
        self.assertAlmostEqual(worstValue[0][self._series[2]][1], 100)
        self.assertAlmostEqual(worstValue[0][self._series[2]][2], l)
        self.assertAlmostEqual(worstValue[0][self._series[2]][3], abs(complex2db(17)-l))

        # check worst value for wire 4
        self.assertAlmostEqual(worstValue[0][self._series[3]][0], complex2db(26))
        self.assertAlmostEqual(worstValue[0][self._series[3]][1], 100)
        self.assertAlmostEqual(worstValue[0][self._series[3]][2], l)
        self.assertAlmostEqual(worstValue[0][self._series[3]][3], abs(complex2db(26)-l))

if __name__ == '__main__':
    unittest.main()
