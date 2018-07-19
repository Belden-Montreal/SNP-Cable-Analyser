from parameters.insertionloss import InsertionLoss
from parameters.parameter import diffComMatrix
from parameters.type import ParameterType

class LCTL(InsertionLoss):
    '''
    LCTL is calculated using the insertionlLoss in Differential-Common (DC).

    Example of LCTL with 4 wires : 
         1 2 3 4
    1  [ _ _ 1 _ ] 
    2  [ _ _ _ 2 ] 
    3  [ _ _ _ _ ] 
    4  [ _ _ _ _ ] 
    '''
    @staticmethod
    def getType():
        return ParameterType.LCTL

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "LCTL"
