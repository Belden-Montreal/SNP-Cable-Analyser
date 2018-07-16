import unittest

from parameters.parameter import complex2db, complex2phase
from parameters.test_parameter import TestParameter
from parameters.next import NEXT
from parameters.dataserie import PortPairDataSerie

class TestNEXT(TestParameter):
    def createParameter(self):
        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[2], self._ports[3]),
        }

        return NEXT(self._config, self._freq, self._matrices)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 1])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 1])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 1])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 1])

        # check the values of the pair (2,3)
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 2, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 2, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 2, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 2, 3])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 1])
        self.assertAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 1])
        self.assertAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 1])
        self.assertAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 1])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 2, 3])
        self.assertAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 2, 3])
        self.assertAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 2, 3])
        self.assertAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 2, 3])

if __name__ == '__main__':
    unittest.main()
