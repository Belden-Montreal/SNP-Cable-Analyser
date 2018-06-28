import unittest
from sample.port import Port, PortConfiguration

class TestPort(unittest.TestCase):
    def setUp(self):
        self._name  = "Port Name"
        self._port  = Port(self._name)

    def testGetName(self):
        self.assertEqual(self._port.getName(), self._name)

class TestPortConfiguration(unittest.TestCase):
    def testPortNoIntersection(self):
        main = {
            0: Port("Port 1"),
            1: Port("Port 2"),
            2: Port("Port 3"),
            3: Port("Port 4"),
        }
        remote = {
            4: Port("Port 1"),
            5: Port("Port 2"),
            6: Port("Port 3"),
            7: Port("Port 4"),
        }
        PortConfiguration(main, remote)

    def testPortIntersection(self):
        main = {
            0: Port("Port 1"),
            1: Port("Port 2"),
            2: Port("Port 3"),
            3: Port("Port 4"),
        }
        remote = {
            4: Port("Port 1"),
            1: Port("Port 2"),
            6: Port("Port 3"),
            7: Port("Port 4"),
        }
        with self.assertRaises(ValueError):
            PortConfiguration(main, remote)

if __name__ == '__main__':
    unittest.main()
