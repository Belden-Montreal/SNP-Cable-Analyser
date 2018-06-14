import unittest

from parameters.test_parameter import TestParameter
from parameters.acrf import ACRF
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss

class TestAcrf(TestParameter):
    def testComputeParameter(self):
        fext = FEXT(self._ports, self._freq, self._matrices)
        il = InsertionLoss(self._ports, self._freq, self._matrices)

        acrf = ACRF(self._ports, self._freq, self._matrices, fext, il)
        parameter = acrf.getParameter()
        #assume fext and il are tested
        
        dbFext = fext.getParameter()
        dbIl = il.getParameter(full=True)

        fextPorts = list(dbFext.keys())
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(fextPorts))
        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[fextPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[1]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[2]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[3]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[fextPorts[0]][0], dbFext[fextPorts[0]][0]-dbIl[fextPorts[0][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[0]][1], dbFext[fextPorts[0]][1]-dbIl[fextPorts[0][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[0]][2], dbFext[fextPorts[0]][2]-dbIl[fextPorts[0][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[0]][3], dbFext[fextPorts[0]][3]-dbIl[fextPorts[0][0]][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[fextPorts[1]][0], dbFext[fextPorts[1]][0]-dbIl[fextPorts[1][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[1]][1], dbFext[fextPorts[1]][1]-dbIl[fextPorts[1][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[1]][2], dbFext[fextPorts[1]][2]-dbIl[fextPorts[1][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[1]][3], dbFext[fextPorts[1]][3]-dbIl[fextPorts[1][0]][3])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[fextPorts[2]][0], dbFext[fextPorts[2]][0]-dbIl[fextPorts[2][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[2]][1], dbFext[fextPorts[2]][1]-dbIl[fextPorts[2][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[2]][2], dbFext[fextPorts[2]][2]-dbIl[fextPorts[2][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[2]][3], dbFext[fextPorts[2]][3]-dbIl[fextPorts[2][0]][3])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[fextPorts[3]][0], dbFext[fextPorts[3]][0]-dbIl[fextPorts[3][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[3]][1], dbFext[fextPorts[3]][1]-dbIl[fextPorts[3][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[3]][2], dbFext[fextPorts[3]][2]-dbIl[fextPorts[3][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[3]][3], dbFext[fextPorts[3]][3]-dbIl[fextPorts[3][0]][3])

if __name__ == '__main__':
    unittest.main()
