import unittest

from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.next import NEXTSingleEnded

class TestNEXTSingleEnded(TestParameter):
    def testComputeParameter(self):
        NEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        parameter = NEXT.getParameter()

        # for a 4 ports, there is only 2 NEXT parameters
        self.assertEqual(len(parameter), 2)

        # make sure the pair were created
        self.assertEqual("Port 1-Port 2" in parameter, True)
        self.assertEqual("Port 3-Port 4" in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter["Port 1-Port 2"]), len(self._freq))
        self.assertEqual(len(parameter["Port 3-Port 4"]), len(self._freq))

        # check the values of the pair 1
        self.assertAlmostEqual(parameter["Port 1-Port 2"][0], complex2db(self._matrices[0, 0, 1]))
        self.assertAlmostEqual(parameter["Port 1-Port 2"][1], complex2db(self._matrices[1, 0, 1]))
        self.assertAlmostEqual(parameter["Port 1-Port 2"][2], complex2db(self._matrices[2, 0, 1]))
        self.assertAlmostEqual(parameter["Port 1-Port 2"][3], complex2db(self._matrices[3, 0, 1]))

        # check the values of the pair 2
        self.assertAlmostEqual(parameter["Port 3-Port 4"][0], complex2db(self._matrices[0, 2, 3]))
        self.assertAlmostEqual(parameter["Port 3-Port 4"][1], complex2db(self._matrices[1, 2, 3]))
        self.assertAlmostEqual(parameter["Port 3-Port 4"][2], complex2db(self._matrices[2, 2, 3]))
        self.assertAlmostEqual(parameter["Port 3-Port 4"][3], complex2db(self._matrices[3, 2, 3]))

    def testComputeComplexParameter(self):
        NEXT = NEXTSingleEnded(self._ports, self._freq, self._matrices)
        parameter = NEXT.getComplexParameter()

        # for a 4 ports, there is only 2 NEXT parameters
        self.assertEqual(len(parameter), 2)

        # make sure the pair were created
        self.assertEqual("Port 1-Port 2" in parameter, True)
        self.assertEqual("Port 3-Port 4" in parameter, True)

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter["Port 1-Port 2"]), len(self._freq))
        self.assertEqual(len(parameter["Port 3-Port 4"]), len(self._freq))

        # check the values of the pair 1
        self.assertAlmostEqual(parameter["Port 1-Port 2"][0], self._matrices[0, 0, 1])
        self.assertAlmostEqual(parameter["Port 1-Port 2"][1], self._matrices[1, 0, 1])
        self.assertAlmostEqual(parameter["Port 1-Port 2"][2], self._matrices[2, 0, 1])
        self.assertAlmostEqual(parameter["Port 1-Port 2"][3], self._matrices[3, 0, 1])

        # check the values of the pair 2
        self.assertAlmostEqual(parameter["Port 3-Port 4"][0], self._matrices[0, 2, 3])
        self.assertAlmostEqual(parameter["Port 3-Port 4"][1], self._matrices[1, 2, 3])
        self.assertAlmostEqual(parameter["Port 3-Port 4"][2], self._matrices[2, 2, 3])
        self.assertAlmostEqual(parameter["Port 3-Port 4"][3], self._matrices[3, 2, 3])

if __name__ == '__main__':
    unittest.main()
