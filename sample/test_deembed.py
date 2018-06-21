import unittest
from sample.test_sample import TestSample
from sample.deembed import Deembed
from parameters.returnloss import ReturnLoss
from parameters.propagationdelay import PropagationDelay
from parameters.nextdelay import NEXTDelay
from parameters.correctednext import CorrectedNEXT
from parameters.plugdelay import PlugDelay
from parameters.dfdelay import DFDelay
import numpy as np

class TestDeembed(TestSample):
    def setUp(self):
        super(TestDeembed, self).setUp()
        self._params = [
            "PCNEXT",
            "NEXTDelay",
            "DNEXT",
            "Cases",
            "Case",
        ]
        self._cases = {
            1:((1,2),(lambda f, cnext: (-38.1+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            2:((1,2),(lambda f, cnext: (-38.6+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            3:((1,2),(lambda f, cnext: (-39+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            4:((1,2),(lambda f, cnext: (-39.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            5:((0,2),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            6:((0,2),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            7:((2,3),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            8:((2,3),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            9:((0,1),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            10:((0,1),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            11:((1,3),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            12:((1,3),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            13:((0,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            14:((0,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)-180))),
        }

    def testParametersBuilding(self):
        rl = ReturnLoss(self._ports, self._freq, self._mm)
        pd = PropagationDelay(self._ports, self._freq, self._mm, rl)
        dfDelay = DFDelay(self._ports, self._freq, self._mm, pd, pd)
        plugDelay = PlugDelay(self._ports, self._freq, self._mm, pd, pd, dfDelay, 1, 2, 3)
        nextDelay = NEXTDelay(self._ports, self._freq, self._mm, plugDelay)
        cnext = CorrectedNEXT(self._ports, self._freq, self._mm, nextDelay)
        d = Deembed(None, cnext, nextDelay, self._cases)
        self.setMockSample(d)
        self.assertEqual(len(d._parameters), len(self._params))
        self.assertListEqual(list(d._parameters.keys()), self._params)
        for param in d._parameters.values():
            self.assertTrue(param)

if __name__ == '__main__':
    unittest.main()