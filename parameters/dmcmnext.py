from parameters.next import NEXT
from parameters.parameter import diffComMatrix
from parameters.type import ParameterType

class DMCMNEXT(NEXT):
    @staticmethod
    def getType():
        return ParameterType.DMCMNEXT

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "DMCMNEXT"
