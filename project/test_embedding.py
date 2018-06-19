import unittest
from xlrd import open_workbook
from project.embedding import Embedding, Filetype
from project.plug import Plug, Filetype
class TestEmbedding(unittest.TestCase):
    def setUp(self):
        self._fileName = "testout_mm.s8p"

    def testFileImport(self):
        p = Plug()

        p.importSamples(self._fileName, Filetype.DFOPEN)
        p.importSamples(self._fileName, Filetype.DFSHORT)
        p.importSamples(self._fileName, Filetype.OPEN)
        p.importSamples(self._fileName, Filetype.SHORT)
        p.setConstants(1,2,3)
        p.importSamples(self._fileName, Filetype.LOAD)

        project = Embedding()
        project.setPlug(p)
        project.importSamples(self._fileName, Filetype.LOAD)


        #should have added 5 samples
        self.assertEqual(len(project._samples),1)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._samples[0]._name, "testout_mm")

       #TODO: re-embedding

        project.removeSamples("testout_mm")
        #should have removed the samples
        self.assertEqual(len(project._samples), 0)

