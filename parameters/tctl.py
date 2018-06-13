from parameters.insertionloss import InsertionLoss
from parameters.parameter import comDiffMatrix

class TCTL(InsertionLoss):
    '''
    TCTL (Transverse Conversion Transfer Loss) is calculated using the Insertion Loss of the common mode - differential mode (cd) matrix

    example of TCTL with 4 wires: 
         1 2 3 4
    1  [ _ _ 1 _ ] 
    2  [ _ _ _ 2 ] 
    3  [ _ _ _ _ ] 
    4  [ _ _ _ _ ] 
    '''
    
    def chooseMatrices(self, matrices):
        return comDiffMatrix(matrices)