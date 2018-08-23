import unittest
from snpanalyzer.parameters.parameter import complex2phase
from snpanalyzer.parameters.test_parameter import TestParameter
from snpanalyzer.parameters.propagationdelay import PropagationDelay
from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.dataserie import PortDataSerie
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
        rl = ReturnLoss(self._config, self._freq, self._matrices)
        return PropagationDelay(self._config, self._freq, self._matrices, rl)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(PortDataSerie(self._ports[0]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[1]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[2]) in self._series, True)
        self.assertEqual(PortDataSerie(self._ports[3]) in self._series, True)

    def assertDelayCorrect(self, param, f, f1, f2, p, prev=None):
        if prev:
            prev = param[PortDataSerie(self._ports[prev])][f]
        self.assertAlmostEqual(param[PortDataSerie(self._ports[p])][f],
            calculateDelay(
                self._matrices[f1, p, p], self._matrices[f2, p, p],
                self._freq[f1], self._freq[f2], previous=prev
            )
        )

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[PortDataSerie(self._ports[0])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[1])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[2])]), len(self._freq))
        self.assertEqual(len(parameter[PortDataSerie(self._ports[3])]), len(self._freq))

        # check the values of the port 0
        self.assertDelayCorrect(parameter, 0, 0, 1, 0)
        self.assertDelayCorrect(parameter, 1, 1, 2, 0, prev=0)
        self.assertDelayCorrect(parameter, 2, 2, 3, 0, prev=1)
        self.assertDelayCorrect(parameter, 3, 2, 3, 0, prev=1)

        # check the values of the port 1
        self.assertDelayCorrect(parameter, 0, 0, 1, 1)
        self.assertDelayCorrect(parameter, 1, 1, 2, 1, prev=0)
        self.assertDelayCorrect(parameter, 2, 2, 3, 1, prev=1)
        self.assertDelayCorrect(parameter, 3, 2, 3, 1, prev=1)

        # check the values of the port 2
        self.assertDelayCorrect(parameter, 0, 0, 1, 2)
        self.assertDelayCorrect(parameter, 1, 1, 2, 2, prev=0)
        self.assertDelayCorrect(parameter, 2, 2, 3, 2, prev=1)
        self.assertDelayCorrect(parameter, 3, 2, 3, 2, prev=1)

        # check the values of the port 3
        self.assertDelayCorrect(parameter, 0, 0, 1, 3)
        self.assertDelayCorrect(parameter, 1, 1, 2, 3, prev=0)
        self.assertDelayCorrect(parameter, 2, 2, 3, 3, prev=1)
        self.assertDelayCorrect(parameter, 3, 2, 3, 3, prev=1)

if __name__ == '__main__':
    unittest.main()
