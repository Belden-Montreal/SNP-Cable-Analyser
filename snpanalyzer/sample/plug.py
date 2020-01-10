from snpanalyzer.sample.sample import Sample
from snpanalyzer.sample.port import EthernetPair, NetworkPort, PlugConfiguration
from snpanalyzer.parameters.type import ParameterType

class PlugSample(Sample):
    def getDefaultConfiguration(self):
        print("getDefaultConfiguration")
        # create the ports for this network
        ports = {
            NetworkPort(0, ptype=EthernetPair.PAIR45),
            NetworkPort(1, ptype=EthernetPair.PAIR12),
            NetworkPort(2, ptype=EthernetPair.PAIR36),
            NetworkPort(3, ptype=EthernetPair.PAIR78),
        }

        # create the configuration for this network
        return PlugConfiguration(ports=ports)

    def getDefaultParameters(self):
        print("getDefaultParameters")
        return dict()

    def getAvailableParameters(self):
        print("getAvailableParameters")
        return [
            ParameterType.RL,
            ParameterType.NEXT,
            ParameterType.PROPAGATION_DELAY,
            ParameterType.PSNEXT,
            ParameterType.LCL,
            ParameterType.TCL,
            ParameterType.CMRL,
            ParameterType.CMNEXT,
            ParameterType.CMDMNEXT,
            ParameterType.CMDMRL,
            ParameterType.DMCMNEXT,
            ParameterType.DMCMRL, 
        ]

    def getAvailableExport(self):
        return self.getAvailableParameters()

        
