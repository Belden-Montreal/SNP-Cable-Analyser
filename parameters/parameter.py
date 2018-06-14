import numpy as np
from limits.Limit import Limit

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
    return 20*np.log10(np.abs(value))

def complex2phase(value, degree=True):
    return np.angle(value, degree)

def order(i,j):
    if i < j:
        return (i,j)
    else:
        return (j,i)

class Parameter(object):
    def __init__(self, ports, freq, mixedModeMatrices):
        self._ports = ports
        self._freq = freq
        self._matrices = self.chooseMatrices(mixedModeMatrices)
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = Limit(self._parameter)

    def chooseMatrices(self, mixedModeMatrices):
        raise NotImplementedError

    def computeParameter(self):
        raise NotImplementedError

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter

    def getLimit(self):
        return self._limit

    def setLimit(self, limit):
        self._limit = limit

    def getWorstMargin(self):
        raise NotImplementedError

    def getWorstValue(self):
        raise NotImplementedError

    def getNumPorts(self):
        return len(self._ports)

class PairedParameter(Parameter):
    def __init__(self, ports, freq, mixedModeMatrices):
        self._ports = ports
        self._freq = freq
        self._matrices = self.chooseMatrices(mixedModeMatrices)
        self._pairs = self.computePairs()
        (self._parameter, self._complexParameter) = self.computeParameter()
        self._limit = Limit(self._parameter)

    def computePairs(self):
        """
        Compute the pairs of this parameter.

        :returns: a set of ordered pairs
        """
        raise NotImplementedError

    def getPairs(self):
        return self._pairs


