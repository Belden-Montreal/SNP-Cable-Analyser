import unittest

from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.tctl import TCTL
from snpanalyzer.parameters.dataserie import WireDataSerie

class TestTCTL(TestParameter):
    def createParameter(self):
        self._dataseries = {
            0: WireDataSerie(self._wires[0]),
            1: WireDataSerie(self._wires[1]),
        }

        return TCTL(self._config, self._freq, self._matrices, reverse=False)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the port 1
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 4, 2])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 4, 2])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 4, 2])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 4, 2])

        # check the values of the port 2
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 5, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 5, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 5, 3])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 5, 3])

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[self._dataseries[0]][0], self._matrices[0, 4, 2])
        self.assertEqual(parameter[self._dataseries[0]][1], self._matrices[1, 4, 2])
        self.assertEqual(parameter[self._dataseries[0]][2], self._matrices[2, 4, 2])
        self.assertEqual(parameter[self._dataseries[0]][3], self._matrices[3, 4, 2])

        # check the values of the port 2
        self.assertEqual(parameter[self._dataseries[1]][0], self._matrices[0, 5, 3])
        self.assertEqual(parameter[self._dataseries[1]][1], self._matrices[1, 5, 3])
        self.assertEqual(parameter[self._dataseries[1]][2], self._matrices[2, 5, 3])
        self.assertEqual(parameter[self._dataseries[1]][3], self._matrices[3, 5, 3])

if __name__ == '__main__':
    unittest.main()
