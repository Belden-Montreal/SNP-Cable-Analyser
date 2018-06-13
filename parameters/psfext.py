from parameters.parameter import Parameter, diffDiffMatrix
import numpy as np

class PSFEXT(Parameter):
    '''
        PSFEXT is calculated using the following formula:
        PSFEXT_k = 10*log10(sum(FEXT_i,k))
        
        where FEXT_i,k is the FEXT loss from wire i to wire k
    '''
    def __init__(self, ports, freq, matrices, fext):
        self._fext = fext
        super(PSFEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        
        psfext = dict()
        for port in self._ports:
            psfext[port] = list()
        dbFext = self._fext.getParameter()
        ports = dbFext.keys()

        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                ps = 10.0*np.log10(np.sum([10**(dbFext[key][f]/10) for key in ports if (key[0] == port)]))
                psfext[port].append(ps)
        return psfext,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)