import numpy as np

def complex2db(self, value, degree=True):
    return 20*np.log10(np.abs(value))

def complex2phase(self, value, degree=True):
    return np.angle(value, degree)

class Parameter(object):
    def __init__(self, ports, freq, matrices, z=True):
        self._ports = ports
        self._freq = freq
        self._matrices = matrices
        self._complex = z
        self._parameter = self.computeParameter()

    def computeParameter(self):
        raise NotImplementedError

    def getParameter(self):
        return self._parameter
