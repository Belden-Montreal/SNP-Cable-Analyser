import unittest

from parameters.test_parameter import TestParameter
from parameters.fext import Fext

class TestFext(TestParameter):
    def testComputeParameter(self):
        fext = Fext(self._ports, self._freq, self._matrices)
        parameter = fext.getComplexParameter()
        fextPorts = list()
        for i,porti in sorted(self._ports.items())[len(self._ports)//2:]:
            for j,portj in sorted(self._ports.items())[:len(self._ports)//2]:
                if not (i == j) and not (abs(i-j) == len(self._ports)//2):
                    fextPorts.append(porti+"-"+portj)
                    fextPorts.append(portj+"-"+porti)
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(fextPorts))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[fextPorts[0]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[1]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[2]]), len(self._freq))
        self.assertEqual(len(parameter[fextPorts[3]]), len(self._freq))

        # check the values of the port 3-port 2
        self.assertEqual(parameter[fextPorts[0]][0], self._matrices[0, 1, 2])
        self.assertEqual(parameter[fextPorts[0]][1], self._matrices[1, 1, 2])
        self.assertEqual(parameter[fextPorts[0]][2], self._matrices[2, 1, 2])
        self.assertEqual(parameter[fextPorts[0]][3], self._matrices[3, 1, 2])

        # check the values of the port 2-port 3
        self.assertEqual(parameter[fextPorts[1]][0], self._matrices[0, 2, 1])
        self.assertEqual(parameter[fextPorts[1]][1], self._matrices[1, 2, 1])
        self.assertEqual(parameter[fextPorts[1]][2], self._matrices[2, 2, 1])
        self.assertEqual(parameter[fextPorts[1]][3], self._matrices[3, 2, 1])

        # check the values of the port 4-port 1
        self.assertEqual(parameter[fextPorts[2]][0], self._matrices[0, 0, 3])
        self.assertEqual(parameter[fextPorts[2]][1], self._matrices[1, 0, 3])
        self.assertEqual(parameter[fextPorts[2]][2], self._matrices[2, 0, 3])
        self.assertEqual(parameter[fextPorts[2]][3], self._matrices[3, 0, 3])

        # check the values of the port 1-port 4
        self.assertEqual(parameter[fextPorts[3]][0], self._matrices[0, 3, 0])
        self.assertEqual(parameter[fextPorts[3]][1], self._matrices[1, 3, 0])
        self.assertEqual(parameter[fextPorts[3]][2], self._matrices[2, 3, 0])
        self.assertEqual(parameter[fextPorts[3]][3], self._matrices[3, 3, 0])

if __name__ == '__main__':
    unittest.main()
