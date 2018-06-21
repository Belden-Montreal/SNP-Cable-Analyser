import numpy as np
import math
from parameters.parameter import Parameter, complex2db, diffDiffMatrix
from parameters.next import NEXT

def powerSum(values):
    return 10*np.log10(np.sum(list(map(lambda v: 10**(v/10), values))))

class PSNEXT(Parameter):
    """
    The PSNEXT is the power sum of all the NEXT affecting a port. The PSNEXT
    is computed using the following formula from the standard:

        PSNEXT(f) = -10log( sum( 10^( -NEXT_n(f) / 10 ) ).
    """
    def __init__(self, ports, freq, matrices, pnext):
        self._next = pnext
        self._SEParameter = None
        super(PSNEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        # initialize the dictionary for each port
        dbPSNEXT = dict()
        dbEEPSNEXT = dict()
        for port in self._ports:
            dbPSNEXT[port] = list()
            dbEEPSNEXT[port] = list()

        # compute the power sum NEXT
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                # get all NEXT pairs containing this port
                pairs = self._next.getPairs()
                pairs = filter(lambda p: port == p[0] or port == p[1], pairs)

                # get the NEXT values of these pairs
                values = map(lambda p: self._next.getParameter(endToEnd=False)[p][f], pairs)

                # compute PSNEXT
                psnext = powerSum(values)

                # add the value to the list
                dbPSNEXT[port].append(psnext)

                # get all NEXT pairs containing this port
                pairs = self._next.getPairs()
                n = (1+math.sqrt(4*self._next.getNumPorts()+1))//2
                pairs = filter(lambda p: (port == p[0] or port == p[1]) and not ((p[0] < n//2 and p[1] >= n//2) or (p[1] < n//2 and p[0] >= n//2)), pairs)

                # get the NEXT values of these pairs
                values = map(lambda p: self._next.getParameter(endToEnd=True)[p][f], pairs)

                # compute PSNEXT
                psnext = powerSum(values)

                # add the value to the list
                dbEEPSNEXT[port].append(psnext)
        self._SEParameter = dbPSNEXT
        return (dbEEPSNEXT, None)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getNEXT(self):
        return self._next

    def getName(self):
        return "PSNEXT"

    def getParameter(self, endToEnd=True):
        if endToEnd:
            return self._parameter
        return self._SEParameter