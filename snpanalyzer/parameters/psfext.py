from parameters.parameter import Parameter, diffDiffMatrix, complex2db, complex2phase
from parameters.dataserie import PortDataSerie
from parameters.type import ParameterType
from analysis.format import DataFormat

import numpy as np

def powerSum(values):
    return 10*np.log10(np.sum(list(map(lambda v: 10**(v[0]/10), values))))

class PSFEXT(Parameter):
    '''
    PSFEXT is calculated using the following formula:

        PSFEXT_k = 10*log10(sum(FEXT_i,k))
        
    where FEXT_i,k is the FEXT loss from wire i to wire k.

    TODO: Subclass Parameter into PowerSumParameter since PSNEXT/PSFEXT are
          pretty much the same.
    '''
    def __init__(self, ports, freq, matrices, fext):
        self._fext = fext
        super(PSFEXT, self).__init__(ports, freq, matrices)

    @staticmethod
    def getType():
        return ParameterType.PSFEXT

    @staticmethod
    def register(parameters):
        return lambda c, f, m: PSFEXT(c, f, m, parameters(ParameterType.FEXT))

    @staticmethod
    def getAvailableFormats():
        return {
            DataFormat.MAGNITUDE,
            DataFormat.PHASE,
            DataFormat.REAL,
            DataFormat.IMAGINARY,
        }

    def computeDataSeries(self):
        mains   = self._ports.getMainPorts()
        remotes = self._ports.getRemotePorts()

        # create a serie for each port
        series = set()
        for p in self._ports.getPorts():
            # find the pairs that affect our port
            fextSeries = set()
            for fextSerie in self._fext.getDataSeries():
                (p1,p2) = fextSerie.getPorts()

                if not p == p1:
                    continue

                fextSeries.add(fextSerie)

            # create the serie for the port
            series.add(PortDataSerie(p, data=fextSeries))

        return series

    def computeParameter(self):
        # initialize the dictionary for each data serie
        dbPSFEXT = {serie: list() for serie in self._series}
        cpPSFEXT = {serie: list() for serie in self._series}

        # compute the power sum FEXT
        for (f,_) in enumerate(self._freq):
            for serie in self._series:
                fextSeries = serie.getData()

                # get the FEXT values of these pairs
                cpValues = [self._fext.getComplexParameter()[s][f] for s in fextSeries]
                dbValues = [self._fext.getParameter()[s][f]        for s in fextSeries]

                # compute PSFEXT
                cpValue = np.sum(list(cpValues))
                dbValue = (powerSum(dbValues), complex2phase(cpValue))

                # add the value to the list
                dbPSFEXT[serie].append(dbValue)
                cpPSFEXT[serie].append(cpValue)

        return (dbPSFEXT, cpPSFEXT)

    def chooseMatrices(self, matrices):
        return diffDiffMatrix(matrices)

    def getFEXT(self):
        return self._fext

    def getName(self):
        return "PSFEXT"
