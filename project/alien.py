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
            samples = pool.starmap(self.__createDisturber, zip(fileNames, [param]*len(fileNames)))
            if self._victims[end][param] is not None:
                self._victims[end][param].setAXEXTD(self.__calculateAXEXTD(samples, param))
            self._disturbers[end][param] = samples
            return samples
        elif len(fileNames) < 2:
            sample = self.__createVictim(fileNames[0], param, self.__calculateAXEXTD(self._disturbers[end][param], param))
            self._victims[end][param] = sample
            return sample

    def __createDisturber(self, name, param):
        return Disturber(name, self.__getParam(param))

    def __createVictim(self, name, param, disturbers):
        return Victim(name, self.__getParam(param), disturbers)

    def __calculateAXEXTD(self, disturbers, param):
        return [x.getParameters()[self.__getParam(param)] for x in disturbers]

    def __getParam(self, name):
        if name == "PSANEXT":
            return "ANEXT"
        else:
            return "AFEXT"

    def removeSample(self, sample):
        for end in self._disturbers:
            for param in self._disturbers[end]:
                if sample in self._disturbers[end][param]:
                    self._disturbers[end][param].remove(sample)
                elif sample == self._victims[end][param]:
                    self._victims[end][param] = None

    def updateDisturbers(self, names, end, param):
        disturbers = [x for x in self._disturbers[end][param] if x.getName() in names]
        if self._victims[end][param]:
            self._victims[end][param].setAXEXTD(self.__calculateAXEXTD(disturbers, param))

    def disturbers(self):
        return self._disturbers

    def victims(self):
        return self._victims

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def nodeFromProject(self):
        return AlienNode(self)

    def setStandard(self, standard):
        for end in self._disturbers:
            for param in self._disturbers[end]:
                for disturber in self._disturbers[end][param]:
                    disturber.setStandard(standard)
                if self._victims[end][param]:
                    self._victims[end][param].setStandard(standard)

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
        self._alienTab = AlienWidget(self)
        return {"Alien": self._alienTab}

    def setStandard(self, standard):
        self._dataObject.setStandard(standard)
        self._alienTab.updateWidget()