import unittest

from parameters.parameter import complex2db, complex2phase
from parameters.test_parameter import TestParameter
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss
from parameters.axext import AXEXT
from parameters.dataserie import PortPairDataSerie

class TestAXEXT(TestParameter):
    def createParameter(self):
        #we assume that fext and il are tested
        fext = FEXT(self._config, self._freq, self._matrices)
        il   = InsertionLoss(self._config, self._freq, self._matrices)
        return AXEXT(self._config, self._freq, self._matrices, fext, il)

    def testComputeDataSeries(self):
        # for a 4 ports, there are 8 ANEXT data series (including reverse)
        self.assertEqual(len(self._series), 8)

        # make sure the correct series were created
        self.assertEqual(PortPairDataSerie(self._ports[0], self._ports[3]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[3], self._ports[0]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[0], self._ports[2]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[2], self._ports[0]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[1], self._ports[2]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[2], self._ports[1]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[1], self._ports[3]) in self._series, True)
        self.assertEqual(PortPairDataSerie(self._ports[3], self._ports[1]) in self._series, True)         

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there are 8 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 8)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[1])]), len(self._freq))

        # check the values of the pair (2,1)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][0], self._matrices[0, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][1], self._matrices[1, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][2], self._matrices[2, 2, 1])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][3], self._matrices[3, 2, 1])

        # check the values of the pair (1,2)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][0], self._matrices[0, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][1], self._matrices[1, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][2], self._matrices[2, 1, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][3], self._matrices[3, 1, 2])

        # check the values of the pair (3,0)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][0], self._matrices[0, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][1], self._matrices[1, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][2], self._matrices[2, 3, 0])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][3], self._matrices[3, 3, 0])

        # check the values of the pair (0,3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][0], self._matrices[0, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][1], self._matrices[1, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][2], self._matrices[2, 0, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][3], self._matrices[3, 0, 3])

        # check the values of the pair (0,2)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][0], self._matrices[0, 0, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][1], self._matrices[1, 0, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][2], self._matrices[2, 0, 2])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][3], self._matrices[3, 0, 2])

        # check the values of the pair (1,3)
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][0], self._matrices[0, 1, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][1], self._matrices[1, 1, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][2], self._matrices[2, 1, 3])
        self.assertComplexAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][3], self._matrices[3, 1, 3])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there are 8 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 8)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[0], self._ports[3])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[3], self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[1], self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortPairDataSerie(self._ports[2], self._ports[1])]), len(self._freq))

        # check the values of the pair (2,1)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][0], self._matrices[0, 2, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][1], self._matrices[1, 2, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][2], self._matrices[2, 2, 1])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[2], self._ports[1])][3], self._matrices[3, 2, 1])

        # check the values of the pair (1,2)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][0], self._matrices[0, 1, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][1], self._matrices[1, 1, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][2], self._matrices[2, 1, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[2])][3], self._matrices[3, 1, 2])

        # check the values of the pair (3,0)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][0], self._matrices[0, 3, 0])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][1], self._matrices[1, 3, 0])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][2], self._matrices[2, 3, 0])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[3], self._ports[0])][3], self._matrices[3, 3, 0])

        # check the values of the pair (0,3)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][0], self._matrices[0, 0, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][1], self._matrices[1, 0, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][2], self._matrices[2, 0, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[3])][3], self._matrices[3, 0, 3])

        # check the values of the pair (0,2)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][0], self._matrices[0, 0, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][1], self._matrices[1, 0, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][2], self._matrices[2, 0, 2])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[0], self._ports[2])][3], self._matrices[3, 0, 2])

        # check the values of the pair (1,3)
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][0], self._matrices[0, 1, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][1], self._matrices[1, 1, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][2], self._matrices[2, 1, 3])
        self.assertAlmostEqual(parameter[PortPairDataSerie(self._ports[1], self._ports[3])][3], self._matrices[3, 1, 3])  
if __name__ == '__main__':
    unittest.main()
