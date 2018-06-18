from parameters.next import NEXT
from parameters.parameter import comComMatrix

class CMNEXT(NEXT):
    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    def getName(self):
        return "CMNEXT"