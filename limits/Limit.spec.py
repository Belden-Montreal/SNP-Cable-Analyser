import unittest
from Limit import Limit
from sympy import Symbol
import numpy as num

class TestLimits(unittest.TestCase):
    def test_parse(self):
        limit = Limit("RL", ["2*f"])
        self.assertEqual(100, limit.evaluate({'f': 50}))

    def test_parse_2(self):
        limit = Limit("RL", ["2^fx"])
        self.assertEqual(12, limit.evaluate({'f': 2, 'x': 3}))

    def test_parse_3(self):
        limit = Limit("RL", ["2/f"], [0, 10])
        self.assertIsInstance(limit.evaluate({'f': -1}), str)

    def test_parse_4(self):
        limit = Limit("RL", ["f+1-x"])
        self.assertIsInstance(limit.evaluate({'f': 4, 'z': 8}), str)

    def test_parse_5(self):
        limit = Limit("RL", ["1.2*(1.808*sqrt(f)+0.017*f+0.2/sqrt(f))"])
        self.assertEqual(1.2*(1.808*num.sqrt(4)+0.017*4+0.2/num.sqrt(4)), limit.evaluate({'f': 4}))

    def test_parse_multiple(self):
        limit = Limit("RL", ["f*2", "f^2"], [0, 10, 50])
        self.assertEqual(5*2, limit.evaluate({'f':5}))
        self.assertEqual(15**2, limit.evaluate({'f':15}))

if __name__ == '__main__':
    unittest.main()