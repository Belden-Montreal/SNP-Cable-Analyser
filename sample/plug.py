from sample.sample import Sample, PORTS_NAME
from sample.port import NetworkPort, PlugConfiguration
from parameters.parameter_factory import ParameterFactory

class PlugSample(Sample):
    def getDefaultConfiguration(self):
        # create the ports for this network
        ports = {
            NetworkPort(0, "12"),
            NetworkPort(1, "36"),
            NetworkPort(2, "45"),
            NetworkPort(3, "78"),
        }

        # create the configuration for this network
        return PlugConfiguration(ports=ports)

    def getDefaultParameters(self):
        return dict()

    def getAvailableParameters(self):
        return {
            "RL",
            "NEXT",
            "Propagation Delay",
            "PSNEXT",
            "LCL",
            "TCL",
            "CMRL",
            "CMNEXT",
            "CMDMNEXT",
            "CMDMRL",
            "DMCMNEXT",
            "DMCMRL",
        }
        
