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

    def importSamples(self, fileNames, end, param, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.map(self.__createDisturber, fileNames)
            if self._victims[end][param] is not None:
                self._victims[end][param].calculateAXEXTD(samples)
            self._disturbers[end][param] = samples
            return samples
        elif len(fileNames) < 2:
            sample = self.__createVictim(fileNames[0], self._disturbers[end][param])
            if len(self._disturbers[end][param]) > 0:
                sample.calculateAXEXTD(self._disturbers[end][param])
            self._victims[end][param] = sample
            return sample

    def __createDisturber(self, name):
        return Disturber(name)

    def __createVictim(self, name, disturbers):
        return Victim(name, disturbers)

    def removeSample(self, sample):
        for end in self._disturbers:
            for param in self._disturbers[end]:
                if sample in self._disturbers[end][param]:
                    self._disturbers[end][param].remove(sample)
                elif sample == self._victims[end][param]:
                    self._victims[end][param] = None

    def disturbers(self):
        return self._disturbers

    def victims(self):
        return self._victims

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
        files = dial.getFiles()
        if files:
            disturbersFile, victimFile, end, param = dial.getFiles()
            samples = list()
            samples = self._dataObject.importSamples(disturbersFile, end, param, disturber=True)
            samples.append(self._dataObject.importSamples([victimFile], end, param, disturber=False))
            self.addChildren(samples, end, param)

    def addChildren(self, samples, end, param):
        node = self.hasChild(end)
        if not node:
            node = Node(end)
            self.appendRow(node)
        subNode = node.hasChild(param)
        if not subNode:
            subNode = Node(param)
            node.appendRow(subNode)
        subNode.children = list()
        for sample in samples:
            subNode.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        for end, params in self._dataObject.disturbers().items():
            for param, samples in params.items():
                if len(samples):
                    self.addChildren(samples, end, param)

    def getWidgets(self):
        alienTab = AlienWidget(self)
        return {"Alien": alienTab}