from project.project import Project
from sample.end_to_end import EndToEnd

class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''
    def __init__(self):
        super(Alien, self).__init__()
        self._victim = None
        self._disturbers = None
        self._alienSample = None

    def importSamples(self, fileNames, disturber=False):
        if disturber:
            self._disturbers = super(Alien, self).importSamples(fileNames)
            return self._disturbers
        elif len(fileNames) < 2:
            self._victim = EndToEnd(fileNames[0])
            self._samples.append(self._victim)
            return self._victim
        else:
            print("can't import multiple victims")

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError