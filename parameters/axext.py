from parameters.parameter import Parameter, complex2db, complex2phase, diffDiffMatrix
from parameters.dataserie import PortPairDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

import itertools

class AXEXT(Parameter):
    """
    The AXEXT parameter can either represent the ANEXT or the AFEXT.

    The following setup can be used for measuring the ANEXT:

        measurement (disturbed) [ ]----------------[x] terminator
        measurement (disturber) [ ]----------------[x] terminator

    The following setup can be used for measuring the AFEXT:

        measurement (disturbed) [ ]----------------[x] terminator
                     terminator [x]----------------[ ] measurement (disturber)

    In both case, the main ports of the configuration should contains the
    measurements of the disturbed and the remote ports of the configuration
    should contains the measurements of the disturber.

    Using this port configuration on 4 twisted pairs cables, we get the
    equivalent network:

                           -----------------
            disturbed 1 ---|               |--- disturber 1
            disturbed 2 ---|               |--- disturber 2
            disturbed 3 ---|               |--- disturber 3
            disturbed 4 ---|               |--- disturber 4
                           -----------------

    In ANEXT or AFEXT, each disturber port affects each disturbed port. This
    means that either parameter has 16 data series in the network above. Using
    the equivalent network above, the calculations can be done by reusing
    other parameters:

        - 12 of these data series are equivalent to a normal FEXT
        -  4 of these data series are equivalent to a normal insertion loss
    """
    def __init__(self, ports, freq, matrices):
        super(AXEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def register(parameters):
        return lambda c, f, m: AXEXT(c, f, m)

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        # create each pair for the AXEXT
        series = set()

        # get all pairs
        mains = self._ports.getMainPorts()
        remotes = self._ports.getRemotePorts()
        for (i,j) in itertools.product(mains, remotes):
            series.add(PortPairDataSerie(i, j))

        return series

    def computeParameter(self):
        # initialize the dictionaries for each port
        dbAXEXT = {serie: list() for serie in self._series}
        cpAXEXT = {serie: list() for serie in self._series}

        # extract the AXEXT value from the matrices
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                (i,j) = serie.getPortIndices()

                # get the value from the matrix
                cpValue = self._matrices[f, i, j]
                dbValue = (complex2db(cpValue), complex2phase(cpValue))

                # add the value into the AXEXT
                cpAXEXT[serie].append(cpValue)
                dbAXEXT[serie].append(dbValue)

        return (dbAXEXT, cpAXEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "AXEXT"

class ANEXT(AXEXT):
    @staticmethod
    def getType():
        return ParameterType.ANEXT

    def getName(self):
        return "ANEXT"

class AFEXT(AXEXT):
    @staticmethod
    def getType():
        return ParameterType.AFEXT

    def getName(self):
        return "AFEXT"
