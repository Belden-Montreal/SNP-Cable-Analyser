import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.next import NEXT
from parameters.psnext import PSNEXT
from parameters.dataserie import PortDataSerie, PortPairDataSerie
from sample.port import NetworkPort, PlugConfiguration
import numpy as np

def powerSum(values):
    return 10*np.log10(np.sum(list(map(lambda v: 10**(v[0]/10), values))))

class TestPSNEXT(TestParameter):
    def setUp(self):
        super(TestPSNEXT, self).setUp()

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        self._nextseries = {
            0: PortPairDataSerie(self._ports[0], self._ports[1]),
            1: PortPairDataSerie(self._ports[1], self._ports[0]),
            2: PortPairDataSerie(self._ports[2], self._ports[3]),
            3: PortPairDataSerie(self._ports[3], self._ports[2]),
        }

    def createParameter(self):
        nnext = NEXT(self._config, self._freq, self._matrices)
        return PSNEXT(self._config, self._freq, self._matrices, nnext)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(self._dataseries[0] in self._series, True)
        self.assertEqual(self._dataseries[1] in self._series, True)
        self.assertEqual(self._dataseries[2] in self._series, True)
        self.assertEqual(self._dataseries[3] in self._series, True)
        for serie in self._series:
            nextSeries = serie.getData()
            self.assertEqual(len(nextSeries), 1)
            if serie == self._dataseries[0]:
                self.assertEqual(self._nextseries[0] in nextSeries, True)
            if serie == self._dataseries[1]:
                self.assertEqual(self._nextseries[1] in nextSeries, True)
            if serie == self._dataseries[2]:
                self.assertEqual(self._nextseries[2] in nextSeries, True)
            if serie == self._dataseries[3]:
                self.assertEqual(self._nextseries[3] in nextSeries, True)

    def testComputeParameter(self):
        parameter = self._parameter.getParameter()
        nnext = self._parameter.getNEXT().getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._dataseries[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._dataseries[3]]), len(self._freq))

        # check the values of the port 0
        self.assertAlmostEqual(parameter[self._dataseries[0]][0][0], powerSum([nnext[self._nextseries[0]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][0], powerSum([nnext[self._nextseries[0]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][2][0], powerSum([nnext[self._nextseries[0]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][3][0], powerSum([nnext[self._nextseries[0]][3]]))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[1]][0][0], powerSum([nnext[self._nextseries[1]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][1][0], powerSum([nnext[self._nextseries[1]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0], powerSum([nnext[self._nextseries[1]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][3][0], powerSum([nnext[self._nextseries[1]][3]]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]][0][0], powerSum([nnext[self._nextseries[2]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][1][0], powerSum([nnext[self._nextseries[2]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][2][0], powerSum([nnext[self._nextseries[2]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0], powerSum([nnext[self._nextseries[2]][3]]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]][0][0], powerSum([nnext[self._nextseries[3]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][1][0], powerSum([nnext[self._nextseries[3]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][2][0], powerSum([nnext[self._nextseries[3]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][3][0], powerSum([nnext[self._nextseries[3]][3]]))

class TestPlugPSNEXT(TestParameter):
    def setUp(self):
        super(TestPlugPSNEXT, self).setUp()

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        self._nextseries = {
             0: PortPairDataSerie(self._ports[0], self._ports[1]),
             1: PortPairDataSerie(self._ports[0], self._ports[2]),
             2: PortPairDataSerie(self._ports[0], self._ports[3]),
             3: PortPairDataSerie(self._ports[1], self._ports[0]),
             4: PortPairDataSerie(self._ports[1], self._ports[2]),
             5: PortPairDataSerie(self._ports[1], self._ports[3]),
             6: PortPairDataSerie(self._ports[2], self._ports[0]),
             7: PortPairDataSerie(self._ports[2], self._ports[1]),
             8: PortPairDataSerie(self._ports[2], self._ports[3]),
             9: PortPairDataSerie(self._ports[3], self._ports[0]),
            10: PortPairDataSerie(self._ports[3], self._ports[1]),
            11: PortPairDataSerie(self._ports[3], self._ports[2]),
        }

        self._nextgroup = {
            0: [self._nextseries[i] for i in [ 0, 1, 2]],
            1: [self._nextseries[i] for i in [ 3, 4, 5]],
            2: [self._nextseries[i] for i in [ 6, 7, 8]],
            3: [self._nextseries[i] for i in [ 9,10,11]],
        }

    def setUpConfiguration(self):
        # create the ports
        self._ports = {
            0: NetworkPort(0 ,"Port 0"),
            1: NetworkPort(1 ,"Port 1"),
            2: NetworkPort(2 ,"Port 2"),
            3: NetworkPort(3 ,"Port 3"),
        }

        # create the plug configuration
        self._config = PlugConfiguration(set(self._ports.values()))

        # crate the parameter
        self._parameter = self.createParameter()

    def createParameter(self):
        nnext = NEXT(self._config, self._freq, self._matrices)
        return PSNEXT(self._config, self._freq, self._matrices, nnext)

    def testComputeDataSeries(self):
        self.assertEqual(len(self._series), 4)
        self.assertEqual(self._dataseries[0] in self._series, True)
        self.assertEqual(self._dataseries[1] in self._series, True)
        self.assertEqual(self._dataseries[2] in self._series, True)
        self.assertEqual(self._dataseries[3] in self._series, True)
        for serie in self._series:
            nextSeries = serie.getData()
            self.assertEqual(len(nextSeries), 3)
            if serie == self._dataseries[0]:
                self.assertEqual(self._nextseries[ 0] in nextSeries, True)
                self.assertEqual(self._nextseries[ 1] in nextSeries, True)
                self.assertEqual(self._nextseries[ 2] in nextSeries, True)
            if serie == self._dataseries[1]:
                self.assertEqual(self._nextseries[ 3] in nextSeries, True)
                self.assertEqual(self._nextseries[ 4] in nextSeries, True)
                self.assertEqual(self._nextseries[ 5] in nextSeries, True)
            if serie == self._dataseries[2]:
                self.assertEqual(self._nextseries[ 6] in nextSeries, True)
                self.assertEqual(self._nextseries[ 7] in nextSeries, True)
                self.assertEqual(self._nextseries[ 8] in nextSeries, True)
            if serie == self._dataseries[3]:
                self.assertEqual(self._nextseries[ 9] in nextSeries, True)
                self.assertEqual(self._nextseries[10] in nextSeries, True)
                self.assertEqual(self._nextseries[11] in nextSeries, True)

    def testComputedParameter(self):
        parameter = self._parameter.getParameter()
        nnext = self._parameter.getNEXT().getParameter()

        # check the values of the port 0
        self.assertAlmostEqual(parameter[self._dataseries[0]][0][0], powerSum([nnext[s][0] for s in self._nextgroup[0]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][1][0], powerSum([nnext[s][1] for s in self._nextgroup[0]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][2][0], powerSum([nnext[s][2] for s in self._nextgroup[0]]))
        self.assertAlmostEqual(parameter[self._dataseries[0]][3][0], powerSum([nnext[s][3] for s in self._nextgroup[0]]))

        # check values of the port 1
        self.assertAlmostEqual(parameter[self._dataseries[1]][0][0], powerSum([nnext[s][0] for s in self._nextgroup[1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][1][0], powerSum([nnext[s][1] for s in self._nextgroup[1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0], powerSum([nnext[s][2] for s in self._nextgroup[1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][3][0], powerSum([nnext[s][3] for s in self._nextgroup[1]]))

        # check values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]][0][0], powerSum([nnext[s][0] for s in self._nextgroup[2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][1][0], powerSum([nnext[s][1] for s in self._nextgroup[2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][2][0], powerSum([nnext[s][2] for s in self._nextgroup[2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0], powerSum([nnext[s][3] for s in self._nextgroup[2]]))

        #check values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]][0][0], powerSum([nnext[s][0] for s in self._nextgroup[3]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][1][0], powerSum([nnext[s][1] for s in self._nextgroup[3]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][2][0], powerSum([nnext[s][2] for s in self._nextgroup[3]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][3][0], powerSum([nnext[s][3] for s in self._nextgroup[3]]))

if __name__ == '__main__':
    unittest.main()
