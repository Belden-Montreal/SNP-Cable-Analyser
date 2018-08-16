from parameters.parameter import Parameter, complex2db, complex2phase
from parameters.case_plot import CasePlot
from parameters.dataserie import PortOrderedPairDataSerie
from parameters.type import ParameterType

import numpy as np
import itertools

class Case(Parameter):
    def __init__(self, ports, freq, matrices, jackVector, cnext, cases):
        self._jackVector = jackVector
        self._cases = cases
        self._cnext = cnext
        super(Case, self).__init__(ports, freq, matrices)
        self._plot = CasePlot(self)

    @staticmethod
    def getType():
        return ParameterType.CASE

    @staticmethod
    def register(parameters):
        return lambda c, f, m: Case(c, f, m,
            parameters(ParameterType.DNEXT),
            parameters(ParameterType.PC_NEXT),
            parameters(ParameterType.CASES),
        )

    def computeDataSeries(self):
        series = set()

        ports = self._ports.getPorts()
        for (i,j) in itertools.product(ports, ports):
            if i is j:
                continue
            series.add(PortOrderedPairDataSerie(i, j))
            
        return series

    def computeParameter(self):
        dbReembedded = {serie: dict() for serie in self._series}
        cpReembedded = {serie: dict() for serie in self._series}

        for serie in self._series:
            cases = filter(lambda case: case[1][0] == serie.getPortIndices() and case[1][1] is not None, self._cases.items())
            
            for (index,_) in cases:
                dbReembedded[serie][index] = list()
                cpReembedded[serie][index] = list()

        jackVector = self._jackVector.getComplexParameter()
        cnext = self._cnext.getComplexParameter()
        for (f,freq) in enumerate(self._freq):
            for serie in self._series:
                cases = [x for x in self._cases.items() if x[1][0] == serie.getPortIndices() and x[1][1] is not None]
                for (n, (_, case)) in cases:
                    plug = case(freq, cnext[serie][f])
                    dbPlug = plug[0]
                    phasePlug = plug[1]
                    
                    amp = 10**(dbPlug/20)
                    
                    re = amp*np.cos(phasePlug*np.pi/180)
                    im = amp*np.sin(phasePlug*np.pi/180)
                    cPlug = complex(re, im)
                    reembed = cPlug + jackVector[serie][f]
                    cpReembedded[serie][n].append(reembed)
                    dbReembedded[serie][n].append((complex2db(reembed), complex2phase(reembed)))

        return (dbReembedded, cpReembedded)

    def getMargins(self, values, limit):
        margins = list()
        freqs = list()
        vals = list()
        for i,(value) in enumerate(values):
            if self._freq[i] in limit:
                if limit[self._freq[i]]:
                    margins.append(limit[self._freq[i]]-value)
                else:
                    margins.append(None)
                freqs.append(self._freq[i])
                vals.append(value)
        return margins, freqs, vals
    def chooseMatrices(self, matrices):
        return None

    def getName(self):
        return "Case"

    def getCases(self):
        return self._cases

    def getDNEXT(self):
        return self._jackVector

    def getCNEXT(self):
        return self._cnext

class ReverseCase(Case):
    def __init__(self, ports, freq, matrices, reverseJackVector, cnext, cases):
        super(ReverseCase, self).__init__(ports, freq, matrices, reverseJackVector, cnext, cases)

    @staticmethod
    def getType():
        return ParameterType.RCASE

    @staticmethod
    def register(parameters):
        return lambda c, f, m: Case(c, f, m,
            parameters(ParameterType.RDNEXT),
            parameters(ParameterType.PC_NEXT),
            parameters(ParameterType.CASES),
        )