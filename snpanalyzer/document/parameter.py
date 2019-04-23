from snpanalyzer.document.object import DocumentObject, normalize
from snpanalyzer.analysis.parameter import ParameterAnalysis
from overrides import overrides

class ParameterDocumentObject(DocumentObject):
    @overrides
    def getBasename(self):
        return normalize(self.getConfiguration().getParameter().getName())

    @overrides
    def getTemplateName(self):
        return "parameter_table.tex"

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
        relative = str(self.getPrefix().joinpath(self.getBasename()+".png")).replace("\\",'/')
        figure = str(self.getRoot().joinpath(relative))
        print("Figure : "+figure)
        analysis.getFigure().savefig(figure, transparent=True)

        # create the arguments
        arguments["figure"] = dict()
        arguments["figure"]["path"]  = relative
        arguments["figure"]["scale"] = .7
        arguments["results"] = dict()
        #arguments["results"]["freq"] = analysis._getXData(serie = None)

        #arguments["results"]["limit"] = analysis._getYData(series = "limit")
        #arguments["results"]["worstCase"] = analysis._getWorstVal


        
        # arguments["parameter"] = dict()
        #arguments["parameter"]["name"] = parameter. 

        return arguments
        
