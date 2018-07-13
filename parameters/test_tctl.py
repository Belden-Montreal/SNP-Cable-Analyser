import unittest

from parameters.test_parameter import TestParameter
from parameters.tctl import TCTL
from parameters.dataserie import PortPairDataSerie

class TestTCTL(TestParameter):
    def createParameter(self):
        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[2]),
            1: PortPairDataSerie(self._ports[1], self._ports[3]),
        }

        return TCTL(self._config, self._freq, self._matrices, reverse=False)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
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
