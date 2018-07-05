from parameters.parameter import PairedParameter, complex2db, complex2phase, diffDiffMatrix

class ReturnLoss(PairedParameter):
    '''
        Example of Return Loss with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
        
        
    '''

    def computePairs(self, ports):
        pairs = dict()
        for i in range(len(ports)):
            port, isRemote = ports[i]
            pairs[(i,i)] = (port, isRemote)
        return pairs
    
    def computeParameter(self):
        
        # initialize the dictionary for each port
        rl = dict()
        cpRl = dict()
        for (i,j) in self._ports:
            rl[(i,j)] = list()
            cpRl[(i,j)] = list()

        # extract the return loss in all matrices
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._ports:
                # get the value
                value = self._matrices[f, i, j]

                # convert to db if specified
                dbValue = complex2db(value)
                phase = complex2phase(value)
                # add the value to the list
                rl[(i,j)].append((dbValue, phase))
                cpRl[(i,j)].append(value)
        return rl, cpRl

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "Return Loss"