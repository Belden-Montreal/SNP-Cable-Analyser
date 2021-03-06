import unittest

from snpanalyzer.parameters.test_parameter import TestPlugParameter
from snpanalyzer.parameters.propagationdelay import PropagationDelay
from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.dfdelay import DFDelay
from snpanalyzer.parameters.plugdelay import PlugDelay
from snpanalyzer.parameters.nextdelay import NEXTDelay
from snpanalyzer.parameters.next import NEXT
from snpanalyzer.parameters.dnext import DNEXT
from snpanalyzer.parameters.correctednext import CorrectedNEXT
from snpanalyzer.parameters.dataserie import PortPairDataSerie

import numpy as np

def correctNEXT(pnext, nextDelay, f):
    amp, phase = pnext
    amp = 10**(amp/20)
    correctedPhase = phase + 360*f*nextDelay
    r = amp*np.cos(correctedPhase*np.pi/180)
    i = amp*np.sin(correctedPhase*np.pi/180)
    correctedNextVal = complex(r,i)
    return correctedNextVal

class TestDNEXT(TestPlugParameter):
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
        pnext = CorrectedNEXT(self._config, self._freq, self._matrices, nextDelay)

        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[0], self._ports[2]),
            2: PortPairDataSerie(self._ports[0], self._ports[3]),
            3: PortPairDataSerie(self._ports[1], self._ports[2]),
            4: PortPairDataSerie(self._ports[1], self._ports[3]),
            5: PortPairDataSerie(self._ports[2], self._ports[3]),
        }

        return DNEXT(self._config, self._freq, self._matrices, nextDelay, pnext)

    def testComputeDataSerie(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()
        nextDelay = self._parameter.getNEXTDelay().getParameter()
        pnext = self._parameter.getPlugNEXT().getComplexParameter()
        jnext = NEXT(self._config, self._freq, self._matrices).getParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        for serie in self._series:
            for f in range(len(self._freq)):
                self.assertAlmostEqual(parameter[serie][f], correctNEXT(
                    jnext[serie][f], nextDelay[serie], self._freq[f])-pnext[serie][f])

if __name__ == '__main__':
    unittest.main()
