import unittest
from parameters.test_parameter import TestParameter
from parameters.psfext import PsFext
from parameters.insertionloss import InsertionLoss
from parameters.fext import Fext
from parameters.psacrf import PsAcrf

class TestPsAcrf(TestParameter):
    def testComputeParameter(self):
        fext = Fext(self._ports, self._freq, self._matrices)
        psfext = PsFext(self._ports, self._freq, self._matrices, fext)
        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True)

        psacrf = PsAcrf(self._ports, self._freq, self._matrices, psfext, il)
        parameter = psacrf.getParameter()
        #assume that psfext and il are tested
        
        dbPsfext = psfext.getParameter()
        dbIl = il.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], dbPsfext[0][0]-dbIl[0][0])
        self.assertAlmostEqual(parameter[0][1], dbPsfext[0][1]-dbIl[0][1])
        self.assertAlmostEqual(parameter[0][2], dbPsfext[0][2]-dbIl[0][2])
        self.assertAlmostEqual(parameter[0][3], dbPsfext[0][3]-dbIl[0][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], dbPsfext[1][0]-dbIl[1][0])
        self.assertAlmostEqual(parameter[1][1], dbPsfext[1][1]-dbIl[1][1])
        self.assertAlmostEqual(parameter[1][2], dbPsfext[1][2]-dbIl[1][2])
        self.assertAlmostEqual(parameter[1][3], dbPsfext[1][3]-dbIl[1][3])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], dbPsfext[2][0]-dbIl[2][0])
        self.assertAlmostEqual(parameter[2][1], dbPsfext[2][1]-dbIl[2][1])
        self.assertAlmostEqual(parameter[2][2], dbPsfext[2][2]-dbIl[2][2])
        self.assertAlmostEqual(parameter[2][3], dbPsfext[2][3]-dbIl[2][3])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], dbPsfext[3][0]-dbIl[3][0])
        self.assertAlmostEqual(parameter[3][1], dbPsfext[3][1]-dbIl[3][1])
        self.assertAlmostEqual(parameter[3][2], dbPsfext[3][2]-dbIl[3][2])
        self.assertAlmostEqual(parameter[3][3], dbPsfext[3][3]-dbIl[3][3])

if __name__ == '__main__':
    unittest.main()
