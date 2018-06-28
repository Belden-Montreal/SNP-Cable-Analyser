from parameters.parameter import Parameter, diffDiffMatrix

class PSAACRX(Parameter):
    '''
        PSAACRX represents both PSAACRN and PSAACRF.

        It is calculated using the following formula:
        PSAACRX_k = PSAXEXT_k - IL_k

        where PSAXEXT is either the PSANEXT or the PSAFEXT on the disturbed pair k and IL_k is the Insertion Loss on the disturbed pair k
    '''
    def __init__(self, ports, freq, matrices, psaxext, il):
        self._psaxext = psaxext
        self._il = il
        super(PSAACRX, self).__init__(ports, freq, matrices)
    
    def computeParameter(self):
        
        psaacrx = dict()
        psaxext = self._psaxext.getParameter()
        il = self._il.getParameter(full=True)

        for port in self._ports:
            psaacrx[port] = list()

        for f,_ in enumerate(self._freq):
            for i in self._ports:
                if i < len(self._ports)//2:
                    ilPort = (i, i+len(self._ports)//2)
                else:
                    ilPort = (i, i-len(self._ports)//2)
                psaacrx[i].append(psaxext[i][f]-il[ilPort][f])
        return psaacrx,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getPSAXEXT(self):
        return self._psaxext

    def getIL(self):
        return self._il

    def getName(self):
        return "PSAACRX"