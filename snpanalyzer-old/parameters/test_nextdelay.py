import unittest

from snpanalyzer.parameters.parameter import complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.propagationdelay import 
from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.dfdelay import DFDelay
from snpanalyzer.parameters.plugdelay import PlugDelay
from snpanalyzer.parameters.nextdelay import NEXTDelay
from snpanalyzer.parameters.dataserie import PortPairDataSerie, PortDataSerie
from snpanalyzer.sample.port import PlugConfiguration

import numpy as np

class TestNEXTDelay(TestParameter):
    def setUpData(self):
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._freq = [100, 200, 300, 500]

    def setUpConfiguration(self):
        super(TestNEXTDelay, self).setUpConfiguration()
        self._config = PlugConfiguration(set(self._ports.values()))
 
    def createParameter(self):
        rl = ReturnLoss(self._config, self._freq, self._matrices)
        opendfDelay = (self._config, self._freq, self._matrices, rl)
        shortdfDelay = (self._config, self._freq, self._matrices, rl)
        dfDelay = DFDelay(self._config, self._freq, self._matrices, opendfDelay, shortdfDelay)
        openDelay = (self._config, self._freq, self._matrices, rl)
        shortDelay = (self._config, self._freq, self._matrices, rl)
        plugDelay = PlugDelay(self._config, self._freq, self._matrices, openDelay, shortDelay, dfDelay, 1, 2, 3)

        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[0], self._ports[2]),
            2: PortPairDataSerie(self._ports[0], self._ports[3]),
            3: PortPairDataSerie(self._ports[1], self._ports[2]),
            4: PortPairDataSerie(self._ports[1], self._ports[3]),
            5: PortPairDataSerie(self._ports[2], self._ports[3]),
        }

        self._portseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        return NEXTDelay(self._config, self._freq, self._matrices, plugDelay)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        plugDelay = self._parameter.getPlugDelay().getParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        # check the values of the port (0,1)
        self.assertAlmostEqual(parameter[self._dataseries[0]],
            plugDelay[self._portseries[0]]+plugDelay[self._portseries[1]])

        # check the values of the port (0,2)
        self.assertAlmostEqual(parameter[self._dataseries[1]],
            plugDelay[self._portseries[0]]+plugDelay[self._portseries[2]])

        # check the values of the port (0,3)
        self.assertAlmostEqual(parameter[self._dataseries[2]],
            plugDelay[self._portseries[0]]+plugDelay[self._portseries[3]])

        # check the values of the port (1,2)
        self.assertAlmostEqual(parameter[self._dataseries[3]],
            plugDelay[self._portseries[1]]+plugDelay[self._portseries[2]])

        # check the values of the port (1,3)
        self.assertAlmostEqual(parameter[self._dataseries[4]],
            plugDelay[self._portseries[1]]+plugDelay[self._portseries[3]])

        # check the values of the port (2,3)
        self.assertAlmostEqual(parameter[self._dataseries[5]],
            plugDelay[self._portseries[2]]+plugDelay[self._portseries[3]])

if __name__ == '__main__':
    unittest.main()
