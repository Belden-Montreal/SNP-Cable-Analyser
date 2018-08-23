from snpanalyzer.parameters.parameter import Parameter, diffDiffMatrix
from snpanalyzer.parameters.dataserie import PortDataSerie
from snpanalyzer.parameters.type import ParameterType
from snpanalyzer.analysis.format import DataFormat

import numpy as np

class PSAXEXT(Parameter):
    '''
    The PSAXEXT parameter can either represent the PSANEXT or the PSAFEXT.

    Assume we have 3 alien measurements for a 2 wires network from 3 different
    disturbers. Only the remote ports should change between the measurements
    as shown below.

                       ---------------
        disturbed 1 ---|             |--- disturber A1
        disturbed 2 ---|             |--- disturber A2
                       ---------------

                       ---------------
        disturbed 1 ---|             |--- disturber B1
        disturbed 2 ---|             |--- disturber B2
                       ---------------

                       ---------------
        disturbed 1 ---|             |--- disturber C1
        disturbed 2 ---|             |--- disturber C2
                       ---------------

    For the first wire, we have a total of 6 AXEXT measurements:

        1. (disturbed 1, dirturber A1)
        2. (disturbed 1, dirturber A2)
        3. (disturbed 1, dirturber B1)
        4. (disturbed 1, dirturber B2)
        5. (disturbed 1, dirturber C1)
        6. (disturbed 1, dirturber C2)

    For the second wire, we have a total of 6 AXEXT measurements:

        1. (disturbed 2, dirturber A1)
        2. (disturbed 2, dirturber A2)
        3. (disturbed 2, dirturber B1)
        4. (disturbed 2, dirturber B2)
        5. (disturbed 2, dirturber C1)
        6. (disturbed 2, dirturber C2)

    The PSAXEXT is calculated using a power sum of every interations like
    shown above.
    '''
    def __init__(self, ports, freq, matrices, axextd):
        self._axextd = axextd
        super(PSAXEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        # all the data series should be identical in each disturber's AXEXT
        try:
            reference = next(iter(self._axextd))
            for disturber in self._axextd:
                if reference.getDataSeries() != disturber.getDataSeries():
                    raise ValueError

            # create the series for this parameter
            series = set()
            for port in self._ports.getMainPorts():
                disturberSeries = dict()
                for disturber in self._axextd:
                    axextSeries = set()
                    for serie in disturber.getDataSeries():
                        if port != serie.getPorts()[0]:
                            continue
                        axextSeries.add(serie)
                    disturberSeries[disturber] = axextSeries
                series.add(PortDataSerie(port, data=disturberSeries))
        except StopIteration:
            series = set()
        return series

    def computeParameter(self):
        # initialize the dictionaries for each series
        dbPSAXEXT = {serie: list() for serie in self._series}
        cpPSAXEXT = {serie: list() for serie in self._series}

        # compute the values 
        for (f,_) in enumerate(self._freq):
            for serie in self._series:

                # compute the PSAXEXT value
                dbSum = 0
                for disturber in serie.getData():
                    for axextSerie in serie.getData()[disturber]:
                        axext = disturber.getParameter()[axextSerie][f][0]
                        dbSum += 10.0**(axext/10)
                dbValue = (10.0*np.log10(dbSum), 0)
                cpValue = 0

                # add the value to the lists
                dbPSAXEXT[serie].append(dbValue)
                cpPSAXEXT[serie].append(cpValue)

        return (dbPSAXEXT, cpPSAXEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getName(self):
        return "PSAXEXT"

    def getDisturbersAXEXT(self):
        return self._axextd

    def recalculate(self, axextd):
        self._axextd = axextd
        (self._parameter, self._complexParameter) = self.computeParameter()

class PSANEXT(PSAXEXT):
    @staticmethod
    def getType():
        return ParameterType.PSANEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSANEXT(c, f, m,
            parameters(ParameterType.ANEXTD)
        )

    def getName(self):
        return "PSANEXT"

class PSAFEXT(PSAXEXT):
    @staticmethod
    def getType():
        return ParameterType.PSAFEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSAFEXT(c, f, m,
            parameters(ParameterType.AFEXTD)
        )

    def getName(self):
        return "PSAFEXT"
