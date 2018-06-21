from parameters.parameter import PairedParameter, complex2db
import numpy as np

class Case(PairedParameter):

    def __init__(self, ports, freq, matrices, dnext, cnext, cases):
        self._dnext = dnext
        self._cases = cases
        self._cnext = cnext
        super(Case, self).__init__(ports, freq, matrices)

    def computePairs(self, ports):
        pairs = dict()
        for i in range(0, len(ports)):
            for j in range(0, len(ports)):
                if i >= j:
                    continue

                port1 = i
                port2 = j
                pairs[(port1, port2)] = ports[port1]+"-"+ports[port2]

        return pairs

    def computeParameter(self):
        reembedded = dict()
        cpReembedded = dict()
        for port in self._ports:
            cpReembedded[port] = dict()
            reembedded[port] = dict()
            cases  = filter(lambda case: case[1][0]==port, self._cases.items())
            for n,_ in cases:
                cpReembedded[port][n] = list()
                reembedded[port][n] = list()

        dnext = self._dnext.getComplexParameter()
        cnext = self._cnext.getComplexParameter()
        for f,freq in enumerate(self._freq):
            for port in self._ports:
                cases = [x for x in self._cases.items() if x[1][0] == port]
                for n, (_, case) in cases:
                    plug = case(freq, cnext[port][f])
                    dbPlug = plug[0]
                    phasePlug = plug[1]
                    
                    amp = 10**(dbPlug/20)
                    
                    re = amp*np.cos(phasePlug*np.pi/180)
                    im = amp*np.sin(phasePlug*np.pi/180)
                    cPlug = complex(re, im)
                    reembed = cPlug + dnext[port][f]
                    cpReembedded[port][n].append(reembed)
                    reembedded[port][n].append(complex2db(reembed))

        return reembedded, cpReembedded

    def chooseMatrices(self, matrices):
        return None

    def getName(self):
        return "Case"

    def getCases(self):
        return self._cases

    def getDNEXT(self):
        return self._dnext

    def getCNEXT(self):
        return self._cnext