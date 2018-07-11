from parameters.parameter import Parameter, complex2phase
from parameters.dataserie import PortDataSerie

class PropagationDelay(Parameter):
    '''
    Propagation delay is calculated by taking the numerical derivative of the
    return loss phase:

        delay = -1/360 * dp/df

    where dp = phase[f2] - phase[f1], df = f2 - f1 and phase[f] is the phase
    of the return loss at a given frequency
    '''

    def __init__(self, ports, freq, matrices, rl):
        self._rl = rl
        super(PropagationDelay, self).__init__(ports, freq, matrices)

    def computeDataSeries(self):
        return {PortDataSerie(port) for port in self._ports.getPorts()}

    def computeParameter(self):
        # initialize the dictionary for each port
        pd = {serie: list() for serie in self._series}

        # extract the return loss for calculations
        dbRl = self._rl.getParameter()

        # extract the propagation delay from the return loss
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                delay = 0.0

                # check if it the last frequency
                if f >= len(self._freq)-1:
                    delay = pd[serie][f-1]
                    pd[serie].append(delay)
                    continue

                # check if it is not the last frequency
                (_,phase1) = dbRl[serie][f+0]
                (_,phase2) = dbRl[serie][f+1]

                dp = phase2 - phase1
                df = self._freq[f+1] - self._freq[f]
                delay = -1/360.0 * dp/df

                if delay < 0.0:
                    if f > 0:
                        delay = pd[serie][f-1]
                    else:
                        delay = 0.0
                pd[serie].append(delay)

        return (pd,pd)

    def getMargins(self, values, limit):
        margins = list()
        freqs = list()
        vals = list()
        for i,value in enumerate(values):
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
        return "Propagation Delay"
