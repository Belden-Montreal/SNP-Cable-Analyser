import unittest

from parameters.test_parameter import TestParameter
from parameters.acrf import ACRF
from parameters.fext import FEXT
from parameters.insertionloss import InsertionLoss
from parameters.dataserie import PortPairDataSerie, WireDataSerie

class TestACRF(TestParameter):
    def setUp(self):
        super(TestACRF, self).setUp()

        self._fextSeries = {
            0: PortPairDataSerie(self._ports[0], self._ports[3]),
            1: PortPairDataSerie(self._ports[3], self._ports[0]),
            2: PortPairDataSerie(self._ports[1], self._ports[2]),
            3: PortPairDataSerie(self._ports[2], self._ports[1]),
        }

        self._ilSeries = {
            0: WireDataSerie(self._wires[0]),
            1: WireDataSerie(self._wires[1]),
            2: WireDataSerie(self._wires[2]),
            3: WireDataSerie(self._wires[3]),
        }

    def createParameter(self):
        # we assume fext and il are tested
        fext = FEXT(self._config, self._freq, self._matrices)
        il   = InsertionLoss(self._config, self._freq, self._matrices)

        return ACRF(self._config, self._freq, self._matrices, fext, il)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(self._fextSeries[0] in self._series, True)
        self.assertEqual(self._fextSeries[1] in self._series, True)
        self.assertEqual(self._fextSeries[2] in self._series, True)
        self.assertEqual(self._fextSeries[3] in self._series, True)
        for serie in self._series:
            if serie == self._fextSeries[0]:
                self.assertEqual(serie.getData() == self._ilSeries[0], True)
            if serie == self._fextSeries[1]:
                self.assertEqual(serie.getData() == self._ilSeries[3], True)
            if serie == self._fextSeries[2]:
                self.assertEqual(serie.getData() == self._ilSeries[1], True)
            if serie == self._fextSeries[3]:
                self.assertEqual(serie.getData() == self._ilSeries[2], True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        
        dbFEXT = self._parameter.getFEXT().getParameter()
        dbIl   = self._parameter.getIL().getParameter()

        series = self._fextSeries
        wires  = self._ilSeries

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[series[0]]), len(self._freq))
        self.assertEqual(len(parameter[series[1]]), len(self._freq))
        self.assertEqual(len(parameter[series[2]]), len(self._freq))
        self.assertEqual(len(parameter[series[3]]), len(self._freq))

        # check the values of the pair (0, 3)
        self.assertAlmostEqual(parameter[series[0]][0][0], dbFEXT[series[0]][0][0]-dbIl[wires[0]][0][0])
        self.assertAlmostEqual(parameter[series[0]][1][0], dbFEXT[series[0]][1][0]-dbIl[wires[0]][1][0])
        self.assertAlmostEqual(parameter[series[0]][2][0], dbFEXT[series[0]][2][0]-dbIl[wires[0]][2][0])
        self.assertAlmostEqual(parameter[series[0]][3][0], dbFEXT[series[0]][3][0]-dbIl[wires[0]][3][0])

        # check the values of the pair (3, 0)
        self.assertAlmostEqual(parameter[series[1]][0][0], dbFEXT[series[1]][0][0]-dbIl[wires[3]][0][0])
        self.assertAlmostEqual(parameter[series[1]][1][0], dbFEXT[series[1]][1][0]-dbIl[wires[3]][1][0])
        self.assertAlmostEqual(parameter[series[1]][2][0], dbFEXT[series[1]][2][0]-dbIl[wires[3]][2][0])
        self.assertAlmostEqual(parameter[series[1]][3][0], dbFEXT[series[1]][3][0]-dbIl[wires[3]][3][0])

        # check the values of the pair (1, 2)
        self.assertAlmostEqual(parameter[series[2]][0][0], dbFEXT[series[2]][0][0]-dbIl[wires[1]][0][0])
        self.assertAlmostEqual(parameter[series[2]][1][0], dbFEXT[series[2]][1][0]-dbIl[wires[1]][1][0])
        self.assertAlmostEqual(parameter[series[2]][2][0], dbFEXT[series[2]][2][0]-dbIl[wires[1]][2][0])
        self.assertAlmostEqual(parameter[series[2]][3][0], dbFEXT[series[2]][3][0]-dbIl[wires[1]][3][0])

        # check the values of the pair (2, 1)
        self.assertAlmostEqual(parameter[series[3]][0][0], dbFEXT[series[3]][0][0]-dbIl[wires[2]][0][0])
        self.assertAlmostEqual(parameter[series[3]][1][0], dbFEXT[series[3]][1][0]-dbIl[wires[2]][1][0])
        self.assertAlmostEqual(parameter[series[3]][2][0], dbFEXT[series[3]][2][0]-dbIl[wires[2]][2][0])
        self.assertAlmostEqual(parameter[series[3]][3][0], dbFEXT[series[3]][3][0]-dbIl[wires[2]][3][0])

if __name__ == '__main__':
    unittest.main()
