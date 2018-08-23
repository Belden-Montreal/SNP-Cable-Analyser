from parameters.next import NEXT
from parameters.parameter import comComMatrix
from parameters.type import ParameterType

class CMNEXT(NEXT):
    @staticmethod
    def getType():
        return ParameterType.CMNEXT

    @staticmethod
    def register(parameters, **kwargs):
        return lambda c, f, m: CMNEXT(c, f, m, **kwargs)

    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    def getName(self):
        return "CMNEXT"
