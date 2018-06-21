import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.cmdmnext import CMDMNEXT

class TestCMDMNEXT(TestParameter):
    def createParameter(self):
        return CMDMNEXT(self._ports, self._freq, self._matrices)       

    def testComputePairs(self):
        pairs = self._parameter.getPairs()

        # for a 4 ports single ended, there are 12 NEXT pairs (including reverse)
        self.assertEqual(len(pairs), 12)

        # make sure the correct pairs are there
        self.assertEqual((0,1) in pairs, True)
        self.assertEqual((2,3) in pairs, True)
        self.assertEqual((1,0) in pairs, True)
        self.assertEqual((3,2) in pairs, True)

        pairs = self._parameter.getParameter(endToEnd=True).keys()
        #for a 4 ports end-to-end, there are 4 NEXT pairs
        self.assertEqual(len(pairs), 4)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there is only 4 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))
        self.assertEqual(len(parameter[(1,0)]), len(self._freq))
        self.assertEqual(len(parameter[(3,2)]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[(0,1)][0], complex2db(self._matrices[0, 4, 1]))
        self.assertAlmostEqual(parameter[(0,1)][1], complex2db(self._matrices[1, 4, 1]))
        self.assertAlmostEqual(parameter[(0,1)][2], complex2db(self._matrices[2, 4, 1]))
        self.assertAlmostEqual(parameter[(0,1)][3], complex2db(self._matrices[3, 4, 1]))

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[(2,3)][0], complex2db(self._matrices[0, 6, 3]))
        self.assertAlmostEqual(parameter[(2,3)][1], complex2db(self._matrices[1, 6, 3]))
        self.assertAlmostEqual(parameter[(2,3)][2], complex2db(self._matrices[2, 6, 3]))
        self.assertAlmostEqual(parameter[(2,3)][3], complex2db(self._matrices[3, 6, 3]))

        # check the values of the pair (1,0)
        self.assertAlmostEqual(parameter[(1,0)][0], complex2db(self._matrices[0, 5, 0]))
        self.assertAlmostEqual(parameter[(1,0)][1], complex2db(self._matrices[1, 5, 0]))
        self.assertAlmostEqual(parameter[(1,0)][2], complex2db(self._matrices[2, 5, 0]))
        self.assertAlmostEqual(parameter[(1,0)][3], complex2db(self._matrices[3, 5, 0]))

        # check the values of the pair (3,2)
        self.assertAlmostEqual(parameter[(3,2)][0], complex2db(self._matrices[0, 7, 2]))
        self.assertAlmostEqual(parameter[(3,2)][1], complex2db(self._matrices[1, 7, 2]))
        self.assertAlmostEqual(parameter[(3,2)][2], complex2db(self._matrices[2, 7, 2]))
        self.assertAlmostEqual(parameter[(3,2)][3], complex2db(self._matrices[3, 7, 2]))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there is only 4 NEXT pairs (including reverse)
        self.assertEqual(len(parameter), 4)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))
        self.assertEqual(len(parameter[(1,0)]), len(self._freq))
        self.assertEqual(len(parameter[(3,2)]), len(self._freq))

        # check the values of the pair (0,1)
        self.assertAlmostEqual(parameter[(0,1)][0], self._matrices[0, 4, 1])
        self.assertAlmostEqual(parameter[(0,1)][1], self._matrices[1, 4, 1])
        self.assertAlmostEqual(parameter[(0,1)][2], self._matrices[2, 4, 1])
        self.assertAlmostEqual(parameter[(0,1)][3], self._matrices[3, 4, 1])

        # check the values of the pair (2,3)
        self.assertAlmostEqual(parameter[(2,3)][0], self._matrices[0, 6, 3])
        self.assertAlmostEqual(parameter[(2,3)][1], self._matrices[1, 6, 3])
        self.assertAlmostEqual(parameter[(2,3)][2], self._matrices[2, 6, 3])
        self.assertAlmostEqual(parameter[(2,3)][3], self._matrices[3, 6, 3])

        # check the values of the pair (1,0)
        self.assertAlmostEqual(parameter[(1,0)][0], self._matrices[0, 5, 0])
        self.assertAlmostEqual(parameter[(1,0)][1], self._matrices[1, 5, 0])
        self.assertAlmostEqual(parameter[(1,0)][2], self._matrices[2, 5, 0])
        self.assertAlmostEqual(parameter[(1,0)][3], self._matrices[3, 5, 0])

        # check the values of the pair (3,2)
        self.assertAlmostEqual(parameter[(3,2)][0], self._matrices[0, 7, 2])
        self.assertAlmostEqual(parameter[(3,2)][1], self._matrices[1, 7, 2])
        self.assertAlmostEqual(parameter[(3,2)][2], self._matrices[2, 7, 2])
        self.assertAlmostEqual(parameter[(3,2)][3], self._matrices[3, 7, 2])

if __name__ == '__main__':
    unittest.main()
