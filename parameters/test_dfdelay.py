import unittest

from parameters.parameter import complex2phase
from parameters.test_parameter import TestParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.dataserie import PortDataSerie
import numpy as np

class TestDFDelay(TestParameter):
    def setUpData(self):
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._freq = [100, 200, 300, 500]

    def createParameter(self):
        rl = ReturnLoss(self._config, self._freq, self._matrices)
        self._openDelay  = PropagationDelay(self._config, self._freq, self._matrices, rl)
        self._shortDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        return DFDelay(self._config, self._freq, self._matrices, self._openDelay, self._shortDelay)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        openDelay = self._parameter.getOpenDelay().getParameter()
        shortDelay = self._parameter.getShortDelay().getParameter()

        # check the values of the port 0
        self.assertAlmostEqual(parameter[self._dataseries[0]],
            (np.mean(openDelay[self._dataseries[0]]) + np.mean(shortDelay[self._dataseries[0]]))/4.0)

        # check the values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[1]],
            (np.mean(openDelay[self._dataseries[1]]) + np.mean(shortDelay[self._dataseries[1]]))/4.0)

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]],
            (np.mean(openDelay[self._dataseries[2]]) + np.mean(shortDelay[self._dataseries[2]]))/4.0)

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]],
            (np.mean(openDelay[self._dataseries[3]]) + np.mean(shortDelay[self._dataseries[3]]))/4.0)

if __name__ == '__main__':
    unittest.main()
