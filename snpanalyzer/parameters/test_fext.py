import unittest

from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.fext import FEXT
from snpanalyzer.parameters.dataserie import PortPairDataSerie

class TestFEXT(TestParameter):
    def createParameter(self):
        return FEXT(self._config, self._freq, self._matrices)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(PortPairDataSerie(self._ports[0], self._ports[3]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[1], self._ports[2]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[3], self._ports[0]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[2], self._ports[1]) in self._series, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there are 4 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[1])]), len(self._freq))

        # check the values of the pair (2, 1)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][0], self._matrices[0, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][1], self._matrices[1, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][2], self._matrices[2, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][3], self._matrices[3, 2, 1])

        # check the values of the pair (1, 2)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][0], self._matrices[0, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][1], self._matrices[1, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][2], self._matrices[2, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][3], self._matrices[3, 1, 2])

        # check the values of the pair (0, 3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][0], self._matrices[0, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][1], self._matrices[1, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][2], self._matrices[2, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][3], self._matrices[3, 3, 0])

        # check the values of the pair (0, 3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][0], self._matrices[0, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][1], self._matrices[1, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][2], self._matrices[2, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][3], self._matrices[3, 0, 3])  

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there are 4 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[1])]), len(self._freq))

        # check the values of the pair (2, 1)
        self.assertEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][0], self._matrices[0, 2, 1])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][1], self._matrices[1, 2, 1])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][2], self._matrices[2, 2, 1])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][3], self._matrices[3, 2, 1])

        # check the values of the pair (1, 2)
        self.assertEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][0], self._matrices[0, 1, 2])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][1], self._matrices[1, 1, 2])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][2], self._matrices[2, 1, 2])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][3], self._matrices[3, 1, 2])

        # check the values of the pair (3, 0)
        self.assertEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][0], self._matrices[0, 3, 0])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][1], self._matrices[1, 3, 0])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][2], self._matrices[2, 3, 0])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][3], self._matrices[3, 3, 0])

        # check the values of the pair (0, 3)
        self.assertEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][0], self._matrices[0, 0, 3])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][1], self._matrices[1, 0, 3])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][2], self._matrices[2, 0, 3])
        self.assertEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][3], self._matrices[3, 0, 3])

if __name__ == '__main__':
    unittest.main()
