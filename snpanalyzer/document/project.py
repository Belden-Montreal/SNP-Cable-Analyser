import operator

from snpanalyzer.document.object import DocumentObject, normalize
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
        arguments["project"] = configuration.getProject().getName()
        arguments["project"]=arguments["project"].replace("_","\_")

        for config in configuration.getSamples().values():
            if isinstance(config, str):
                continue
            if not config.doExport():
                continue

            # create the document object for the sample
            name   = normalize(config.getName())
            name=name.replace("_","\_")
            root   = self.getRoot()
            prefix = self.getPrefix().joinpath(name)
            docobj = config.generateDocumentObject(root, prefix)

            # create the arguments for this sample
            sample = dict()
            sample["path"] = docobj.getRelativePath()
            arguments["samples"].append(sample)
            sample["name"] = name
        #arguments["samples"].sort(key=operator.itemgetter('name'))

        return arguments

        
