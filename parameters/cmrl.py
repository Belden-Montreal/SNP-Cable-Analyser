from parameters.returnloss import ReturnLoss
from parameters.parameter import comComMatrix

class CMRL(ReturnLoss):
    def chooseMatrices(self, matrices):
        return comComMatrix(matrices)

    def getName(self):
        return "CMRL"
