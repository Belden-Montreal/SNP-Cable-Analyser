from sample.sample import Sample
from sample.port import EthernetPair, NetworkPort, AlienConfiguration

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
            NetworkPort(0, "12 (v)", ptype=EthernetPair.PAIR12),
            NetworkPort(1, "36 (v)", ptype=EthernetPair.PAIR36),
            NetworkPort(2, "45 (v)", ptype=EthernetPair.PAIR45),
            NetworkPort(3, "78 (v)", ptype=EthernetPair.PAIR78),
        }

        # create the disturber ports
        disturbers = {
            NetworkPort(4, "12 (d)", ptype=EthernetPair.PAIR12),
            NetworkPort(5, "36 (d)", ptype=EthernetPair.PAIR36),
            NetworkPort(6, "45 (d)", ptype=EthernetPair.PAIR45),
            NetworkPort(7, "78 (d)", ptype=EthernetPair.PAIR78),
        }

        # create the configuration for this network
        return AlienConfiguration(victims=victims, disturbers=disturbers)
