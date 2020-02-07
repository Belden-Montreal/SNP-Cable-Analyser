import unittest
from snpanalyzer.limits.Limit import Limit
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
        self.assertEqual(0, limit.evaluate({'f': -1}))

    def test_parse_4(self):
        limit = Limit("RL", ["f+1-x"])
        self.assertEqual(0, limit.evaluate({'f': 4, 'z': 8}))

    def test_parse_5(self):
        limit = Limit("RL", ["1.2*(1.808*sqrt(f)+0.017*f+0.2/sqrt(f))"])
        self.assertEqual(1.2*(1.808*num.sqrt(4)+0.017*4+0.2/num.sqrt(4)), limit.evaluate({'f': 4}))

    def test_parse_multiple(self):
        limit = Limit("RL", ["f*2", "f^2"], [0, 10, 50])
        self.assertEqual(5*2, limit.evaluate({'f':5}))
        self.assertEqual(15**2, limit.evaluate({'f':15}))

    def test_parse_array(self):
        limit = Limit("RL", ["2*f"])
        self.assertListEqual([(1,2),(2,4),(3,6),(4,8)], limit.evaluateArray({'f':[1,2,3,4]}, 4))

    def test_parse_array_2(self):
        limit = Limit("RL", ["2*f*x"])
        self.assertListEqual([(1, 8),(2, 12),(3, 12),(4, 8)], limit.evaluateArray({'f':[1,2,3,4], 'x':[4,3,2,1]}, 4))

    def test_parse_dict(self):
        limit = Limit("RL", ["2*f"])
        self.assertEqual({1:2, 2:4, 3:6, 4:8}, limit.evaluateDict({'f':[1,2,3,4]}, 4))

    def test_parse_neg(self):
        limit = Limit("RL", ["2*f"], [1,10])
        self.assertEqual([(2,-4)], limit.evaluateArray({'f':[2]}, 1, neg=True))

    def test_repeat(self):
        limit = Limit("RL", ["2*f"])
        self.assertEqual({1:2, 2:4, 3:6, 4:8}, limit.evaluateDict({'f':[1,2,3,4]}, 4))

        self.assertEqual({1:-2, 2:-4, 3:-6, 4:-8}, limit.evaluateDict({'f':[1,2,3,4]}, 4, True))

        self.assertEqual({1:2, 2:4, 3:6, 4:8}, limit.evaluateDict({'f':[1,2,3,4]}, 4))

if __name__ == '__main__':
    unittest.main()