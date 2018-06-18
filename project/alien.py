from project.project import Project
from sample.disturber import Disturber
from sample.victim import Victim
from multiprocessing.dummy import Pool as ThreadPool


class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''
    def __init__(self):
        super(Alien, self).__init__()
        self._victim = None
        self._disturbers = list()
        self._axextd = None

    def importSamples(self, fileNames, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.map(self.__createDisturber, fileNames)
            self._disturbers.extend(samples)
            self._samples.extend(samples)
            self._axextd = self.calculateAXEXTD()
            if self._victim:
                self._victim.setAxextd(self._axextd)
        elif len(fileNames) < 2:
            if len(self._disturbers):
                self._victim = self.__createVictim(fileNames[0], self._axextd)
                self._samples.append(self._victim)
            else:
                print("can't import victim before disturbers")
        else:
            print("can't import multiple victims")

    def calculateAXEXTD(self):
        return [disturber.getParameters()["AXEXT"] for disturber in self._disturbers]

    def removeSamples(self, names):
        super(Alien, self).removeSamples(names)
        if self._victim.getName() in names:
            self._victim = None

        self._disturbers = [x for x in self._disturbers if x.getName() not in names]

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def __createDisturber(self, name):
        return Disturber(name)

    def __createVictim(self, name, axextd):
        return Victim(name, axextd)