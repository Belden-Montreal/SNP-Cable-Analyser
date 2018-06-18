from parameters.insertionloss import InsertionLoss
from parameters.parameter import diffComMatrix

class LCTL(InsertionLoss):
    '''
    LCTL is calculated using the Insertion Loss of the differential mode - common mode (dc) matrix

    Example of LCTL with 4 wires : 
         1 2 3 4
    1  [ _ _ 1 _ ] 
    2  [ _ _ _ 2 ] 
    3  [ _ _ _ _ ] 
    4  [ _ _ _ _ ] 
    '''

    def chooseMatrices(self, matrices):
        return diffComMatrix(matrices)

    def getName(self):
        return "LCTL"