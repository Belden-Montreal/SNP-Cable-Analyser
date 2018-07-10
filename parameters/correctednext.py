from parameters.next import NEXT
from parameters.parameter import complex2db, takeClosest
import numpy as np

class CorrectedNEXT(NEXT):

    def __init__(self, ports, freq, matrices, nextDelay):
        self._nextDelay = nextDelay
        super(CorrectedNEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        nextDelay = self._nextDelay.getParameter()
        pnext,cpnext = super(CorrectedNEXT, self).computeParameter()
        correctedNext = dict()
        cpCorrectedNext = dict()
        for i,j in pnext:
            correctedNext[(i,j)] = list()
            cpCorrectedNext[(i,j)] = list()
            for f,freq in enumerate(self._freq):
                #phase correction
                _, phase = pnext[(i,j)][f]
                amp = np.abs(cpnext[(i,j)][f])
                if i > j:
                    pair = (j,i)
                else:
                    pair = (i,j)
                correctedPhase = phase + 360*freq*nextDelay[pair]
                re = amp*np.cos(correctedPhase*np.pi/180)
                im = amp*np.sin(correctedPhase*np.pi/180)
                correctedNextVal = complex(re,im)
                if pair == (0,2) and f == takeClosest(100, self._freq):
                    print(self._ports[(0,2)])
                    print(phase)
                    print(amp)
                    print(correctedPhase)
                    print(correctedNextVal)
                    print(20*np.log10(np.sqrt(re**2+im**2)))
                cpCorrectedNext[(i,j)].append(correctedNextVal)
                correctedNext[(i,j)].append((complex2db(correctedNextVal), correctedPhase))
        return correctedNext, cpCorrectedNext

    def getNEXTDelay(self):
        return self._nextDelay

    def getName(self):
        return "CNEXT"

    def getParameter(self):
        return self._parameter

    def getComplexParameter(self):
        return self._complexParameter