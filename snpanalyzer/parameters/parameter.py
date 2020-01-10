import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left
from snpanalyzer.limits.Limit import Limit

from snpanalyzer.parameters.dataserie import GenericDataSerie

from copy import deepcopy

def diffDiffMatrix(matrices):
    halfway = matrices[0].shape[0]//2
    return matrices[:,:halfway,:halfway]

def diffComMatrix(matrices):
    halfway = matrices[0].shape[0]//2
    return matrices[:,:halfway,halfway:]

def comDiffMatrix(matrices):
    halfway = matrices[0].shape[0]//2
    return matrices[:,halfway:,:halfway]

def comComMatrix(matrices):
    halfway = matrices[0].shape[0]//2
    return matrices[:,halfway:,halfway:]

def complex2db(value, degree=True):
    if value == 0:
        return -np.Infinity
    return 20*np.log10(np.abs(value))

def complex2phase(value, degree=True):
    return np.angle(value, degree)

def order(i,j):
    if i < j:
        return (i,j)
    else:
        return (j,i)

def takeClosest(x, numbers):
        pos = bisect_left(numbers, x)
        if pos == 0:
            return 0
        if pos == len(numbers):
            return pos-1
        before = numbers[pos-1]
        after = numbers[pos]
        if after - x > x - before:
            return pos-1
        return pos

class Parameter(object):
    def __init__(self, ports, freq, mixedModeMatrices):
        self._visible = True
        self._ports = ports
        self._freq = freq
        self._matrices = self.chooseMatrices(mixedModeMatrices)

        self._series = self.computeDataSeries()
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = None
        self._averageLimit = None
        self._worstMargin = DataAnalysis()
        self._worstValue = DataAnalysis()

    @staticmethod
    def getType():
        raise NotImplementedError

    @staticmethod
    def register(parameters):
        raise NotImplementedError

    @staticmethod
    def getAvailableFormats():
        raise NotImplementedError

    def chooseMatrices(self, mixedModeMatrices):
        raise NotImplementedError

    def computeDataSeries(self):
        raise NotImplementedError

    def computeParameter(self):
        raise NotImplementedError

    def _getYData(self, identifier):
        raise NotImplementedError

    def getDataSeries(self, limit = False):
        # print("Getting Data Series (Parameters")
        if limit:
            try:
                limitDataSeries = GenericDataSerie(name="Limit", data=self.getLimit() )
                self._series.add(limitDataSeries)
            except:
                pass
        return self._series

    def getParameter(self,limit=False):
        if limit:
            return {**self._parameter, **{GenericDataSerie(name="Limit", data=self.getLimit()) : [self.getLimit()]}}
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter

    def getLimit(self):

        return self._limit
 
    def setLimit(self, limit):
        self._limit = deepcopy(limit)
        self._worstMargin = DataAnalysis()
        self._worstValue = DataAnalysis()

    def getAverageLimit(self): 
        return self._averageLimit

    def setAverageLimit(self, limit):
        self._averageLimit = limit

    def getPorts(self):
        return self._ports

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
                    if v > l:
                        self._worstMargin.passed = False
                    self._worstMargin.setPair(pair, PairValues(v, f, l, worstMargin))
            return self._worstMargin
        return DataAnalysis()

    def getMargins(self, values, limit):
        margins = list()
        freqs = list()
        vals = list()
        for i,(value,_) in enumerate(values):
            if self._freq[i] in limit:
                if limit[self._freq[i]]:
                    margins.append(limit[self._freq[i]]-value)
                else:
                    margins.append(None)
                freqs.append(self._freq[i])
                vals.append(value)
        return margins, freqs, vals

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
                worstVal = max(vals)
                index = vals.index(worstVal)
                m, f = margins[index], freqs[index]
                l = limit[f]
                if l and worstVal > l:
                    self._worstValue.passed = False
                if m:
                    m = abs(m)
                self._worstValue.setPair(pair, PairValues(worstVal, f, l, m))
        return self._worstValue

    def getNumPorts(self):
        return len(self._ports)

    def getName(self):
        raise NotImplementedError

    def getDescription(self):
        raise NotImplementedError

    def getFrequencies(self):
        return self._freq

    def visible(self):
        return self._visible

class PairedParameter(Parameter):
    def __init__(self, ports, freq, mixedModeMatrices):
        self._visible = True
        self._freq = freq
        self._matrices = self.chooseMatrices(mixedModeMatrices)
        self._ports = ports
        self._pairs = self.computePairs(ports)
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = None
        self._worstMargin = DataAnalysis()
        self._worstValue = DataAnalysis()
        
    def computePairs(self, ports):
        """
        Compute the pairs of this parameter.

        :returns: a set of ordered pairs
        """
        raise NotImplementedError

    def getPairs(self):
        return self._ports

class PairValues(object):
    def __init__(self, value, freq, limit, margin):
        self._value = value
        self._freq = freq
        self._limit = limit
        self._margin = margin

    @property
    def value(self):
        return self._value

    @property
    def freq(self):
        return self._freq

    @property
    def limit(self):
        return self._limit

    @property
    def margin(self):
        return self._margin

class DataAnalysis(object):
    def __init__(self):
        self._passed = True
        self._pairs = dict()
    
    def hasData(self):
        return len(self._pairs) > 0

    def setPair(self, pair, values):
        self._pairs[pair] = values

    @property
    def passed(self):
        return self._passed

    @passed.setter
    def passed(self, ppassed):
        self._passed = ppassed

    @property
    def pairs(self):
        return self._pairs

    def getWorstPairValue(self):
        maximum = -float('inf')
        worstPair = None
        for pair, values in self.pairs.items():
            if maximum < values.value:
                maximum = values.value
                worstPair = pair
        return worstPair

    def getWorstPairMargin(self):
        minimum = float('inf')
        worstPair = None
        for pair, values in self.pairs.items():
            if minimum > values.margin:
                minimum = values.margin
                worstPair = pair
        return worstPair