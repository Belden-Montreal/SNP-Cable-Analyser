import unittest
import numpy as np
from parameters.test_parameter import TestParameter
from parameters.psanext import PSANEXT
from parameters.anext import ANEXT
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss

def powersum(anextd, f, port):
    return 10*np.log10(np.sum([np.sum([10**(disturber.getParameter()[key][f]/10) for key in disturber.getParameter().keys() if (key[0] == port )]) for disturber in anextd ]))

class TestPsFEXT(TestParameter):
    def createParameter(self):
        # we assume that ANEXT, fext and il are tested
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        fext = FEXT(self._ports, self._freq, self._matrices)
        anextd = [ANEXT(self._ports, self._freq, self._matrices, fext, il) for x in range(4)]

        return PSANEXT(self._ports, self._freq, self._matrices, anextd)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        anextd = self._parameter.getANEXT()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], powersum(anextd, 0, 0))
        self.assertAlmostEqual(parameter[0][1], powersum(anextd, 1, 0))
        self.assertAlmostEqual(parameter[0][2], powersum(anextd, 2, 0))
        self.assertAlmostEqual(parameter[0][3], powersum(anextd, 3, 0))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], powersum(anextd, 0, 1))
        self.assertAlmostEqual(parameter[1][1], powersum(anextd, 1, 1))
        self.assertAlmostEqual(parameter[1][2], powersum(anextd, 2, 1))
        self.assertAlmostEqual(parameter[1][3], powersum(anextd, 3, 1))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], powersum(anextd, 0, 2))
        self.assertAlmostEqual(parameter[2][1], powersum(anextd, 1, 2))
        self.assertAlmostEqual(parameter[2][2], powersum(anextd, 2, 2))
        self.assertAlmostEqual(parameter[2][3], powersum(anextd, 3, 2))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], powersum(anextd, 0, 3))
        self.assertAlmostEqual(parameter[3][1], powersum(anextd, 1, 3))
        self.assertAlmostEqual(parameter[3][2], powersum(anextd, 2, 3))
        self.assertAlmostEqual(parameter[3][3], powersum(anextd, 3, 3))

if __name__ == '__main__':
    unittest.main()
