import unittest
from snpanalyzer.parameters.parameter import complex2db, complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.dataserie import PortDataSerie
from snpanalyzer.limits.Standard import Standard
from snpanalyzer.limits.Limit import Limit

class TestReturnLoss(TestParameter):
    def createParameter(self):
        return ReturnLoss(self._config, self._freq, self._matrices)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(PortDataSerie(self._ports[0]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[1]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[2]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[3]) in self._series, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortDataSerie(self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[3])]), len(self._freq))

        # check the values of the port 1
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][0], self._matrices[0, 0, 0])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][1], self._matrices[1, 0, 0])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][2], self._matrices[2, 0, 0])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][3], self._matrices[3, 0, 0])

        # check the values of the port 2
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][0], self._matrices[0, 1, 1])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][1], self._matrices[1, 1, 1])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][2], self._matrices[2, 1, 1])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][3], self._matrices[3, 1, 1])

        # check the values of the port 3
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][0], self._matrices[0, 2, 2])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][1], self._matrices[1, 2, 2])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][2], self._matrices[2, 2, 2])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][3], self._matrices[3, 2, 2])

        # check the values of the port 4
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][0], self._matrices[0, 3, 3])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][1], self._matrices[1, 3, 3])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][2], self._matrices[2, 3, 3])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][3], self._matrices[3, 3, 3])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortDataSerie(self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[3])]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][0], self._matrices[0, 0, 0])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][1], self._matrices[1, 0, 0])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][2], self._matrices[2, 0, 0])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][3], self._matrices[3, 0, 0])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][0], self._matrices[0, 1, 1])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][1], self._matrices[1, 1, 1])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][2], self._matrices[2, 1, 1])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][3], self._matrices[3, 1, 1])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][0], self._matrices[0, 2, 2])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][1], self._matrices[1, 2, 2])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][2], self._matrices[2, 2, 2])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][3], self._matrices[3, 2, 2])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][0], self._matrices[0, 3, 3])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][1], self._matrices[1, 3, 3])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][2], self._matrices[2, 3, 3])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][3], self._matrices[3, 3, 3])

    def testWorstMargin(self):
        l = complex2db(50)
        limit = Limit("RL", ["-"+str(l)])
        self._parameter.setLimit(limit)
        worstMargin = self._parameter.getWorstMargin()

        # make sure we get a correct tuple
        self.assertEqual(len(worstMargin), 2)

        # margin should not pass
        self.assertFalse(worstMargin[1])

        # check worst margin for port 1
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[0])][0], complex2db(193))
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[0])][1], 400)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[0])][2], l)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[0])][3], abs(l-complex2db(193)))

        # check worst margin for port 2
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[1])][0], complex2db(202))
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[1])][1], 400)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[1])][2], l)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[1])][3], abs(l-complex2db(202)))

        # check worst margin for port 3
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[2])][0], complex2db(211))
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[2])][1], 400)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[2])][2], l)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[2])][3], abs(l-complex2db(211)))

        # check worst margin for port 4
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[3])][0], complex2db(220))
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[3])][1], 400)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[3])][2], l)
        self.assertAlmostEqual(worstMargin[0][PortDataSerie(self._ports[3])][3], abs(l-complex2db(220)))

    def testWorstValue(self):
        l = complex2db(50)
        limit = Limit("RL", ["-"+str(l)])
        self._parameter.setLimit(limit)
        worstValue = self._parameter.getWorstValue()

        # make sure we get a correct tuple
        self.assertEqual(len(worstValue), 2)

        # margin should not pass
        self.assertFalse(worstValue[1])

        # check worst margin for port 1
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[0])][0], complex2db(193))
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[0])][1], 400)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[0])][2], l)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[0])][3], abs(l-complex2db(193)))

        # check worst margin for port 2
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[1])][0], complex2db(202))
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[1])][1], 400)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[1])][2], l)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[1])][3], abs(l-complex2db(202)))

        # check worst margin for port 3
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[2])][0], complex2db(211))
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[2])][1], 400)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[2])][2], l)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[2])][3], abs(l-complex2db(211)))

        # check worst margin for port 4
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[3])][0], complex2db(220))
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[3])][1], 400)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[3])][2], l)
        self.assertAlmostEqual(worstValue[0][PortDataSerie(self._ports[3])][3], abs(l-complex2db(220)))

if __name__ == '__main__':
    unittest.main()
