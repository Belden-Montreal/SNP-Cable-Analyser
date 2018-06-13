import unittest
from parameters.parameter import complex2db
from parameters.test_parameter import TestParameter
from parameters.lcl import LCL

class TestLCL(TestParameter):
    def testComputeParameter(self):
        lcl = LCL(self._ports, self._freq, self._matrices)
        parameter = lcl.getParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertAlmostEqual(parameter[0][0], complex2db(self._matrices[0, 0, 4]))
        self.assertAlmostEqual(parameter[0][1], complex2db(self._matrices[1, 0, 4]))
        self.assertAlmostEqual(parameter[0][2], complex2db(self._matrices[2, 0, 4]))
        self.assertAlmostEqual(parameter[0][3], complex2db(self._matrices[3, 0, 4]))

        # check the values of the port 2
        self.assertAlmostEqual(parameter[1][0], complex2db(self._matrices[0, 1, 5]))
        self.assertAlmostEqual(parameter[1][1], complex2db(self._matrices[1, 1, 5]))
        self.assertAlmostEqual(parameter[1][2], complex2db(self._matrices[2, 1, 5]))
        self.assertAlmostEqual(parameter[1][3], complex2db(self._matrices[3, 1, 5]))

        # check the values of the port 3
        self.assertAlmostEqual(parameter[2][0], complex2db(self._matrices[0, 2, 6]))
        self.assertAlmostEqual(parameter[2][1], complex2db(self._matrices[1, 2, 6]))
        self.assertAlmostEqual(parameter[2][2], complex2db(self._matrices[2, 2, 6]))
        self.assertAlmostEqual(parameter[2][3], complex2db(self._matrices[3, 2, 6]))

        # check the values of the port 4
        self.assertAlmostEqual(parameter[3][0], complex2db(self._matrices[0, 3, 7]))
        self.assertAlmostEqual(parameter[3][1], complex2db(self._matrices[1, 3, 7]))
        self.assertAlmostEqual(parameter[3][2], complex2db(self._matrices[2, 3, 7]))
        self.assertAlmostEqual(parameter[3][3], complex2db(self._matrices[3, 3, 7]))

    def testComputeComplexParameter(self):
        lcl = LCL(self._ports, self._freq, self._matrices)
        parameter = lcl.getComplexParameter()

        # there should be a parameter for each ports
        self.assertEqual(len(parameter), len(self._ports))

        # the number of sample should be the same as the number of frequencies
        self.assertEqual(len(parameter[0]), len(self._freq))
        self.assertEqual(len(parameter[1]), len(self._freq))
        self.assertEqual(len(parameter[2]), len(self._freq))
        self.assertEqual(len(parameter[3]), len(self._freq))

        # check the values of the port 1
        self.assertEqual(parameter[0][0], self._matrices[0, 0, 4])
        self.assertEqual(parameter[0][1], self._matrices[1, 0, 4])
        self.assertEqual(parameter[0][2], self._matrices[2, 0, 4])
        self.assertEqual(parameter[0][3], self._matrices[3, 0, 4])

        # check the values of the port 2
        self.assertEqual(parameter[1][0], self._matrices[0, 1, 5])
        self.assertEqual(parameter[1][1], self._matrices[1, 1, 5])
        self.assertEqual(parameter[1][2], self._matrices[2, 1, 5])
        self.assertEqual(parameter[1][3], self._matrices[3, 1, 5])

        # check the values of the port 3
        self.assertEqual(parameter[2][0], self._matrices[0, 2, 6])
        self.assertEqual(parameter[2][1], self._matrices[1, 2, 6])
        self.assertEqual(parameter[2][2], self._matrices[2, 2, 6])
        self.assertEqual(parameter[2][3], self._matrices[3, 2, 6])

        # check the values of the port 4
        self.assertEqual(parameter[3][0], self._matrices[0, 3, 7])
        self.assertEqual(parameter[3][1], self._matrices[1, 3, 7])
        self.assertEqual(parameter[3][2], self._matrices[2, 3, 7])
        self.assertEqual(parameter[3][3], self._matrices[3, 3, 7])
if __name__ == '__main__':
    unittest.main()
