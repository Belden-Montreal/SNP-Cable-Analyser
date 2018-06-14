from parameters.parameter import Parameter, diffDiffMatrix

class PSACRF(Parameter):
    '''
        PSACRF is calculated using the following formula:
        PSACRF_k = PSFEXT_k - IL_k
        
        where PSFEXT_k is the PSFEXT on wire k and IL_k is the Insertion Loss on wire k
    '''
    def __init__(self, ports, freq, matrices, psFext, il):
        self._psFext = psFext
        self._il = il
        super(PSACRF, self).__init__(ports, freq, matrices)
    
    def computeParameter(self):
        
        psacrf = dict()
        psfext = self._psFext.getParameter()
        il = self._il.getParameter(full=True)

        for port in self._ports:
            psacrf[port] = list()

        for f,_ in enumerate(self._freq):
            for port in self._ports:
                psacrf[port].append(psfext[port][f]-il[port][f])
        return psacrf,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)