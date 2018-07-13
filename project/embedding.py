from project.project import Project, ProjectNode
from project.embedding_import_dialog import EmbedImportDialog, ReverseState
from app.save_manager import SaveManager
from sample.single_ended import SingleEnded
from sample.deembed import Deembed
import numpy as np

class Case():
    CAT5E = {
            1:((0,2),(lambda f, cnext: (-35.8+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            2:((0,2),(None)),
            3:((0,2),(None)),
            4:((0,2),(lambda f, cnext: (-39.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            5:((1,2),(lambda f, cnext: (-42+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            6:((1,2),(lambda f, cnext: (-50+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            7:((2,3),(lambda f, cnext: (-42+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            8:((2,3),(lambda f, cnext: (-50+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            9:((0,1),(lambda f, cnext: (-50+20*np.log10(f/100), 90))),
            10:((0,1),(None)),
            11:((0,3),(lambda f, cnext: (-50+20*np.log10(f/100), 90))),
            12:((0,3),(None)),
            13:((1,3),(lambda f, cnext: (-60+20*np.log10(f/100), 90))),
            14:((1,3),(None)),
            }
    CAT6 = {
            1:((0,2),(lambda f, cnext: (-38.1+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            2:((0,2),(lambda f, cnext: (-38.6+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            3:((0,2),(lambda f, cnext: (-39+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            4:((0,2),(lambda f, cnext: (-39.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            5:((1,2),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            6:((1,2),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            7:((2,3),(lambda f, cnext: (-46.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            8:((2,3),(lambda f, cnext: (-49.5+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            9:((0,1),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            10:((0,1),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            11:((0,3),(lambda f, cnext: (-57+20*np.log10(f/100), 90))),
            12:((0,3),(lambda f, cnext: (-70+20*np.log10(f/100), -90))),
            13:((1,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)))),
            14:((1,3),(lambda f, cnext: (-66+20*np.log10(f/100), np.angle(cnext, deg=True)-180))),
            }

class Embedding(Project):
    '''
    This class represents a project for analyzing plug embedding
    '''
    def __init__(self, name):
        super(Embedding, self).__init__(name)
        self._plug = None
        self._sides = dict()
        self._sides["Forward"] = list()
        self._sides["Reverse"] = list()

    def setPlug(self, plug):
        self._plug = plug
    
    def removeSample(self, sample):
        for side in self._sides.values():
            if sample in side:
                side.remove(sample)

    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError

    def nodeFromProject(self):
        return EmbeddingNode(self)


from app.node import Node
from sample.sample import SampleNode
from project.plug import PlugNode
from widgets.embed_widget import EmbedWidget
from PyQt5 import QtWidgets
class EmbeddingNode(ProjectNode):

    def openImportWindow(self, parent):
        dial = EmbedImportDialog(parent)
        files = dial.getFiles()
        if files:
            loadFile, plugFile, k1, k2, k3, cat, reverse, openFile, shortFile = files
            samples = list()
            if cat == "CAT5e":
                cases = Case.CAT5E
            else:
                cases = Case.CAT6
            if reverse == ReverseState.REVERSE:
                openSample = SingleEnded(openFile)
                shortSample = SingleEnded(shortFile)
                samples.extend([openSample, shortSample])
            plugProject = SaveManager().loadProject(plugFile)
            loadSample = Deembed(loadFile, plugProject.getPlugNext(), plugProject.getNextDelay(), cases)
            samples.append(loadSample)
            self._dataObject._sides[reverse] = samples
            self._dataObject.setPlug(plugProject)
            self.addChildren(samples, plugProject, reverse)

    def addChildren(self, samples, plug, side):
        node = self.hasChild(side)
        if not node:
            node = Node(side)
            self.appendRow(node)
        node.appendRow(PlugNode(plug))
        for sample in samples:
            node.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        for side, samples in self._dataObject._sides.items():
            if len(samples):
                self.addChildren(samples, self._dataObject._plug, side)

    def getWidgets(self):
        embedTab = EmbedWidget()
        return {"Embedding": embedTab}