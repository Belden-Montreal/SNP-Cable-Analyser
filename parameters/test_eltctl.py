import unittest

from parameters.test_parameter import TestParameter
from parameters.eltctl import ELTCTL
from parameters.tctl import TCTL
from parameters.insertionloss import InsertionLoss

class TestELTCTL(TestParameter):
    def createParameter(self):
        # we assume FEXT and IL are tested
        tctl = TCTL(self._ports, self._freq, self._matrices)
        il = InsertionLoss(self._ports, self._freq, self._matrices)

        return ELTCTL(self._ports, self._freq, self._matrices, il, tctl)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        dbTCTL = self._parameter.getTCTL().getParameter()
        dbIL = self._parameter.getIL().getParameter()

        tctlPorts = list(dbTCTL.keys())
       
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(tctlPorts))
        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[tctlPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[tctlPorts[1]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[tctlPorts[0]][0], dbTCTL[tctlPorts[0]][0]-dbIL[tctlPorts[0]][0])
        self.assertAlmostEqual(parameter[tctlPorts[0]][1], dbTCTL[tctlPorts[0]][1]-dbIL[tctlPorts[0]][1])
        self.assertAlmostEqual(parameter[tctlPorts[0]][2], dbTCTL[tctlPorts[0]][2]-dbIL[tctlPorts[0]][2])
        self.assertAlmostEqual(parameter[tctlPorts[0]][3], dbTCTL[tctlPorts[0]][3]-dbIL[tctlPorts[0]][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[tctlPorts[1]][0], dbTCTL[tctlPorts[1]][0]-dbIL[tctlPorts[1]][0])
        self.assertAlmostEqual(parameter[tctlPorts[1]][1], dbTCTL[tctlPorts[1]][1]-dbIL[tctlPorts[1]][1])
        self.assertAlmostEqual(parameter[tctlPorts[1]][2], dbTCTL[tctlPorts[1]][2]-dbIL[tctlPorts[1]][2])
        self.assertAlmostEqual(parameter[tctlPorts[1]][3], dbTCTL[tctlPorts[1]][3]-dbIL[tctlPorts[1]][3])


if __name__ == '__main__':
    unittest.main()
