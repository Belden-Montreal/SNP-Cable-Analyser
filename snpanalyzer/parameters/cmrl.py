from snpanalyzer.parameters.returnloss import ReturnLoss
from snpanalyzer.parameters.parameter import comComMatrix
from snpanalyzer.parameters.type import ParameterType

class CMRL(ReturnLoss):
    @staticmethod
    def getType():
        return ParameterType.CMRL

    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    @staticmethod
    def register(parameters):
        return lambda c, f, m: CMRL(c, f, m)

    def getName(self):
        return "CMRL"
