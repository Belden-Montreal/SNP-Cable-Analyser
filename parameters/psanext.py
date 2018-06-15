from parameters.parameter import Parameter, diffDiffMatrix
import numpy as np

class PSANEXT(Parameter):
    '''
        PSANEXT is calculated by taking the ANEXT of every disturber pair on every pair of the victim and computing the powersum

        PSANEXT should be measured on the same side of the hardware for the disturbers or the disturbed
    '''
    def __init__(self, ports, freq, matrices, anextd):
        self._anextd = anextd
        super(PSANEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        
        psanext = dict()
        for port in self._ports:
            psanext[port] = list()
        

        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                ps = 10.0*np.log10(np.sum([np.sum([10**(disturber.getParameter()[key][f]/10) for key in disturber.getParameter().keys() if (key[0] == port)]) for disturber in self._anextd]))
                psanext[port].append(ps)
        return psanext,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getANEXT(self):
        return self._anextd
