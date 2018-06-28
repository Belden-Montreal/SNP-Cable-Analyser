from parameters.parameter import PairedParameter, diffDiffMatrix
from math import sqrt, floor
class ACRF(PairedParameter):
    '''
        ACRF is calculated using the following formula : 

        ACRF_k = FEXT_k - IL_k
    '''

    def __init__(self, ports, freq, matrices, fext, il):
        self._fext = fext
        self._il = il
        super(ACRF, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        # create each pair for the ACRF
        pairs = dict()
        
        pairs = self._fext.getPorts()

        return pairs
        
    def computeParameter(self):
        acrf = dict()
        dbFext = self._fext.getParameter()
        dbIl = self._il.getParameter(full=True)
        for port in self._ports:
            acrf[port] = list()
        half = floor(sqrt(len(self._ports)))
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._ports:
                if i < half:
                    ilPort = (i, i+half)
                else:
                    ilPort = (i, i-half)
                acrf[(i,j)].append(dbFext[(i,j)][f]-dbIl[ilPort][f])

        return acrf,_
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getFEXT(self):
        return self._fext

    def getIL(self):
        return self._il

    def getName(self):
        return "ACRF"
