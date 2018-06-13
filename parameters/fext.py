from parameters.parameter import PairedParameter, complex2db, diffDiffMatrix

class Fext(PairedParameter):
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
                port1 = i
                port2 = j
                pairs.add((port1, port2))

                # create the pair for the second end of the line
                pairs.add((port2, port1))
        return pairs

    def computeParameter(self):
        fext = dict()
        cpFext = dict()
        for i,j in self._pairs:
            fext[(i,j)] = list()
            cpFext[(i,j)] = list()

        # extract the fext in all matrices
        for (f,_) in enumerate(self._freq):
            for i,j in self._pairs:
                # get the value
                value = self._matrices[f, i, j]
                fext[(i,j)].append(complex2db(value))
                cpFext[(i,j)].append(value)

        return fext, cpFext

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)
