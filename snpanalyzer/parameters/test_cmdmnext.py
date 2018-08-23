import unittest

from snpanalyzer.parameters.parameter import complex2db, complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.cmdmnext import CMDMNEXT
from snpanalyzer.parameters.dataserie import PortPairDataSerie

class TestCMDMNEXT(TestParameter):
    def createParameter(self):
        return CMDMNEXT(self._config, self._freq, self._matrices, order=False)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(PortPairDataSerie(self._ports[0], self._ports[1]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[2], self._ports[3]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[1], self._ports[0]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[3], self._ports[2]) in self._series, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there is only 2 CMDMNEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[3])]), len(self._freq))
        
        # check the values of the pair (0,1)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][0], self._matrices[0, 4, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][1], self._matrices[1, 4, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][2], self._matrices[2, 4, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][3], self._matrices[3, 4, 1])

        # check the values of the pair (2,3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][0], self._matrices[0, 6, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][1], self._matrices[1, 6, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][2], self._matrices[2, 6, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][3], self._matrices[3, 6, 3])
        
    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there is only 2 CMDMNEXT pairs
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[3])]), len(self._freq))
        
        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][0], self._matrices[0, 4, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][1], self._matrices[1, 4, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][2], self._matrices[2, 4, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[1])][3], self._matrices[3, 4, 1])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][0], self._matrices[0, 6, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][1], self._matrices[1, 6, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][2], self._matrices[2, 6, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[3])][3], self._matrices[3, 6, 3])

if __name__ == '__main__':
    unittest.main()
