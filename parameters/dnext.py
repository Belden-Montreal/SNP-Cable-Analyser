from parameters.parameter import complex2phase, complex2db
from parameters.correctednext import CorrectedNEXT
import numpy as np

class DNEXT(CorrectedNEXT):
    '''
        DNEXT is the de-embedded NEXT Loss
    '''
    def __init__(self, ports, freq, matrices, plugNextDelay, plugNext):
        self._plugNext = plugNext
        super(DNEXT, self).__init__(ports, freq, matrices, plugNextDelay)
    
    def computeParameter(self):
        
        cpDnext = dict()
        dnext = dict()
        _, cpCorrectedNext = super(DNEXT, self).computeParameter()
        plugNext = self._plugNext.getComplexParameter()
        for port in self._ports:
            dnext[port] = list()
            cpDnext[port] = list()

        for f,_ in enumerate(self._freq):
            for port in self._ports:
                
                dnext[port].append(complex2db(cpCorrectedNext[port][f] - plugNext[port][f]))
                cpDnext[port].append(cpCorrectedNext[port][f] - plugNext[port][f])
        return dnext,cpDnext

    def getPlugNEXT(self):
        return self._plugNext

    def getName(self):
        return "DNEXT"