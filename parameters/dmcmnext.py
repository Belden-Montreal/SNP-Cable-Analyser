from parameters.next import NEXT
from parameters.parameter import diffComMatrix

class DMCMNEXT(NEXT):
    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "DMCMNEXT"