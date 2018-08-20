class Analysis(object):
    def __init__(self, export=True):
        self._export = export

    def doExport(self):
        return self._export

    def setExport(self, export=True):
        self._export = export

    def generateDocumentObject(self, prefix):
        NotImplementedError


"""
project: {
    latex: <filename.tex>
    samples: {
        sample1: {
            latex: <filename.tex>
            parameters: {
                insertionloss: {
                    latex: <filename.tex>
                    graph: <filename.pgf>
                }
                returnloss: {
                    latex: <filename.tex>
                    graph: <filename.pgf>
                }
            }
        }
    }
}

root:
    document.tex
    samples:
        sample1:
            sample1.tex
            worstcase.tex
            parameters:
                insertionloss:
                    parameter.tex
                    graph.pgf
                returnloss:
                    parameter.tex
                    graph.pgf
        sample2:
            sample2.tex
            worstcase.tex
            parameters:
                insertionloss:
                    parameter.tex
                    graph.pgf
                returnloss:
                    parameter.tex
                    graph.pgf

document.tex:
\input{samples/sample1/sample1}
\input{samples/sample2/sample2}

sample1.tex:
\input{samples/sample1/worstcase}
\input{samples/sample1/parameters/insertionloss/parameter}
\input{samples/sample1/parameters/returnloss/parameter}

sample2.tex:
\input{samples/sample2/worstcase}
\input{samples/sample2/parameters/insertionloss/parameter}
\input{samples/sample2/parameters/returnloss/parameter}

parameter.tex:
\input{samples/sample$N/parameters/$PARAM/graph}

project.generate(".")

for sample in samples:
    sample.generate(prefix+"samples"+sample.getName())
"""
