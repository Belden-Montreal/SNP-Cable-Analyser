import unittest
from xlrd import open_workbook
from project.alien import Alien

class TestAlien(unittest.TestCase):
    def setUp(self):
        self._fileNames = ["snps/ALIEN TEST/AlienEnd1_2redo3 _3.s16p", "snps/ALIEN TEST/AlienEnd1_2redo3 _4.s16p"]

    def testFileImport(self):
        project = Alien("test")

        disturbers = project.importSamples(self._fileNames, "End 1", "PSANEXT", True)
        #should have added 2 disturber
        self.assertEqual(len(project._disturbers["End 1"]["PSANEXT"]),2)

        victim = project.importSamples(["snps/ALIEN TEST/Test_ALIEN_VICTIM_REDO_GOOD.s16p"], "End 1", "PSANEXT")
         #should have added a victim
        self.assertIsNot(project._victims["End 1"]["PSANEXT"], None)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._disturbers["End 1"]["PSANEXT"][0]._name, "AlienEnd1_2redo3 _3")
        self.assertEqual(project._disturbers["End 1"]["PSANEXT"][1]._name, "AlienEnd1_2redo3 _4")

        project.removeSample(disturbers[0])
        #should have removed a sample
        self.assertEqual(len(project._disturbers["End 1"]["PSANEXT"]), 1)
        self.assertEqual(project._disturbers["End 1"]["PSANEXT"][0]._name, "AlienEnd1_2redo3 _4")

        project.removeSample(victim)
        #should have no victim and 1 disturber
        self.assertEqual(project._victims["End 1"]["PSANEXT"], None)
        self.assertEqual(len(project._disturbers["End 1"]["PSANEXT"]), 1)
