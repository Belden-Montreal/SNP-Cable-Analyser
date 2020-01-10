from snpanalyzer.parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix, DataAnalysis, PairValues
from snpanalyzer.parameters.dataserie import WireDataSerie
from snpanalyzer.parameters.type import ParameterType
from snpanalyzer.analysis.format import DataFormat

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

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

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
        if len(self._worstMargin.pairs):
            return self._worstMargin
        if self._limit is None:
            return DataAnalysis()
        limit = self._limit.evaluateDict({'f': self._freq}, len(self._freq), neg=True)
        self._worstMargin = DataAnalysis()
        if limit:
            for pair,values in self._parameter.items():
                margins, freqs, vals = self.getMargins(values, limit)
                if len(margins):
                    worstMargin = min(margins)
                    index = margins.index(worstMargin)
                    v, f = vals[index], freqs[index]
                    l = limit[f]
                    if v < l:
                        self._worstMargin.passed = False
                    self._worstMargin.setPair(pair, PairValues(v, f, l, worstMargin))
            return self._worstMargin
        return DataAnalysis()

    def getWorstValue(self):
        if len(self._worstValue.pairs):
            return self._worstValue
        limit = dict()
        if self._limit is not None:
            limit = self._limit.evaluateDict({'f': self._freq}, len(self._freq), neg=True)
        if len(limit) == 0:
            limit = {freq: None for freq in self._freq}
        self._worstValue = DataAnalysis()
        for pair,values in self._parameter.items():
            margins, freqs, vals = self.getMargins(values, limit)
            if len(vals):
                worstVal = min(vals)
                index = vals.index(worstVal)
                m, f = margins[index], freqs[index]
                l = limit[f]
                if l and worstVal < l:
                    self._worstValue.passed = False
                if m:
                    m = abs(m)
                self._worstValue.setPair(pair, PairValues(worstVal, f, l, m))
        return self._worstValue
    
    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "Insertion Loss"
