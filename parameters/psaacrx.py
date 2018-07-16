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
        self._ports = dict()
        for port, (name, isRemote) in ports.items():
            if not isRemote:
                self._ports[port] = (name, isRemote)
        super(PSAACRX, self).__init__(self._ports, freq, matrices)
    
    def computeParameter(self):
        
        psaacrx = dict()
        psaxext = self._psaxext.getParameter()
        il = self._il.getParameter(full=True)

        for port in self._ports:
            psaacrx[port] = list()

        for f,_ in enumerate(self._freq):
            for i in self._ports:
                ilPort = (i, i+len(self._ports))
                psaacrx[i].append((psaxext[i][f][0]-il[ilPort][f][0], 0))

        return psaacrx,_

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getPSAXEXT(self):
        return self._psaxext

    def getIL(self):
        return self._il

    def getName(self):
        return "PSAACRX"

    def recalculate(self, psaxext):
        self._psaxext = psaxext
        (self._parameter, self._complexParameter) = self.computeParameter()