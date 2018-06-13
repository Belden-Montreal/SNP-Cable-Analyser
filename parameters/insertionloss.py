from parameters.parameter import Parameter, complex2db

class InsertionLoss(Parameter):

    def __init__(self, ports, freq, matrices, full=False):
        self._full = full
        super().__init__(ports, freq, matrices)
        

    def computeParameter(self):
        # initialize the dictionary for each port
        il = dict()
        cpIl = dict()
        for i, port in self._ports.items():
            if i < len(self._ports)//2:
                il[port] = list()
                cpIl[port] = list()
            elif self._full:
                il[self._ports[i]] = list()
                cpIl[self._ports[i]] = list()

        # extract the insertion loss in all matrices
        for (f,_) in enumerate(self._freq):
            for (i,port) in self._ports.items():
                # get the value
                if i < len(self._ports)//2:
                    topRight = self._matrices[f, i, i+len(self._ports)//2]
                    il[port].append(complex2db(topRight))
                    cpIl[port].append(topRight)
                    if self._full:
                        bottomLeft = self._matrices[f, i+len(self._ports)//2, i]
                        il[self._ports[i+len(self._ports)//2]].append(complex2db(bottomLeft))
                        cpIl[self._ports[i+len(self._ports)//2]].append(bottomLeft)

        return il, cpIl
