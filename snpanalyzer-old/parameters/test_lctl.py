import unittest

from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.lctl import LCTL
from snpanalyzer.parameters.dataserie import WireDataSerie

class TestLCTL(TestParameter):
    def createParameter(self):
        self._dataseries = {
            0: WireDataSerie(self._wires[0]),
            1: WireDataSerie(self._wires[1]),
        }

        return LCTL(self._config, self._freq, self._matrices, reverse=False)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the port 0
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 6])
        self.assertComplexAlmostEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 6])

        # check the values of the port 1
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][0], self._matrices[0, 1, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][1], self._matrices[1, 1, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][2], self._matrices[2, 1, 7])
        self.assertComplexAlmostEqual(parameter[self._dataseries[1]][3], self._matrices[3, 1, 7]) 

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # the number of sample should be the same as the number of frequencies
        for serie in self._dataseries.values():
            self.assertEqual(len(parameter[serie]), len(self._freq))

        # check the values of the port 0
        self.assertEqual(parameter[self._dataseries[0]][0], self._matrices[0, 0, 6])
        self.assertEqual(parameter[self._dataseries[0]][1], self._matrices[1, 0, 6])
        self.assertEqual(parameter[self._dataseries[0]][2], self._matrices[2, 0, 6])
        self.assertEqual(parameter[self._dataseries[0]][3], self._matrices[3, 0, 6])

        # check the values of the port 1
        self.assertEqual(parameter[self._dataseries[1]][0], self._matrices[0, 1, 7])
        self.assertEqual(parameter[self._dataseries[1]][1], self._matrices[1, 1, 7])
        self.assertEqual(parameter[self._dataseries[1]][2], self._matrices[2, 1, 7])
        self.assertEqual(parameter[self._dataseries[1]][3], self._matrices[3, 1, 7])

if __name__ == '__main__':
    unittest.main()
