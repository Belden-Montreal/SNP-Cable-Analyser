import unittest
from parameters.parameter import complex2phase
from parameters.test_parameter import TestParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
import numpy as np

def calculateDelay(rl1, rl2, f1, f2, previous=None):
    p1 = complex2phase(rl1)
    p2 = complex2phase(rl2)
    delay = -1/360 * (p2-p1)/(f2-f1)
    if delay < 0:
        if previous:
            delay = previous
        else:
            delay = 0.0
    return delay

class TestPropagationDelay(TestParameter):
    def setUp(self):
        super(TestPropagationDelay, self).setUp()
        self._matrices = np.array([
            [
                [complex(x,2*(z%2-1/2)*x) for x in range(8*y+1,8*(y+1)+1)] for y in range(8*z, 8*(z+1))
            ] for z in range(4)
        ], np.complex)
        self._parameter = self.createParameter()
 
    def createParameter(self):
        rl = ReturnLoss(self._ports, self._freq, self._matrices)

        return PropagationDelay(self._ports, self._freq, self._matrices, rl)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,0)]), len(self._freq))
        self.assertEqual(len(parameter[(1,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,2)]), len(self._freq))
        self.assertEqual(len(parameter[(3,3)]), len(self._freq))
        # check the values of the port 1
        self.assertAlmostEqual(parameter[(0,0)][0], calculateDelay(self._matrices[0, 0, 0],
            self._matrices[1, 0, 0], self._freq[0], self._freq[1]))
        self.assertAlmostEqual(parameter[(0,0)][1], calculateDelay(self._matrices[1, 0, 0],
            self._matrices[2, 0, 0], self._freq[1], self._freq[2], parameter[(0,0)][0]))
        self.assertAlmostEqual(parameter[(0,0)][2], calculateDelay(self._matrices[2, 0, 0],
            self._matrices[3, 0, 0], self._freq[2], self._freq[3], parameter[(0,0)][1]))
        self.assertAlmostEqual(parameter[(0,0)][3], calculateDelay(self._matrices[2, 0, 0],
            self._matrices[3, 0, 0], self._freq[2], self._freq[3], parameter[(0,0)][1]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[(1,1)][0], calculateDelay(self._matrices[0, 1, 1],
            self._matrices[1, 1, 1], self._freq[0], self._freq[1]))
        self.assertAlmostEqual(parameter[(1,1)][1], calculateDelay(self._matrices[1, 1, 1],
            self._matrices[2, 1, 1], self._freq[1], self._freq[2], parameter[(1,1)][0]))
        self.assertAlmostEqual(parameter[(1,1)][2], calculateDelay(self._matrices[2, 1, 1],
            self._matrices[3, 1, 1], self._freq[2], self._freq[3], parameter[(1,1)][1]))
        self.assertAlmostEqual(parameter[(1,1)][3], calculateDelay(self._matrices[2, 1, 1],
            self._matrices[3, 1, 1], self._freq[2], self._freq[3], parameter[(1,1)][1]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[(2,2)][0], calculateDelay(self._matrices[0, 2, 2],
            self._matrices[1, 2, 2], self._freq[0], self._freq[1]))
        self.assertAlmostEqual(parameter[(2,2)][1], calculateDelay(self._matrices[1, 2, 2],
            self._matrices[2, 2, 2], self._freq[1], self._freq[2], parameter[(2,2)][0]))
        self.assertAlmostEqual(parameter[(2,2)][2], calculateDelay(self._matrices[2, 2, 2],
            self._matrices[3, 2, 2], self._freq[2], self._freq[3], parameter[(2,2)][1]))
        self.assertAlmostEqual(parameter[(2,2)][3], calculateDelay(self._matrices[2, 2, 2],
            self._matrices[3, 2, 2], self._freq[2], self._freq[3], parameter[(2,2)][1]))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[(3,3)][0], calculateDelay(self._matrices[0, 3, 3],
            self._matrices[1, 3, 3], self._freq[0], self._freq[1]))
        self.assertAlmostEqual(parameter[(3,3)][1], calculateDelay(self._matrices[1, 3, 3],
            self._matrices[2, 3, 3], self._freq[1], self._freq[2], parameter[(3,3)][0]))
        self.assertAlmostEqual(parameter[(3,3)][2], calculateDelay(self._matrices[2, 3, 3],
            self._matrices[3, 3, 3], self._freq[2], self._freq[3], parameter[(3,3)][1]))
        self.assertAlmostEqual(parameter[(3,3)][3], calculateDelay(self._matrices[2, 3, 3],
            self._matrices[3, 3, 3], self._freq[2], self._freq[3], parameter[(3,3)][1]))

if __name__ == '__main__':
    unittest.main()
