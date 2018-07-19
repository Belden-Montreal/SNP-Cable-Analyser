from parameters.next import NEXT
from parameters.parameter import comComMatrix
from parameters.type import ParameterType

class CMNEXT(NEXT):
    @staticmethod
    def getType():
        return ParameterType.CMNEXT

    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    def getName(self):
        return "CMNEXT"
