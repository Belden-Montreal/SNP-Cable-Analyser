import unittest
from sample.snp_analyzer import SNPAnalyzer
from skrf.network import Network as rf

class TestSNPAnalyzer(unittest.TestCase):

    def setUp(self):
        self._file = "testout_mm.s8p"
        rs = rf(self._file)
        rs.se2gmm(p = int(rs.number_of_ports/2))
        self._mm = rs.s

    def testFileReading(self):
        snp = SNPAnalyzer(self._file)
        mm, freq, nPorts = snp.getMM()
        #should have 8 ports
        self.assertEqual(nPorts, 8)
        
        #first frequency should be 300000
        self.assertAlmostEqual(freq[0], 300000.0)

        #all values should be the same
        for i,f in enumerate(mm):
            for j,sx in enumerate(f):
                for k,sy in enumerate(sx):
                    self.assertAlmostEqual(sy, self._mm[i,j,k])