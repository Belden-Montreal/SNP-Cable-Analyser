from parameters.parameter import Parameter, diffDiffMatrix
import numpy as np

class PSAXEXT(Parameter):
    '''
        PSAXEXT represents both the PSANEXT and the PSAFEXT
        It is calculated by taking the either the ANEXT or the AFEXT of every disturber pair on every pair of the victim and computing the powersum
    '''
    def __init__(self, ports, freq, matrices, axextd):
        self._axextd = axextd
        super(PSAXEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        
        psaxext = dict()
        for port in self._ports:
            psaxext[port] = list()
        

        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                ps = 10.0*np.log10(np.sum([np.sum([10**(disturber.getParameter()[key][f]/10) for key in disturber.getParameter().keys() if (key[0] == port)]) for disturber in self._axextd]))
                psaxext[port].append(ps)
        return psaxext,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getAXEXT(self):
        return self._axextd
