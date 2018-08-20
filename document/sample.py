from document.object import DocumentObject, normalize, latex
from overrides import overrides

class SampleDocumentObject(DocumentObject):
    def __init__(self, prefix, sample):
        self._sample = sample
        super(SampleDocumentObject, self).__init__(prefix)

    @overrides
    def getBasename(self):
        return normalize(self._sample.getName())

    @overrides
    def getTemplateName(self):
        return "sample.tex"

    @overrides
    def getTemplateArguments(self):
        arguments = dict()

        # create the parameter document objects
        arguments['name'] = latex(self._sample.getName())
        arguments['parameters'] = set()
        for (ptype, analysis) in self._sample.getAnalyses().items():
            # make sure the analysis is set to export
            if not analysis.doExport():
                continue

            # generate the analysis' document object
            name = normalize(analysis.getParameter().getName())
            path = self.getPrefix().joinpath(name)
            obj = analysis.generateDocumentObject(path)
            arguments['parameters'].add(obj.getFilePath())

        return arguments
