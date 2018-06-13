from parameters.parameter import Parameter

class Acrf(Parameter):
    '''
        ACRF is calculated using the following formula : 

        ACRF_k = FEXT_k - IL_k
    '''

    def __init__(self, ports, freq, matrices, fext, il):
        self._fext = fext
        self._il = il
        super(Acrf, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        acrf = dict()
        dbFext = self._fext.getParameter()
        dbIl = self._il.getParameter()
        ports = dbFext.keys()
        for port in ports:
            acrf[port] = list()
        for (f,_) in enumerate(self._freq):
            for port in ports:
                ilPort = port[0]
                acrf[port].append(dbFext[port][f]-dbIl[ilPort][f])
        return acrf,_