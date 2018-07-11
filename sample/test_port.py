import unittest
from sample.port import NetworkPort, WirePort, Wire, ReversedWire, PlugConfiguration, CableConfiguration

class TestNetworkPort(unittest.TestCase):
    def setUp(self):
        self._index = 2
        self._name  = "Port Name"
        self._port  = NetworkPort(self._index, self._name)

    def testGetIndex(self):
        self.assertEqual(self._port.getIndex(), self._index)

    def testGetName(self):
        self.assertEqual(self._port.getName(), self._name)

class TestWirePort(TestNetworkPort):
    def setUp(self):
        self._index  = 2
        self._name   = "Port Name"
        self._remote = True
        self._port   = WirePort(self._index, self._name, self._remote)

    def testIsRemote(self):
        self.assertEqual(self._port.isRemote(), self._remote)

    def testSetRemote(self):
        self._port.setRemote(False)
        self.assertEqual(self._port.isRemote(), False)
        self._port.setRemote(True)
        self.assertEqual(self._port.isRemote(), True)

class TestWire(unittest.TestCase):
    def setUp(self):
        self._name   = "Wire"
        self._main   = WirePort(0, "Port 0", False)
        self._remote = WirePort(1, "Port 1", True)
        self._wire   = Wire(self._name, self._main, self._remote)

    def testConstructorMainIsRemote(self):
        self._main = WirePort(0, "Port 0", True)
        with self.assertRaises(ValueError):
            Wire(self._name, self._main, self._remote)

    def testConstructorRemoteNotRemote(self):
        self._remote = WirePort(1, "Port 1", False)
        with self.assertRaises(ValueError):
            Wire(self._name, self._main, self._remote)

    def testGetName(self):
        self.assertEqual(self._wire.getName(), self._name)

    def testGetMainPort(self):
        self.assertEqual(self._wire.getMainPort(), self._main)

    def testGetRemotePort(self):
        self.assertEqual(self._wire.getRemotePort(), self._remote)

    def testContains(self):
        self.assertEqual(self._main   in self._wire, True)
        self.assertEqual(self._remote in self._wire, True)
        self.assertEqual(WirePort(0, "Port 0", False) in self._wire, False)
        self.assertEqual(WirePort(1, "Port 1", True)  in self._wire, False)

class TestReversedWire(TestWire):
    def setUp(self):
        super(TestReversedWire, self).setUp()
        self._wire = ReversedWire(self._wire)

    def testGetMainPort(self):
        self.assertEqual(self._wire.getMainPort(), self._remote)

    def testGetRemotePort(self):
        self.assertEqual(self._wire.getRemotePort(), self._main)

class TestPlugConfiguration(unittest.TestCase):
    def setUp(self):
        self._ports = {
            0: NetworkPort(0, "Port 0"),
            1: NetworkPort(1, "Port 1"),
            2: NetworkPort(2, "Port 2"),
            3: NetworkPort(3, "Port 3"),
        }

        self._config = PlugConfiguration(set(self._ports.values()))

    def testConstructorNoDuplicateIndices(self):
        PlugConfiguration(set(self._ports.values()))

    def testConstructorDuplicateIndices(self):
        self._ports[5] = NetworkPort(0, "Port 1")
        with self.assertRaises(ValueError):
            PlugConfiguration(set(self._ports.values()))

    def testAddPortNoDuplicateIndices(self):
        config = PlugConfiguration(set(self._ports.values()))
        port = NetworkPort(4, "Port 4")
        config.addPort(port)
        self.assertEqual(port in config.getPorts(), True)

    def testAddPortDuplicateIndices(self):
        config = PlugConfiguration(set(self._ports.values()))
        port = NetworkPort(0, "Port 0")
        with self.assertRaises(ValueError):
            config.addPort(port)

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

    def testIterator(self):
        for port in self._config:
            self.assertEqual(port in self._ports.values(), True)

    def testLen(self):
        self.assertEqual(len(self._config), 4)

class TestCableConfiguration(unittest.TestCase):
    def setUp(self):
        self._ports = {
            0: WirePort(0, "Port 0", False), 4: WirePort(4, "Port 4", True),
            1: WirePort(1, "Port 1", False), 5: WirePort(5, "Port 5", True),
            2: WirePort(2, "Port 2", False), 6: WirePort(6, "Port 6", True),
            3: WirePort(3, "Port 3", False), 7: WirePort(7, "Port 7", True),
        }

        self._wires = {
            0: Wire("Wire 0", self._ports[0], self._ports[4]),
            1: Wire("Wire 1", self._ports[1], self._ports[5]),
            2: Wire("Wire 2", self._ports[2], self._ports[6]),
            3: Wire("Wire 3", self._ports[3], self._ports[7]),
        }

        self._config = CableConfiguration(set(self._wires.values()))

    def addWire(self):
        self._ports[8] = WirePort("Port 8", 8, False)
        self._ports[9] = WirePort("Port 9", 9, True)
        self._wires[5] = Wire("Wire 5", self._ports[8], self._ports[9])
        self._config.addWire(self._wires[5])

    def testConstructorMainIsRemote(self):
        wire = Wire("Wire 4", WirePort(8, "Port 8", False), WirePort(9, "Port 9", True))
        wire.getMainPort().setRemote(True)
        self._wires[4] = wire
        with self.assertRaises(ValueError):
            self._config = CableConfiguration(set(self._wires.values()))

    def testConstructorRemoteNotRemote(self):
        wire = Wire("Wire 4", WirePort(8, "Port 8", False), WirePort(9, "Port 9", True))
        wire.getRemotePort().setRemote(False)
        self._wires[4] = wire
        with self.assertRaises(ValueError):
            self._config = CableConfiguration(set(self._wires.values()))

    def testConstructorDuplicatePortIndices(self):
        wire = Wire("Wire 4", WirePort(0, "Port 0", False), WirePort(9, "Port 9", True))
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

    def testAddWireDuplicateIndexMain(self):
        main   = WirePort(0, "Port 0", False)
        remote = WirePort(8, "Port 8", True)
        wire   = Wire("Wire 4", main, remote)
        with self.assertRaises(ValueError):
            self._config.addWire(wire)

    def testAddWireDuplicateIndexRemote(self):
        main   = WirePort(8, "Port 8", False)
        remote = WirePort(7, "Port 7", True)
        wire   = Wire("Wire 4", main, remote)
        with self.assertRaises(ValueError):
            self._config.addWire(wire)

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

            self.assertEqual(foward[(j,i)].getName() is wire.getName(), True)
            self.assertEqual(foward[(j,i)].getMainPort() is remote, True)
            self.assertEqual(foward[(j,i)].getRemotePort() is main, True)
            
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
