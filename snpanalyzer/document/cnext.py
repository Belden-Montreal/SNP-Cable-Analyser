import operator

from snpanalyzer.document.object import DocumentObject, normalize
from snpanalyzer.analysis.parameter import ParameterAnalysis
from overrides import overrides

from snpanalyzer.analysis.format import DataFormat


class cnextDocumentObject(DocumentObject):
    @overrides
    def getBasename(self):
        return normalize(self.getConfiguration().getParameter().getName())

    @overrides
    def getTemplateName(self):
        return "cnext.tex"

    @overrides
    def getTemplateArguments(self, configuration):
        arguments = dict()
        format=[DataFormat.MAGNITUDE, DataFormat.PHASE]

        # create the analysis with the right data series
        parameter = configuration.getParameter()
        series   = {s for (s,e) in configuration.getDataSeries().items() if e}
        print(type(parameter))
        analysis  = ParameterAnalysis(parameter, series=series)
        arguments["figure"] = dict()
        for f in format:
            print(f.getName())
            analysis.setFormat(f)
            if f == DataFormat.MAGNITUDE:
                analysis.setColorSeries(0, 1, 0)
            elif f == DataFormat.PHASE:
                analysis.setColorSeries(0.2, 0.1, 0.7)

            analysis.setScale(configuration.getScale())

            # save the figure
            relative = str(self.getPrefix().joinpath(self.getBasename()+f.getName() + ".pgf")).replace("\\",'/')
            figure = str(self.getRoot().joinpath(relative))
            print("Figure : "+figure)
            analysis.setTitle("CNEXT:"+str(configuration.getName()), fontsize=20)
            analysis.getFigure().savefig(figure, transparent=True)
            # create the arguments
            arguments["figure"][f.getName()] = relative


        arguments["figure"]["scale"] = 0.60

        return arguments
