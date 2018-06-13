import numpy as np
from limits.Limit import Limit

def complex2db(value, degree=True):
    return 20*np.log10(np.abs(value))

def complex2phase(value, degree=True):
    return np.angle(value, degree)

def order(i,j):
    if i < j:
        return (i,j)
    else:
        return (j,i)

class Parameter(object):
    def __init__(self, ports, freq, matrices):
        self._ports = ports
        self._freq = freq
        self._matrices = matrices
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = Limit(self._parameter)

    def computeParameter(self):
        raise NotImplementedError

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter

    def getLimit(self):
        return self._limit

    def getWorstMargin(self):
        raise NotImplementedError

    def getWorstValue(self):
        raise NotImplementedError

class PairedParameter(Parameter):
    def __init__(self, ports, freq, matrices):
        self._ports = ports
        self._freq = freq
        self._matrices = matrices
        self._pairs = self.computePairs()
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = Limit(self._parameter)

    def computePairs(self):
        """
        Compute the pairs of this parameter.

        :returns: a set of ordered pairs
        """
        raise NotImplemented

    def getPairs(self):
        return self._pairs


