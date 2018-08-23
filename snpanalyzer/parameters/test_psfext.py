import unittest

from parameters.test_parameter import TestParameter
from parameters.fext import FEXT
from parameters.psfext import PSFEXT
from parameters.dataserie import PortDataSerie, PortPairDataSerie
from sample.port import NetworkPort, PlugConfiguration
import numpy as np

def powerSum(values):
    return 10*np.log10(np.sum(list(map(lambda v: 10**(v[0]/10), values))))

class TestPSFEXT(TestParameter):
    def setUp(self):
        super(TestPSFEXT, self).setUp()

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        self._fextseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[3]),
            1: PortPairDataSerie(self._ports[1], self._ports[2]),
            2: PortPairDataSerie(self._ports[2], self._ports[1]),
            3: PortPairDataSerie(self._ports[3], self._ports[0]),
        }

    def createParameter(self):
        fext = FEXT(self._config, self._freq, self._matrices)
        return PSFEXT(self._config, self._freq, self._matrices, fext)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(self._dataseries[0] in self._series, True)
        self.assertEqual(self._dataseries[1] in self._series, True)
        self.assertEqual(self._dataseries[2] in self._series, True)
        self.assertEqual(self._dataseries[3] in self._series, True)
        for serie in self._series:
            fextSeries = serie.getData()
            self.assertEqual(len(fextSeries), 1)
            if serie == self._dataseries[0]:
                self.assertEqual(self._fextseries[0] in fextSeries, True)
            if serie == self._dataseries[1]:
                self.assertEqual(self._fextseries[1] in fextSeries, True)
            if serie == self._dataseries[2]:
                self.assertEqual(self._fextseries[2] in fextSeries, True)
            if serie == self._dataseries[3]:
                self.assertEqual(self._fextseries[3] in fextSeries, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        fext = self._parameter.getFEXT().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[3]]), len(self._freq))

        # check the values of the port 0
        self.assertAlmostEqual(parameter[self._dataseries[0]][0][0], powerSum([fext[self._fextseries[0]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][0], powerSum([fext[self._fextseries[0]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][2][0], powerSum([fext[self._fextseries[0]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][3][0], powerSum([fext[self._fextseries[0]][3]]))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[1]][0][0], powerSum([fext[self._fextseries[1]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][1][0], powerSum([fext[self._fextseries[1]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0], powerSum([fext[self._fextseries[1]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][3][0], powerSum([fext[self._fextseries[1]][3]]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]][0][0], powerSum([fext[self._fextseries[2]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][1][0], powerSum([fext[self._fextseries[2]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][2][0], powerSum([fext[self._fextseries[2]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0], powerSum([fext[self._fextseries[2]][3]]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]][0][0], powerSum([fext[self._fextseries[3]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][1][0], powerSum([fext[self._fextseries[3]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][2][0], powerSum([fext[self._fextseries[3]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][3][0], powerSum([fext[self._fextseries[3]][3]]))

if __name__ == '__main__':
    unittest.main()
