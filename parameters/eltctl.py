from parameters.parameter import PairedParameter

class ELTCTL(PairedParameter):
    '''
    ELTCTL (Equal Level Transverse Conversion Transfer Loss) is calculated using the following formula:

    ELTCTL_k = TCTL_k - IL_k
    '''
    def __init__(self, ports, freq, matrices, il, tctl):
        self._il = il
        self._tctl = tctl
        super(ELTCTL, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        pairs = dict()
        for i in range(len(ports)//2):
            port1, isRemote1 = ports[i]
            port2, isRemote2 = ports[i+len(ports)//2]

            if isRemote1 is not isRemote2:
                pairs[(i, i+len(ports)//2)] = (port1+"-"+port2, isRemote1)
                pairs[(i+len(ports)//2, i)] = (port2+"-"+port1, isRemote2)

        return pairs

    def computeParameter(self):
        eltctl = dict()
        dbIl = self._il.getParameter()
        dbTctl = self._tctl.getParameter()

        for port in self._ports:
            eltctl[port] = list()

        for f,_ in enumerate(self._freq):
            for port in self._ports:
                eltctl[port].append(dbTctl[port][f] - dbIl[port][f])

        return eltctl,eltctl

    def chooseMatrices(self, matrices):
        return None

    def getIL(self):
        return self._il

    def getTCTL(self):
        return self._tctl

    def getName(self):
        return "ELTCTL"
