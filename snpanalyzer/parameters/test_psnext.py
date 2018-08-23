import unittest

from snpanalyzer.parameters.parameter import complex2db
from snpanalyzer.parameters.test_parameter import TestParameter, TestPlugParameter
from snpanalyzer.parameters.next import NEXT
from snpanalyzer.parameters.psnext import PSNEXT
from snpanalyzer.parameters.dataserie import PortDataSerie, PortOrderedPairDataSerie
from snpanalyzer.sample.port import NetworkPort, PlugConfiguration
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
            0: PortOrderedPairDataSerie(self._ports[0], self._ports[1]),
            1: PortOrderedPairDataSerie(self._ports[2], self._ports[3]),
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
                self.assertEqual(self._nextseries[0] in nextSeries, True)
            if serie == self._dataseries[2]:
                self.assertEqual(self._nextseries[1] in nextSeries, True)
            if serie == self._dataseries[3]:
                self.assertEqual(self._nextseries[1] in nextSeries, True)

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
        self.assertAlmostEqual(parameter[self._dataseries[1]][0][0], powerSum([nnext[self._nextseries[0]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][1][0], powerSum([nnext[self._nextseries[0]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][2][0], powerSum([nnext[self._nextseries[0]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[1]][3][0], powerSum([nnext[self._nextseries[0]][3]]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[self._dataseries[2]][0][0], powerSum([nnext[self._nextseries[1]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][1][0], powerSum([nnext[self._nextseries[1]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][2][0], powerSum([nnext[self._nextseries[1]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[2]][3][0], powerSum([nnext[self._nextseries[1]][3]]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[self._dataseries[3]][0][0], powerSum([nnext[self._nextseries[1]][0]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][1][0], powerSum([nnext[self._nextseries[1]][1]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][2][0], powerSum([nnext[self._nextseries[1]][2]]))
        self.assertAlmostEqual(parameter[self._dataseries[3]][3][0], powerSum([nnext[self._nextseries[1]][3]]))

class TestPlugPSNEXT(TestPlugParameter):
    def setUp(self):
        super(TestPlugPSNEXT, self).setUp()

        self._dataseries = {
            0: PortDataSerie(self._ports[0]),
            1: PortDataSerie(self._ports[1]),
            2: PortDataSerie(self._ports[2]),
            3: PortDataSerie(self._ports[3]),
        }

        self._nextseries = {
             0: PortOrderedPairDataSerie(self._ports[0], self._ports[1]),
             1: PortOrderedPairDataSerie(self._ports[0], self._ports[2]),
             2: PortOrderedPairDataSerie(self._ports[0], self._ports[3]),
             3: PortOrderedPairDataSerie(self._ports[1], self._ports[2]),
             4: PortOrderedPairDataSerie(self._ports[1], self._ports[3]),
             5: PortOrderedPairDataSerie(self._ports[2], self._ports[3]),
        }

        self._nextgroup = {
            0: [self._nextseries[i] for i in [ 0, 1, 2]],
            1: [self._nextseries[i] for i in [ 0, 3, 4]],
            2: [self._nextseries[i] for i in [ 1, 3, 5]],
            3: [self._nextseries[i] for i in [ 2, 4, 5]],
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
            self.assertEqual(len(nextSeries), 3)
            if serie == self._dataseries[0]:
                self.assertEqual(self._nextseries[0] in nextSeries, True)
                self.assertEqual(self._nextseries[1] in nextSeries, True)
                self.assertEqual(self._nextseries[2] in nextSeries, True)
            if serie == self._dataseries[1]:
                self.assertEqual(self._nextseries[0] in nextSeries, True)
                self.assertEqual(self._nextseries[3] in nextSeries, True)
                self.assertEqual(self._nextseries[4] in nextSeries, True)
            if serie == self._dataseries[2]:
                self.assertEqual(self._nextseries[1] in nextSeries, True)
                self.assertEqual(self._nextseries[3] in nextSeries, True)
                self.assertEqual(self._nextseries[5] in nextSeries, True)
            if serie == self._dataseries[3]:
                self.assertEqual(self._nextseries[2] in nextSeries, True)
                self.assertEqual(self._nextseries[4] in nextSeries, True)
                self.assertEqual(self._nextseries[5] in nextSeries, True)

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
