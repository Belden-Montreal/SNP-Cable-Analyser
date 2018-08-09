from parameters.parameter import comDiffMatrix
from parameters.returnloss import ReturnLoss
from parameters.type import ParameterType

class TCL(ReturnLoss):
    '''
    TCL (Transverse Conversion Loss) is calculated using the return loss
    Common-Differential (CD) mode.
    
    Example of TCL with 4 wires:
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
    '''
    @staticmethod
    def getType():
        return ParameterType.TCL

    @staticmethod
    def register(parameters):
        return lambda c, f, m: TCL(c, f, m)

    def chooseMatrices(self, matrices):
        return comDiffMatrix(matrices)

    def getName(self):
        return "TCL"
