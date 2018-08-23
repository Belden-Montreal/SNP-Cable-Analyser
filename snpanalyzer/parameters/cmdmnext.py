from snpanalyzer.parameters.next import NEXT
from snpanalyzer.parameters.parameter import comDiffMatrix
from snpanalyzer.parameters.type import ParameterType

class CMDMNEXT(NEXT):
    '''
    CMDMNEXT is calculated using the NEXT of the common mode - differential mode (cd) matrix

    Example of CMDMNEXT for a 3 wires network.
    
             1   2   3   4   5   6
    
       1   [ _  1-2 1-3  _   _   _ ]
       2   [1-2  _  2-3  _   _   _ ]
       3   [1-3 2-3  _   _   _   _ ]
       4   [ _   _   _   _  4-5 4-6]
       5   [ _   _   _  4-5  _  5-6]
       6   [ _   _   _  4-6 5-6  _ ]

    We have the following pairs twice: (1,2), (1,3), (2,3), (4,5), (4,6), (5,6).
    '''
    @staticmethod
    def getType():
        return ParameterType.CMDMNEXT

    @staticmethod
    def register(parameters, **kwargs):
        return lambda c, f, m: CMDMNEXT(c, f, m, **kwargs)

    def chooseMatrices(self, matrices):
        return comDiffMatrix(matrices)

    def getName(self):
        return "CMDMNEXT"
