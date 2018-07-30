from enum import Enum

class EthernetPair(Enum):
    DUMMY  = 0
    PAIR12 = 1
    PAIR36 = 2
    PAIR45 = 3
    PAIR78 = 4

class NetworkPort(object):
    """
    Basic class representing a port in a network. A port has an index in the
    network and a name.
    """
    def __init__(self, index, name, ptype=None):
        self._index = index
        self._name  = name
        self._type  = ptype

    def getIndex(self):
        return self._index

    def getName(self):
        return self._name

    def getType(self):
        return self._type

class WirePort(NetworkPort):
    """
    This class represents a wire port in a network. A wire has two ports, a
    main port and a remote one.
    """
    def __init__(self, index, name, remote=False, **kwargs):
        super(WirePort, self).__init__(index, name, **kwargs)
        self._remote = remote

    def isRemote(self):
        return self._remote

    def setRemote(self, remote=True):
        self._remote = remote

class Wire(object):
    """
    This class represents a wire in a network. A wire has a name and  two ports,
    a main one and a remote one.
    """
    def __init__(self, name, main, remote, wtype=None):
        if main.isRemote():
            raise ValueError

        if not remote.isRemote():
            raise ValueError

        self._name    = name
        self._main    = main
        self._remote  = remote
        self._type    = wtype
        self._reverse = None

    def getName(self):
        return self._name

    def getMainPort(self):
        return self._main

    def getRemotePort(self):
        return self._remote

    def getType(self):
        return self._type

    def getReverse(self):
        return self._reverse

    def setReverse(self, reverse):
        self._reverse = reverse

    def __contains__(self, port):
        if self._main is port:
            return True
        if self._remote is port:
            return True
        return False

class PortPair(object):
    """
    This class represents a pair of ports.
    """
    def __init__(self, port1, port2, name=None):
        if port1.getIndex() < port2.getIndex():
            self._ports = (port1, port2)
        else:
            self._ports = (port2, port1)
        if name is None:
            self._name = port1.getName() + "-" + port2.getName()

    def getPorts(self):
        return self._ports

    def getPortIndices(self):
        (p1,p2) = self._ports
        return (p1.getIndex(), p2.getIndex())

    def getName(self):
        return self._name

class ReversedWire(Wire):
    """
    This class represents a wire traveled in the other direction.
    """
    def __init__(self, wire):
        self._name    = wire.getName()
        self._main    = wire.getRemotePort()
        self._remote  = wire.getMainPort()
        self._type    = wire.getType()
        self._reverse = wire
        wire.setReverse(self)

class NetworkConfiguration(object):
    """
    This class represents a network configuration.
    """
    def getPorts(self):
        raise NotImplementedError

    def getMainPorts(self):
        raise NotImplementedError

    def getRemotePorts(self):
        raise NotImplementedError

    def getByType(self):
        raise NotImplementedError

    def __iter__(self):
        return self.getPorts().__iter__()

    def __len__(self):
        return self.getPorts().__len__()

class PlugConfiguration(NetworkConfiguration):
    """
    This class represents a plug configuration of a network.
    """
    def __init__(self, ports=set()):
        # save all ports in the configration
        self._indices = set()
        self._types   = dict()
        self._ports = set()
        {self.addPort(port) for port in ports}

    def _registerType(self, port):
        # make sure the port as a type
        if port.getType() is None:
            return

        # types must be unique
        if port.getType() in self._types:
            raise ValueError("Duplicate types in the configuration")

        # add the port
        self._types[port.getType()] = port

    def _registerIndex(self, port):
        # indices must be unique
        if port.getIndex() in self._indices:
            raise ValueError("Duplicate port indices in the configuration")

        # add the index
        self._indices.add(port.getIndex())

    def addPort(self, port):
        # make sure there is no duplicate
        try:
            self._registerIndex(port)
            self._registerType(port)
        except ValueError:
            if port.getIndex() in self._indices:
                self._indices.discard(port.getIndex())
            if port in self._types.values():
                self._types.pop(port.getType())
            raise

        # add the port to the configuration
        self._ports.add(port)

    def getPorts(self):
        return self._ports

    def getMainPorts(self):
        return self._ports

    def getRemotePorts(self):
        return set()

    def getByType(self, ptype):
        if ptype not in self._types:
            return None
        return self._types[ptype]

class AlienConfiguration(NetworkConfiguration):
    """
    This class represents a alien configuration of a network.
    """
    def __init__(self, victims=set(), disturbers=set()):
        # save all ports in the configuration
        self._ports      = victims.union(disturbers)
        self._victims    = victims
        self._disturbers = disturbers

        # make sure all ports are unique
        indices = {p.getIndex() for p in self._ports}
        if len(indices) != len(self._ports):
            error = ValueError("All ports must be unique in the configuration")
            raise error

    def getPorts(self):
        return self._ports

    def getVictimPorts(self):
        return self._victims

    def getDisturberPorts(self):
        return self._disturbers

    def getMainPorts(self):
        return self.getVictimPorts()

    def getRemotePorts(self):
        return self.getDisturberPorts()

class CableConfiguration(NetworkConfiguration):
    """
    This class represents a cable configuration of a network.
    """
    def __init__(self, foward=set()):
        # save all wire in the configration
        self._indices  = set()
        self._types    = dict()
        self._ports    = set()
        self._mains    = set()
        self._remotes  = set()
        self._foward   = set()
        self._reversed = set()
        self._wires    = set()
        {self.addWire(wire) for wire in foward}
    
    def _registerType(self, wire):
        # make sure the wire as a type
        if wire.getType() is None:
            return

        # types must be unique
        if wire.getType() in self._types:
            raise ValueError("Duplicate types in the configuration")

        # add the port
        self._types[wire.getType()] = wire

    def _registerIndex(self, port):
        # indices must be unique
        if port.getIndex() in self._indices:
            raise ValueError("Duplicate port indices in the configuration")

        # add the index
        self._indices.add(port.getIndex())

    def addWire(self, wire):
        # make sure there is no duplicate
        try:
            self._registerIndex(wire.getMainPort())
            self._registerIndex(wire.getRemotePort())
            self._registerType(wire)
        except ValueError:
            if wire.getMainPort().getIndex() in self._indices:
                self._indices.discard(wire.getMainPort().getIndex())
            if wire.getRemotePort().getIndex() in self._indices:
                self._indices.discard(wire.getRemotePort().getIndex())
            if wire.getType() in self._types:
                self._types.pop(wire.getType())
            raise

        # set proper remote in the ports
        wire.getMainPort().setRemote(False)
        wire.getRemotePort().setRemote(True)

        # update the configuration ports
        self._ports.add(wire.getMainPort())
        self._ports.add(wire.getRemotePort())
        self._mains.add(wire.getMainPort())
        self._remotes.add(wire.getRemotePort())

        # update the configuration wires
        self._wires.add(wire)
        self._foward.add(wire)
        rwire = ReversedWire(wire)
        self._wires.add(rwire)
        self._reversed.add(rwire)

    def getWires(self):
        return self._wires

    def getFowardWires(self):
        return self._foward

    def getReversedWires(self):
        return self._reversed

    def getPorts(self):
        return self._ports

    def getMainPorts(self):
        return self._mains

    def getRemotePorts(self):
        return self._remotes

    def getByType(self, wtype):
        if wtype not in self._types:
            return None
        return self._types[wtype]
