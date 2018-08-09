from parameters.insertionloss import InsertionLoss
from parameters.parameter import comDiffMatrix
from parameters.type import ParameterType

class TCTL(InsertionLoss):
    '''
    TCTL (Transverse Conversion Transfer Loss) is calculated using the
    insertion loss in Common-Differential mode (CD).

    example of TCTL with 4 wires: 
         1 2 3 4
    1  [ _ _ 1 _ ] 
    2  [ _ _ _ 2 ] 
    3  [ _ _ _ _ ] 
    4  [ _ _ _ _ ] 
    '''
    @staticmethod
    def getType():
        return ParameterType.TCTL

    @staticmethod
    def register(parameters, **kwargs):
        return lambda c, f, m: TCTL(c, f, m, **kwargs)

    def chooseMatrices(self, matrices):
        return comDiffMatrix(matrices)

    def getName(self):
        return "TCTL"
