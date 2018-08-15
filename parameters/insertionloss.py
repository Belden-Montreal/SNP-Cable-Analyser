from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.dataserie import WireDataSerie
from parameters.type import ParameterType

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
    def __init__(self, ports, freq, matrices, forward=True, reverse=True):
        self._forward = forward
        self._reverse = reverse
        super(InsertionLoss, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.IL

    @staticmethod
    def register(parameters, forward=True, reverse=True):
        return lambda c, f, m: InsertionLoss(c, f, m, forward=forward, reverse=reverse)

    def computeDataSeries(self):
        series = set()
        if self._forward:
            wires = self._ports.getFowardWires()
            [series.add(WireDataSerie(wire)) for wire in wires]
        if self._reverse:
            wires = self._ports.getReversedWires()
            [series.add(WireDataSerie(wire)) for wire in wires]
        return series

    def computeParameter(self):
        # initialize the dictionary for each port
        dbIL = {serie: list() for serie in self._series}
        cpIL = {serie: list() for serie in self._series}

        # extract the insertion loss in all matrices
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                (i,j) = serie.getPortIndices()

                cpValue = self._matrices[f, i, j]
                dbValue = (complex2db(cpValue), complex2phase(cpValue))

                cpIL[serie].append(cpValue)
                dbIL[serie].append(dbValue)

        return (dbIL, cpIL)

    def getMargins(self, values, limit):
        margins = list()
        freqs = list()
        vals = list()
        for i,(value,_) in enumerate(values):
            if self._freq[i] in limit:
                if limit[self._freq[i]]:
                    margins.append(value-limit[self._freq[i]])
                else:
                    margins.append(None)
                freqs.append(self._freq[i])
                vals.append(value)
        return margins, freqs, vals

    def getWorstMargin(self):
        if len(self._worstMargin[0]):
            return self._worstMargin
        if self._limit is None:
            return (dict(), None)
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
        return (dict(), None)

    def getWorstValue(self):
        if len(self._worstValue[0]):
            return self._worstValue
        
        if self._limit is not None:
            limit = self._limit.evaluateDict({'f': self._freq}, len(self._freq), neg=True)
        else:
            limit = {freq: None for freq in self._freq}
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
                    if l and worstVal < l:
                        passed = False
                    if m:
                        m = abs(m)
                    worst[pair] = worstVal, f, l, m
            self._worstValue = worst, passed
            return self._worstValue
        return (dict(), None)
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "Insertion Loss"
