from parameters.returnloss import ReturnLoss
from parameters.parameter import diffComMatrix

class DMCMRL(ReturnLoss):
    '''
    DMCMRL is calculated using the Return Loss of the differential mode - common mode (dc) matrix

    Example of DMCMRL with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
    '''

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)