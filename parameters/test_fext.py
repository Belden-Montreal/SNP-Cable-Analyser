import unittest

from parameters.test_parameter import TestParameter
from parameters.fext import Fext

class TestFext(TestParameter):
    def testComputeParameter(self):
        fext = Fext(self._ports, self._freq, self._matrices)
        parameter = fext.getComplexParameter()

        # there should be a parameter for each ports
        # for a 4 ports, there are 4 Fext measurements as it is double-ended only
        self.assertEqual(len(parameter), 4)

        # make sure the pair were created
        self.assertEqual((0,3) in parameter, True)
        self.assertEqual((3,0) in parameter, True)
        self.assertEqual((1,2) in parameter, True)
        self.assertEqual((2,1) in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[(0,3)]), len(self._freq))
        self.assertEqual(len(parameter[(3,0)]), len(self._freq))
        self.assertEqual(len(parameter[(1,2)]), len(self._freq))
        self.assertEqual(len(parameter[(2,1)]), len(self._freq))

        # check the values of the port 3-port 2
        self.assertEqual(parameter[(2,1)][0], self._matrices[0, 2, 1])
        self.assertEqual(parameter[(2,1)][1], self._matrices[1, 2, 1])
        self.assertEqual(parameter[(2,1)][2], self._matrices[2, 2, 1])
        self.assertEqual(parameter[(2,1)][3], self._matrices[3, 2, 1])

        # check the values of the port 2-port 3
        self.assertEqual(parameter[(1,2)][0], self._matrices[0, 1, 2])
        self.assertEqual(parameter[(1,2)][1], self._matrices[1, 1, 2])
        self.assertEqual(parameter[(1,2)][2], self._matrices[2, 1, 2])
        self.assertEqual(parameter[(1,2)][3], self._matrices[3, 1, 2])

        # check the values of the port 4-port 1
        self.assertEqual(parameter[(3,0)][0], self._matrices[0, 3, 0])
        self.assertEqual(parameter[(3,0)][1], self._matrices[1, 3, 0])
        self.assertEqual(parameter[(3,0)][2], self._matrices[2, 3, 0])
        self.assertEqual(parameter[(3,0)][3], self._matrices[3, 3, 0])

        # check the values of the port 1-port 4
        self.assertEqual(parameter[(0,3)][0], self._matrices[0, 0, 3])
        self.assertEqual(parameter[(0,3)][1], self._matrices[1, 0, 3])
        self.assertEqual(parameter[(0,3)][2], self._matrices[2, 0, 3])
        self.assertEqual(parameter[(0,3)][3], self._matrices[3, 0, 3])

if __name__ == '__main__':
    unittest.main()
