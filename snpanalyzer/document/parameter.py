from snpanalyzer.document.object import DocumentObject, normalize
from snpanalyzer.analysis.parameter import ParameterAnalysis
from overrides import overrides

class ParameterDocumentObject(DocumentObject):
    @overrides
    def getBasename(self):
        return normalize(self.getConfiguration().getParameter().getName())

    @overrides
    def getTemplateName(self):
        return "parameter.tex"

    @overrides
    def getTemplateArguments(self, configuration):
        arguments = dict()

        # create the analysis with the right data series
        parameter = configuration.getParameter()
        series    = {s for (s,e) in configuration.getDataSeries().items() if e}
        analysis  = ParameterAnalysis(parameter, series=series)
        analysis.setFormat(configuration.getFormat())
        analysis.setScale(configuration.getScale())

        # save the figure
        relative = str(self.getPrefix().joinpath(self.getBasename()+".pgf")).replace("\\",'/')
        figure = str(self.getRoot().joinpath(relative))
        print("Figure : "+figure)
        analysis.getFigure().savefig(figure)

        # create the arguments
        arguments["figure"] = dict()
        arguments["figure"]["path"]  = relative
        arguments["figure"]["scale"] = 0.4
        # arguments["parameter"] = dict()
        #arguments["parameter"]["name"] = parameter. 

        return arguments
        
