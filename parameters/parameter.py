import numpy as np
import matplotlib.pyplot as plt
from bisect import bisect_left
from limits.Limit import Limit
from parameters.plot import ParameterPlot
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
        self._worstMargin = (dict(), None)
        self._worstValue = (dict(), None)
        self._plot = ParameterPlot(self)

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

    def getDataSeries(self):
        return self._series

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter

    def getLimit(self):
        return self._limit

    def setLimit(self, limit):
        self._limit = deepcopy(limit)
        self._plot.setLimit(self._limit)
        self._worstMargin = (dict(), None)
        self._worstValue = (dict(), None)

    def getPorts(self):
        return self._ports

    def getPlot(self):
        return self._plot

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
                    if v > l:
                        passed = False
                    worst[pair] = v, f, l, abs(worstMargin)
            self._worstMargin = worst, passed
            return self._worstMargin
        return (dict(), None)

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
                    worstVal = max(vals)
                    index = vals.index(worstVal)
                    m, f = margins[index], freqs[index]
                    l = limit[f]
                    if l and worstVal > l:
                        passed = False
                    if m:
                        m = abs(m)
                    worst[pair] = worstVal, f, l, m
            self._worstValue = worst, passed
            return self._worstValue
        return (dict(), None)

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
        self._worstMargin = (dict(), None)
        self._worstValue = (dict(), None)
        self._plot = ParameterPlot(self)
        
    def computePairs(self, ports):
        """
        Compute the pairs of this parameter.

        :returns: a set of ordered pairs
        """
        raise NotImplementedError

    def getPairs(self):
        return self._ports
