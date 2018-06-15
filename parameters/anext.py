from parameters.parameter import PairedParameter, complex2db, order, diffDiffMatrix

class ANEXT(PairedParameter):
    """
        ANEXT is calculated by taking both the FEXT and the Insertion Loss of the disturbed hardware
        For ANEXT measurements to be valid, the measurements must be done on the same side :

        measurement (disturbed) []------            --------//[]
                                        |           |
                                         -----------
                                         -----------
                                        |           |
        measurement (disturber) []------            --------//[]
    """

    def __init__(self, ports, freq, matrices, fext, il):
        self._fext = fext
        self._il = il
        super(ANEXT, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        # create each pair for the ANEXT
        pairs = dict()
        for i in range(0, len(ports)//2):
            for j in range(len(ports)//2, len(ports)):
                if i == j or abs(i-j) == len(ports)//2:
                    continue

                # create the pair for the il
                pairs[(i, i)] = ports[i]+"-"+ports[i]

                # create the pair for the first end of the line
                pairs[(i, j)] = ports[i]+"-"+ports[j]

                # create the pair for the second end of the line
                pairs[(j, i)] = ports[j]+"-"+ports[i]

        return pairs

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbANEXT, cpANEXT) = (dict(), dict())
        dbIl = self._il.getParameter(full=False)
        cpIl = self._il.getComplexParameter(full=False)
        dbFext = self._fext.getParameter()
        cpFext = self._fext.getComplexParameter()

        for (i,j) in self._ports:
            dbANEXT[(i,j)] = list()
            cpANEXT[(i,j)] = list()

        # extract the ANEXT values from the fext and il
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._ports:
                if i==j:
                    cpANEXT[(i,j)].append(cpIl[i][f])
                    dbANEXT[(i,j)].append(dbIl[i][f])
                else:
                    cpANEXT[(i,j)].append(cpFext[(i,j)][f])
                    dbANEXT[(i,j)].append(dbFext[(i,j)][f])

        return (dbANEXT, cpANEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)
