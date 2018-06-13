import unittest
from parameters.test_parameter import TestParameter
from parameters.psfext import PsFext
from parameters.insertionloss import InsertionLoss
from parameters.psacrf import PsAcrf

class TestPsAcrf(TestParameter):
    def testComputeParameter(self):
        psacrf = PsAcrf(self._ports, self._freq, self._matrices)
        parameter = psacrf.getParameter()
        #assume that psfext and il are tested
        psfext = PsFext(self._ports, self._freq, self._matrices).getParameter()
        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True).getParameter()
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], psfext[0][0]-il[0][0])
        self.assertAlmostEqual(parameter[0][1], psfext[0][1]-il[0][1])
        self.assertAlmostEqual(parameter[0][2], psfext[0][2]-il[0][2])
        self.assertAlmostEqual(parameter[0][3], psfext[0][3]-il[0][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], psfext[1][0]-il[1][0])
        self.assertAlmostEqual(parameter[1][1], psfext[1][1]-il[1][1])
        self.assertAlmostEqual(parameter[1][2], psfext[1][2]-il[1][2])
        self.assertAlmostEqual(parameter[1][3], psfext[1][3]-il[1][3])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], psfext[2][0]-il[2][0])
        self.assertAlmostEqual(parameter[2][1], psfext[2][1]-il[2][1])
        self.assertAlmostEqual(parameter[2][2], psfext[2][2]-il[2][2])
        self.assertAlmostEqual(parameter[2][3], psfext[2][3]-il[2][3])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], psfext[3][0]-il[3][0])
        self.assertAlmostEqual(parameter[3][1], psfext[3][1]-il[3][1])
        self.assertAlmostEqual(parameter[3][2], psfext[3][2]-il[3][2])
        self.assertAlmostEqual(parameter[3][3], psfext[3][3]-il[3][3])

if __name__ == '__main__':
    unittest.main()
