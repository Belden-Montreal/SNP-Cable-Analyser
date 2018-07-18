from skrf import Network
from os.path import getctime
from time import ctime

from sample.sample import Sample
from sample.port import WirePort, Wire, CableConfiguration

class CableSample(Sample):
    def getDefaultConfiguration(self):
        # create the ports for this network
        ports = {
            1: WirePort(0, "Port 1", remote=False),
            2: WirePort(1, "Port 2", remote=False),
            3: WirePort(2, "Port 3", remote=False),
            4: WirePort(3, "Port 4", remote=False),
            5: WirePort(4, "Port 5", remote=True),
            6: WirePort(5, "Port 6", remote=True),
            7: WirePort(6, "Port 7", remote=True),
            8: WirePort(7, "Port 8", remote=True),
        }

        # create the wires for this network
        wires = {
            Wire("12", ports[1], ports[5]),
            Wire("36", ports[2], ports[6]),
            Wire("45", ports[3], ports[7]),
            Wire("78", ports[4], ports[8]),
        }

        # create the configuration for this network
        return CableConfiguration(foward=wires)

    def getDefaultParameters(self):
        return dict()

    def getAvailableParameters(self):
        return {
            "RL",
            "IL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "FEXT",
            "PSFEXT",
            "ACRF",
            "PSACRF",
            "LCL",
            "LCTL",
            "TCL",
            "TCTL",
            "ELTCTL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL",
        }
