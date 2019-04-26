from snpanalyzer.gui.widget.export.parameter import ExportParameterWidget
from snpanalyzer.gui.widget.export.sample import ExportSampleWidget
from snpanalyzer.gui.widget.export.project import ExportProjectWidget
from snpanalyzer.gui.dialog.export_configuration import ExportConfigurationDialog
from snpanalyzer.gui.dialog.compilation_configuration import CompilationConfigurationDialog

from snpanalyzer.export.parameter import ParameterExportConfiguration
from snpanalyzer.export.sample import SampleExportConfiguration
from snpanalyzer.export.project import ProjectExportConfiguration

from snpanalyzer.project.project import Project
from snpanalyzer.sample.cable import CableSample
from snpanalyzer.parameters.type import ParameterType

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

from sys import argv
from pathlib import Path

class MainWindow(QMainWindow): 
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.widget = ExportProjectWidget()
        self.setCentralWidget(self.widget)

project = Project("test project")
project.importSamples({
    "./snps/plug/plug1.s8p",
    "./snps/plug/plug2.s8p",
    "./snps/plug/plug3.s8p",
    "./snps/plug/plug4.s8p",
    "./snps/plug/plug5.s8p",
})

config = ProjectExportConfiguration(project)

app = QApplication(argv)
#from snpanalyzer.gui.dialog.vna_test import VNATestDialog
#vna = VNATestDialog()
#vna.show()

#window = MainWindow()
#window.widget.setExportConfiguration(config)
#window.show()
'''dialog = ExportConfigurationDialog(config)
dialog.show()
app.exec_()
obj = config.generateDocumentObject(
    dialog.getTemporaryDirectory(),
    Path("")
) '''

dialog = CompilationConfigurationDialog(project.getSamples())
dialog.show()
app.exec_()
obj = config.generateDocumentObject(
    dialog.getTemporaryDirectory(),
    Path("")
)

obj.compile(filename=dialog.getDocumentFilename())
