from snpanalyzer.export.configuration import ExportConfiguration
from snpanalyzer.export.sample import SampleExportConfiguration
from snpanalyzer.document.project import ProjectDocumentObject
from overrides import overrides




class ProjectExportConfiguration(ExportConfiguration):
    def __init__(self, project, **kwargs):
        super(ProjectExportConfiguration, self).__init__(**kwargs)
        self._project = project
        self._samples = dict()
        print(project)

        # by default, we export all samples
        self._samples["project"] = "-Acquired Samples-"
        for sample in self._project.getSamples():
            self._samples[sample] = SampleExportConfiguration(sample)

        if self._project.getType() == "Plug":
            self._samples["cnext"] = "-Corrected Samples( {} )-".format(self._project.getLoadSample().getName())
            self._samples[self._project.getPlugNext()]=SampleExportConfiguration(self._project.getPlugNext(), cnext=True)
            self._samples[self._project.getLoadSample()] = SampleExportConfiguration(self._project.getLoadSample())
            self._samples[self._project.getLoadSample()].setName("Return Loss")

            self._samples["project"] = "-Acquired Samples-"
            for sample in self._project.getSamples():
                self._samples[sample] = SampleExportConfiguration(sample)
                self._samples[sample].setExport(False)
        if self._project.getType() == "Embedding":

            if self._project.load()["Forward"]:
                self._samples["forward"] = "Embedded Case -Forward-"
                self._samples[self._project.getCaseF()] = SampleExportConfiguration(self._project.getCaseF(), case = True)
                self._samples[self._project.getCaseF()].setName("Case(Forward)")
            if self._project.load()["Reverse"]:
                self._samples["reverse"] = "Embedded Case -Reverse-"
                self._samples[self._project.getCaseR()] = SampleExportConfiguration(self._project.getCaseR(), case=True)
                self._samples[self._project.getCaseR()].setName("Case(Reverse)")
            self._samples["plug"] = "Plug Samples"
            for sample in self._project.plug().getSamples():
                self._samples[sample] = SampleExportConfiguration(sample)
                self._samples[sample].setExport(False)
            self._samples["cnext"] = "Plug corrected NEXT"
            self._samples[self._project.plug().getPlugNext()] = SampleExportConfiguration(self._project.plug().getPlugNext(),
                                                                                              cnext=True)

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
