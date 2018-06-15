from parameters.parameter import Parameter

class ELTCTL(Parameter):
    '''
    ELTCTL (Equal Level Transverse Conversion Transfer Loss) is calculated using the following formula:

    ELTCTL_k = TCTL_k - IL_k
    '''
    def __init__(self, ports, freq, matrices, il, tctl):
        self._il = il
        self._tctl = tctl
        super(ELTCTL, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        eltctl = dict()
        dbIl = self._il.getParameter()
        dbTctl = self._tctl.getParameter()

        ports = dbIl.keys()

        for port in ports:
            eltctl[port] = list()

        for f,_ in enumerate(self._freq):
            for port in ports:
                eltctl[port].append(dbTctl[port][f] - dbIl[port][f])

        return eltctl,_

    def chooseMatrices(self, matrices):
        return None

    def getIL(self):
        return self._il

    def getTCTL(self):
        return self._tctl
