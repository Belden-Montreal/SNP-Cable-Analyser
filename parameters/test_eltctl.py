import unittest

from parameters.test_parameter import TestParameter
from parameters.eltctl import ELTCTL
from parameters.tctl import TCTL
from parameters.insertionloss import InsertionLoss
from parameters.dataserie import PortPairDataSerie

class TestELTCTL(TestParameter):
    def createParameter(self):
        # we assume TCTL and IL are tested
        tctl = TCTL(self._config, self._freq, self._matrices, reverse=False)
        il   = InsertionLoss(self._config, self._freq, self._matrices, reverse=False)

        self._dataseries = {
            0: PortPairDataSerie.fromWire(self._wires[0]),
            1: PortPairDataSerie.fromWire(self._wires[1]),
        }

        return ELTCTL(self._config, self._freq, self._matrices, il, tctl)

    def testComputeDataSeries(self):
        self.assertEqual(self._series, set(self._dataseries.values()))

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        dbTCTL = self._parameter.getTCTL().getParameter()
        dbIL = self._parameter.getIL().getParameter()

        tctlPorts = list(dbTCTL.keys())
       
        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[tctlPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[tctlPorts[1]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[tctlPorts[0]][0][0], dbTCTL[tctlPorts[0]][0][0]-dbIL[tctlPorts[0]][0][0])
        self.assertAlmostEqual(parameter[tctlPorts[0]][1][0], dbTCTL[tctlPorts[0]][1][0]-dbIL[tctlPorts[0]][1][0])
        self.assertAlmostEqual(parameter[tctlPorts[0]][2][0], dbTCTL[tctlPorts[0]][2][0]-dbIL[tctlPorts[0]][2][0])
        self.assertAlmostEqual(parameter[tctlPorts[0]][3][0], dbTCTL[tctlPorts[0]][3][0]-dbIL[tctlPorts[0]][3][0])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[tctlPorts[1]][0][0], dbTCTL[tctlPorts[1]][0][0]-dbIL[tctlPorts[1]][0][0])
        self.assertAlmostEqual(parameter[tctlPorts[1]][1][0], dbTCTL[tctlPorts[1]][1][0]-dbIL[tctlPorts[1]][1][0])
        self.assertAlmostEqual(parameter[tctlPorts[1]][2][0], dbTCTL[tctlPorts[1]][2][0]-dbIL[tctlPorts[1]][2][0])
        self.assertAlmostEqual(parameter[tctlPorts[1]][3][0], dbTCTL[tctlPorts[1]][3][0]-dbIL[tctlPorts[1]][3][0])


if __name__ == '__main__':
    unittest.main()
