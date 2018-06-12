from parameters.parameter import Parameter, complex2phase
from parameters.returnloss import ReturnLoss

class PropagationDelay(Parameter):
    def computeParameter(self):
        # initialize the dictionary for each port
        pd = dict()
        for _,port in self._ports.items():
                pd[port] = list()

        # extract the return loss for calculations
        rl = ReturnLoss(self._ports, self._freq, self._matrices).getComplexParameter()

        # extract the propagation delay from the return loss
        for (f,_) in enumerate(self._freq):
            for (_,port) in self._ports.items():
                delay = 0.0
                if f < len(self._freq)-1: #if not last frequency
                    phase1 = complex2phase(rl[port][f])
                    phase2 = complex2phase(rl[port][f+1])

                    dp = phase2 - phase1
                    df = self._freq[f+1] - self._freq[f]
                    delay = -1/360.0 * dp/df
                    if delay < 0.0:
                        if f > 0:
                            delay = pd[port][f-1]
                        else:
                            delay = 0.0
                else:
                    delay = pd[port][f-1]
                pd[port].append(delay)


        return pd,_