import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.next import NEXTSingleEnded
from parameters.psnext import PSNEXT, powerSum

class TestPSNEXT(TestParameter):
    def testComputeParameter(self):
        pNEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        pPSNEXT = PSNEXT(self._ports, self._freq, self._matrices, pNEXT)
        parameter = pPSNEXT.getParameter()

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

        # check the values of the port 0
        self.assertAlmostEqual(parameter[0][0], powerSum([pNEXT.getParameter()[(0,1)][0]]))
        self.assertAlmostEqual(parameter[0][1], powerSum([pNEXT.getParameter()[(0,1)][1]]))
        self.assertAlmostEqual(parameter[0][2], powerSum([pNEXT.getParameter()[(0,1)][2]]))
        self.assertAlmostEqual(parameter[0][3], powerSum([pNEXT.getParameter()[(0,1)][3]]))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[1][0], powerSum([pNEXT.getParameter()[(0,1)][0]]))
        self.assertAlmostEqual(parameter[1][1], powerSum([pNEXT.getParameter()[(0,1)][1]]))
        self.assertAlmostEqual(parameter[1][2], powerSum([pNEXT.getParameter()[(0,1)][2]]))
        self.assertAlmostEqual(parameter[1][3], powerSum([pNEXT.getParameter()[(0,1)][3]]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[2][0], powerSum([pNEXT.getParameter()[(2,3)][0]]))
        self.assertAlmostEqual(parameter[2][1], powerSum([pNEXT.getParameter()[(2,3)][1]]))
        self.assertAlmostEqual(parameter[2][2], powerSum([pNEXT.getParameter()[(2,3)][2]]))
        self.assertAlmostEqual(parameter[2][3], powerSum([pNEXT.getParameter()[(2,3)][3]]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[3][0], powerSum([pNEXT.getParameter()[(2,3)][0]]))
        self.assertAlmostEqual(parameter[3][1], powerSum([pNEXT.getParameter()[(2,3)][1]]))
        self.assertAlmostEqual(parameter[3][2], powerSum([pNEXT.getParameter()[(2,3)][2]]))
        self.assertAlmostEqual(parameter[3][3], powerSum([pNEXT.getParameter()[(2,3)][3]]))

    def testComputeComplexParameter(self):
        pNEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        pPSNEXT = PSNEXT(self._ports, self._freq, self._matrices, pNEXT)
        parameter = pPSNEXT.getComplexParameter()

        # for a 4 ports, there is only 2 NEXT parameters
        self.assertEqual(parameter, None)

if __name__ == '__main__':
    unittest.main()
