from parameters.parameter import Parameter
from parameters.fext import Fext
from parameters.insertionloss import InsertionLoss

class Acrf(Parameter):
    def computeParameter(self):
        '''
        ACRF is calculated using the following formula : 

        ACRF_k = FEXT_k - IL_k
        '''
        acrf = dict()
        fext = Fext(self._ports, self._freq, self._matrices).getParameter()
        il = InsertionLoss(self._ports, self._freq, self._matrices, full=True).getParameter()
        ports = fext.keys()
        for port in ports:
            acrf[port] = list()
        for (f,_) in enumerate(self._freq):
            for port in ports:
                ilPort = port.split("-")[0]
                acrf[port].append(fext[port][f]-il[ilPort][f])
        return acrf,_