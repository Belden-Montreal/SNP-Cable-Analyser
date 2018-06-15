import unittest
from parameters.test_parameter import TestParameter
from parameters.insertionloss import InsertionLoss
from parameters.psaxext import PSAXEXT
from parameters.psaacrx import PSAACRX
from parameters.axext import AXEXT
from parameters.fext import FEXT

class TestPSAACRX(TestParameter):
    def createParameter(self):
        # we assume that psfext and il are tested
        il = InsertionLoss(self._ports, self._freq, self._matrices)
        fext = FEXT(self._ports, self._freq, self._matrices)
        axextd = [AXEXT(self._ports, self._freq, self._matrices, fext, il) for i in range(4)]
        psaxext = PSAXEXT(self._ports, self._freq, self._matrices, axextd)

        return PSAACRX(self._ports, self._freq, self._matrices, psaxext, il)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        
        dbPSAXEXT = self._parameter.getPSAXEXT().getParameter()
        dbIL = self._parameter.getIL().getParameter(full=True)

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], dbPSAXEXT[0][0]-dbIL[0][0])
        self.assertAlmostEqual(parameter[0][1], dbPSAXEXT[0][1]-dbIL[0][1])
        self.assertAlmostEqual(parameter[0][2], dbPSAXEXT[0][2]-dbIL[0][2])
        self.assertAlmostEqual(parameter[0][3], dbPSAXEXT[0][3]-dbIL[0][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], dbPSAXEXT[1][0]-dbIL[1][0])
        self.assertAlmostEqual(parameter[1][1], dbPSAXEXT[1][1]-dbIL[1][1])
        self.assertAlmostEqual(parameter[1][2], dbPSAXEXT[1][2]-dbIL[1][2])
        self.assertAlmostEqual(parameter[1][3], dbPSAXEXT[1][3]-dbIL[1][3])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], dbPSAXEXT[2][0]-dbIL[2][0])
        self.assertAlmostEqual(parameter[2][1], dbPSAXEXT[2][1]-dbIL[2][1])
        self.assertAlmostEqual(parameter[2][2], dbPSAXEXT[2][2]-dbIL[2][2])
        self.assertAlmostEqual(parameter[2][3], dbPSAXEXT[2][3]-dbIL[2][3])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], dbPSAXEXT[3][0]-dbIL[3][0])
        self.assertAlmostEqual(parameter[3][1], dbPSAXEXT[3][1]-dbIL[3][1])
        self.assertAlmostEqual(parameter[3][2], dbPSAXEXT[3][2]-dbIL[3][2])
        self.assertAlmostEqual(parameter[3][3], dbPSAXEXT[3][3]-dbIL[3][3])

if __name__ == '__main__':
    unittest.main()
