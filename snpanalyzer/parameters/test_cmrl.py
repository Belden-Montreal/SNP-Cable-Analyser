import unittest

from snpanalyzer.parameters.parameter import complex2db, complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.cmrl import CMRL
from snpanalyzer.parameters.dataserie import PortDataSerie

class TestCMRL(TestParameter):
    def createParameter(self):
        return CMRL(self._config, self._freq, self._matrices)

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
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][0], self._matrices[0, 4, 4])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][1], self._matrices[1, 4, 4])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][2], self._matrices[2, 4, 4])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[0])][3], self._matrices[3, 4, 4])

        # check the values of the port 2
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][0], self._matrices[0, 5, 5])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][1], self._matrices[1, 5, 5])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][2], self._matrices[2, 5, 5])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[1])][3], self._matrices[3, 5, 5])

        # check the values of the port 3
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][0], self._matrices[0, 6, 6])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][1], self._matrices[1, 6, 6])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][2], self._matrices[2, 6, 6])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[2])][3], self._matrices[3, 6, 6])

        # check the values of the port 4
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][0], self._matrices[0, 7, 7])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][1], self._matrices[1, 7, 7])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][2], self._matrices[2, 7, 7])
        self.assertComplexAlmostEqual(parameter[PortDataSerie(self._ports[3])][3], self._matrices[3, 7, 7])

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
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][0], self._matrices[0, 4, 4])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][1], self._matrices[1, 4, 4])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][2], self._matrices[2, 4, 4])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[0])][3], self._matrices[3, 4, 4])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][0], self._matrices[0, 5, 5])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][1], self._matrices[1, 5, 5])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][2], self._matrices[2, 5, 5])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[1])][3], self._matrices[3, 5, 5])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][0], self._matrices[0, 6, 6])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][1], self._matrices[1, 6, 6])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][2], self._matrices[2, 6, 6])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[2])][3], self._matrices[3, 6, 6])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][0], self._matrices[0, 7, 7])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][1], self._matrices[1, 7, 7])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][2], self._matrices[2, 7, 7])
        self.assertAlmostEqual(parameter[PortDataSerie(self._ports[3])][3], self._matrices[3, 7, 7])

if __name__ == '__main__':
    unittest.main()