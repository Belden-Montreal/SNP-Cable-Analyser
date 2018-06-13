import unittest
import numpy as np
from parameters.test_parameter import TestParameter
from parameters.psfext import PsFext
from parameters.fext import Fext

def powersum(fext, f, port):
    keys = fext.keys()
    return 10*np.log10(np.sum([10**(fext[key][f]/10) for key in keys if (key[0] == port ) ]))

class TestPsFext(TestParameter):
    def testComputeParameter(self):

        fext = Fext(self._ports, self._freq, self._matrices)
        psfext = PsFext(self._ports, self._freq, self._matrices, fext)
        parameter = psfext.getParameter()
        #assume that fext is tested
        dbFext = fext.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], powersum(dbFext, 0, 0))
        self.assertAlmostEqual(parameter[0][1], powersum(dbFext, 1, 0))
        self.assertAlmostEqual(parameter[0][2], powersum(dbFext, 2, 0))
        self.assertAlmostEqual(parameter[0][3], powersum(dbFext, 3, 0))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], powersum(dbFext, 0, 1))
        self.assertAlmostEqual(parameter[1][1], powersum(dbFext, 1, 1))
        self.assertAlmostEqual(parameter[1][2], powersum(dbFext, 2, 1))
        self.assertAlmostEqual(parameter[1][3], powersum(dbFext, 3, 1))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], powersum(dbFext, 0, 2))
        self.assertAlmostEqual(parameter[2][1], powersum(dbFext, 1, 2))
        self.assertAlmostEqual(parameter[2][2], powersum(dbFext, 2, 2))
        self.assertAlmostEqual(parameter[2][3], powersum(dbFext, 3, 2))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], powersum(dbFext, 0, 3))
        self.assertAlmostEqual(parameter[3][1], powersum(dbFext, 1, 3))
        self.assertAlmostEqual(parameter[3][2], powersum(dbFext, 2, 3))
        self.assertAlmostEqual(parameter[3][3], powersum(dbFext, 3, 3))

if __name__ == '__main__':
    unittest.main()
