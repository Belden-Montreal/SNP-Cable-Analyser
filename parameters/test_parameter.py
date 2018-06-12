import unittest
import numpy as np

from parameters.parameter import Parameter

class TestParameter(unittest.TestCase):
    def setUp(self):
        self._ports = {
            0: "Port 1",
            1: "Port 2",
            2: "Port 3",
            3: "Port 4",
        }

        self._freq = [100, 200, 300, 400]

        self._matrices = np.array([
            [
                [ 1,  2,  3,  4],
                [ 5,  6,  7,  8],
                [ 9, 10, 11, 12],
                [13, 14, 15, 16],
            ],[
                [17, 18, 19, 20],
                [21, 22, 23, 24],
                [25, 26, 27, 28],
                [29, 30, 31, 32],
            ],[
                [33, 34, 35, 36],
                [37, 38, 39, 40],
                [41, 42, 43, 44],
                [45, 46, 47, 48],
            ],[
                [49, 50, 51, 52],
                [53, 54, 55, 56],
                [57, 58, 59, 60],
                [61, 62, 63, 64],
            ]
        ], np.int32)

if __name__ == '__main__':
    unittest.main()
