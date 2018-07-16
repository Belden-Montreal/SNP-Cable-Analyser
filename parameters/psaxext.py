from parameters.parameter import Parameter, diffDiffMatrix
import numpy as np

class PSAXEXT(Parameter):
    '''
        PSAXEXT represents both the PSANEXT and the PSAFEXT
        It is calculated by taking either the ANEXT or the AFEXT of every disturber pair on every pair of the victim and computing the powersum
    '''
    def __init__(self, ports, freq, matrices, axextd):
        self._axextd = axextd
        self._ports = dict()
        for port, (name, isRemote) in ports.items():
            if not isRemote:
                self._ports[port] = (name, isRemote)
        super(PSAXEXT, self).__init__(self._ports, freq, matrices)

    def computeParameter(self):
        
        psaxext = dict()
        cpPsaxext = dict()
        for port in self._ports:
            psaxext[port] = list()
            cpPsaxext[port] = list()

        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                ps = 10.0*np.log10(np.sum([
                    np.sum([
                        10**(disturber.getParameter()[key][f][0]/10)
                    for key in disturber.getParameter().keys() if (key[0] == port)])
                for disturber in self._axextd]))
                psaxext[port].append((ps, 0))

                # cp = np.sum([
                #     np.sum([
                #         disturber.getComplexParameter()[key][f]
                #     for key in disturber.getComplexParameter().keys() if (key[0] == port)])
                # for disturber in self._axextd])
                
                cpPsaxext[port].append(0)
        return psaxext,cpPsaxext

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getAXEXT(self):
        return self._axextd

    def getName(self):
        return "PSAXEXT"

    def recalculate(self, axextd):
        self._axextd = axextd
        (self._parameter, self._complexParameter) = self.computeParameter()
        