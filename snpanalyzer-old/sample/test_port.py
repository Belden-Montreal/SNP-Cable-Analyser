import unittest
from snpanalyzer.sample.port import EthernetPair, NetworkPort, WirePort, Wire, ReversedWire
from snpanalyzer.sample.port import PlugConfiguration, CableConfiguration

class TestNetworkPort(unittest.TestCase):
    def setUp(self):
        self._index = 2
        self._type  = EthernetPair.PAIR12
        self._port  = NetworkPort(self._index, self._type)

    def testGetIndex(self):
        self.assertEqual(self._port.getIndex(), self._index)

    def testGetName(self):
        self.assertEqual(self._port.getName(), self._type.getName())

    def testGetType(self):
        self.assertEqual(self._port.getType(), self._type)

    def testSetType(self):
        self._port.setType(EthernetPair.PAIR36)
        self.assertEqual(self._port.getType(), EthernetPair.PAIR36)
        self.assertEqual(self._port.getName(), EthernetPair.PAIR36.getName())

class TestWirePort(TestNetworkPort):
    def setUp(self):
        super(TestWirePort, self).setUp()
        self._remote = True
        self._port   = WirePort(self._index, self._type, self._remote)

    def testGetName(self):
        self.assertEqual(self._port.getName(), "{} (r)".format(self._type.getName()))

    def testIsRemote(self):
        self.assertEqual(self._port.isRemote(), self._remote)

    def testSetRemote(self):
        self._port.setRemote(False)
        self.assertEqual(self._port.isRemote(), False)
        self.assertEqual(self._port.getName(), "{}".format(self._type.getName()))
        self._port.setRemote(True)
        self.assertEqual(self._port.isRemote(), True)
        self.assertEqual(self._port.getName(), "{} (r)".format(self._type.getName()))

class TestWire(unittest.TestCase):
    def setUp(self):
        self._main   = WirePort(0, remote=False)
        self._remote = WirePort(1, remote=True)
        self._type   = EthernetPair.PAIR36
        self._wire   = Wire(self._main, self._remote, wtype=self._type)

    def testConstructorSetType(self):
        self.assertEqual(self._main.getType(),   self._type)
        self.assertEqual(self._remote.getType(), self._type)

    def testConstructorMainIsRemote(self):
        self._main = WirePort(0, remote=True)
        with self.assertRaises(ValueError):
            Wire(self._main, self._remote)

    def testConstructorRemoteNotRemote(self):
        self._remote = WirePort(1, remote=False)
        with self.assertRaises(ValueError):
            Wire(self._main, self._remote)

    def testGetName(self):
        self.assertEqual(self._wire.getName(), self._type.getName())

    def testGetMainPort(self):
        self.assertEqual(self._wire.getMainPort(), self._main)

    def testGetRemotePort(self):
        self.assertEqual(self._wire.getRemotePort(), self._remote)

    def testGetType(self):
        self.assertEqual(self._wire.getType(), self._type)

    def testGetReverse(self):
        self.assertEqual(self._wire.getReverse(), None)

    def testSetReverse(self):
        self._wire.setReverse(self)
        self.assertEqual(self._wire.getReverse(), self)

    def testContains(self):
        self.assertEqual(self._main   in self._wire, True)
        self.assertEqual(self._remote in self._wire, True)
        self.assertEqual(WirePort(0, remote=False) in self._wire, False)
        self.assertEqual(WirePort(1, remote=True)  in self._wire, False)

    def testIsReverse(self):
        self.assertEqual(self._wire.isReverse(), False)

class TestReversedWire(TestWire):
    def setUp(self):
        super(TestReversedWire, self).setUp()
        self._foward = self._wire
        self._wire = ReversedWire(self._wire)

    def testGetName(self):
        self.assertEqual(self._wire.getName(), "{} (r)".format(self._type.getName()))

    def testGetMainPort(self):
        self.assertEqual(self._wire.getMainPort(), self._remote)

    def testGetRemotePort(self):
        self.assertEqual(self._wire.getRemotePort(), self._main)

    def testGetReverse(self):
        self.assertEqual(self._wire.getReverse(), self._foward)

    def testIsReverse(self):
        self.assertEqual(self._wire.isReverse(), True)

class TestPlugConfiguration(unittest.TestCase):
    def setUp(self):
        self._ports = {
            0: NetworkPort(0, ptype=EthernetPair.PAIR12),
            1: NetworkPort(1, ptype=EthernetPair.PAIR36),
            2: NetworkPort(2, ptype=EthernetPair.PAIR45),
            3: NetworkPort(3, ptype=EthernetPair.PAIR78),
        }

        self._config = PlugConfiguration(set(self._ports.values()))

    def testConstructorNoDuplicateIndices(self):
        PlugConfiguration(set(self._ports.values()))

    def testConstructorDuplicateIndices(self):
        self._ports[5] = NetworkPort(0)
        with self.assertRaises(ValueError):
            PlugConfiguration(set(self._ports.values()))

    def testConstructorDuplicateTypes(self):
        self._ports[5] = NetworkPort(4, ptype=EthernetPair.PAIR12)
        with self.assertRaises(ValueError):
            PlugConfiguration(set(self._ports.values()))

    def testAddPortNoDuplicateIndices(self):
        port = NetworkPort(4)
        self._config.addPort(port)
        self.assertEqual(port in self._config.getPorts(), True)

    def testAddPortNewType(self):
        port = NetworkPort(4, ptype=EthernetPair.DUMMY)
        self._config.addPort(port)
        self.assertEqual(self._config.getByType(EthernetPair.DUMMY, False), port)

    def testAddPortDuplicateTypes(self):
        port = NetworkPort(4, ptype=EthernetPair.PAIR12)
        with self.assertRaises(ValueError):
            self._config.addPort(port)
        self.assertEqual(port.getIndex() not in self._config._indices, True)
        self.assertEqual(self._config.getByType(EthernetPair.PAIR12, False), self._ports[0])

    def testAddPortDuplicateIndices(self):
        port = NetworkPort(0)
        with self.assertRaises(ValueError):
            self._config.addPort(port)
        self.assertEqual(port.getIndex() not in self._config._indices, True)

    def testGetPorts(self):
        ports = self._config.getPorts()
        self.assertEqual(len(ports), 4)
        for port in self._ports.values():
            self.assertEqual(port in ports, True)

    def testGetMainPorts(self):
        ports = self._config.getMainPorts()
        self.assertEqual(len(ports), 4)
        for port in self._ports.values():
            self.assertEqual(port in ports, True)

    def testGetRemotePorts(self):
         ports = self._config.getRemotePorts()
         self.assertEqual(len(ports), 0)

    def testGetByType(self):
        self.assertEqual(self._config.getByType(EthernetPair.DUMMY,  False), None)
        self.assertEqual(self._config.getByType(EthernetPair.PAIR12, False), self._ports[0])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR36, False), self._ports[1])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR45, False), self._ports[2])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR78, False), self._ports[3])

    def testIterator(self):
        for port in self._config:
            self.assertEqual(port in self._ports.values(), True)

    def testLen(self):
        self.assertEqual(len(self._config), 4)

class TestCableConfiguration(unittest.TestCase):
    def setUp(self):
        self._ports = {
            0: WirePort(0, remote=False), 4: WirePort(4, remote=True),
            1: WirePort(1, remote=False), 5: WirePort(5, remote=True),
            2: WirePort(2, remote=False), 6: WirePort(6, remote=True),
            3: WirePort(3, remote=False), 7: WirePort(7, remote=True),
        }

        self._wires = {
            0: Wire(self._ports[0], self._ports[4], wtype=EthernetPair.PAIR12),
            1: Wire(self._ports[1], self._ports[5], wtype=EthernetPair.PAIR36),
            2: Wire(self._ports[2], self._ports[6], wtype=EthernetPair.PAIR45),
            3: Wire(self._ports[3], self._ports[7], wtype=EthernetPair.PAIR78),
        }

        self._config = CableConfiguration(set(self._wires.values()))

    def addWire(self):
        self._ports[8] = WirePort(8, remote=False)
        self._ports[9] = WirePort(9, remote=True)
        self._wires[5] = Wire(self._ports[8], self._ports[9])
        self._config.addWire(self._wires[5])

    def testConstructorDuplicatePortIndices(self):
        wire = Wire(WirePort(0, remote=False), WirePort(9, remote=True))
        self._wires[4] = wire
        with self.assertRaises(ValueError):
            self._config = CableConfiguration(set(self._wires.values()))

    def testContructorPortAreFiltered(self):
        self.assertEqual(len(self._config.getMainPorts()),   4)
        self.assertEqual(len(self._config.getRemotePorts()), 4)
        for wire in self._wires.values():
            self.assertEqual(wire.getMainPort()   in self._config.getPorts(),       True)
            self.assertEqual(wire.getRemotePort() in self._config.getPorts(),       True)
            self.assertEqual(wire.getMainPort()   in self._config.getMainPorts(),   True)
            self.assertEqual(wire.getRemotePort() in self._config.getRemotePorts(), True)
            self.assertEqual(wire.getMainPort()   in self._config.getRemotePorts(), False)
            self.assertEqual(wire.getRemotePort() in self._config.getMainPorts(),   False)

    def testAddWireDuplicateType(self):
        main   = WirePort(8, remote=False)
        remote = WirePort(9, remote=True)
        wire   = Wire(main, remote, wtype=EthernetPair.PAIR12)
        with self.assertRaises(ValueError):
            self._config.addWire(wire)
        self.assertEqual(main.getIndex()   not in self._config._indices, True)
        self.assertEqual(remote.getIndex() not in self._config._indices, True)
        self.assertEqual(main   not in self._config._ports, True)
        self.assertEqual(remote not in self._config._ports, True)
        self.assertEqual(main   not in self._config._mains, True)
        self.assertEqual(remote not in self._config._mains, True)
        self.assertEqual(main   not in self._config._remotes, True)
        self.assertEqual(remote not in self._config._remotes, True)
        self.assertEqual(wire not in self._config._wires,    True)
        self.assertEqual(wire not in self._config._reversed, True)
        self.assertEqual(wire not in self._config._reversed, True)

    def testAddWireDuplicateIndexMain(self):
        main   = WirePort(0, remote=False)
        remote = WirePort(8, remote=True)
        wire   = Wire(main, remote)
        with self.assertRaises(ValueError):
            self._config.addWire(wire)
        self.assertEqual(main.getIndex()   not in self._config._indices, True)
        self.assertEqual(remote.getIndex() not in self._config._indices, True)
        self.assertEqual(main   not in self._config._ports, True)
        self.assertEqual(remote not in self._config._ports, True)
        self.assertEqual(main   not in self._config._mains, True)
        self.assertEqual(remote not in self._config._mains, True)
        self.assertEqual(main   not in self._config._remotes, True)
        self.assertEqual(remote not in self._config._remotes, True)
        self.assertEqual(wire not in self._config._wires,    True)
        self.assertEqual(wire not in self._config._reversed, True)
        self.assertEqual(wire not in self._config._reversed, True)

    def testAddWireDuplicateIndexRemote(self):
        main   = WirePort(8, remote=False)
        remote = WirePort(7, remote=True)
        wire   = Wire(main, remote)
        with self.assertRaises(ValueError):
            self._config.addWire(wire)
        self.assertEqual(main.getIndex()   not in self._config._indices, True)
        self.assertEqual(remote.getIndex() not in self._config._indices, True)
        self.assertEqual(main   not in self._config._ports, True)
        self.assertEqual(remote not in self._config._ports, True)
        self.assertEqual(main   not in self._config._mains, True)
        self.assertEqual(remote not in self._config._mains, True)
        self.assertEqual(main   not in self._config._remotes, True)
        self.assertEqual(remote not in self._config._remotes, True)
        self.assertEqual(wire not in self._config._wires,    True)
        self.assertEqual(wire not in self._config._reversed, True)
        self.assertEqual(wire not in self._config._reversed, True)

    def testGetWires(self, size=8):
        wires = self._config.getWires()
        self.assertEqual(len(wires), size)
        for wire in self._wires.values():
            self.assertEqual(wire in wires, True)

    def testGetWiresAfterAddWire(self, size=8):
        self.addWire()
        self.testGetWires(size=10)

    def testGetFowardWires(self, size=4):
        wires = self._config.getFowardWires()
        self.assertEqual(len(wires), size)
        for wire in self._wires.values():
            self.assertEqual(wire in wires, True)

    def testGetFowardWiresAfterAddWire(self):
        self.addWire()
        self.testGetFowardWires(size=5)

    def testGetReversedWires(self, size=4):
        foward = dict()
        for wire in self._wires.values():
            i = wire.getMainPort().getIndex()
            j = wire.getRemotePort().getIndex()
            foward[(i,j)] = wire

        wires = self._config.getReversedWires()
        self.assertEqual(len(wires), size)
        for wire in wires:
            main = wire.getMainPort()
            remote = wire.getRemotePort()

            i = main.getIndex()
            j = remote.getIndex()

            self.assertEqual("{} (r)".format(foward[(j,i)].getName()), wire.getName())
            self.assertEqual(foward[(j,i)].getType(), wire.getType())
            self.assertEqual(foward[(j,i)].getMainPort()   is remote, True)
            self.assertEqual(foward[(j,i)].getRemotePort() is main,   True)
            
    def testGetReversedWiresAfterAddWire(self):
        self.addWire()
        self.testGetReversedWires(size=5)

    def testGetPorts(self, size=8):
        ports = self._config.getPorts()
        self.assertEqual(len(ports), size)
        for wire in self._wires.values():
            self.assertEqual(wire.getMainPort()   in ports, True)
            self.assertEqual(wire.getRemotePort() in ports, True)

    def testGetPortsAfterAddWire(self):
        self.addWire()
        self.testGetPorts(size=10)

    def testGetMainPorts(self, size=4):
        ports = self._config.getMainPorts()
        self.assertEqual(len(ports), size)
        for wire in self._wires.values():
            self.assertEqual(wire.getMainPort()   in ports, True)
            self.assertEqual(wire.getRemotePort() in ports, False)

    def testGetMainPortsAfterAddWire(self):
        self.addWire()
        self.testGetMainPorts(size=5)

    def testGetRemotePorts(self, size=4):
        ports = self._config.getRemotePorts()
        self.assertEqual(len(ports), size)
        for wire in self._wires.values():
            self.assertEqual(wire.getMainPort()   in ports, False)
            self.assertEqual(wire.getRemotePort() in ports, True)

    def testGetByType(self):
        self.assertEqual(self._config.getByType(EthernetPair.DUMMY), None)
        self.assertEqual(self._config.getByType(EthernetPair.PAIR12), self._wires[0])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR36), self._wires[1])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR45), self._wires[2])
        self.assertEqual(self._config.getByType(EthernetPair.PAIR78), self._wires[3])

    def testGetRemotePortsAfterAddWire(self):
        self.addWire()
        self.testGetRemotePorts(size=5)

    def testIterator(self):
        for port in self._config:
            self.assertEqual(port in self._ports.values(), True)

    def testLen(self):
        self.assertEqual(len(self._config), 8)

if __name__ == '__main__':
    unittest.main()
