import unittest
from parameters.parameter import complex2phase
from parameters.test_parameter import TestParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
import numpy as np

class TestNEXTDelay(TestParameter):
    def setUp(self):
        self._ports = {
            0: "Port 1",
            1: "Port 2",
            2: "Port 3",
            3: "Port 4",
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
        return NEXTDelay(self._ports, self._freq, self._matrices, plugDelay)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        plugDelay = self._parameter.getPlugDelay().getParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        # check the values of the port 1-2
        self.assertAlmostEqual(parameter[(0,1)], plugDelay[0]+plugDelay[1])
        # check the values of the port 1-3
        self.assertAlmostEqual(parameter[(0,2)], plugDelay[0]+plugDelay[2])
        # check the values of the port 1-4
        self.assertAlmostEqual(parameter[(0,3)], plugDelay[0]+plugDelay[3])
        # check the values of the port 2-3
        self.assertAlmostEqual(parameter[(1,2)], plugDelay[1]+plugDelay[2])
        # check the values of the port 2-4
        self.assertAlmostEqual(parameter[(1,3)], plugDelay[1]+plugDelay[3])
        # check the values of the port 3-4
        self.assertAlmostEqual(parameter[(2,3)], plugDelay[2]+plugDelay[3])

if __name__ == '__main__':
    unittest.main()
