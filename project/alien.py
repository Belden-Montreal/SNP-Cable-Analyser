from project.project import Project, ProjectNode
from sample.disturber import Disturber
from sample.victim import Victim
from project.alien_import_dialog import AlienImportDialog
from multiprocessing.dummy import Pool as ThreadPool


class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''
    def __init__(self, name):
        super(Alien, self).__init__(name)
        self._ends = dict()
        self._ends["End 1"] = dict()
        self._ends["End 2"] = dict()
        for end in self._ends.values():
            end["ANEXT"] = list()
            end["AFEXT"] = list()        

    def removeSample(self, sample):
        for end in self._ends.values():
            for param in end.values():
                if sample in param:
                    param.remove(sample)

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def nodeFromProject(self):
        return AlienNode(self)

from app.node import Node
from sample.sample import SampleNode
class AlienNode(ProjectNode):

    def openImportWindow(self, parent):
        dial = AlienImportDialog(parent)
        disturbersFile, victimFile, end, param = dial.getFiles()
        samples = list()
        disturbers = self.importSamples(disturbersFile, disturber=True)
        victim = self.importSamples([victimFile], disturber=False)
        samples.extend(disturbers)
        samples.append(victim)
        self._dataObject._ends[end][param] = samples
        self._dataObject._victim = victim
        self._dataObject._disturbers = disturbers
        self.addChildren(samples, end, param)

    def importSamples(self, fileNames, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.map(self.__createDisturber, fileNames)
            self._axextd = self.calculateAXEXTD(samples)
            return samples
        elif len(fileNames) < 2:
                return self.__createVictim(fileNames[0], self._axextd)
                

    def __createDisturber(self, name):
        return Disturber(name)

    def __createVictim(self, name, axextd):
        return Victim(name, axextd)

    def calculateAXEXTD(self, disturbers):
        return [disturber.getParameters()["AXEXT"] for disturber in disturbers]


    def addChildren(self, samples, end, param):
        node = self.hasChild(end)
        if not node:
            node = Node(end)
            self.appendRow(node)
        subNode = self.hasChild(param)
        if not subNode:
            subNode = Node(param)
            node.appendRow(subNode)
        subNode.children = list()
        for sample in samples:
            subNode.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        for end, params in self._dataObject._ends.items():
            for param, samples in params.items():
                if len(samples):
                    self.addChildren(samples, end, param)