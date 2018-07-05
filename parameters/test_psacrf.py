import unittest
from parameters.test_parameter import TestParameter
from parameters.psfext import PSFEXT
from parameters.insertionloss import InsertionLoss
from parameters.fext import FEXT
from parameters.psacrf import PSACRF

class TestPsAcrf(TestParameter):
    def createParameter(self):
        # we assume that psfext and il are tested
        fext = FEXT(self._e2ePorts, self._freq, self._matrices)
        psfext = PSFEXT(self._e2ePorts, self._freq, self._matrices, fext)
        il = InsertionLoss(self._e2ePorts, self._freq, self._matrices)

        return PSACRF(self._e2ePorts, self._freq, self._matrices, psfext, il)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        
        dbPSFEXT = self._parameter.getPSFEXT().getParameter()
        dbIL = self._parameter.getIL().getParameter(full=True)

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0][0], dbPSFEXT[0][0][0]-dbIL[(0,2)][0][0])
        self.assertAlmostEqual(parameter[0][1][0], dbPSFEXT[0][1][0]-dbIL[(0,2)][1][0])
        self.assertAlmostEqual(parameter[0][2][0], dbPSFEXT[0][2][0]-dbIL[(0,2)][2][0])
        self.assertAlmostEqual(parameter[0][3][0], dbPSFEXT[0][3][0]-dbIL[(0,2)][3][0])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0][0], dbPSFEXT[1][0][0]-dbIL[(1,3)][0][0])
        self.assertAlmostEqual(parameter[1][1][0], dbPSFEXT[1][1][0]-dbIL[(1,3)][1][0])
        self.assertAlmostEqual(parameter[1][2][0], dbPSFEXT[1][2][0]-dbIL[(1,3)][2][0])
        self.assertAlmostEqual(parameter[1][3][0], dbPSFEXT[1][3][0]-dbIL[(1,3)][3][0])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0][0], dbPSFEXT[2][0][0]-dbIL[(2,0)][0][0])
        self.assertAlmostEqual(parameter[2][1][0], dbPSFEXT[2][1][0]-dbIL[(2,0)][1][0])
        self.assertAlmostEqual(parameter[2][2][0], dbPSFEXT[2][2][0]-dbIL[(2,0)][2][0])
        self.assertAlmostEqual(parameter[2][3][0], dbPSFEXT[2][3][0]-dbIL[(2,0)][3][0])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0][0], dbPSFEXT[3][0][0]-dbIL[(3,1)][0][0])
        self.assertAlmostEqual(parameter[3][1][0], dbPSFEXT[3][1][0]-dbIL[(3,1)][1][0])
        self.assertAlmostEqual(parameter[3][2][0], dbPSFEXT[3][2][0]-dbIL[(3,1)][2][0])
        self.assertAlmostEqual(parameter[3][3][0], dbPSFEXT[3][3][0]-dbIL[(3,1)][3][0])

if __name__ == '__main__':
    unittest.main()
