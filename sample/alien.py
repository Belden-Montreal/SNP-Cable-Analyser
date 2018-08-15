from sample.sample import Sample
from sample.port import EthernetPair, WirePort, AlienConfiguration

class AlienSample(Sample):
    '''
    Abstract class for alien sample.
    '''
    def __init__(self, snp, remote=False, **kwargs):
        self._remote = remote
        super(AlienSample, self).__init__(snp, **kwargs)
    
    def isRemote(self):
        return self._remote

    def getDefaultConfiguration(self):
        # create the victim ports
        victims = {
            WirePort(0, ptype=EthernetPair.PAIR12, remote=True),
            WirePort(1, ptype=EthernetPair.PAIR36, remote=True),
            WirePort(2, ptype=EthernetPair.PAIR45, remote=True),
            WirePort(3, ptype=EthernetPair.PAIR78, remote=True),
        }

        # create the disturber ports
        disturbers = {
            WirePort(4, ptype=EthernetPair.PAIR12),
            WirePort(5, ptype=EthernetPair.PAIR36),
            WirePort(6, ptype=EthernetPair.PAIR45),
            WirePort(7, ptype=EthernetPair.PAIR78),
        }

        # create the configuration for this network
        return AlienConfiguration(victims=victims, disturbers=disturbers)
