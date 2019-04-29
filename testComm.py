

from snpanalyzer.project.project import Project

from snpanalyzer.project.project import Project

from snpanalyzer.vna import VNA
from snpanalyzer.gui.dialog.vna_test import VNATestDialog

from snpanalyzer.sample.cable import CableSample
from snpanalyzer.parameters.type import ParameterType

from snpanalyzer.app.project_manager import ProjectManager

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

from sys import argv
from pathlib import Path


class MainWindow(QMainWindow): 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.widget = ExportProjectWidget()
        self.setCentralWidget(self.widget)

app = QApplication(argv)


projectManager = ProjectManager()
node = projectManager.newProject("TestVNA")
_vnaManager = VNA()
_vnaManager.connect()

vnaDialog = VNATestDialog()
vnaDialog.show()
app.exec_()
name = vnaDialog.getSampleName()
ports = vnaDialog.getPorts()
sample_file = _vnaManager.acquire(name, 8, vnaDialog.getVNACOnfiguration())
node.addSamples([sample_file])



