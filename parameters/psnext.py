import numpy as np
import math
from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.next import NEXT
from parameters.dataserie import PortDataSerie

def powerSum(values):
    return 10*np.log10(np.sum(list(map(lambda v: 10**(v[0]/10), values))))

class PSNEXT(Parameter):
    """
    The PSNEXT is the power sum of all the NEXT affecting a port. The PSNEXT
    is computed using the following formula from the standard:

        PSNEXT(f) = -10log( sum( 10^( -NEXT_n(f) / 10 ) ).
    """
    def __init__(self, ports, freq, matrices, pnext):
        self._next = pnext
        super(PSNEXT, self).__init__(ports, freq, matrices)

    def computeDataSeries(self):
        mains   = self._ports.getMainPorts()
        remotes = self._ports.getRemotePorts()

        # create a serie for each port
        series = set()
        for p in self._ports.getPorts():
            # find pair that affects our port
            nextSeries = set()
            for nextSerie in self._next.getDataSeries():
                (p1,p2) = nextSerie.getPorts()

                if not p == p1:
                    continue

                nextSeries.add(nextSerie)

            # create the serie for the port
            series.add(PortDataSerie(p, data=nextSeries))

        return series

    def computeParameter(self):
        # initialize the dictionary for each data serie
        dbPSNEXT = {serie: list() for serie in self._series}
        cpPSNEXT = {serie: list() for serie in self._series}

        # compute the power sum NEXT
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                nextSeries = serie.getData()

                # get the NEXT values of these pairs
                cpValues = [self._next.getComplexParameter()[s][f] for s in nextSeries]
                dbValues = [self._next.getParameter()[s][f]        for s in nextSeries]
                
                # compute PSNEXT
                cpValue = np.sum(list(cpValues))
                dbValue = (powerSum(dbValues), complex2phase(cpValue))

                # add the value to the list
                dbPSNEXT[serie].append(dbValue)
                cpPSNEXT[serie].append(cpValue)

        return (dbPSNEXT, cpPSNEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getNEXT(self):
        return self._next

    def getName(self):
        return "PSNEXT"
