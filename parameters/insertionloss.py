from parameters.parameter import PairedParameter, complex2db, diffDiffMatrix

class InsertionLoss(PairedParameter):
    '''
        Example of Insertion Loss with 4 wires
        For non-full measurement, only take the top right values (1 and 2 in this case)
        
             1 2 3 4
        1  [ _ _ 1 _ ] 
        2  [ _ _ _ 2 ] 
        3  [ 3 _ _ _ ] 
        4  [ _ 4 _ _ ] 
        
        
    ''' 

    def computePairs(self, ports):
        pairs = dict()
        for i in range(len(ports)//2):
            port1, isRemote1 = ports[i]
            port2, isRemote2 = ports[i+len(ports)//2]

            if isRemote1 is not isRemote2:
                pairs[(i, i+len(ports)//2)] = (port1+"-"+port2, isRemote1)
                pairs[(i+len(ports)//2, i)] = (port2+"-"+port1, isRemote2)

        return pairs

    def computeParameter(self):
        # initialize the dictionary for each port
        il = dict()
        cpIl = dict()
        for port in self._ports:
            il[port] = list()
            cpIl[port] = list()

        # extract the insertion loss in all matrices
        for (f,_) in enumerate(self._freq):
            for (i,j) in self._ports:
                # get the value
                value = self._matrices[f, i, j]
                il[(i,j)].append(complex2db(value))
                cpIl[(i,j)].append(value)

        return il, cpIl

    def getParameter(self, full=True):
        if not full:
            return {(i,j): self._parameter[(i,j)] for (i,j) in self._parameter if i < j}
        else:
            return self._parameter

    def getComplexParameter(self, full=True):
        if not full:
            return {(i,j): self._complexParameter[(i,j)] for (i,j) in self._complexParameter if i < j}
        else:
            return self._complexParameter

    def getMargins(self, values, limit):
        margins = list()
        freqs = list()
        vals = list()
        for i,value in enumerate(values):
            if self._freq[i] in limit:
                margins.append(value-limit[self._freq[i]])
                freqs.append(self._freq[i])
                vals.append(value)
        return margins, freqs, vals

    def getWorstMargin(self):
        if len(self._worstMargin[0]):
            return self._worstMargin
        if self._limit is None:
            return (None, None)
        limit = self._limit.evaluateDict({'f': self._freq}, len(self._freq), neg=True)
        passed = True
        worst = dict()
        if limit:
            for pair,values in self._parameter.items():
                margins, freqs, vals = self.getMargins(values, limit)
                if len(margins):
                    worstMargin = min(margins)
                    index = margins.index(worstMargin)
                    v, f = vals[index], freqs[index]
                    l = limit[f]
                    if v < l:
                        passed = False
                    worst[pair] = v, f, l, abs(worstMargin)
            self._worstMargin = worst, passed
            return self._worstMargin

    def getWorstValue(self):
        if len(self._worstValue[0]):
            return self._worstValue
        if self._limit is None:
            return (None, None)
        limit = self._limit.evaluateDict({'f': self._freq}, len(self._freq), neg=True)
        passed = True
        worst = dict()
        if limit:
            for pair,values in self._parameter.items():
                margins, freqs, vals = self.getMargins(values, limit)
                if len(vals):
                    worstVal = min(vals)
                    index = vals.index(worstVal)
                    m, f = margins[index], freqs[index]
                    l = limit[f]
                    if worstVal < l:
                        passed = False
                    worst[pair] = worstVal, f, l, abs(m)
            self._worstValue = worst, passed
            return self._worstValue
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "Insertion Loss"
