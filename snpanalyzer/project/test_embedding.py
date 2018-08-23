import unittest
from xlrd import open_workbook
from snpanalyzer.project.embedding import Embedding
from snpanalyzer.project.plug import Plug
class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self._fileName = "testout_mm.s8p"
        self._plugFileName = "projects/p4.bnap"

    def testFileImport(self):

        project = Embedding("test")
        project.importPlug(self._plugFileName)
        load = project.importLoad(self._fileName, side="Forward", cat="CAT6")

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project.load()["Forward"].getName(), "testout_mm")

        cases = project.load()["Forward"].getParameters()["Case"].getParameter()
        n= 0
        for case in cases.values():
            n += len(case)

        #should have 14 cases
        self.assertEqual(n, 14)

        project.removeSample(load)
        #should have removed the samples
        self.assertEqual(project.load()["Forward"], None)

