from parameters.parameter import Parameter
from parameters.psfext import PsFext
from parameters.insertionloss import InsertionLoss

class PsAcrf(Parameter):
    def computeParameter(self):
        '''
        PSACRF is calculated using the following formula:
        PSACRF_k = PSFEXT_k - IL_k
        
        where PSFEXT_k is the PSFEXT on wire k and IL_k is the Insertion Loss on wire k
        '''
        psacrf = dict()
        psfext = PsFext(self._ports, self._freq, self._matrices).getParameter()
        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True).getParameter()

        for _,port in self._ports.items():
            psacrf[port] = list()

        for f,_ in enumerate(self._freq):
            for _,port in self._ports.items():
                psacrf[port].append(psfext[port][f]-il[port][f])
        return psacrf,_