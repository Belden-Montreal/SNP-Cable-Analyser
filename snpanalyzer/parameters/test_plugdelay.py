import unittest

from snpanalyzer.parameters.parameter import complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.propagationdelay import PropagationDelay
from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.dfdelay import DFDelay
from snpanalyzer.parameters.plugdelay import PlugDelay
from snpanalyzer.parameters.dataserie import PortDataSerie
from snpanalyzer.sample.port import PlugConfiguration

import numpy as np

class TestPlugDelay(TestParameter):
    def setUpData(self):
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._freq = [100, 200, 300, 500]
 
    def setUpConfiguration(self):
        super(TestPlugDelay, self).setUpConfiguration()
        self._config = PlugConfiguration(set(self._ports.values()))

    def createParameter(self):
        rl = ReturnLoss(self._config, self._freq, self._matrices)
        opendfDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        shortdfDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        dfDelay = DFDelay(self._config, self._freq, self._matrices, opendfDelay, shortdfDelay)
        openDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        shortDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)

        k1 = 1
        k2 = 2
        k3 = 3

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        return PlugDelay(self._config, self._freq, self._matrices, openDelay, shortDelay, dfDelay, k1, k2, k3)

    def testComputeDataSeries(self):
        self.assertEqual(set(self._dataseries.values()), self._series)

    def testComputeParameter(self):
        parameter  = self._parameter.getParameter()
        openDelay  = self._parameter.getOpenDelay().getParameter()
        shortDelay = self._parameter.getShortDelay().getParameter()
        dfDelay    = self._parameter.getDFDelay().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))
        
        # check the values of the port 0
        self.assertAlmostEqual(parameter[self._dataseries[0]],
            ( np.mean(openDelay[self._dataseries[0]])
            + np.mean(shortDelay[self._dataseries[0]]) - 3)/4.0
            - dfDelay[self._dataseries[0]] + 3)

        # check the values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[1]],
            ( np.mean(openDelay[self._dataseries[1]])
            + np.mean(shortDelay[self._dataseries[1]]) - 3)/4.0
            - dfDelay[self._dataseries[1]] + 3)

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]],
            ( np.mean(openDelay[self._dataseries[2]])
            + np.mean(shortDelay[self._dataseries[2]]) - 3)/4.0 
            - dfDelay[self._dataseries[2]] + 3)

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]],
            ( np.mean(openDelay[self._dataseries[3]])
            + np.mean(shortDelay[self._dataseries[3]]) - 3)/4.0
            - dfDelay[self._dataseries[3]] + 3)

if __name__ == '__main__':
    unittest.main()
