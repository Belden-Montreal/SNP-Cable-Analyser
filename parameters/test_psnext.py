import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.next import NEXT
from parameters.psnext import PSNEXT, powerSum

class TestPSNEXT(TestParameter):
    def createParameter(self):
        nnext = NEXT(self._e2ePorts, self._freq, self._matrices)

        return PSNEXT(self._e2ePorts, self._freq, self._matrices, nnext)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        nnext = self._parameter.getNEXT().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # make sure the port were created
        self.assertEqual(0 in parameter, True)
        self.assertEqual(1 in parameter, True)
        self.assertEqual(2 in parameter, True)
        self.assertEqual(3 in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[1][0], powerSum([nnext[(0,1)][0]]))
        self.assertAlmostEqual(parameter[1][1], powerSum([nnext[(0,1)][1]]))
        self.assertAlmostEqual(parameter[1][2], powerSum([nnext[(0,1)][2]]))
        self.assertAlmostEqual(parameter[1][3], powerSum([nnext[(0,1)][3]]))

        # check the values of the port 0
        self.assertAlmostEqual(parameter[0][0], powerSum([nnext[(0,1)][0]]))
        self.assertAlmostEqual(parameter[0][1], powerSum([nnext[(0,1)][1]]))
        self.assertAlmostEqual(parameter[0][2], powerSum([nnext[(0,1)][2]]))
        self.assertAlmostEqual(parameter[0][3], powerSum([nnext[(0,1)][3]]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[3][0], powerSum([nnext[(2,3)][0]]))
        self.assertAlmostEqual(parameter[3][1], powerSum([nnext[(2,3)][1]]))
        self.assertAlmostEqual(parameter[3][2], powerSum([nnext[(2,3)][2]]))
        self.assertAlmostEqual(parameter[3][3], powerSum([nnext[(2,3)][3]]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[2][0], powerSum([nnext[(2,3)][0]]))
        self.assertAlmostEqual(parameter[2][1], powerSum([nnext[(2,3)][1]]))
        self.assertAlmostEqual(parameter[2][2], powerSum([nnext[(2,3)][2]]))
        self.assertAlmostEqual(parameter[2][3], powerSum([nnext[(2,3)][3]]))

    def testComputeOneEndedParameter(self):
        pnext = NEXT(self._ports, self._freq, self._matrices)
        sePSNext = PSNEXT(self._ports, self._freq, self._matrices, pnext)

        parameter = sePSNext.getParameter()
        nnext = pnext.getParameter()

        # check the values of the port 0
        self.assertAlmostEqual(parameter[0][0], powerSum([nnext[(0,1)][0], nnext[(0,2)][0], nnext[(0,3)][0]]))
        self.assertAlmostEqual(parameter[0][1], powerSum([nnext[(0,1)][1], nnext[(0,2)][1], nnext[(0,3)][1]]))
        self.assertAlmostEqual(parameter[0][2], powerSum([nnext[(0,1)][2], nnext[(0,2)][2], nnext[(0,3)][2]]))
        self.assertAlmostEqual(parameter[0][3], powerSum([nnext[(0,1)][3], nnext[(0,2)][3], nnext[(0,3)][3]]))

        # check values of the port 1
        self.assertAlmostEqual(parameter[1][0], powerSum([nnext[(0,1)][0], nnext[(1,2)][0], nnext[(1,3)][0]]))
        self.assertAlmostEqual(parameter[1][1], powerSum([nnext[(0,1)][1], nnext[(1,2)][1], nnext[(1,3)][1]]))
        self.assertAlmostEqual(parameter[1][2], powerSum([nnext[(0,1)][2], nnext[(1,2)][2], nnext[(1,3)][2]]))
        self.assertAlmostEqual(parameter[1][3], powerSum([nnext[(0,1)][3], nnext[(1,2)][3], nnext[(1,3)][3]]))

        # check values of the port 2
        self.assertAlmostEqual(parameter[2][0], powerSum([nnext[(0,2)][0], nnext[(1,2)][0], nnext[(2,3)][0]]))
        self.assertAlmostEqual(parameter[2][1], powerSum([nnext[(0,2)][1], nnext[(1,2)][1], nnext[(2,3)][1]]))
        self.assertAlmostEqual(parameter[2][2], powerSum([nnext[(0,2)][2], nnext[(1,2)][2], nnext[(2,3)][2]]))
        self.assertAlmostEqual(parameter[2][3], powerSum([nnext[(0,2)][3], nnext[(1,2)][3], nnext[(2,3)][3]]))

        #check values of the port 3
        self.assertAlmostEqual(parameter[3][0], powerSum([nnext[(0,3)][0], nnext[(1,3)][0], nnext[(2,3)][0]]))
        self.assertAlmostEqual(parameter[3][1], powerSum([nnext[(0,3)][1], nnext[(1,3)][1], nnext[(2,3)][1]]))
        self.assertAlmostEqual(parameter[3][2], powerSum([nnext[(0,3)][2], nnext[(1,3)][2], nnext[(2,3)][2]]))
        self.assertAlmostEqual(parameter[3][3], powerSum([nnext[(0,3)][3], nnext[(1,3)][3], nnext[(2,3)][3]]))

if __name__ == '__main__':
    unittest.main()
