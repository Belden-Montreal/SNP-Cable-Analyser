from parameters.parameter import PairedParameter, complex2db, diffDiffMatrix

class FEXT(PairedParameter):
    '''
    Example of FEXT loss with 4 wires (double-ended only).
        
              1   2   3   4   5   6
        1  [  _   _   _   _  1-5 1-6] 
        2  [  _   _   _  2-4  _  2-6] 
        3  [  _   _   _  3-4 3-5  _ ] 
        4  [  _  2-4 3-4  _   _   _ ] 
        5  [ 1-5  _  3-5  _   _   _ ] 
        6  [ 1-6 2-6  _   _   _   _ ]

    We have the following pairs twice: (1,5), (1,6), (2,4), (2,6), (3,4), (3,5).
    '''
    def computePairs(self):
        # create each pair for the NEXT
        pairs = set()
        for i in range(0, self.getNumPorts()//2):
            for j in range(self.getNumPorts()//2, self.getNumPorts()):
                if i == j or abs(i-j) == self.getNumPorts()//2:
                    continue

                # create the pair for the first end of the line
                pairs.add((i, j))

                # create the pair for the second end of the line
                pairs.add((j, i))

        return pairs

    def computeParameter(self):
        # initialize the dictionaries for each port
        (dbFEXT, cpFEXT) = (dict(), dict())
        for (i,j) in self._pairs:
            dbFEXT[(i,j)] = list()
            cpFEXT[(i,j)] = list()

        # extract the FEXT value from the matrices
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._pairs:
                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = complex2db(cpValue)

                # add the value into the FEXT
                cpFEXT[(i,j)].append(cpValue)
                dbFEXT[(i,j)].append(dbValue)

        return (dbFEXT, cpFEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)
