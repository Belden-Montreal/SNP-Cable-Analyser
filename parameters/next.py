from parameters.parameter import PairedParameter, complex2db, order

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

    We have the following pairs: (1,2), (1,3), (2,3), (4,5), (4,6), (5,6).
    """
    def computePairs(self):
        # create each pair for the NEXT
        pairs = set()
        for i in range(0, self.getNumPorts()//2):
            for j in range(0, self.getNumPorts()//2):
                if i >= j:
                    continue

                # create the pair for the first end of the line
                port1 = i
                port2 = j
                pairs.add((port1, port2))

                # create the pair for the second end of the line
                port1 = i + self.getNumPorts()//2
                port2 = j + self.getNumPorts()//2
                pairs.add(order(port1, port2))

        return pairs

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbNEXT, cpNEXT) = (dict(), dict())
        for (i,j) in self._pairs:
            dbNEXT[(i,j)] = list()
            cpNEXT[(i,j)] = list()

        # extract the NEXT values from the matrices
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._pairs:
                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = complex2db(cpValue)

                # add the value into the NEXT
                cpNEXT[(i,j)].append(cpValue)
                dbNEXT[(i,j)].append(dbValue)

        return (dbNEXT, cpNEXT)
