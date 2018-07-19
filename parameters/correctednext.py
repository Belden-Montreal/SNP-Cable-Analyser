from parameters.next import NEXT
from parameters.parameter import complex2db, takeClosest
from parameters.type import ParameterType

import numpy as np

class CorrectedNEXT(NEXT):
    def __init__(self, ports, freq, matrices, nextDelay):
        self._nextDelay = nextDelay
        super(CorrectedNEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.CORRECTED_NEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: CorrectedNEXT(c, f, m,
            parameters(ParameterType.NEXT_DELAY)
        )

    def computeParameter(self):
        dbCorrectedNEXT = {serie: list() for serie in self._series}
        cpCorrectedNEXT = {serie: list() for serie in self._series}

        NEXTDelay = self._nextDelay.getParameter()
        (dbNEXT,cpNEXT) = super(CorrectedNEXT, self).computeParameter()

        for serie in self._series:
            for (f,freq) in enumerate(self._freq):
                # phase correction
                _, phase = dbNEXT[serie][f]
                amp = np.abs(cpNEXT[serie][f])
                correctedPhase = phase + 360*freq*NEXTDelay[serie]

                # apply this correction to the complex parameter
                re = amp*np.cos(correctedPhase*np.pi/180)
                im = amp*np.sin(correctedPhase*np.pi/180)
                cpCorrectedNEXTVal = complex(re,im)

                # crate the magnitude/phase value
                dbCorrectedNEXTVal = (amp, correctedPhase)

                # add the values into the result lists
                cpCorrectedNEXT[serie].append(cpCorrectedNEXTVal)
                dbCorrectedNEXT[serie].append(dbCorrectedNEXTVal)

        return (dbCorrectedNEXT, cpCorrectedNEXT)

    def recalculate(self, nextDelay):
        self._nextDelay = nextDelay
        (self._parameter, self._complexParameter) = self.computeParameter()

    def getNEXTDelay(self):
        return self._nextDelay

    def getName(self):
        return "CNEXT"

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter
