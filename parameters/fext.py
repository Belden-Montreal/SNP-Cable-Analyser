from parameters.parameter import PairedParameter, complex2db, order

class Fext(PairedParameter):
    '''
        Example of FEXT loss with 4 wires (double-ended only)
        
              1   2   3   4
        1  [  _   _   _  1-4 ] 
        2  [  _   _  2-3  _  ] 
        3  [  _  3-2  _   _  ] 
        4  [ 4-1  _   _   _  ] 
        
        
    '''
    def computePairs(self):
        numPorts = len(self._ports)

        # create each pair for the NEXT
        pairs = set()
        for i in range(0, numPorts//2):
            for j in range(numPorts//2, numPorts):
                if i == j or abs(i-j) == numPorts//2:
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