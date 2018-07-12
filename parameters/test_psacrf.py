import unittest
from parameters.test_parameter import TestParameter
from parameters.psfext import PSFEXT
from parameters.insertionloss import InsertionLoss
from parameters.fext import FEXT
from parameters.psacrf import PSACRF
from parameters.dataserie import PortDataSerie, PortPairDataSerie

class TestPSACRF(TestParameter):
    def setUp(self):
        super(TestPSACRF, self).setUp()

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        self._ilseries = {
            0: PortPairDataSerie.fromWire(self._wires[0]),
            1: PortPairDataSerie.fromWire(self._wires[1]),
            2: PortPairDataSerie.fromWire(self._wires[2]),
            3: PortPairDataSerie.fromWire(self._wires[3]),
        }

    def createParameter(self):
        # we assume that dependent parameters are tested
        fext   = FEXT(self._config, self._freq, self._matrices)
        psfext = PSFEXT(self._config, self._freq, self._matrices, fext)
        il     = InsertionLoss(self._config, self._freq, self._matrices)

        return PSACRF(self._config, self._freq, self._matrices, psfext, il)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(self._dataseries[0] in self._series, True)
        self.assertEqual(self._dataseries[1] in self._series, True)
        self.assertEqual(self._dataseries[2] in self._series, True)
        self.assertEqual(self._dataseries[3] in self._series, True)
        for serie in self._series:
            ilSerie = serie.getData()
            if serie == self._dataseries[0]:
                self.assertEqual(ilSerie, self._ilseries[0])
            if serie == self._dataseries[1]:
                self.assertEqual(ilSerie, self._ilseries[1])
            if serie == self._dataseries[2]:
                self.assertEqual(ilSerie, self._ilseries[2])
            if serie == self._dataseries[3]:
                self.assertEqual(ilSerie, self._ilseries[3])

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()

        # get the dependent parameters
        dbPSFEXT = self._parameter.getPSFEXT().getParameter()
        dbIL     = self._parameter.getIL().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[3]]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[0]][0][0],
		dbPSFEXT[self._dataseries[0]][0][0]-dbIL[self._ilseries[0]][0][0])
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][0],
		dbPSFEXT[self._dataseries[0]][1][0]-dbIL[self._ilseries[0]][1][0])
        self.assertAlmostEqual(parameter[self._dataseries[0]][2][0],
		dbPSFEXT[self._dataseries[0]][2][0]-dbIL[self._ilseries[0]][2][0])
        self.assertAlmostEqual(parameter[self._dataseries[0]][3][0],
		dbPSFEXT[self._dataseries[0]][3][0]-dbIL[self._ilseries[0]][3][0])

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[1]][0][0],
		dbPSFEXT[self._dataseries[1]][0][0]-dbIL[self._ilseries[1]][0][0])
        self.assertAlmostEqual(parameter[self._dataseries[1]][1][0],
		dbPSFEXT[self._dataseries[1]][1][0]-dbIL[self._ilseries[1]][1][0])
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0],
		dbPSFEXT[self._dataseries[1]][2][0]-dbIL[self._ilseries[1]][2][0])
        self.assertAlmostEqual(parameter[self._dataseries[1]][3][0],
		dbPSFEXT[self._dataseries[1]][3][0]-dbIL[self._ilseries[1]][3][0])

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[2]][0][0],
		dbPSFEXT[self._dataseries[2]][0][0]-dbIL[self._ilseries[2]][0][0])
        self.assertAlmostEqual(parameter[self._dataseries[2]][1][0],
		dbPSFEXT[self._dataseries[2]][1][0]-dbIL[self._ilseries[2]][1][0])
        self.assertAlmostEqual(parameter[self._dataseries[2]][2][0],
		dbPSFEXT[self._dataseries[2]][2][0]-dbIL[self._ilseries[2]][2][0])
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0],
		dbPSFEXT[self._dataseries[2]][3][0]-dbIL[self._ilseries[2]][3][0])

        # check the values of the port 4
        self.assertAlmostEqual(parameter[self._dataseries[3]][0][0],
		dbPSFEXT[self._dataseries[3]][0][0]-dbIL[self._ilseries[3]][0][0])
        self.assertAlmostEqual(parameter[self._dataseries[3]][1][0],
		dbPSFEXT[self._dataseries[3]][1][0]-dbIL[self._ilseries[3]][1][0])
        self.assertAlmostEqual(parameter[self._dataseries[3]][2][0],
		dbPSFEXT[self._dataseries[3]][2][0]-dbIL[self._ilseries[3]][2][0])
        self.assertAlmostEqual(parameter[self._dataseries[3]][3][0],
		dbPSFEXT[self._dataseries[3]][3][0]-dbIL[self._ilseries[3]][3][0])

if __name__ == '__main__':
    unittest.main()
