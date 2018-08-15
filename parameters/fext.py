from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.dataserie import PortPairDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

import itertools

class FEXT(Parameter):
    '''
    Example of FEXT loss with 4 wires (double-ended only).
        
              1   2   3   4   5   6
        1  [  _   _   _   _  1-5 1-6] 
        2  [  _   _   _  2-4  _  2-6] 
        3  [  _   _   _  3-4 3-5  _ ] 
        4  [  _  2-4 3-4  _   _   _ ] 
        5  [ 1-5  _  3-5  _   _   _ ] 
        6  [ 1-6 2-6  _   _   _   _ ]

    We have the following pairs twice: (1,5), (1,6), (2,4), (2,6), (3,4), (3,5).
    '''
    def __init__(self, ports, freq, matrices, forward=True, reverse=True):
        self._forward = forward
        self._reverse = reverse
        super(FEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.FEXT

    @staticmethod
    def register(parameters, forward=True, reverse=True):
        return lambda c, f, m: FEXT(c, f, m, forward=forward, reverse=reverse)

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        # create each pair for the FEXT
        series = set()

        # get all FEXT pairs
        wires = self._ports.getFowardWires()
        for (i,j) in itertools.product(wires, wires):
            if i is j:
                continue

            if self._forward:
                series.add(PortPairDataSerie(i.getMainPort(), j.getRemotePort()))

            if self._reverse:
                series.add(PortPairDataSerie(i.getRemotePort(), j.getMainPort()))

        return series

    def computeParameter(self):
        # initialize the dictionaries for each port
        dbFEXT = {serie: list() for serie in self._series}
        cpFEXT = {serie: list() for serie in self._series}

        # extract the FEXT value from the matrices
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                (i,j) = serie.getPortIndices()

                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = (complex2db(cpValue), complex2phase(cpValue))

                # add the value into the FEXT
                cpFEXT[serie].append(cpValue)
                dbFEXT[serie].append(dbValue)

        return (dbFEXT, cpFEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "FEXT"
