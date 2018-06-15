from parameters.parameter import Parameter, diffDiffMatrix
import numpy as np

class PSAFEXT(Parameter):
    '''
        PSAFEXT is calculated by taking the AFEXT of every disturber pair on every pair of the victim and computing the powersum

        PSAFEXT should be measured on the opposite side of the hardware for the disturbers or the disturbed
    '''
    def __init__(self, ports, freq, matrices, afextd):
        self._anextd = afextd
        super(PSAFEXT, self).__init__(ports, freq, matrices)

    def getAFEXT(self):
        return self._anextd
