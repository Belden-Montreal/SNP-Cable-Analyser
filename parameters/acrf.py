from parameters.parameter import PairedParameter, diffDiffMatrix

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
        for i in range(0, len(ports)//2):
            for j in range(len(ports)//2, len(ports)):
                if i == j or abs(i-j) == len(ports)//2:
                    continue

                # create the pair for the first end of the line
                pairs[(i, j)] = ports[i]+"-"+ports[j]

                # create the pair for the second end of the line
                pairs[(j, i)] = ports[j]+"-"+ports[i]

        return pairs
        
    def computeParameter(self):
        acrf = dict()
        dbFext = self._fext.getParameter()
        dbIl = self._il.getParameter(full=True)
        ports = dbFext.keys()
        for port in ports:
            acrf[port] = list()
        for (f,_) in enumerate(self._freq):
            for port in ports:
                ilPort = port[0]
                acrf[port].append(dbFext[port][f]-dbIl[ilPort][f])
        return acrf,_
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getFEXT(self):
        return self._fext

    def getIL(self):
        return self._il

    def getName(self):
        return "ACRF"
