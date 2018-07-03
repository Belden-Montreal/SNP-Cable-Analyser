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
        cpPSNEXT = dict()
        for port in self._ports:
            dbPSNEXT[port] = list()
            cpPSNEXT[port] = list()

        # compute the power sum NEXT
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                # get all NEXT pairs containing this port
                pairs = self._next.getPairs()
                pairs = [p for p in pairs if port == p[1] or port == p[0]]

                # get the NEXT values of these pairs
                values = [self._next.getParameter()[p][f] for p in pairs]
                cpValues = [self._next.getComplexParameter()[p][f] for p in pairs]

                # compute PSNEXT
                psnext = powerSum(values)
                cpPsnext = np.sum(list(cpValues))

                # add the value to the list
                dbPSNEXT[port].append(psnext)
                cpPSNEXT[port].append(cpPsnext)
        return (dbPSNEXT, cpPSNEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getNEXT(self):
        return self._next

    def getName(self):
        return "PSNEXT"
