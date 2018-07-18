from sample.sample import Sample
from sample.port import NetworkPort, AlienConfiguration

class AlienSample(Sample):
    '''
    Abstract class for alien sample.
    '''
    def __init__(self, snp, remote=False, config=None, standard=None):
        self._remote = remote
        super(AlienSample, self).__init__(snp, config=config, standard=standard)
    
    def isRemote(self):
        return self._remote

    def getDefaultConfiguration(self):
        # create the victim ports
        victims = {
            NetworkPort(0, "12 (v)"),
            NetworkPort(1, "36 (v)"),
            NetworkPort(2, "45 (v)"),
            NetworkPort(3, "78 (v)"),
        }

        # create the disturber ports
        disturbers = {
            NetworkPort(4, "12 (d)"),
            NetworkPort(5, "36 (d)"),
            NetworkPort(6, "45 (d)"),
            NetworkPort(7, "78 (d)"),
        }

        # create the configuration for this network
        return AlienConfiguration(victims=victims, disturbers=disturbers)
