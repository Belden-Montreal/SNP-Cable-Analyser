from parameters.next import NEXT
from parameters.parameter import complex2db
import numpy as np

class CorrectedNEXT(NEXT):

    def __init__(self, ports, freq, matrices, nextDelay):
        self._nextDelay = nextDelay
        super(CorrectedNEXT, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        nextDelay = self._nextDelay.getParameter()
        pnext, cpnext = super(CorrectedNEXT, self).computeParameter()
        correctedNext = dict()
        cpCorrectedNext = dict()
        for i,j in pnext:
            correctedNext[(i,j)] = list()
            cpCorrectedNext[(i,j)] = list()
            for f,freq in enumerate(self._freq):
                #phase correction
                phase = np.angle(cpnext[(i,j)][f])
                if i > j:
                    pair = (j,i)
                else:
                    pair = (i,j)
                correctedPhase = phase + 360*freq*nextDelay[pair]

                amp = np.abs(cpnext[(i,j)][f])

                re = amp*np.cos(correctedPhase*np.pi/180)
                im = amp*np.sin(correctedPhase*np.pi/180)
                correctedNextVal = complex(re,im)
                cpCorrectedNext[(i,j)].append(correctedNextVal)
                correctedNext[(i,j)].append(complex2db(correctedNextVal))
        return correctedNext, cpCorrectedNext

    def getNEXTDelay(self):
        return self._nextDelay

    def getName(self):
        return "CNEXT"