from document.object import DocumentObject, normalize
from overrides import overrides

class ParameterDocumentObject(DocumentObject):
    def __init__(self, prefix, analysis):
        self._analysis = analysis
        super(ParameterDocumentObject, self).__init__(prefix)

    @overrides
    def getBasename(self):
        return normalize(self._analysis.getParameter().getName())

    @overrides
    def getTemplateName(self):
        return "parameter.tex"

    @overrides
    def getTemplateArguments(self):
        figure = str(self.getPrefix().joinpath(self.getBasename()+".pgf"))
        self._analysis.getFigure().savefig(figure)

        return {
            'figure': {
                'path': figure,
                'scale': 0.3,
            },
        }
        
