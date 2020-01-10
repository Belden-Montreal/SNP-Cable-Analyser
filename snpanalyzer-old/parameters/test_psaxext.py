import unittest
import numpy as np
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.psaxext import PSAXEXT
from snpanalyzer.parameters.axext import AXEXT
from snpanalyzer.parameters.parameter import complex2db
from snpanalyzer.parameters.dataserie import PortDataSerie, PortPairDataSerie

class TestPSAXEXT(TestParameter):
    def assertIn(self, value, collection):
        self.assertEqual(value in collection, True)

    def createParameter(self):
        self._axextd = {
            0: AXEXT(self._config, self._freq, self._matrices),
            1: AXEXT(self._config, self._freq, self._matrices),
            2: AXEXT(self._config, self._freq, self._matrices),
            3: AXEXT(self._config, self._freq, self._matrices),
        }

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
        }

        self._pairseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[2]),
            1: PortPairDataSerie(self._ports[0], self._ports[3]),
            2: PortPairDataSerie(self._ports[1], self._ports[2]),
            3: PortPairDataSerie(self._ports[1], self._ports[3]),
            4: PortPairDataSerie(self._ports[2], self._ports[0]),
            5: PortPairDataSerie(self._ports[2], self._ports[1]),
            6: PortPairDataSerie(self._ports[3], self._ports[0]),
            7: PortPairDataSerie(self._ports[3], self._ports[1]),
        }

        self._expected = {
            self._dataseries[0]: {
                self._axextd[0]: {self._pairseries[0], self._pairseries[1]},
                self._axextd[1]: {self._pairseries[0], self._pairseries[1]},
                self._axextd[2]: {self._pairseries[0], self._pairseries[1]},
                self._axextd[3]: {self._pairseries[0], self._pairseries[1]},
            },
            self._dataseries[1]: {
                self._axextd[0]: {self._pairseries[2], self._pairseries[3]},
                self._axextd[1]: {self._pairseries[2], self._pairseries[3]},
                self._axextd[2]: {self._pairseries[2], self._pairseries[3]},
                self._axextd[3]: {self._pairseries[2], self._pairseries[3]},
            },
        }

        return PSAXEXT(self._config, self._freq, self._matrices, self._axextd.values())

    def assertPowerSum(self, value, port, freq):
        dbSum = 0
        for disturber in self._expected[port]:
            for pair in self._expected[port][disturber]:
                axext = disturber.getParameter()[pair][freq][0]
                dbSum += 10.0**(axext/10)
        result = 10.0*np.log10(dbSum)

        self.assertAlmostEqual(value, result)

    def testComputeDataSeries(self):
        expected = self._expected
        self.assertEqual(len(self._series), 2)
        for serie in self._series:
            data = serie.getData()
            disturbers = data.keys()
            self.assertIn(serie, expected)
            self.assertEqual(len(disturbers), len(expected[serie]))
            for disturber in disturbers:
                self.assertIn(disturber, expected[serie])
                self.assertEqual(len(data[disturber]), len(expected[serie][disturber]))
                for pair in data[disturber]:
                    self.assertIn(pair, expected[serie][disturber])

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), 2)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))

        # check the values of the port 0
        self.assertPowerSum(parameter[self._dataseries[0]][0][0], self._dataseries[0], 0)
        self.assertPowerSum(parameter[self._dataseries[0]][1][0], self._dataseries[0], 1)
        self.assertPowerSum(parameter[self._dataseries[0]][2][0], self._dataseries[0], 2)
        self.assertPowerSum(parameter[self._dataseries[0]][3][0], self._dataseries[0], 3)

        # check the values of the port 1
        self.assertPowerSum(parameter[self._dataseries[1]][0][0], self._dataseries[1], 0)
        self.assertPowerSum(parameter[self._dataseries[1]][1][0], self._dataseries[1], 1)
        self.assertPowerSum(parameter[self._dataseries[1]][2][0], self._dataseries[1], 2)
        self.assertPowerSum(parameter[self._dataseries[1]][3][0], self._dataseries[1], 3)

if __name__ == '__main__':
    unittest.main()
