class NetworkPort(object):
    """
    Basic class representing a port in a network. A port has an index in the
    network and a name.
    """
    def __init__(self, index, name):
        self._index = index
        self._name  = name

    def getIndex(self):
        return self._index

    def getName(self):
        return self._name

class WirePort(NetworkPort):
    """
    This class represents a wire port in a network. A wire has two ports, a
    main port and a remote one.
    """
    def __init__(self, index, name, remote=False):
        super(WirePort, self).__init__(index, name)
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
    def __init__(self, name, main, remote):
        if main.isRemote():
            raise ValueError

        if not remote.isRemote():
            raise ValueError

        self._name   = name
        self._main   = main
        self._remote = remote

    def getName(self):
        return self._name

    def getMainPort(self):
        return self._main

    def getRemotePort(self):
        return self._remote

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
        self._name   = wire.getName()
        self._main   = wire.getRemotePort()
        self._remote = wire.getMainPort()

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
        self._ports = ports

        # all the indices must be unique
        self._indices = {port.getIndex() for port in self._ports}
        if len(self._indices) != len(self._ports):
            raise ValueError

    def addPort(self, port):
        # make sure the port index isn't already in the configuration
        if port.getIndex() in self._indices:
            raise ValueError

        # add the port to the configuration
        self._ports.add(port)
        self._indices.add(port.getIndex())

    def getPorts(self):
        return self._ports

    def getMainPorts(self):
        return self._ports

    def getRemotePorts(self):
        return set()

class CableConfiguration(NetworkConfiguration):
    """
    This class represents a cable configuration of a network.
    """
    def __init__(self, foward=set()):
        # save all foward wires in the configuration
        self._foward = foward

        # create the reversed wires
        self._reversed = {ReversedWire(wire) for wire in foward}

        # create the aggregate of all wires
        self._wires = self._foward.union(self._reversed)

        # all main ports must not be remote
        self._mains = {wire.getMainPort() for wire in foward}
        if not all([not port.isRemote() for port in self._mains]):
            raise ValueError

        # all remote ports must be remote
        self._remotes = {wire.getRemotePort() for wire in foward}
        if not all([port.isRemote() for port in self._remotes]):
            raise ValueError

        # save all ports in the configuration
        self._ports = self._mains.union(self._remotes)

        # all the indices must be unique
        self._indices = {port.getIndex() for port in self._ports}
        if len(self._indices) != len(self._ports):
            raise ValueError

    def addWire(self, wire):
        # the main port index must not be in the configuration
        if wire.getMainPort().getIndex() in self._indices:
            raise ValueError
        self._indices.add(wire.getMainPort().getIndex())

        # the remote port index must not be in the configuration
        if wire.getRemotePort().getIndex() in self._indices:
            raise ValueError
        self._indices.add(wire.getRemotePort().getIndex())

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
