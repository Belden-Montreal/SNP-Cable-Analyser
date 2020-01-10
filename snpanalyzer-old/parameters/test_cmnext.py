import unittest

from snpanalyzer.parameters.parameter import complex2db, complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.cmnext import CMNEXT
from snpanalyzer.parameters.dataserie import PortPairDataSerie

class TestCMNEXT(TestParameter):
    def createParameter(self):
        return CMNEXT(self._config, self._freq, self._matrices, order=False)       

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(PortPairDataSerie(self._ports[0], self._ports[1]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[2], self._ports[3]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[1], self._ports[0]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[3], self._ports[2]) in self._series, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there is only 4 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[2])]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][0], self._matrices[0, 4, 5])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][1], self._matrices[1, 4, 5])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][2], self._matrices[2, 4, 5])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][3], self._matrices[3, 4, 5])

        # check the values of the pair (2,3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][0], self._matrices[0, 6, 7])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][1], self._matrices[1, 6, 7])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][2], self._matrices[2, 6, 7])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][3], self._matrices[3, 6, 7])

        # check the values of the pair (1,0)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][0], self._matrices[0, 5, 4])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][1], self._matrices[1, 5, 4])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][2], self._matrices[2, 5, 4])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][3], self._matrices[3, 5, 4])

        # check the values of the pair (3,2)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][0], self._matrices[0, 7, 6])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][1], self._matrices[1, 7, 6])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][2], self._matrices[2, 7, 6])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][3], self._matrices[3, 7, 6])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there is only 2 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[2])]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][0], self._matrices[0, 4, 5])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][1], self._matrices[1, 4, 5])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][2], self._matrices[2, 4, 5])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][3], self._matrices[3, 4, 5])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][0], self._matrices[0, 6, 7])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][1], self._matrices[1, 6, 7])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][2], self._matrices[2, 6, 7])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][3], self._matrices[3, 6, 7])

        # check the values of the pair (1,0)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][0], self._matrices[0, 5, 4])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][1], self._matrices[1, 5, 4])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][2], self._matrices[2, 5, 4])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[0])][3], self._matrices[3, 5, 4])

        # check the values of the pair (3,2)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][0], self._matrices[0, 7, 6])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][1], self._matrices[1, 7, 6])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][2], self._matrices[2, 7, 6])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[2])][3], self._matrices[3, 7, 6])

if __name__ == '__main__':
    unittest.main()
