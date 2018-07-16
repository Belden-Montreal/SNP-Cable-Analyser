import unittest

from parameters.test_parameter import TestParameter
from parameters.dmcmnext import DMCMNEXT
from parameters.dataserie import PortPairDataSerie

class TestDMCMNEXT(TestParameter):
    def createParameter(self):
        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[1], self._ports[0]),
            2: PortPairDataSerie(self._ports[2], self._ports[3]),
            3: PortPairDataSerie(self._ports[3], self._ports[2]),
        }

        return DMCMNEXT(self._config, self._freq, self._matrices, order=False)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 5])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 5])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 5])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 5])

        # check the values of the pair (1,0)
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 1, 4])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 1, 4])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 1, 4])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 1, 4])

        # check the values of the pair (2,3)
        self.assertComplexAlmostEqual(parameter[self._dataseries[2]][0], self._matrices[0, 2, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[2]][1], self._matrices[1, 2, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[2]][2], self._matrices[2, 2, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[2]][3], self._matrices[3, 2, 7])

        # check the values of the pair (3,2)
        self.assertComplexAlmostEqual(parameter[self._dataseries[3]][0], self._matrices[0, 3, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[3]][1], self._matrices[1, 3, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[3]][2], self._matrices[2, 3, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[3]][3], self._matrices [3, 3, 6])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 5])
        self.assertAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 5])
        self.assertAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 5])
        self.assertAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 5])

        # check the values of the pair (1,0)
        self.assertAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 1, 4])
        self.assertAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 1, 4])
        self.assertAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 1, 4])
        self.assertAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 1, 4])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[self._dataseries[2]][0], self._matrices[0, 2, 7])
        self.assertAlmostEqual(parameter[self._dataseries[2]][1], self._matrices[1, 2, 7])
        self.assertAlmostEqual(parameter[self._dataseries[2]][2], self._matrices[2, 2, 7])
        self.assertAlmostEqual(parameter[self._dataseries[2]][3], self._matrices[3, 2, 7])

        # check the values of the pair (3,2)
        self.assertAlmostEqual(parameter[self._dataseries[3]][0], self._matrices[0, 3, 6])
        self.assertAlmostEqual(parameter[self._dataseries[3]][1], self._matrices[1, 3, 6])
        self.assertAlmostEqual(parameter[self._dataseries[3]][2], self._matrices[2, 3, 6])
        self.assertAlmostEqual(parameter[self._dataseries[3]][3], self._matrices[3, 3, 6])

if __name__ == '__main__':
    unittest.main()
