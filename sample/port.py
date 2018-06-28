class Port(object):
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name

class PortConfiguration(object):
    def __init__(self, main, remote):
        # make sure a port index isn't in both the mains and the remotes
        if set(main.keys()).intersection(set(remote.keys())):
            raise ValueError

        self._main = main
        self._remote = remote
        self._ports = dict(main)
        self._ports.update(remote)

    def getMainPorts(self):
        return self._main

    def getRemotePorts(self):
        return self._remote

    def getAllPorts(self):
        return self._ports

    def __getitem__(self, key):
        return self.getAllPorts()[key]

    def __iter__(self):
        return self._ports.items().__iter__()
