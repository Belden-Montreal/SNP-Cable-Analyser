import unittest
from xlrd import open_workbook
from project.plug import Plug

class TestPlug(unittest.TestCase):
    def setUp(self):
        self._fileName = "testout_mm.s8p"

    def testFileImport(self):
        project = Plug("test")

        project.importDfOpen(self._fileName)
        project.importDfShort(self._fileName)
        project.importOpen(self._fileName)
        project.importShort(self._fileName)
        project.setConstants(1,2,3)
        load = project.importLoad(self._fileName)

        #should have added 5 samples
        self.assertNotEqual((project._loadSample),None)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._loadSample.getName(), "testout_mm")

        #should have access to plug NEXT and NEXT delay
        self.assertTrue(project.getPlugNext())
        self.assertTrue(project.getNextDelay())

        project.removeSample(load)
        #should have removed the samples
        self.assertEqual(project._loadSample, None)

