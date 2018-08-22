from document.object import DocumentObject, normalize
from overrides import overrides

class ProjectDocumentObject(DocumentObject):
    @overrides
    def getBasename(self):
        return normalize(self.getConfiguration().getProject().getName())

    @overrides
    def getTemplateName(self):
        return "project.tex"

    @overrides
    def getTemplateArguments(self, configuration):
        arguments = dict()
        arguments["samples"] = list()

        for config in configuration.getSamples().values():
            if not config.doExport():
                continue

            # create the document object for the sample
            name   = normalize(config.getSample().getName())
            root   = self.getRoot()
            prefix = self.getPrefix().joinpath(name)
            docobj = config.generateDocumentObject(root, prefix)

            # create the arguments for this sample
            sample = dict()
            sample["path"] = docobj.getRelativePath()
            arguments["samples"].append(sample)

        return arguments

        
