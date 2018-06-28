import unittest
from sample.port import Port, PortConfiguration

class TestPort(unittest.TestCase):
    def setUp(self):
        self._name  = "Port Name"
        self._port  = Port(self._name)

    def testGetName(self):
        self.assertEqual(self._port.getName(), self._name)

class TestPortConfiguration(unittest.TestCase):
    def setUp(self):
        self._main = {
            0: Port("Port 1"),
            1: Port("Port 2"),
            2: Port("Port 3"),
            3: Port("Port 4"),
        }
        self._remote = {
            4: Port("Port 1"),
            5: Port("Port 2"),
            6: Port("Port 3"),
            7: Port("Port 4"),
        }

    def testPortNoIntersection(self):
        PortConfiguration(self._main, self._remote)

    def testPortIntersection(self):
        self._remote[0] = "Port 1"
        with self.assertRaises(ValueError):
            PortConfiguration(self._main, self._remote)

    def testIterator(self):
        ports = PortConfiguration(self._main, self._remote)
        total = dict(self._main)
        total.update(self._remote)
        for (index,port) in ports:
            self.assertEqual(index in total.keys(), True)
            self.assertEqual(port in total.values(), True)
            total.pop(index)
        self.assertEqual(len(total), 0)



if __name__ == '__main__':
    unittest.main()
