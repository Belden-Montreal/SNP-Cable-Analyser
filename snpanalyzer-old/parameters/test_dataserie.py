from unittest import TestCase

from snpanalyzer.sample.port import NetworkPort, WirePort, EthernetPair, Wire, ReversedWire
from snpanalyzer.parameters.dataserie import PortDataSerie, WireDataSerie
from snpanalyzer.parameters.dataserie import PortPairDataSerie, PortOrderedPairDataSerie

class TestPortDataSerie(TestCase):
    def testEqualSameType(self):
        serie1 = PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR12))
        serie2 = PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR12))
        self.assertEqual(serie1, serie2)

    def testEqualDifferentTypes(self):
        serie1 = PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR12))
        serie2 = PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR36))
        self.assertNotEqual(serie1, serie2)

    def testEqualDifferentRemotes(self):
        serie1 = PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR12, remote=False))
        serie2 = PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR36, remote=True))
        self.assertNotEqual(serie1, serie2)

    def testHash(self):
        series = set()

        series.add(PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR12)))
        series.add(PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR36)))
        self.assertEqual(len(series), 2)
        self.assertEqual(PortDataSerie(NetworkPort(2, ptype=EthernetPair.PAIR12)) in series, True)
        self.assertEqual(PortDataSerie(NetworkPort(3, ptype=EthernetPair.PAIR36)) in series, True)

        series.add(PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR36)))
        self.assertEqual(len(series), 2)
        self.assertEqual(PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR12)) in series, True)
        self.assertEqual(PortDataSerie(NetworkPort(5, ptype=EthernetPair.PAIR36)) in series, True)

        series.add(PortDataSerie(NetworkPort(0, ptype=EthernetPair.PAIR45)))
        self.assertEqual(len(series), 3)
        self.assertEqual(PortDataSerie(NetworkPort(2, ptype=EthernetPair.PAIR12)) in series, True)
        self.assertEqual(PortDataSerie(NetworkPort(9, ptype=EthernetPair.PAIR36)) in series, True)
        self.assertEqual(PortDataSerie(NetworkPort(1, ptype=EthernetPair.PAIR45)) in series, True)

class TestPortPairDataSerie(TestCase):
    def testEqualSameType(self):
        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36)
        port3 = NetworkPort(3, ptype=EthernetPair.PAIR12)
        port4 = NetworkPort(4, ptype=EthernetPair.PAIR36)

        serie1 = PortPairDataSerie(port1, port2)
        serie2 = PortPairDataSerie(port3, port4)
        self.assertEqual(serie1, serie2)

    def testEqualDifferentTypes(self):
        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36)
        port3 = NetworkPort(3, ptype=EthernetPair.PAIR45)
        port4 = NetworkPort(4, ptype=EthernetPair.PAIR36)

        serie1 = PortPairDataSerie(port1, port2)
        serie2 = PortPairDataSerie(port3, port4)
        self.assertNotEqual(serie1, serie2)

    def testEqualDifferentRemotes(self):
        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12, remote=True)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36, remote=True)
        port3 = NetworkPort(3, ptype=EthernetPair.PAIR45, remote=False)
        port4 = NetworkPort(4, ptype=EthernetPair.PAIR36, remote=False)

        serie1 = PortPairDataSerie(port1, port2)
        serie2 = PortPairDataSerie(port3, port4)
        self.assertNotEqual(serie1, serie2)

    def testEqualFlipped(self):
        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36)

        serie1 = PortPairDataSerie(port1, port2)
        serie2 = PortPairDataSerie(port2, port1)
        self.assertNotEqual(serie1, serie2)

    def testHash(self):
        series = set()

        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36)
        port3 = NetworkPort(3, ptype=EthernetPair.PAIR45)
        port4 = NetworkPort(4, ptype=EthernetPair.PAIR36)
        series.add(PortPairDataSerie(port1, port2))
        series.add(PortPairDataSerie(port3, port4))
        self.assertEqual(len(series), 2)
        self.assertEqual(PortPairDataSerie(port1, port2) in series, True)
        self.assertEqual(PortPairDataSerie(port3, port4) in series, True)
 
        port5 = NetworkPort(5, ptype=EthernetPair.PAIR45)
        port6 = NetworkPort(6, ptype=EthernetPair.PAIR36)
        series.add(PortPairDataSerie(port5, port6))
        self.assertEqual(len(series), 2)
        self.assertEqual(PortPairDataSerie(port1, port2) in series, True)
        self.assertEqual(PortPairDataSerie(port3, port4) in series, True)

        port7 = NetworkPort(7, ptype=EthernetPair.PAIR45)
        port8 = NetworkPort(8, ptype=EthernetPair.PAIR78)
        series.add(PortPairDataSerie(port7, port8))
        self.assertEqual(len(series), 3)
        self.assertEqual(PortPairDataSerie(port1, port2) in series, True)
        self.assertEqual(PortPairDataSerie(port3, port4) in series, True)
        self.assertEqual(PortPairDataSerie(port7, port8) in series, True)

class TestOrderedPortPairDataSerie(TestCase):
    def testEqualFlipped(self):
        port1 = NetworkPort(1, ptype=EthernetPair.PAIR12)
        port2 = NetworkPort(2, ptype=EthernetPair.PAIR36)

        serie1 = PortOrderedPairDataSerie(port1, port2)
        serie2 = PortOrderedPairDataSerie(port2, port1)
        self.assertEqual(serie1, serie2)

class TestWireDataSerie(TestCase):
    def testEqualSameType(self):
        wire1 = Wire(WirePort(0, remote=False), WirePort(1, remote=True), wtype=EthernetPair.PAIR12)
        wire2 = Wire(WirePort(2, remote=False), WirePort(3, remote=True), wtype=EthernetPair.PAIR12)

        serie1 = WireDataSerie(wire1)
        serie2 = WireDataSerie(wire2)
        self.assertEqual(serie1, serie2)

    def testEqualDifferentTypes(self):
        wire1 = Wire(WirePort(0, remote=False), WirePort(1, remote=True), wtype=EthernetPair.PAIR12)
        wire2 = Wire(WirePort(2, remote=False), WirePort(3, remote=True), wtype=EthernetPair.PAIR36)

        serie1 = WireDataSerie(wire1)
        serie2 = WireDataSerie(wire2)
        self.assertNotEqual(serie1, serie2)

    def testEqualDifferentDirection(self):
        wire1 = Wire(WirePort(0, remote=False), WirePort(1, remote=True), wtype=EthernetPair.PAIR12)
        wire2 = ReversedWire(wire1)

        serie1 = WireDataSerie(wire1)
        serie2 = WireDataSerie(wire2)
        self.assertNotEqual(serie1, serie2)

    def testHash(self):
        series = set()

        wire1 = Wire(WirePort( 1, remote=False), WirePort( 2, remote=True), wtype=EthernetPair.PAIR12)
        wire2 = Wire(WirePort( 3, remote=False), WirePort( 4, remote=True), wtype=EthernetPair.PAIR12)
        wire3 = Wire(WirePort( 5, remote=False), WirePort( 6, remote=True), wtype=EthernetPair.PAIR36)
        wire4 = Wire(WirePort( 7, remote=False), WirePort( 8, remote=True), wtype=EthernetPair.PAIR36)
        wire5 = Wire(WirePort( 9, remote=False), WirePort(10, remote=True), wtype=EthernetPair.PAIR36)
        wire6 = Wire(WirePort(11, remote=False), WirePort(12, remote=True), wtype=EthernetPair.PAIR78)
        wire7 = Wire(WirePort(11, remote=False), WirePort(12, remote=True), wtype=EthernetPair.PAIR78)
        wire8 = ReversedWire(wire7)
        wire9 = ReversedWire(wire7)

        series.add(WireDataSerie(wire1))
        series.add(WireDataSerie(wire3))
        self.assertEqual(len(series), 2)
        self.assertEqual(WireDataSerie(wire2) in series, True)
        self.assertEqual(WireDataSerie(wire4) in series, True)

        series.add(WireDataSerie(wire5))
        self.assertEqual(len(series), 2)
        self.assertEqual(WireDataSerie(wire2) in series, True)
        self.assertEqual(WireDataSerie(wire4) in series, True)

        series.add(WireDataSerie(wire6))
        self.assertEqual(len(series), 3)
        self.assertEqual(WireDataSerie(wire2) in series, True)
        self.assertEqual(WireDataSerie(wire4) in series, True)
        self.assertEqual(WireDataSerie(wire7) in series, True)

        series.add(WireDataSerie(wire8))
        series.add(WireDataSerie(wire9))
        self.assertEqual(len(series), 4)
        self.assertEqual(WireDataSerie(wire2) in series, True)
        self.assertEqual(WireDataSerie(wire4) in series, True)
        self.assertEqual(WireDataSerie(wire7) in series, True)
        self.assertEqual(WireDataSerie(wire8) in series, True)


