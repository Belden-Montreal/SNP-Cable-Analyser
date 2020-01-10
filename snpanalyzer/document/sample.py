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
        arguments["name"] = latex(configuration.getName())
        arguments["parameters"] = list()
        arguments["cnext"]=list()

        for (ptype, config) in configuration.getParameters().items():
            if not config.doExport():
                continue
          # create the document object for the parameter
            name   = normalize(config.getName())
            root   = self.getRoot()
            prefix = self.getPrefix().joinpath(name)
            parameter = dict()
            if config.isCnext() or config.isEmb():
                docobj = config.generateDocumentObject(root, prefix, plug=config.isCnext(), emb = config.isEmb())
                parameter["path"] = docobj.getRelativePath()
                arguments["cnext"].append(parameter)
            else:
                docobj = config.generateDocumentObject(root, prefix)
                parameter["path"] = docobj.getRelativePath()
                arguments["parameters"].append(parameter)


        return arguments
