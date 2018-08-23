import unittest

from parameters.parameter import complex2phase
from parameters.test_parameter import TestPlugParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
from parameters.next import NEXT
from parameters.correctednext import CorrectedNEXT
from parameters.dataserie import PortPairDataSerie

import numpy as np

def correctNEXT(pnext, nextDelay, f):
    amp, phase = pnext
    amp = 10**(amp/20)
    correctedPhase = phase + 360*f*nextDelay
    r = amp*np.cos(correctedPhase*np.pi/180)
    i = amp*np.sin(correctedPhase*np.pi/180)
    cpValue = complex(r,i)
    dbValue = (amp, correctedPhase)
    return (dbValue, cpValue)

class TestCorrectedNEXT(TestPlugParameter):
    def setUpData(self):
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._freq = [100, 200, 300, 500]

    def createParameter(self):
        rl = ReturnLoss(self._config, self._freq, self._matrices)
        opendfDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        shortdfDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        dfDelay = DFDelay(self._config, self._freq, self._matrices, opendfDelay, shortdfDelay)
        openDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        shortDelay = PropagationDelay(self._config, self._freq, self._matrices, rl)
        plugDelay = PlugDelay(self._config, self._freq, self._matrices, openDelay, shortDelay, dfDelay, 1, 2, 3)
        nextDelay = NEXTDelay(self._config, self._freq, self._matrices, plugDelay)

        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[0], self._ports[2]),
            2: PortPairDataSerie(self._ports[0], self._ports[3]),
            3: PortPairDataSerie(self._ports[1], self._ports[2]),
            4: PortPairDataSerie(self._ports[1], self._ports[3]),
            5: PortPairDataSerie(self._ports[2], self._ports[3]),
        }

        return CorrectedNEXT(self._config, self._freq, self._matrices, nextDelay)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()
        nextDelay = self._parameter.getNEXTDelay().getParameter()
        dbNEXT = NEXT(self._config, self._freq, self._matrices).getParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        # check the values of the port 1-2
        for serie in self._dataseries.values():
            for f in range(len(self._freq)):
                (_, cpValue) = correctNEXT(dbNEXT[serie][f], nextDelay[serie], self._freq[f])
                self.assertAlmostEqual(parameter[serie][f], cpValue)

if __name__ == '__main__':
    unittest.main()
