from snpanalyzer.export.configuration import ExportConfiguration
from snpanalyzer.export.sample import SampleExportConfiguration
from snpanalyzer.document.project import ProjectDocumentObject
from overrides import overrides

class ProjectExportConfiguration(ExportConfiguration):
    def __init__(self, project, **kwargs):
        super(ProjectExportConfiguration, self).__init__(**kwargs)
        self._project = project
        self._samples = dict()

        # by default, we export all samples
        for sample in self._project.getSamples():
            self._samples[sample] = SampleExportConfiguration(sample)
            self._samples[sample].setExport(True)

    def addSample(self, sample):
        if sample in self._samples:
            self._samples[sample].setExport(True)

    def removeSample(self, sample):
        if sample in self._samples:
            self._samples[sample].setExport(False)

    def getSamples(self):
        return self._samples

    def getProject(self):
        return self._project

    @overrides
    def generateDocumentObject(self, root, prefix):
        return ProjectDocumentObject(root, prefix, self)
