import unittest
import numpy as np

from snpanalyzer.parameters.parameter import Parameter, complex2db, complex2phase
from snpanalyzer.sample.port import WirePort, Wire, CableConfiguration, NetworkPort, PlugConfiguration
from snpanalyzer.sample.port import EthernetPair

class TestParameter(unittest.TestCase):
    def assertComplexAlmostEqual(self, dbParam, cpExpected):
        (d1,d2) = dbParam
        (e1,e2) = (complex2db(cpExpected), complex2phase(cpExpected))
        self.assertAlmostEqual(d1, e1)
        self.assertAlmostEqual(d2, e2)

    def setUp(self):
        # create the data
        self.setUpData()

        # create the network configuration
        self.setUpConfiguration()

        # create the parameter
        self._parameter = self.createParameter()
        if self._parameter is None:
            return

        # get the series
        self._series = self._parameter.getDataSeries()

    def setUpData(self):
        # define the frequencies
        self._freq = [100, 200, 300, 400]

        # define the S parameter matrices
        self._matrices = np.array([
            [
                [  1,  2,    3,   4,   5,   6,   7,   8],
                [  9,  10,  11,  12,  13,  14,  15,  16],
                [ 17,  18,  19,  20,  21,  22,  23,  24],
                [ 25,  26,  27,  28,  29,  30,  31,  32],
                [ 33,  34,  35,  36,  37,  38,  39,  40],
                [ 41,  42,  43,  44,  45,  46,  47,  48],
                [ 49,  50,  51,  52,  53,  54,  55,  56],
                [ 57,  58,  59,  60,  61,  62,  63,  64],
            ],[
                [ 65,  66,  67,  68,  69,  70,  71,  72],
                [ 73,  74,  75,  76,  77,  78,  79,  80],
                [ 81,  82,  83,  84,  85,  86,  87,  88],
                [ 89,  90,  91,  92,  93,  94,  95,  96],
                [ 97,  98,  99, 100, 101, 102, 103, 104],
                [105, 106, 107, 108, 109, 110, 111, 112],
                [113, 114, 115, 116, 117, 118, 119, 120],
                [121, 122, 123, 124, 125, 126, 127, 128],
            ],[
                [129, 130, 131, 132, 133, 134, 135, 136],
                [137, 138, 139, 140, 141, 142, 143, 144],
                [145, 146, 147, 148, 149, 150, 151, 152],
                [153, 154, 155, 156, 157, 158, 159, 160],
                [161, 162, 163, 164, 165, 166, 167, 168],
                [169, 170, 171, 172, 173, 174, 175, 176],
                [177, 178, 179, 180, 181, 182, 183, 184],
                [185, 186, 187, 188, 189, 190, 191, 192],
            ],[
                [193, 194, 195, 196, 197, 198, 199, 200],
                [201, 202, 203, 204, 205, 206, 207, 208],
                [209, 210, 211, 212, 213, 214, 215, 216],
                [217, 218, 219, 220, 221, 222, 223, 224],
                [225, 226, 227, 228, 229, 230, 231, 232],
                [233, 234, 235, 236, 237, 238, 239, 240],
                [241, 242, 243, 244, 245, 246, 247, 248],
                [249, 250, 251, 252, 253, 254, 255, 256],
            ]
        ], np.int32)

    def setUpConfiguration(self):
       # create the ports
        self._ports = {
            0: WirePort(0, remote=False),
            1: WirePort(1, remote=False),
            2: WirePort(2, remote=True),
            3: WirePort(3, remote=True),
        }

        # create the wires
        self._wires = {
            0: Wire(self._ports[0], self._ports[2], wtype=EthernetPair.PAIR12),
            1: Wire(self._ports[1], self._ports[3], wtype=EthernetPair.PAIR36),
        }

        # create the cable configuration
        self._config = CableConfiguration(set(self._wires.values()))
        
        # get the reversed wires
        for wire in self._config.getReversedWires():
            if wire.getMainPort().getIndex() == 2 and wire.getRemotePort().getIndex() == 0:
                self._wires[2] = wire
            if wire.getMainPort().getIndex() == 3 and wire.getRemotePort().getIndex() == 1:
                self._wires[3] = wire

    def createParameter(self):
        if type(self) == TestParameter:
            return

        raise NotImplementedError

    def testName(self):
        if type(self) == TestParameter:
            return
        self.assertEqual(isinstance(self._parameter.getName(), str), True)

class TestPlugParameter(TestParameter):
    def setUpConfiguration(self):
       # create the ports
        self._ports = {
            0: NetworkPort(0, ptype=EthernetPair.PAIR12),
            1: NetworkPort(1, ptype=EthernetPair.PAIR36),
            2: NetworkPort(2, ptype=EthernetPair.PAIR45),
            3: NetworkPort(3, ptype=EthernetPair.PAIR78),
        }

        # create the cable configuration
        self._config = PlugConfiguration(set(self._ports.values()))

    def createParameter(self):
        if type(self) == TestPlugParameter:
            return

        raise NotImplementedError

    def testName(self):
        if type(self) == TestPlugParameter:
            return
        self.assertEqual(isinstance(self._parameter.getName(), str), True)

if __name__ == '__main__':
    unittest.main()
