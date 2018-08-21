from parameters.parameter import complex2phase, complex2db
from parameters.correctednext import CorrectedNEXT
from parameters.type import ParameterType

import numpy as np

class DNEXT(CorrectedNEXT):
    '''
    DNEXT is the de-embedded NEXT Loss.
    '''
    def __init__(self, ports, freq, matrices, plugNextDelay, plugNext):
        self._plugNext = plugNext
        super(DNEXT, self).__init__(ports, freq, matrices, plugNextDelay)
    
    @staticmethod
    def getType():
        return ParameterType.DNEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: DNEXT(c, f, m,
            parameters(ParameterType.NEXT_DELAY),
            parameters(ParameterType.PC_NEXT)
        )

    def computeParameter(self):
        # create the series
        cpDNEXT = {serie: list() for serie in self._series}
        dbDNEXT = {serie: list() for serie in self._series}

        # get the computed data from the superclass
        (_, cpCorrectedNEXT) = super(DNEXT, self).computeParameter()

        # get the plug's NEXT
        cpPlugNEXT = self._plugNext.getComplexParameter()

        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                # compute magnitude/phase
                magnitude = complex2db(cpCorrectedNEXT[serie][f] - cpPlugNEXT[serie][f])
                phase = complex2phase(cpCorrectedNEXT[serie][f] - cpPlugNEXT[serie][f])
                dbValue = (magnitude, phase)

                # compute the complex value
                cpValue = cpCorrectedNEXT[serie][f] - cpPlugNEXT[serie][f]

                # add the values into the lists
                dbDNEXT[serie].append(dbValue)
                cpDNEXT[serie].append(cpValue)

        return (dbDNEXT,cpDNEXT)

    def getPlugNEXT(self):
        return self._plugNext

    def getName(self):
        return "DNEXT"

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter

class ReverseDNEXT(DNEXT):
    def __init__(self, ports, freq, matrices, jackNextDelay, plugNext):
        super(ReverseDNEXT, self).__init__(ports, freq, matrices, jackNextDelay, plugNext)
    
    @staticmethod
    def getType():
        return ParameterType.RDNEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: DNEXT(c, f, m,
            parameters(ParameterType.JACK_NEXT_DELAY),
            parameters(ParameterType.PC_NEXT)
        )
