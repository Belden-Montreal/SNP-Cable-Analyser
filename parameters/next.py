from parameters.parameter import PairedParameter, complex2db, complex2phase, diffDiffMatrix
import math

class NEXT(PairedParameter):
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
    def computePairs(self, ports):
        # create each pair for the NEXT
        pairs = dict()
        for i in range(0, len(ports)):
            for j in range(0, len(ports)):
                if i >= j:
                    continue

                port1, isRemote1 = ports[i]
                port2, isRemote2 = ports[j]

                if isRemote1 is isRemote2:
                    pairs[(i, j)] = (port1+"-"+port2, isRemote1)
                    #pairs[(j, i)] = (port2+"-"+port1, isRemote2)

        return pairs

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbNEXT, cpNEXT) = (dict(), dict())
        for (i,j) in self._ports:
            dbNEXT[(i,j)] = list()
            cpNEXT[(i,j)] = list()

        # extract the NEXT values from the matrices
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._ports:
                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = complex2db(cpValue)
                phase = complex2phase(cpValue)
                # add the value into the NEXT
                cpNEXT[(i,j)].append(cpValue)
                dbNEXT[(i,j)].append((dbValue, phase))

        return (dbNEXT, cpNEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "NEXT"