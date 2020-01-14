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

from snpanalyzer.app.project_manager import ProjectManager


from snpanalyzer.limits.LimitParser import LimitParser
from snpanalyzer.limits.TreeItem import TreeItem
from snpanalyzer.limits.Limit import Limit

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

from sys import argv
from pathlib import Path

f = r"C:\Users\LXF09011\Desktop\SNP-Cable-Analyser\testOtherProj\snps\plug4.s8p"

projectManager = ProjectManager()
node = projectManager.newProject("test")
project = node.getObject()
project.importSamples([r"C:\Users\LXF09011\Desktop\SNP-Cable-Analyser\testOtherProj\snps\plug4.s8p"])

parser = LimitParser("snpanalyzer/limits/test.xml")
root = parser.parseFile()
standard = root.child(0).child(0).child(0) #Connecting Hardware
project.setStandard(standard.standard)

print(project._standard.__str__())
print(project.getSamples())

project.generateExcel("output2.xlsx", ["plug4.s8p"], z=False)

print(project._samples[0].getStandard().__str__())
