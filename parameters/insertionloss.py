from parameters.parameter import Parameter, complex2db, diffDiffMatrix

class InsertionLoss(Parameter):
    '''
        Example of Insertion Loss with 4 wires
        For non-full measurement, only take the top right values (1 and 2 in this case)
        
             1 2 3 4
        1  [ _ _ 1 _ ] 
        2  [ _ _ _ 2 ] 
        3  [ 3 _ _ _ ] 
        4  [ _ 4 _ _ ] 
        
        
    ''' 

    def computeParameter(self):
        # initialize the dictionary for each port
        il = dict()
        cpIl = dict()
        for port in self._ports:
            il[port] = list()
            cpIl[port] = list()

        # extract the insertion loss in all matrices
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                # get the value
                if port < len(self._ports)//2:
                    topRight = self._matrices[f, port, port+len(self._ports)//2]
                    il[port].append(complex2db(topRight))
                    cpIl[port].append(topRight)

                    bottomLeft = self._matrices[f, port+len(self._ports)//2, port]
                    il[port+len(self._ports)//2].append(complex2db(bottomLeft))
                    cpIl[port+len(self._ports)//2].append(bottomLeft)

        return il, cpIl

    def getParameter(self, full=False):
        if not full:
            return {k: self._parameter[k] for k in sorted(self._parameter)[:len(self._ports)//2]}
        else:
            return self._parameter

    def getComplexParameter(self, full=False):
        if not full:
            return {k: self._complexParameter[k] for k in sorted(self._complexParameter)[:len(self._ports)//2]}
        else:
            return self._complexParameter

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)
