import operator

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
        # arguments["resultat"] = dict()
        # arguments["marg"] = dict()
        # arguments["labelvalue"] = dict()
        # arguments["labelmargin"] = dict()
        arguments["format"] = list()
        # arguments["figure"] = dict()

        # create the analysis with the right data series
        parameter = configuration.getParameter()
        series   = {s for (s,e) in configuration.getDataSeries().items() if e}
        analysis  = ParameterAnalysis(parameter, series=series)
        for i, form in enumerate(configuration.getFormatExport()):
            analysis.setFormat(form)
            form = form.getName()
            form=dict()

            form["resultat"] = list()
            form["marg"] = list()
            form["labelvalue"] = list()
            form["labelmargin"] = list()
            analysis.setScale(configuration.getScale())

        # save the figure
            relative = str(self.getPrefix().joinpath(self.getBasename() +str(i)+ ".pgf")).replace("\\",'/')
            figure = str(self.getRoot().joinpath(relative))
            analysis.getFigure().savefig(figure, transparent=True)

            # Build tables
            worstValue =analysis._getWorstVal()
            worstMargin = analysis._getWorstMar()
            self.createTable(worstValue, form["resultat"],form["labelvalue"],analysis)
            self.createTable(worstMargin, form["marg"], form["labelmargin"], analysis)

            # create the arguments
            form["figure"] = dict()
            form["figure"]["path"]  = relative
            form["figure"]["scale"] = 0.62
            arguments["format"].append(form)



        return arguments

    def createTable(self, worst, argument, label,analysis):
        for pair in worst._pairs:
            label.clear()
            valeur = dict()
            valeur["nom"] = analysis._getLabel(pair)
            if worst.pairs[pair]._value:
                valeur["Value"] =round(worst.pairs[pair]._value, 2)
                label.append("Value")
            if worst.pairs[pair]._freq:
                valeur["Freq."]=round(worst.pairs[pair]._freq, 2)
                label.append("Freq.")
            if worst.pairs[pair]._limit:
                valeur["Limit"] = round(worst.pairs[pair]._limit, 2)
                label.append("Limit")
            if worst.pairs[pair]._margin:
                valeur["Margin"] = round(worst.pairs[pair]._margin, 2)
                label.append("Margin")
            argument.append(valeur)

        argument.sort(key=operator.itemgetter('nom'))
