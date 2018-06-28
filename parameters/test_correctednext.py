import unittest
from parameters.parameter import complex2phase
from parameters.test_parameter import TestParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
from parameters.next import NEXT
from parameters.correctednext import CorrectedNEXT
import numpy as np

def correctNEXT(pnext, nextDelay, f):
    phase = np.angle(pnext)
    correctedPhase = phase + 360*f*nextDelay
    amp = np.abs(pnext)
    r = amp*np.cos(correctedPhase*np.pi/180)
    i = amp*np.sin(correctedPhase*np.pi/180)
    correctedNextVal = complex(r,i)
    return correctedNextVal

class TestCorrectedNEXT(TestParameter):
    def setUp(self):
        self._ports = {
            0: ("Port 1", False),
            1: ("Port 2", False),
            2: ("Port 3", False),
            3: ("Port 4", False),
        }
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._freq = [100, 200, 300, 500]
        self._parameter = self.createParameter()
 
    def createParameter(self):
        rl = ReturnLoss(self._ports, self._freq, self._matrices)
        opendfDelay = PropagationDelay(self._ports, self._freq, self._matrices, rl)
        shortdfDelay = PropagationDelay(self._ports, self._freq, self._matrices, rl)
        dfDelay = DFDelay(self._ports, self._freq, self._matrices, opendfDelay, shortdfDelay)
        openDelay = PropagationDelay(self._ports, self._freq, self._matrices, rl)
        shortDelay = PropagationDelay(self._ports, self._freq, self._matrices, rl)
        plugDelay = PlugDelay(self._ports, self._freq, self._matrices, openDelay, shortDelay, dfDelay, 1, 2, 3)
        nextDelay = NEXTDelay(self._ports, self._freq, self._matrices, plugDelay)

        return CorrectedNEXT(self._ports, self._freq, self._matrices, nextDelay)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        nextDelay = self._parameter.getNEXTDelay().getParameter()
        pnext = NEXT(self._ports, self._freq, self._matrices).getParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 12)

        # check the values of the port 1-2
        self.assertAlmostEqual(parameter[(0,1)][0], correctNEXT(pnext[(0,1)][0], nextDelay[(0,1)], self._freq[0]))
        self.assertAlmostEqual(parameter[(0,1)][1], correctNEXT(pnext[(0,1)][1], nextDelay[(0,1)], self._freq[1]))
        self.assertAlmostEqual(parameter[(0,1)][2], correctNEXT(pnext[(0,1)][2], nextDelay[(0,1)], self._freq[2]))
        self.assertAlmostEqual(parameter[(0,1)][3], correctNEXT(pnext[(0,1)][3], nextDelay[(0,1)], self._freq[3]))

        # check the values of the port 2-1
        self.assertAlmostEqual(parameter[(1,0)][0], correctNEXT(pnext[(1,0)][0], nextDelay[(0,1)], self._freq[0]))
        self.assertAlmostEqual(parameter[(1,0)][1], correctNEXT(pnext[(1,0)][1], nextDelay[(0,1)], self._freq[1]))
        self.assertAlmostEqual(parameter[(1,0)][2], correctNEXT(pnext[(1,0)][2], nextDelay[(0,1)], self._freq[2]))
        self.assertAlmostEqual(parameter[(1,0)][3], correctNEXT(pnext[(1,0)][3], nextDelay[(0,1)], self._freq[3]))

        # check the values of the port 3-4
        self.assertAlmostEqual(parameter[(2,3)][0], correctNEXT(pnext[(2,3)][0], nextDelay[(2,3)], self._freq[0]))
        self.assertAlmostEqual(parameter[(2,3)][1], correctNEXT(pnext[(2,3)][1], nextDelay[(2,3)], self._freq[1]))
        self.assertAlmostEqual(parameter[(2,3)][2], correctNEXT(pnext[(2,3)][2], nextDelay[(2,3)], self._freq[2]))
        self.assertAlmostEqual(parameter[(2,3)][3], correctNEXT(pnext[(2,3)][3], nextDelay[(2,3)], self._freq[3]))

        # check the values of the port 4-3
        self.assertAlmostEqual(parameter[(3,2)][0], correctNEXT(pnext[(3,2)][0], nextDelay[(2,3)], self._freq[0]))
        self.assertAlmostEqual(parameter[(3,2)][1], correctNEXT(pnext[(3,2)][1], nextDelay[(2,3)], self._freq[1]))
        self.assertAlmostEqual(parameter[(3,2)][2], correctNEXT(pnext[(3,2)][2], nextDelay[(2,3)], self._freq[2]))
        self.assertAlmostEqual(parameter[(3,2)][3], correctNEXT(pnext[(3,2)][3], nextDelay[(2,3)], self._freq[3]))

if __name__ == '__main__':
    unittest.main()
