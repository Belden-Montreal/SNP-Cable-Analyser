import unittest
from xlrd import open_workbook
from project.plug import Plug, Filetype

class TestPlug(unittest.TestCase):
    def setUp(self):
        self._fileName = "testout_mm.s8p"

    def testFileImport(self):
        project = Plug("test")

        project.importSamples(self._fileName, Filetype.DFOPEN)
        project.importSamples(self._fileName, Filetype.DFSHORT)
        project.importSamples(self._fileName, Filetype.OPEN)
        project.importSamples(self._fileName, Filetype.SHORT)
        project.setConstants(1,2,3)
        project.importSamples(self._fileName, Filetype.LOAD)

        #should have added 5 samples
        self.assertEqual(len(project._samples),5)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._samples[0]._name, "testout_mm")

        #should have access to plug NEXT and NEXT delay
        self.assertTrue(project.getPlugNext())
        self.assertTrue(project.getNextDelay())

        project.removeSamples("testout_mm")
        #should have removed the samples
        self.assertEqual(len(project._samples), 0)

