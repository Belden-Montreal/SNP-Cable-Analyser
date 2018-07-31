from sample.alien import AlienSample
from sample.port import NetworkPort, AlienConfiguration
from parameters.type import ParameterType

class DisturberSample(AlienSample):
    '''
    The Disturber class contains the measurements for alien parameters of one
    disturber on the victim.
    '''
    def getDefaultParameters(self):
        return dict()

    def getAvailableParameters(self):
        if self.isRemote():
            return {ParameterType.AFEXT}
        else:
            return {ParameterType.ANEXT}
