import unittest
import numpy as np
from parameters.test_parameter import TestParameter
from parameters.psaxext import PSAXEXT
from parameters.axext import AXEXT
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss

def powersum(axextd, f, port):
    return 10*np.log10(np.sum([np.sum([10**(disturber.getParameter()[key][f]/10) for key in disturber.getParameter().keys() if (key[0] == port )]) for disturber in axextd ]))

class TestPSAXEXT(TestParameter):
    def createParameter(self):
        # we assume that ANEXT, fext and il are tested
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        fext = FEXT(self._ports, self._freq, self._matrices)
        axextd = [AXEXT(self._ports, self._freq, self._matrices, fext, il) for x in range(4)]

        return PSAXEXT(self._ports, self._freq, self._matrices, axextd)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        axextd = self._parameter.getAXEXT()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], powersum(axextd, 0, 0))
        self.assertAlmostEqual(parameter[0][1], powersum(axextd, 1, 0))
        self.assertAlmostEqual(parameter[0][2], powersum(axextd, 2, 0))
        self.assertAlmostEqual(parameter[0][3], powersum(axextd, 3, 0))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], powersum(axextd, 0, 1))
        self.assertAlmostEqual(parameter[1][1], powersum(axextd, 1, 1))
        self.assertAlmostEqual(parameter[1][2], powersum(axextd, 2, 1))
        self.assertAlmostEqual(parameter[1][3], powersum(axextd, 3, 1))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], powersum(axextd, 0, 2))
        self.assertAlmostEqual(parameter[2][1], powersum(axextd, 1, 2))
        self.assertAlmostEqual(parameter[2][2], powersum(axextd, 2, 2))
        self.assertAlmostEqual(parameter[2][3], powersum(axextd, 3, 2))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], powersum(axextd, 0, 3))
        self.assertAlmostEqual(parameter[3][1], powersum(axextd, 1, 3))
        self.assertAlmostEqual(parameter[3][2], powersum(axextd, 2, 3))
        self.assertAlmostEqual(parameter[3][3], powersum(axextd, 3, 3))

if __name__ == '__main__':
    unittest.main()
