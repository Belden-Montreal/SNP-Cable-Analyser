import unittest
from parameters.test_parameter import TestParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
from parameters.next import NEXT
from parameters.dnext import DNEXT
from parameters.correctednext import CorrectedNEXT
from parameters.case import Case
import numpy as np

def plugToComplex(plug):
    dbPlug = plug[0]
    phasePlug = plug[1]
    
    amp = 10**(dbPlug/20)
    
    re = amp*np.cos(phasePlug*np.pi/180)
    im = amp*np.sin(phasePlug*np.pi/180)
    cPlug = complex(re, im)
    return cPlug

class TestCase(TestParameter):
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
        pnext = CorrectedNEXT(self._ports, self._freq, self._matrices, nextDelay)
        dnext = DNEXT(self._ports, self._freq, self._matrices, nextDelay, pnext)

        self._cases = {
            1:((0,1),(lambda f, cnext: (30-20*np.log10(f/100), np.angle(cnext)))),
            2:((0,2),(lambda f, cnext: (20-20*np.log10(f/100), 90))),
            3:((0,3),(lambda f, cnext: (10-20*np.log10(f/100), 90))),
            4:((1,2),(lambda f, cnext: (15-20*np.log10(f/100), 90))),
            5:((1,3),(lambda f, cnext: (5-20*np.log10(f/100), 90))),
            6:((2,3),(lambda f, cnext: (35-20*np.log10(f/100), np.angle(cnext))))
            }
        return Case(self._ports, self._freq, self._matrices, dnext, pnext, self._cases)

    def testComputeParameter(self):
        parameter = self._parameter.getComplexParameter()
        cases = self._parameter.getCases()
        dnext = self._parameter.getDNEXT().getComplexParameter()
        cnext = self._parameter.getCNEXT().getComplexParameter()
        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        # check the values of the port 1-2
        self.assertAlmostEqual(parameter[(0,1)][1][0], dnext[(0,1)][0]+plugToComplex(cases[1][1](self._freq[0], cnext[(0,1)][0])))
        self.assertAlmostEqual(parameter[(0,1)][1][1], dnext[(0,1)][1]+plugToComplex(cases[1][1](self._freq[1], cnext[(0,1)][1])))
        self.assertAlmostEqual(parameter[(0,1)][1][2], dnext[(0,1)][2]+plugToComplex(cases[1][1](self._freq[2], cnext[(0,1)][2])))
        self.assertAlmostEqual(parameter[(0,1)][1][3], dnext[(0,1)][3]+plugToComplex(cases[1][1](self._freq[3], cnext[(0,1)][3])))

        # check the values of the port 1-3
        self.assertAlmostEqual(parameter[(0,2)][2][0], dnext[(0,2)][0]+plugToComplex(cases[2][1](self._freq[0], cnext[(0,2)][0])))
        self.assertAlmostEqual(parameter[(0,2)][2][1], dnext[(0,2)][1]+plugToComplex(cases[2][1](self._freq[1], cnext[(0,2)][1])))
        self.assertAlmostEqual(parameter[(0,2)][2][2], dnext[(0,2)][2]+plugToComplex(cases[2][1](self._freq[2], cnext[(0,2)][2])))
        self.assertAlmostEqual(parameter[(0,2)][2][3], dnext[(0,2)][3]+plugToComplex(cases[2][1](self._freq[3], cnext[(0,2)][3])))

        # check the values of the port 1-4
        self.assertAlmostEqual(parameter[(0,3)][3][0], dnext[(0,3)][0]+plugToComplex(cases[3][1](self._freq[0], cnext[(0,3)][0])))
        self.assertAlmostEqual(parameter[(0,3)][3][1], dnext[(0,3)][1]+plugToComplex(cases[3][1](self._freq[1], cnext[(0,3)][1])))
        self.assertAlmostEqual(parameter[(0,3)][3][2], dnext[(0,3)][2]+plugToComplex(cases[3][1](self._freq[2], cnext[(0,3)][2])))
        self.assertAlmostEqual(parameter[(0,3)][3][3], dnext[(0,3)][3]+plugToComplex(cases[3][1](self._freq[3], cnext[(0,3)][3])))

        # check the values of the port 2-3
        self.assertAlmostEqual(parameter[(1,2)][4][0], dnext[(1,2)][0]+plugToComplex(cases[4][1](self._freq[0], cnext[(1,2)][0])))
        self.assertAlmostEqual(parameter[(1,2)][4][1], dnext[(1,2)][1]+plugToComplex(cases[4][1](self._freq[1], cnext[(1,2)][1])))
        self.assertAlmostEqual(parameter[(1,2)][4][2], dnext[(1,2)][2]+plugToComplex(cases[4][1](self._freq[2], cnext[(1,2)][2])))
        self.assertAlmostEqual(parameter[(1,2)][4][3], dnext[(1,2)][3]+plugToComplex(cases[4][1](self._freq[3], cnext[(1,2)][3])))

        # check the values of the port 2-4
        self.assertAlmostEqual(parameter[(1,3)][5][0], dnext[(1,3)][0]+plugToComplex(cases[5][1](self._freq[0], cnext[(1,3)][0])))
        self.assertAlmostEqual(parameter[(1,3)][5][1], dnext[(1,3)][1]+plugToComplex(cases[5][1](self._freq[1], cnext[(1,3)][1])))
        self.assertAlmostEqual(parameter[(1,3)][5][2], dnext[(1,3)][2]+plugToComplex(cases[5][1](self._freq[2], cnext[(1,3)][2])))
        self.assertAlmostEqual(parameter[(1,3)][5][3], dnext[(1,3)][3]+plugToComplex(cases[5][1](self._freq[3], cnext[(1,3)][3])))

        # check the values of the port 3-4
        self.assertAlmostEqual(parameter[(2,3)][6][0], dnext[(2,3)][0]+plugToComplex(cases[6][1](self._freq[0], cnext[(2,3)][0])))
        self.assertAlmostEqual(parameter[(2,3)][6][1], dnext[(2,3)][1]+plugToComplex(cases[6][1](self._freq[1], cnext[(2,3)][1])))
        self.assertAlmostEqual(parameter[(2,3)][6][2], dnext[(2,3)][2]+plugToComplex(cases[6][1](self._freq[2], cnext[(2,3)][2])))
        self.assertAlmostEqual(parameter[(2,3)][6][3], dnext[(2,3)][3]+plugToComplex(cases[6][1](self._freq[3], cnext[(2,3)][3])))    

if __name__ == '__main__':
    unittest.main()
