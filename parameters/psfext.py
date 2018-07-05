from parameters.parameter import Parameter, diffDiffMatrix, complex2db, complex2phase
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
        cpPsfext = dict()
        for port in self._ports:
            psfext[port] = list()
            cpPsfext[port] = list()
        dbFext = self._fext.getParameter()
        cpFext = self._fext.getComplexParameter()
        ports = dbFext.keys()
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                ps = 10.0*np.log10(np.sum([10**(dbFext[key][f][0]/10) for key in ports if (key[0] == port)]))
                #psfext[port].append(ps)
                cp = np.sum([cpFext[key][f] for key in ports if (key[0] == port)])
                cpPsfext[port].append(cp)
                #ps = complex2db(cp)
                phase = complex2phase(cp)
                psfext[port].append((ps, phase))
        return psfext,cpPsfext

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getFEXT(self):
        return self._fext

    def getName(self):
        return "PSFEXT"