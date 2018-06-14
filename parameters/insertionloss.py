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
