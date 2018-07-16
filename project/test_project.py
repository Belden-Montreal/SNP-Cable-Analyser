import unittest
from xlrd import open_workbook

from project.project import Project

class TestProject(unittest.TestCase):
    def setUp(self):
        self._fileNames = ["testout_mm.s8p", "testout_mm1.s16p"]

    def testFileImport(self):
        project = Project("test")
        samples = project.importSamples(self._fileNames)

        #should create 2 samples
        self.assertEqual(len(project._samples), 2)

        #samples should have the correct names
        #self.assertEqual(project._samples[0]._name, "fci")
        self.assertEqual(project._samples[0]._name, "testout_mm")
        self.assertEqual(project._samples[1]._name, "testout_mm1")

        project.removeSample(samples[0])
        #should have removed a sample
        self.assertEqual(len(project._samples), 1)
        self.assertEqual(project._samples[0]._name, "testout_mm1")

        project.removeSample(samples[1])
        #should have no samples
        self.assertEqual(len(project._samples), 0)

    # def testExcel(self): #This is a long test
    #     project = Project()
    #     project.importSamples(self._fileNames)
    #     project.generateExcel("testProject", ["testout_mm", "testout_mm1"])
    #     workbook = open_workbook("testProject.xlsx")
    #     sheets = workbook.sheets()

    #     #should have created 2 sheets
    #     self.assertEqual(len(sheets), 2)
