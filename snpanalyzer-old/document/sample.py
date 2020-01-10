from snpanalyzer.document.object import DocumentObject, normalize, latex
from overrides import overrides

class SampleDocumentObject(DocumentObject):
    @overrides
    def getBasename(self):
        return normalize(self.getConfiguration().getSample().getName())

    @overrides
    def getTemplateName(self):
        return "sample.tex"

    @overrides
    def getTemplateArguments(self, configuration):
        arguments = dict()
        arguments["name"] = latex(configuration.getSample().getName())
        arguments["parameters"] = list()

        for (ptype, config) in configuration.getParameters().items():
            if not config.doExport():
                continue

            # create the document object for the parameter
            name   = normalize(config.getParameter().getName())
            root   = self.getRoot()
            prefix = self.getPrefix().joinpath(name)
            docobj = config.generateDocumentObject(root, prefix)

            # create the arguments for this sample
            parameter = dict()
            parameter["path"] = docobj.getRelativePath()
            arguments["parameters"].append(parameter)

        return arguments
