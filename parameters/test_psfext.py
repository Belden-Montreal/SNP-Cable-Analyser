import unittest
import numpy as np
from parameters.test_parameter import TestParameter
from parameters.psfext import PsFext
from parameters.fext import Fext

def powersum(fext, f, port):
    keys = fext.keys()
    return 10*np.log10(np.sum([10**(fext[key][f]/10) for key in keys if (key.split("-")[0] == port ) ]))

class TestPsFext(TestParameter):
    def testComputeParameter(self):
        psfext = PsFext(self._ports, self._freq, self._matrices)
        parameter = psfext.getParameter()
        #assume that fext is tested
        fext = Fext(self._ports, self._freq, self._matrices).getParameter()
        
        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[self._ports[0]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[1]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[2]]), len(self._freq))
        self.assertEqual(len(parameter[self._ports[3]]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[self._ports[0]][0], powersum(fext, 0, self._ports[0]))
        self.assertEqual(parameter[self._ports[0]][1], powersum(fext, 1, self._ports[0]))
        self.assertEqual(parameter[self._ports[0]][2], powersum(fext, 2, self._ports[0]))
        self.assertEqual(parameter[self._ports[0]][3], powersum(fext, 3, self._ports[0]))

        # check the values of the port 2
        self.assertEqual(parameter[self._ports[1]][0], powersum(fext, 0, self._ports[1]))
        self.assertEqual(parameter[self._ports[1]][1], powersum(fext, 1, self._ports[1]))
        self.assertEqual(parameter[self._ports[1]][2], powersum(fext, 2, self._ports[1]))
        self.assertEqual(parameter[self._ports[1]][3], powersum(fext, 3, self._ports[1]))

        # check the values of the port 3
        self.assertEqual(parameter[self._ports[2]][0], powersum(fext, 0, self._ports[2]))
        self.assertEqual(parameter[self._ports[2]][1], powersum(fext, 1, self._ports[2]))
        self.assertEqual(parameter[self._ports[2]][2], powersum(fext, 2, self._ports[2]))
        self.assertEqual(parameter[self._ports[2]][3], powersum(fext, 3, self._ports[2]))

        # check the values of the port 4
        self.assertEqual(parameter[self._ports[3]][0], powersum(fext, 0, self._ports[3]))
        self.assertEqual(parameter[self._ports[3]][1], powersum(fext, 1, self._ports[3]))
        self.assertEqual(parameter[self._ports[3]][2], powersum(fext, 2, self._ports[3]))
        self.assertEqual(parameter[self._ports[3]][3], powersum(fext, 3, self._ports[3]))

if __name__ == '__main__':
    unittest.main()
