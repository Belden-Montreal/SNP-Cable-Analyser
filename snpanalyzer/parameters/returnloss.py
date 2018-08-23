from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

class ReturnLoss(Parameter):
    '''
        Example of Return Loss with 4 wires
        
             1 2 3 4
        1  [ 1 _ _ _ ] 
        2  [ _ 2 _ _ ] 
        3  [ _ _ 3 _ ] 
        4  [ _ _ _ 4 ] 
        
    '''
    @staticmethod
    def getType():
        return ParameterType.RL

    @staticmethod
    def register(parameters):
        return lambda c, f, m: ReturnLoss(c, f, m)
        
    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        return {PortDataSerie(port) for port in self._ports.getPorts()}

    def computeParameter(self):
        # initialize the dictionary for each port
        dbRL = {serie: list() for serie in self._series}
        cpRL = {serie: list() for serie in self._series}

        # extract the return loss in all matrices
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                i = serie.getPort().getIndex()

                # get the value
                cpValue = self._matrices[f, i, i]
                dbValue = (complex2db(cpValue), complex2phase(cpValue))

                # add the value to the lists
                dbRL[serie].append(dbValue)
                cpRL[serie].append(cpValue)

        return (dbRL, cpRL)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "Return Loss"
