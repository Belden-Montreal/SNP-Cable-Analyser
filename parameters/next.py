from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.dataserie import PortPairDataSerie, PortOrderedPairDataSerie
from parameters.type import ParameterType

import itertools

class NEXT(Parameter):
    """
    Example of NEXT for a 3 wires network.
    
             1   2   3   4   5   6
    
       1   [ _  1-2 1-3  _   _   _ ]
       2   [1-2  _  2-3  _   _   _ ]
       3   [1-3 2-3  _   _   _   _ ]
       4   [ _   _   _   _  4-5 4-6]
       5   [ _   _   _  4-5  _  5-6]
       6   [ _   _   _  4-6 5-6  _ ]

    We have the following pairs twice: (1,2), (1,3), (2,3), (4,5), (4,6), (5,6).
    """
    def __init__(self, ports, freq, matrices, mains=True, remotes=True, order=True):
        self._mains   = mains
        self._remotes = remotes
        self._order   = order
        super(NEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.NEXT

    @staticmethod
    def register(parameters, mains=True, remotes=True, order=True):
        return lambda c, f, m: NEXT(c, f, m, mains=mains, remotes=remotes, order=order)

    def computeDataSeries(self):
        # create each pair for the NEXT
        series = set()

        # get the NEXT pairs between the main ports
        if self._mains:
            mains = self._ports.getMainPorts()
            for (i,j) in itertools.product(mains, mains):
                if i is j:
                    continue
                if self._order:
                    series.add(PortOrderedPairDataSerie(i, j))
                else:
                    series.add(PortPairDataSerie(i, j))
 
        # get the NEXT pairs between the remote ports
        if self._remotes:
            remotes = self._ports.getRemotePorts()
            for (i,j) in itertools.product(remotes, remotes):
                if i is j:
                    continue
                if self._order:
                    series.add(PortOrderedPairDataSerie(i, j))
                else:
                    series.add(PortPairDataSerie(i, j))

        return series

    def computeParameter(self):
        # initialize the dictionaries for each port
        dbNEXT = {serie: list() for serie in self._series}
        cpNEXT = {serie: list() for serie in self._series}

        # extract the NEXT values from the matrices
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                (i,j) = serie.getPortIndices()

                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = (complex2db(cpValue), complex2phase(cpValue))

                # add the value into the NEXT
                cpNEXT[serie].append(cpValue)
                dbNEXT[serie].append(dbValue)

        return (dbNEXT, cpNEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "NEXT"
