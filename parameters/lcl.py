from parameters.returnloss import ReturnLoss
from parameters.parameter import diffComMatrix

class LCL(ReturnLoss):
    '''
    LCL is calculated using the return loss of the differential mode - common mode (dc) matrix
    
    Example of LCL with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
    '''

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "LCL"