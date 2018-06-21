from parameters.parameter import PairedParameter, complex2db, order, diffDiffMatrix
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

                # create the pair for the first end of the line
                port1 = i
                port2 = j
                pairs[(port1, port2)] = ports[port1]+"-"+ports[port2]
                pairs[(port2, port1)] = ports[port2]+"-"+ports[port1]

                # # create the pair for the second end of the line
                # port1 = i + len(ports)//2
                # port2 = j + len(ports)//2
                # pairs[(port1, port2)] = ports[port1]+"-"+ports[port2]
                # pairs[(port2, port1)] = ports[port2]+"-"+ports[port1]

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

                # add the value into the NEXT
                cpNEXT[(i,j)].append(cpValue)
                dbNEXT[(i,j)].append(dbValue)

        return (dbNEXT, cpNEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "NEXT"

    def getParameter(self, endToEnd=True):
        if endToEnd:
            n = (1+math.sqrt(4*self.getNumPorts()+1))//2
            return {(i,j): v for (i,j),v in sorted(self._parameter.items()) if not ((i < n//2 and j >= n//2) or (j < n//2 and i >= n//2))}
        return self._parameter

    def getComplexParameter(self, endToEnd=True):
        if endToEnd:
            n = (1+math.sqrt(4*self.getNumPorts()+1))//2
            return {(i,j): v for (i,j),v in sorted(self._complexParameter.items()) if not ((i < n//2 and j >= n//2) or (j < n//2 and i >= n//2))}
        return self._complexParameter