from parameters.returnloss import ReturnLoss
from parameters.parameter import comComMatrix
from parameters.type import ParameterType

class CMRL(ReturnLoss):
    @staticmethod
    def getType():
        return ParameterType.CMRL

    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    def getName(self):
        return "CMRL"
