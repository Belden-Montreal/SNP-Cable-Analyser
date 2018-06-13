import unittest

from parameters.test_parameter import TestParameter
from parameters.eltctl import ELTCTL
from parameters.tctl import TCTL
from parameters.insertionloss import InsertionLoss

class TestELTCTL(TestParameter):
    def testComputeParameter(self):
        tctl = TCTL(self._ports, self._freq, self._matrices)
        il = InsertionLoss(self._ports, self._freq, self._matrices)

        eltctl = ELTCTL(self._ports, self._freq, self._matrices, il, tctl)
        parameter = eltctl.getParameter()
        #assume fext and il are tested
        
        dbTctl = tctl.getParameter()
        dbIl = il.getParameter()

        tctlPorts = list(dbTctl.keys())
       
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(tctlPorts))
        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[tctlPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[tctlPorts[1]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[tctlPorts[0]][0], dbTctl[tctlPorts[0]][0]-dbIl[tctlPorts[0]][0])
        self.assertAlmostEqual(parameter[tctlPorts[0]][1], dbTctl[tctlPorts[0]][1]-dbIl[tctlPorts[0]][1])
        self.assertAlmostEqual(parameter[tctlPorts[0]][2], dbTctl[tctlPorts[0]][2]-dbIl[tctlPorts[0]][2])
        self.assertAlmostEqual(parameter[tctlPorts[0]][3], dbTctl[tctlPorts[0]][3]-dbIl[tctlPorts[0]][3])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[tctlPorts[1]][0], dbTctl[tctlPorts[1]][0]-dbIl[tctlPorts[1]][0])
        self.assertAlmostEqual(parameter[tctlPorts[1]][1], dbTctl[tctlPorts[1]][1]-dbIl[tctlPorts[1]][1])
        self.assertAlmostEqual(parameter[tctlPorts[1]][2], dbTctl[tctlPorts[1]][2]-dbIl[tctlPorts[1]][2])
        self.assertAlmostEqual(parameter[tctlPorts[1]][3], dbTctl[tctlPorts[1]][3]-dbIl[tctlPorts[1]][3])


if __name__ == '__main__':
    unittest.main()
