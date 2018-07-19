from parameters.parameter import Parameter
from parameters.dataserie import PortOrderedPairDataSerie, PortDataSerie
from parameters.type import ParameterType

import itertools

class NEXTDelay(Parameter):
    def __init__(self, ports, freq, matrices, plugDelay, mains=True, remotes=False):
        self._mains   = mains
        self._remotes = remotes
        self._plugDelay = plugDelay
        super(NEXTDelay, self).__init__(ports, freq, matrices)
        self._visible = False

    @staticmethod
    def getType():
        return ParameterType.NEXT_DELAY

    @staticmethod
    def register(parameters, mains=True, remotes=False):
        return lambda c, f, m: NEXTDelay(c, f, m,
            parameters(ParameterType.PLUG_DELAY),
            mains=mains, remotes=remotes
        )

    def computeDataSeries(self):
        series = set()

        # get the NEXT pairs between the main ports
        if self._mains:
            mains = self._ports.getMainPorts()
            for (i,j) in itertools.product(mains, mains):
                if i is j:
                    continue
                series.add(PortOrderedPairDataSerie(i, j))

        # get the NEXT pairs between the remote ports
        if self._remotes:
            remotes = self._ports.getRemotePorts()
            for (i,j) in itertools.product(remotes, remotes):
                if i is j:
                    continue
                series.add(PortOrderedPairDataSerie(i, j))

        return series

    def computeParameter(self):
        nextDelay = dict()
        plugDelay = self._plugDelay.getParameter()

        for serie in self._series:
            (serie1, serie2) = serie.getPortSeries()
            nextDelay[serie] = plugDelay[serie1] + plugDelay[serie2]

        return (nextDelay,None)
    
    def recalculate(self, plugDelay):
        self._plugDelay = plugDelay
        (self._parameter, self._complexParameter) = self.computeParameter()

    def getPlugDelay(self):
        return self._plugDelay

    def getName(self):
        return "NEXTDelay"

    def chooseMatrices(self, matrices):
        return None
