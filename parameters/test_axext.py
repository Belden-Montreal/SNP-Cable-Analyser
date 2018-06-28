import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss
from parameters.axext import AXEXT

class TestAXEXT(TestParameter):
    def createParameter(self):
        #we assume that fext and il are tested
        fext = FEXT(self._e2ePorts, self._freq, self._matrices)
        il = InsertionLoss(self._e2ePorts, self._freq, self._matrices)
        return AXEXT(self._e2ePorts, self._freq, self._matrices, fext, il)

    def testComputePairs(self):
        pairs = self._parameter.getPairs()

        # for a 4 ports, there are 8 ANEXT pairs (including reverse)
        self.assertEqual(len(pairs), 8)

        # make sure the correct pairs were created
        self.assertEqual((0,3) in pairs, True)
        self.assertEqual((3,0) in pairs, True)
        self.assertEqual((0,2) in pairs, True)
        self.assertEqual((2,0) in pairs, True)
        self.assertEqual((1,2) in pairs, True)
        self.assertEqual((2,1) in pairs, True)
        self.assertEqual((1,3) in pairs, True)
        self.assertEqual((3,1) in pairs, True)     

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # for a 4 ports, there are 8 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 8)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,3)]), len(self._freq))
        self.assertEqual(len(parameter[(3,0)]), len(self._freq))
        self.assertEqual(len(parameter[(1,2)]), len(self._freq))
        self.assertEqual(len(parameter[(2,1)]), len(self._freq))

        # check the values of the pair (2,1)
        self.assertEqual(parameter[(2,1)][0], complex2db(self._matrices[0, 2, 1]))
        self.assertEqual(parameter[(2,1)][1], complex2db(self._matrices[1, 2, 1]))
        self.assertEqual(parameter[(2,1)][2], complex2db(self._matrices[2, 2, 1]))
        self.assertEqual(parameter[(2,1)][3], complex2db(self._matrices[3, 2, 1]))

        # check the values of the pair (1,2)
        self.assertEqual(parameter[(1,2)][0], complex2db(self._matrices[0, 1, 2]))
        self.assertEqual(parameter[(1,2)][1], complex2db(self._matrices[1, 1, 2]))
        self.assertEqual(parameter[(1,2)][2], complex2db(self._matrices[2, 1, 2]))
        self.assertEqual(parameter[(1,2)][3], complex2db(self._matrices[3, 1, 2]))

        # check the values of the pair (3,0)
        self.assertEqual(parameter[(3,0)][0], complex2db(self._matrices[0, 3, 0]))
        self.assertEqual(parameter[(3,0)][1], complex2db(self._matrices[1, 3, 0]))
        self.assertEqual(parameter[(3,0)][2], complex2db(self._matrices[2, 3, 0]))
        self.assertEqual(parameter[(3,0)][3], complex2db(self._matrices[3, 3, 0]))

        # check the values of the pair (0,3)
        self.assertEqual(parameter[(0,3)][0], complex2db(self._matrices[0, 0, 3]))
        self.assertEqual(parameter[(0,3)][1], complex2db(self._matrices[1, 0, 3]))
        self.assertEqual(parameter[(0,3)][2], complex2db(self._matrices[2, 0, 3]))
        self.assertEqual(parameter[(0,3)][3], complex2db(self._matrices[3, 0, 3]))

        # check the values of the pair (0,2)
        self.assertEqual(parameter[(0,2)][0], complex2db(self._matrices[0, 0, 2]))
        self.assertEqual(parameter[(0,2)][1], complex2db(self._matrices[1, 0, 2]))
        self.assertEqual(parameter[(0,2)][2], complex2db(self._matrices[2, 0, 2]))
        self.assertEqual(parameter[(0,2)][3], complex2db(self._matrices[3, 0, 2]))

        # check the values of the pair (1,3)
        self.assertEqual(parameter[(1,3)][0], complex2db(self._matrices[0, 1, 3]))
        self.assertEqual(parameter[(1,3)][1], complex2db(self._matrices[1, 1, 3]))
        self.assertEqual(parameter[(1,3)][2], complex2db(self._matrices[2, 1, 3]))
        self.assertEqual(parameter[(1,3)][3], complex2db(self._matrices[3, 1, 3]))

    def testComputeComplexParameter(self):
        parameter = self._parameter.getComplexParameter()

        # for a 4 ports, there are 8 FEXT pairs (including reverse)
        self.assertEqual(len(parameter), 8)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,3)]), len(self._freq))
        self.assertEqual(len(parameter[(3,0)]), len(self._freq))
        self.assertEqual(len(parameter[(1,2)]), len(self._freq))
        self.assertEqual(len(parameter[(2,1)]), len(self._freq))

        # check the values of the pair (2,1)
        self.assertEqual(parameter[(2,1)][0], self._matrices[0, 2, 1])
        self.assertEqual(parameter[(2,1)][1], self._matrices[1, 2, 1])
        self.assertEqual(parameter[(2,1)][2], self._matrices[2, 2, 1])
        self.assertEqual(parameter[(2,1)][3], self._matrices[3, 2, 1])

        # check the values of the pair (1,2)
        self.assertEqual(parameter[(1,2)][0], self._matrices[0, 1, 2])
        self.assertEqual(parameter[(1,2)][1], self._matrices[1, 1, 2])
        self.assertEqual(parameter[(1,2)][2], self._matrices[2, 1, 2])
        self.assertEqual(parameter[(1,2)][3], self._matrices[3, 1, 2])

        # check the values of the pair (3,0)
        self.assertEqual(parameter[(3,0)][0], self._matrices[0, 3, 0])
        self.assertEqual(parameter[(3,0)][1], self._matrices[1, 3, 0])
        self.assertEqual(parameter[(3,0)][2], self._matrices[2, 3, 0])
        self.assertEqual(parameter[(3,0)][3], self._matrices[3, 3, 0])

        # check the values of the pair (0,3)
        self.assertEqual(parameter[(0,3)][0], self._matrices[0, 0, 3])
        self.assertEqual(parameter[(0,3)][1], self._matrices[1, 0, 3])
        self.assertEqual(parameter[(0,3)][2], self._matrices[2, 0, 3])
        self.assertEqual(parameter[(0,3)][3], self._matrices[3, 0, 3])

        # check the values of the pair (0,2)
        self.assertEqual(parameter[(0,2)][0], self._matrices[0, 0, 2])
        self.assertEqual(parameter[(0,2)][1], self._matrices[1, 0, 2])
        self.assertEqual(parameter[(0,2)][2], self._matrices[2, 0, 2])
        self.assertEqual(parameter[(0,2)][3], self._matrices[3, 0, 2])

        # check the values of the pair (1,3)
        self.assertEqual(parameter[(1,3)][0], self._matrices[0, 1, 3])
        self.assertEqual(parameter[(1,3)][1], self._matrices[1, 1, 3])
        self.assertEqual(parameter[(1,3)][2], self._matrices[2, 1, 3])
        self.assertEqual(parameter[(1,3)][3], self._matrices[3, 1, 3])
if __name__ == '__main__':
    unittest.main()
