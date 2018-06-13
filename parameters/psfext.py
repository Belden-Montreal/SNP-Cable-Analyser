from parameters.parameter import Parameter
from parameters.fext import Fext
import numpy as np
class PsFext(Parameter):
    def computeParameter(self):
        psfext = dict()
        for _,port in self._ports.items():
            psfext[port] = list()
        fext = Fext(self._ports, self._freq, self._matrices).getParameter()
        ports = fext.keys()

        for (f,_) in enumerate(self._freq):
            for (_,port) in self._ports.items():
                ps = 10.0*np.log10(np.sum([10**(fext[key][f]/10) for key in ports if (key.split("-")[0] == port)]))
                psfext[port].append(ps)
        return psfext,_