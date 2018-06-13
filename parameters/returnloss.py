from parameters.parameter import Parameter, complex2db

class ReturnLoss(Parameter):
    '''
        Example of Return Loss with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
        
        
    '''
    
    def computeParameter(self):
        
        # initialize the dictionary for each port
        rl = dict()
        cpRl = dict()
        for port in self._ports:
            rl[port] = list()
            cpRl[port] = list()

        # extract the return loss in all matrices
        for (f,_) in enumerate(self._freq):
            for port in self._ports:
                # get the value
                value = self._matrices[f, port, port]

                # convert to db if specified
                dbValue = complex2db(value)
                # add the value to the list
                rl[port].append(dbValue)
                cpRl[port].append(value)
        return rl, cpRl
