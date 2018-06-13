import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.next import NEXTSingleEnded

class TestNEXTSingleEnded(TestParameter):
    def testComputePairs(self):
        NEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        pairs = NEXT.getPairs()

        # for a 4 ports, there is only 2 NEXT pairs
        self.assertEqual(len(pairs), 2)

        # make sure the two correct pairs are there
        self.assertEqual((0,1) in pairs, True)
        self.assertEqual((2,3) in pairs, True)

    def testComputeParameter(self):
        NEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        parameter = NEXT.getParameter()

        # for a 4 ports, there is only 2 NEXT parameters
        self.assertEqual(len(parameter), 2)

        # make sure the pair were created
        self.assertEqual((0,1) in parameter, True)
        self.assertEqual((2,3) in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))

        # check the values of the pair 1
        self.assertAlmostEqual(parameter[(0,1)][0], complex2db(self._matrices[0, 0, 1]))
        self.assertAlmostEqual(parameter[(0,1)][1], complex2db(self._matrices[1, 0, 1]))
        self.assertAlmostEqual(parameter[(0,1)][2], complex2db(self._matrices[2, 0, 1]))
        self.assertAlmostEqual(parameter[(0,1)][3], complex2db(self._matrices[3, 0, 1]))

        # check the values of the pair 2
        self.assertAlmostEqual(parameter[(2,3)][0], complex2db(self._matrices[0, 2, 3]))
        self.assertAlmostEqual(parameter[(2,3)][1], complex2db(self._matrices[1, 2, 3]))
        self.assertAlmostEqual(parameter[(2,3)][2], complex2db(self._matrices[2, 2, 3]))
        self.assertAlmostEqual(parameter[(2,3)][3], complex2db(self._matrices[3, 2, 3]))

    def testComputeComplexParameter(self):
        NEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        parameter = NEXT.getComplexParameter()

        # for a 4 ports, there is only 2 NEXT parameters
        self.assertEqual(len(parameter), 2)

        # make sure the pair were created
        self.assertEqual((0,1) in parameter, True)
        self.assertEqual((2,3) in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,1)]), len(self._freq))
        self.assertEqual(len(parameter[(2,3)]), len(self._freq))

        # check the values of the pair 1
        self.assertAlmostEqual(parameter[(0,1)][0], self._matrices[0, 0, 1])
        self.assertAlmostEqual(parameter[(0,1)][1], self._matrices[1, 0, 1])
        self.assertAlmostEqual(parameter[(0,1)][2], self._matrices[2, 0, 1])
        self.assertAlmostEqual(parameter[(0,1)][3], self._matrices[3, 0, 1])

        # check the values of the pair 2
        self.assertAlmostEqual(parameter[(2,3)][0], self._matrices[0, 2, 3])
        self.assertAlmostEqual(parameter[(2,3)][1], self._matrices[1, 2, 3])
        self.assertAlmostEqual(parameter[(2,3)][2], self._matrices[2, 2, 3])
        self.assertAlmostEqual(parameter[(2,3)][3], self._matrices[3, 2, 3])

if __name__ == '__main__':
    unittest.main()
