from parameters.parameter import Parameter, diffDiffMatrix

class PSACRF(Parameter):
    '''
        PSACRF is calculated using the following formula:
        PSACRF_k = PSFEXT_k - IL_k
        
        where PSFEXT_k is the PSFEXT on wire k and IL_k is the Insertion Loss on wire k
    '''
    def __init__(self, ports, freq, matrices, psfext, il):
        self._psfext = psfext
        self._il = il
        super(PSACRF, self).__init__(ports, freq, matrices)
    
    def computeParameter(self):
        
        psacrf = dict()
        psfext = self._psfext.getParameter()
        il = self._il.getParameter(full=True)

        for port in self._ports:
            psacrf[port] = list()

        for f,_ in enumerate(self._freq):
            for i in self._ports:
                if i < len(self._ports)//2:
                    ilPort = (i, i+len(self._ports)//2)
                else:
                    ilPort = (i, i-len(self._ports)//2)
                psacrf[i].append(psfext[i][f]-il[ilPort][f])
        return psacrf,psacrf

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getPSFEXT(self):
        return self._psfext

    def getIL(self):
        return self._il

    def getName(self):
        return "PSACRF"