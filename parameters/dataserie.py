class DataSerie(object):
    def getName(self):
        raise NotImplementedError

class PortDataSerie(DataSerie):
    def __init__(self, port, data=None):
        self._port = port
        self._data = data

    @staticmethod
    def fromSerie(port, data=None):
        return PortDataSerie(port.getPort(), data=data)

    def getName(self):
        return self._port.getName()

    def getPort(self):
        return self._port

    def getData(self):
        return self._data

    def __eq__(self, other):
        return (self._port is other.getPort())

    def __hash__(self):
        return self._port.__hash__()

class PortPairDataSerie(DataSerie):
    def __init__(self, port1, port2, data=None):
        self._ports = (port1, port2)
        self._name = port1.getName() + "-" + port2.getName()
        self._data = data

    @staticmethod
    def fromSerie(portpair, data=None):
        (p1,p2) = portpair.getPorts()
        return PortPairDataSerie(p1, p2, data=data)
    
    @staticmethod
    def fromWire(wire):
        return PortPairDataSerie(wire.getMainPort(), wire.getRemotePort())

    def getName(self):
        return self._name

    def getPorts(self):
        return self._ports

    def getPortIndices(self):
        (p1,p2) = self._ports
        return (p1.getIndex(), p2.getIndex())

    def getData(self):
        return self._data

    def __eq__(self, other):
        (p1,p2) = self._ports
        (o1,o2) = other.getPorts()
        if p1 is not o1:
            return False
        if p2 is not o2:
            return False
        return True

    def __hash__(self):
        return self.getPortIndices().__hash__()

class PortOrderedPairDataSerie(PortPairDataSerie):
    def __init__(self, port1, port2, data=None):
        if port1.getIndex() > port2.getIndex():
            (port2, port1) = (port1, port2)
        super(PortOrderedPairDataSerie, self).__init__(port1, port2, data=data)

class WireDataSerie(PortPairDataSerie):
    def __init__(self, wire, data=None):
        main = wire.getMainPort()
        remote = wire.getRemotePort()
        super(WireDataSerie, self).__init__(main, remote, data=data)

        self._wire = wire

    def getName(self):
        return self._wire.getName()

    def getWire(self):
        return self._wire

    def getMainPort(self):
        return self._wire.getMainPort()

    def getRemotePort(self):
        return self._wire.getRemotePort()

    def __eq__(self, other):
        return (self._wire is other.getWire())

    def __hash__(self):
        return self._wire.__hash__()
        
