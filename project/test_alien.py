import unittest
from xlrd import open_workbook
from project.alien import Alien

class TestAlien(unittest.TestCase):
    def setUp(self):
        self._fileNames = ["snps/ALIEN TEST/AlienEnd1_2redo3 _3.s16p", "snps/ALIEN TEST/AlienEnd1_2redo3 _4.s16p"]

    def testFileImport(self):
        project = Alien()

        project.importSamples(self._fileNames, True)
        #should have added 2 disturber
        self.assertEqual(len(project._disturbers),2)

        project.importSamples(["snps/ALIEN TEST/Test_ALIEN_VICTIM_REDO_GOOD.s16p"])
         #should have added a victim
        self.assertIsNot(project._victim, None)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._samples[0]._name, "AlienEnd1_2redo3 _3")
        self.assertEqual(project._samples[1]._name, "AlienEnd1_2redo3 _4")

        project.removeSamples(['AlienEnd1_2redo3 _3'])
        #should have removed a sample
        self.assertEqual(len(project._samples), 2)
        self.assertEqual(project._samples[0]._name, "AlienEnd1_2redo3 _4")

        project.removeSamples(['Test_ALIEN_VICTIM_REDO_GOOD'])
        #should have no victim and 1 disturber
        self.assertEqual(project._victim, None)
        self.assertEqual(len(project._disturbers), 1)
