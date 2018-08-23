import unittest

from parameters.test_parameter import TestPlugParameter
from parameters.propagationdelay import PropagationDelay
from parameters.returnloss import ReturnLoss
from parameters.dfdelay import DFDelay
from parameters.plugdelay import PlugDelay
from parameters.nextdelay import NEXTDelay
from parameters.next import NEXT
from parameters.dnext import DNEXT
from parameters.correctednext import CorrectedNEXT
from parameters.case import Case
from parameters.dataserie import PortPairDataSerie

import numpy as np

def plugToComplex(plug):
    dbPlug = plug[0]
    phasePlug = plug[1]
    
    amp = 10**(dbPlug/20)
    
    re = amp*np.cos(phasePlug*np.pi/180)
    im = amp*np.sin(phasePlug*np.pi/180)
    cPlug = complex(re, im)
    return cPlug

class TestCase(TestPlugParameter):
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
        dnext = DNEXT(self._config, self._freq, self._matrices, nextDelay, pnext)

        self._dataseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[0], self._ports[2]),
            2: PortPairDataSerie(self._ports[0], self._ports[3]),
            3: PortPairDataSerie(self._ports[1], self._ports[2]),
            4: PortPairDataSerie(self._ports[1], self._ports[3]),
            5: PortPairDataSerie(self._ports[2], self._ports[3]),
        }

        self._cases = {
            1:(self._dataseries[0],(lambda f, cnext: (30-20*np.log10(f/100), np.angle(cnext)))),
            2:(self._dataseries[1],(lambda f, cnext: (20-20*np.log10(f/100), 90))),
            3:(self._dataseries[2],(lambda f, cnext: (10-20*np.log10(f/100), 90))),
            4:(self._dataseries[3],(lambda f, cnext: (15-20*np.log10(f/100), 90))),
            5:(self._dataseries[4],(lambda f, cnext: (5-20*np.log10(f/100), 90))),
            6:(self._dataseries[5],(lambda f, cnext: (35-20*np.log10(f/100), np.angle(cnext))))
        }

        return Case(self._config, self._freq, self._matrices, dnext, pnext, self._cases)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getComplexParameter()
        cases = self._parameter.getCases()
        dnext = self._parameter.getDNEXT().getComplexParameter()
        cnext = self._parameter.getCNEXT().getComplexParameter()

        # there should be a parameter for each port combo        
        self.assertEqual(len(parameter), 6)

        # check the values of the port (0,1)
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][0],
            dnext[self._dataseries[0]][0]+plugToComplex(cases[1][1](self._freq[0], cnext[self._dataseries[0]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][1],
            dnext[self._dataseries[0]][1]+plugToComplex(cases[1][1](self._freq[1], cnext[self._dataseries[0]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][2],
            dnext[self._dataseries[0]][2]+plugToComplex(cases[1][1](self._freq[2], cnext[self._dataseries[0]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][3],
            dnext[self._dataseries[0]][3]+plugToComplex(cases[1][1](self._freq[3], cnext[self._dataseries[0]][3])))

        # check the values of the port (0,2)
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0],
            dnext[self._dataseries[1]][0]+plugToComplex(cases[2][1](self._freq[0], cnext[self._dataseries[1]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][1],
            dnext[self._dataseries[1]][1]+plugToComplex(cases[2][1](self._freq[1], cnext[self._dataseries[1]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][2],
            dnext[self._dataseries[1]][2]+plugToComplex(cases[2][1](self._freq[2], cnext[self._dataseries[1]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][3],
            dnext[self._dataseries[1]][3]+plugToComplex(cases[2][1](self._freq[3], cnext[self._dataseries[1]][3]))) 

        # check the values of the port (0,3)
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0],
            dnext[self._dataseries[2]][0]+plugToComplex(cases[3][1](self._freq[0], cnext[self._dataseries[2]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][1],
            dnext[self._dataseries[2]][1]+plugToComplex(cases[3][1](self._freq[1], cnext[self._dataseries[2]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][2],
            dnext[self._dataseries[2]][2]+plugToComplex(cases[3][1](self._freq[2], cnext[self._dataseries[2]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][3],
            dnext[self._dataseries[2]][3]+plugToComplex(cases[3][1](self._freq[3], cnext[self._dataseries[2]][3]))) 

        # check the values of the port (1,2)
        self.assertAlmostEqual(parameter[self._dataseries[3]][4][0],
            dnext[self._dataseries[3]][0]+plugToComplex(cases[4][1](self._freq[0], cnext[self._dataseries[3]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[3]][4][1],
            dnext[self._dataseries[3]][1]+plugToComplex(cases[4][1](self._freq[1], cnext[self._dataseries[3]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[3]][4][2],
            dnext[self._dataseries[3]][2]+plugToComplex(cases[4][1](self._freq[2], cnext[self._dataseries[3]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[3]][4][3],
            dnext[self._dataseries[3]][3]+plugToComplex(cases[4][1](self._freq[3], cnext[self._dataseries[3]][3]))) 

        # check the values of the port (1,3)
        self.assertAlmostEqual(parameter[self._dataseries[4]][5][0],
            dnext[self._dataseries[4]][0]+plugToComplex(cases[5][1](self._freq[0], cnext[self._dataseries[4]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[4]][5][1],
            dnext[self._dataseries[4]][1]+plugToComplex(cases[5][1](self._freq[1], cnext[self._dataseries[4]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[4]][5][2],
            dnext[self._dataseries[4]][2]+plugToComplex(cases[5][1](self._freq[2], cnext[self._dataseries[4]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[4]][5][3],
            dnext[self._dataseries[4]][3]+plugToComplex(cases[5][1](self._freq[3], cnext[self._dataseries[4]][3]))) 

        # check the values of the port (2,3)
        self.assertAlmostEqual(parameter[self._dataseries[5]][6][0],
            dnext[self._dataseries[5]][0]+plugToComplex(cases[6][1](self._freq[0], cnext[self._dataseries[5]][0])))
        self.assertAlmostEqual(parameter[self._dataseries[5]][6][1],
            dnext[self._dataseries[5]][1]+plugToComplex(cases[6][1](self._freq[1], cnext[self._dataseries[5]][1])))
        self.assertAlmostEqual(parameter[self._dataseries[5]][6][2],
            dnext[self._dataseries[5]][2]+plugToComplex(cases[6][1](self._freq[2], cnext[self._dataseries[5]][2])))
        self.assertAlmostEqual(parameter[self._dataseries[5]][6][3],
            dnext[self._dataseries[5]][3]+plugToComplex(cases[6][1](self._freq[3], cnext[self._dataseries[5]][3])))     

if __name__ == '__main__':
    unittest.main()
