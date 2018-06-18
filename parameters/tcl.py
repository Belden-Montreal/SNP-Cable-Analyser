from parameters.parameter import comDiffMatrix
from parameters.returnloss import ReturnLoss

class TCL(ReturnLoss):
    '''
    TCL (Transverse Conversion Loss) is calculated using the return loss of the common mode - differential (cd) matrix
    
    Example of TCL with 4 wires:
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
    '''

    def chooseMatrices(self, matrices):
        return comDiffMatrix(matrices)

    def getName(self):
        return "TCL"