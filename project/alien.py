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
        self._disturbers = dict()
        self._victims = dict()
        self._disturbers["End 1"] = dict()
        self._disturbers["End 2"] = dict()
        self._victims["End 1"] = dict()
        self._victims["End 2"] = dict()
        for end in self._disturbers:
            self._disturbers[end]["PSANEXT"] = list()
            self._disturbers[end]["PSAACRF"] = list()
            self._victims[end]["PSANEXT"] = None
            self._victims[end]["PSAACRF"] = None 

    def removeSample(self, sample):
        for end in self._disturbers:
            for param in self._disturbers[end]:
                if sample in self._disturbers[end][param]:
                    self._disturbers[end][param].remove(sample)
                elif sample == self._victims[end][param]:
                    self._victims[end][param] = None

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def nodeFromProject(self):
        return AlienNode(self)

from app.node import Node
from sample.sample import SampleNode
from widgets.alien_widget import AlienWidget
from PyQt5 import QtWidgets
class AlienNode(ProjectNode):

    def openImportWindow(self, parent):
        dial = AlienImportDialog(parent)
        disturbersFile, victimFile, end, param = dial.getFiles()
        samples = list()
        disturbers = self.importSamples(disturbersFile, disturber=True)
        victim = self.importSamples([victimFile], disturber=False)
        samples.extend(disturbers)
        samples.append(victim)
        self._dataObject._disturbers[end][param] = disturbers
        self._dataObject._victims[end][param] = victim
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
        for end, params in self._dataObject._disturbers.items():
            for param, samples in params.items():
                if len(samples):
                    self.addChildren(samples, end, param)

    def getWidgets(self):
        alienTab = AlienWidget(self._dataObject)
        return {"Alien": alienTab}