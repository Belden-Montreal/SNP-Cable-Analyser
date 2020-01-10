from snpanalyzer.parameters.next import NEXT
from snpanalyzer.parameters.parameter import diffComMatrix
from snpanalyzer.parameters.type import ParameterType

class DMCMNEXT(NEXT):
    @staticmethod
    def getType():
        return ParameterType.DMCMNEXT

    @staticmethod
    def register(parameters, **kwargs):
        return lambda c, f, m: DMCMNEXT(c, f, m, **kwargs)

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "DMCMNEXT"
