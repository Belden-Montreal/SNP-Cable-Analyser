import unittest

from parameters.test_parameter import TestParameter
from parameters.acrf import Acrf
from parameters.fext import Fext
from parameters.insertionloss import InsertionLoss

class TestAcrf(TestParameter):
    def testComputeParameter(self):
        acrf = Acrf(self._ports, self._freq, self._matrices)
        parameter = acrf.getParameter()
        #assume fext and il are tested
        fext = Fext(self._ports, self._freq, self._matrices).getParameter()
        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True).getParameter()
        fextPorts = list(fext.keys())
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(fextPorts))
        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[fextPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[1]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[2]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[3]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[fextPorts[0]][0], fext[fextPorts[0]][0]-il[fextPorts[0][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[0]][1], fext[fextPorts[0]][1]-il[fextPorts[0][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[0]][2], fext[fextPorts[0]][2]-il[fextPorts[0][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[0]][3], fext[fextPorts[0]][3]-il[fextPorts[0][0]][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[fextPorts[1]][0], fext[fextPorts[1]][0]-il[fextPorts[1][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[1]][1], fext[fextPorts[1]][1]-il[fextPorts[1][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[1]][2], fext[fextPorts[1]][2]-il[fextPorts[1][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[1]][3], fext[fextPorts[1]][3]-il[fextPorts[1][0]][3])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[fextPorts[2]][0], fext[fextPorts[2]][0]-il[fextPorts[2][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[2]][1], fext[fextPorts[2]][1]-il[fextPorts[2][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[2]][2], fext[fextPorts[2]][2]-il[fextPorts[2][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[2]][3], fext[fextPorts[2]][3]-il[fextPorts[2][0]][3])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[fextPorts[3]][0], fext[fextPorts[3]][0]-il[fextPorts[3][0]][0])
        self.assertAlmostEqual(parameter[fextPorts[3]][1], fext[fextPorts[3]][1]-il[fextPorts[3][0]][1])
        self.assertAlmostEqual(parameter[fextPorts[3]][2], fext[fextPorts[3]][2]-il[fextPorts[3][0]][2])
        self.assertAlmostEqual(parameter[fextPorts[3]][3], fext[fextPorts[3]][3]-il[fextPorts[3][0]][3])

if __name__ == '__main__':
    unittest.main()
