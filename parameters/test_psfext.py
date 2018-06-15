import unittest
import numpy as np
from parameters.test_parameter import TestParameter
from parameters.psfext import PSFEXT
from parameters.fext import FEXT

def powersum(fext, f, port):
    keys = fext.keys()
    return 10*np.log10(np.sum([10**(fext[key][f]/10) for key in keys if (key[0] == port ) ]))

class TestPsFEXT(TestParameter):
    def createParameter(self):
        # we assume that FEXT is tested
        fext = FEXT(self._ports, self._freq, self._matrices)

        return PSFEXT(self._ports, self._freq, self._matrices, fext)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        dbFEXT = self._parameter.getFEXT().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], powersum(dbFEXT, 0, 0))
        self.assertAlmostEqual(parameter[0][1], powersum(dbFEXT, 1, 0))
        self.assertAlmostEqual(parameter[0][2], powersum(dbFEXT, 2, 0))
        self.assertAlmostEqual(parameter[0][3], powersum(dbFEXT, 3, 0))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], powersum(dbFEXT, 0, 1))
        self.assertAlmostEqual(parameter[1][1], powersum(dbFEXT, 1, 1))
        self.assertAlmostEqual(parameter[1][2], powersum(dbFEXT, 2, 1))
        self.assertAlmostEqual(parameter[1][3], powersum(dbFEXT, 3, 1))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], powersum(dbFEXT, 0, 2))
        self.assertAlmostEqual(parameter[2][1], powersum(dbFEXT, 1, 2))
        self.assertAlmostEqual(parameter[2][2], powersum(dbFEXT, 2, 2))
        self.assertAlmostEqual(parameter[2][3], powersum(dbFEXT, 3, 2))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], powersum(dbFEXT, 0, 3))
        self.assertAlmostEqual(parameter[3][1], powersum(dbFEXT, 1, 3))
        self.assertAlmostEqual(parameter[3][2], powersum(dbFEXT, 2, 3))
        self.assertAlmostEqual(parameter[3][3], powersum(dbFEXT, 3, 3))

if __name__ == '__main__':
    unittest.main()
