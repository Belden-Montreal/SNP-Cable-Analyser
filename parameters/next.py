from parameters.parameter import Parameter, complex2db

class NEXTSingleEnded(Parameter):
    def computeParameter(self):
        # Example of NEXT for 6 single ended wires.
        #
        #        1 2 3 4 5 6
        #
        #   1   [_ 1 2 _ _ _]
        #   2   [1 _ 3 _ _ _]
        #   3   [2 3 _ _ _ _]
        #   4   [_ _ _ _ 4 5]
        #   5   [_ _ _ 4 _ 6]
        #   6   [_ _ _ 5 6 _]
        #
        numPorts = len(self._ports)

        # initialize the dictionaries for each port
        (dbNEXT, cpNEXT) = (dict(), dict())

        # create each pair for the NEXT
        pairs = list()
        for i in range(0, numPorts//2):
            for j in range(0, numPorts//2):
                if i >= j:
                    continue

                # create the pair for the first end of the line
                port1 = i
                port2 = j
                pairname = self._ports[port1] + "-" + self._ports[port2]
                pairs.append((port1, port2, pairname))
                dbNEXT[pairname] = list()
                cpNEXT[pairname] = list()

                # create the pair for the second end of the line
                port1 = i + numPorts//2
                port2 = j + numPorts//2
                pairname = self._ports[port1] + "-" + self._ports[port2]
                pairs.append((port1, port2, pairname))
                dbNEXT[pairname] = list()
                cpNEXT[pairname] = list()

        # extract the NEXT values from the matrices
        for (f,_) in enumerate(self._freq):
            for (i,j,pair) in pairs:
                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = complex2db(cpValue)

                # add the value into the NEXT
                cpNEXT[pair].append(cpValue)
                dbNEXT[pair].append(dbValue)

        return (dbNEXT, cpNEXT)
