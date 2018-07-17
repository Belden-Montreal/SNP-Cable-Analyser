from project.project import Project, ProjectNode
from sample.disturber import Disturber
from sample.victim import Victim
from project.alien_import_dialog import AlienImportDialog
from multiprocessing.dummy import Pool as ThreadPool
from copy import deepcopy

class Alien(Project):
    '''
    The Alien class represents a project where multiple samples are disturbing a victim sample
    '''
    def __init__(self, name):
        super(Alien, self).__init__(name)
        self._disturbers = dict()
        self._victims = dict()
        self._disturbers["PSANEXT"] = dict()
        self._disturbers["PSAACRF"] = dict()
        self._victims["PSANEXT"] = dict()
        self._victims["PSAACRF"] = dict()
        for param in self._disturbers:
            self._disturbers[param]["End 1"] = list()
            self._disturbers[param]["End 2"] = list()
            self._victims[param]["End 1"] = None
            self._victims[param]["End 2"] = None 

    def importSamples(self, fileNames, end, param, disturber=False):
        if disturber:
            pool = ThreadPool()
            samples = pool.starmap(self.__createDisturber, zip(fileNames, [param]*len(fileNames)))
            if self._victims[param][end] is not None:
                self._victims[param][end].setAXEXTD(self.__calculateAXEXTD(samples, param))
            self._disturbers[param][end] = samples
            return samples
        elif len(fileNames) < 2:
            sample = self.__createVictim(fileNames[0], param, self.__calculateAXEXTD(self._disturbers[param][end], param))
            self._victims[param][end] = sample
            return sample

    def __createDisturber(self, name, param):
        return Disturber(name, self.__getParam(param), self._standard)

    def __createVictim(self, name, param, disturbers):
        return Victim(name, self.__getParam(param), disturbers, self._standard)

    def __calculateAXEXTD(self, disturbers, param):
        return [x.getParameters()[self.__getParam(param)] for x in disturbers]

    def __getParam(self, name):
        if name == "PSANEXT":
            return "ANEXT"
        else:
            return "AFEXT"

    def removeSample(self, sample):
        for param in self._disturbers:
            for end in self._disturbers[end]:
                if sample in self._disturbers[param][end]:
                    self._disturbers[param][end].remove(sample)
                elif sample == self._victims[param][end]:
                    self._victims[param][end] = None

    def updateDisturbers(self, names, end, param):
        disturbers = [x for x in self._disturbers[param][end] if x.getName() in names]
        if self._victims[param][end]:
            self._victims[param][end].setAXEXTD(self.__calculateAXEXTD(disturbers, param))

    def disturbers(self):
        return self._disturbers

    def victims(self):
        return self._victims

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def nodeFromProject(self):
        return AlienNode(self)

    def setStandard(self, standard):
        self._standard = standard
        for param in self._disturbers:
            for end in self._disturbers[param]:
                for disturber in self._disturbers[param][end]:
                    disturber.setStandard(standard)
                if self._victims[param][end]:
                    self._victims[param][end].setStandard(standard)

from app.node import Node
from sample.sample import SampleNode
from widgets.alien_widget import AlienWidget
from PyQt5 import QtWidgets
class AlienNode(ProjectNode):

    def openImportWindow(self, parent):
        dial = AlienImportDialog(parent)
        files = dial.getFiles()
        if files:
            disturbersFile, victimFile, end, param = files
            samples = list()
            samples = deepcopy(self._dataObject.importSamples(disturbersFile, end, param, disturber=True))
            samples.append(self._dataObject.importSamples([victimFile], end, param, disturber=False))
            self.addChildren(samples, end, param)
            if self._alienTab:
                self._alienTab.updateWidget()

    def addChildren(self, samples, end, param):
        node = self.hasChild(param)
        if not node:
            node = Node(param)
            self.appendRow(node)
        subNode = node.hasChild(end)
        if not subNode:
            subNode = Node(end)
            node.appendRow(subNode)
        subNode.children = list()
        for sample in samples:
            subNode.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        for param, ends in self._dataObject.disturbers().items():
            for end, samples in ends.items():
                if len(samples):
                    self.addChildren(samples, end, param)

    def getWidgets(self):
        self._alienTab = AlienWidget(self)
        return {"Alien": self._alienTab}

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)
        self._alienTab.updateWidget()