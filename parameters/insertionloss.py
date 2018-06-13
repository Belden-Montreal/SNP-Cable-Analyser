from parameters.parameter import Parameter, complex2db

class InsertionLoss(Parameter):

    def __init__(self, ports, freq, matrices, full=False):
        self._full = full
        super().__init__(ports, freq, matrices)
        

    def computeParameter(self):
        '''
        Example of Insertion Loss with 4 wires
        For non-full measurement, only take the top right values (1 and 2 in this case)
        
             1 2 3 4
        1  [ _ _ 1 _ ] 
        2  [ _ _ _ 2 ] 
        3  [ 3 _ _ _ ] 
        4  [ _ 4 _ _ ] 
        
        
        '''
        # initialize the dictionary for each port
        il = dict()
        cpIl = dict()
        for port in self._ports:
            if port < len(self._ports)//2:
                il[port] = list()
                cpIl[port] = list()
            elif self._full:
                il[port] = list()
                cpIl[port] = list()

        # extract the insertion loss in all matrices
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                # get the value
                if port < len(self._ports)//2:
                    topRight = self._matrices[f, port, port+len(self._ports)//2]
                    il[port].append(complex2db(topRight))
                    cpIl[port].append(topRight)
                    if self._full:
                        bottomLeft = self._matrices[f, port+len(self._ports)//2, port]
                        il[port+len(self._ports)//2].append(complex2db(bottomLeft))
                        cpIl[port+len(self._ports)//2].append(bottomLeft)

        return il, cpIl
