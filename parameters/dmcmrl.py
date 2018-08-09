from parameters.returnloss import ReturnLoss
from parameters.parameter import diffComMatrix
from parameters.type import ParameterType

class DMCMRL(ReturnLoss):
    '''
    DMCMRL is calculated using the return loss in Differential-Common (DC) mode.

    Example of DMCMRL with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
    '''
    @staticmethod
    def getType():
        return ParameterType.DMCMRL

    @staticmethod
    def register(parameters):
        return lambda c, f, m: DMCMRL(c, f, m)

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "DMCMRL"
