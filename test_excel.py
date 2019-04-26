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


from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtCore import Qt

from sys import argv
from pathlib import Path

f = r"C:\Users\LXF09011\Desktop\SNP-Cable-Analyser\embeddingNew2\embeddingNew2.xml"

projectManager = ProjectManager()
node = projectManager.loadProject(f)
project = node.getObject()

project.generateExcel("output2.xlsx", [f], z=False)
