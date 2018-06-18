import unittest
from xlrd import open_workbook
from project.alien import Alien

class TestAlien(unittest.TestCase):
    def setUp(self):
        self._fileNames = ["testout_mm.s8p", "testout_mm1.s16p"]

    def testFileImport(self):
        project = Alien()

        project.importSamples(self._fileNames, True)
        #should have added 2 disturber
        self.assertEqual(len(project._disturbers),2)

        project.importSamples([self._fileNames[1]])
         #should have added a victim
        self.assertIsNot(project._victim, None)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._samples[0]._name, "testout_mm")
        self.assertEqual(project._samples[1]._name, "testout_mm1")

        project.removeSamples(['testout_mm1'])
        #should have removed a sample
        self.assertEqual(len(project._samples), 1)
        self.assertEqual(project._samples[0]._name, "testout_mm")

        #should have no victim and 1 disturber
        self.assertEqual(project._victim, None)
        self.assertEqual(len(project._disturbers), 1)
