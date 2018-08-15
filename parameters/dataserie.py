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

    def getType(self):
        return self._port.getType()

    def isRemote(self):
        return self._port.isRemote()

    def __eq__(self, other):
        if self.getType() != other.getType():
            return False
        if self.isRemote() != other.isRemote():
            return False
        return True

    def __hash__(self):
        return (self.getType(), self.isRemote()).__hash__()

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

    def getTypes(self):
        (p1,p2) = self._ports
        return (p1.getType(), p2.getType())

    def getRemotes(self):
        (p1,p2) = self._ports
        return (p1.isRemote(), p2.isRemote())

    def getPortSeries(self):
        serie1 = PortDataSerie(self._ports[0])
        serie2 = PortDataSerie(self._ports[1])
        return (serie1, serie2)

    def getData(self):
        return self._data

    def isRemote(self):
        return self._ports[0].isRemote()

    def __eq__(self, other):
        (p1,p2) = self.getPorts()
        (o1,o2) = other.getPorts()
        if p1.isRemote() != o1.isRemote():
            return False
        if p1.getType() != o1.getType():
            return False
        return True

    def __hash__(self):
        return (self.getTypes(), self.getRemotes()).__hash__()

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

    def getType(self):
        return self._wire.getType()

    def isReverse(self):
        return self._wire.isReverse()

    def __eq__(self, other):
        if self.isReverse() != other.isReverse():
            return False
        if self.getType() != other.getType():
            return False
        return True

    def __hash__(self):
        return (self.getType(), self.isReverse()).__hash__()
        
