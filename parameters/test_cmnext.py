import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.cmnext import CMNEXT

class TestCMNEXT(TestParameter):
    def createParameter(self):
        return CMNEXT(self._e2ePorts, self._freq, self._matrices)       

    def testComputePairs(self):
        seCmnext = CMNEXT(self._ports, self._freq, self._matrices)
        pairs = seCmnext.getPairs()

        # for a 4 ports single ended, there are 6 CMNEXT pairs 
        self.assertEqual(len(pairs), 6)

        # make sure the correct pairs are there
        self.assertEqual((0,1) in pairs, True)
        self.assertEqual((2,3) in pairs, True)

        pairs = self._parameter.getParameter().keys()
        #for a 4 ports end-to-end, there are 2 NEXT pairs
        self.assertEqual(len(pairs), 2)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there is only 4 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 2)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[(0,1)][0], complex2db(self._matrices[0, 4, 5]))
        self.assertAlmostEqual(parameter[(0,1)][1], complex2db(self._matrices[1, 4, 5]))
        self.assertAlmostEqual(parameter[(0,1)][2], complex2db(self._matrices[2, 4, 5]))
        self.assertAlmostEqual(parameter[(0,1)][3], complex2db(self._matrices[3, 4, 5]))

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[(2,3)][0], complex2db(self._matrices[0, 6, 7]))
        self.assertAlmostEqual(parameter[(2,3)][1], complex2db(self._matrices[1, 6, 7]))
        self.assertAlmostEqual(parameter[(2,3)][2], complex2db(self._matrices[2, 6, 7]))
        self.assertAlmostEqual(parameter[(2,3)][3], complex2db(self._matrices[3, 6, 7]))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there is only 2 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 2)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[(0,1)][0], self._matrices[0, 4, 5])
        self.assertAlmostEqual(parameter[(0,1)][1], self._matrices[1, 4, 5])
        self.assertAlmostEqual(parameter[(0,1)][2], self._matrices[2, 4, 5])
        self.assertAlmostEqual(parameter[(0,1)][3], self._matrices[3, 4, 5])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[(2,3)][0], self._matrices[0, 6, 7])
        self.assertAlmostEqual(parameter[(2,3)][1], self._matrices[1, 6, 7])
        self.assertAlmostEqual(parameter[(2,3)][2], self._matrices[2, 6, 7])
        self.assertAlmostEqual(parameter[(2,3)][3], self._matrices[3, 6, 7])

if __name__ == '__main__':
    unittest.main()
