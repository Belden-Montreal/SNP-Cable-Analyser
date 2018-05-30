import unittest
from Limit import Limit
from sympy import Symbol
import numpy as num

class TestLimits(unittest.TestCase):
    def test_parse(self):
        limit = Limit("RL", "2*f")
        self.assertEqual(100, limit.evaluate({'f': 50}))

    def test_parse_2(self):
        limit = Limit("RL", "2^fx")
        self.assertEqual(12, limit.evaluate({'f': 2, 'x': 3}))

    def test_parse_3(self):
        limit = Limit("RL", "2/f")
        self.assertEqual(0.5, limit.evaluate({'f': 4}))
        self.assertEqual(10, limit.evaluate({'f': 0.2}))

    def test_parse_4(self):
        limit = Limit("RL", "f+1-x")
        self.assertIsInstance(limit.evaluate({'f': 4, 'z': 8}), str)

    def test_parse_5(self):
        limit = Limit("RL", "1.2*(1.808*sqrt(f)+0.017*f+0.2/sqrt(f))")
        print(limit.evaluate({'f':4}))
        self.assertEqual(1.2*(1.808*num.sqrt(4)+0.017*4+0.2/num.sqrt(4)), limit.evaluate({'f': 4}))

if __name__ == '__main__':
    unittest.main()