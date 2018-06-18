from parameters.parameter import Parameter, complex2phase

class PropagationDelay(Parameter):
    '''
        Propagation delay is calculated by taking the numerical derivative of the return loss phase:
        Delay = -1/360 * dp/df

        where dp = phase[f2] - phase[f1], df = f2 - f1
        and phase[f] is the phase of the return loss at a given frequency
        
    '''

    def __init__(self, ports, freq, matrices, rl):
        self._rl = rl
        super(PropagationDelay, self).__init__(ports, freq, matrices)

    def computeParameter(self):
        # initialize the dictionary for each port
        pd = dict()
        for port in self._ports:
                pd[port] = list()

        # extract the return loss for calculations
        dbRl = self._rl.getComplexParameter()

        # extract the propagation delay from the return loss
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                delay = 0.0
                if f < len(self._freq)-1: #if not last frequency
                    phase1 = complex2phase(dbRl[port][f])
                    phase2 = complex2phase(dbRl[port][f+1])

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

    def chooseMatrices(self, matrices):
        return None

    def getName(self):
        return "Propagation Delay"