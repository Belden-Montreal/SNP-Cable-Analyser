from project.project import Project, ProjectNode
from sample.delay import Delay
from sample.plug_sample import PlugSample
from project.plug_import_dialog import PlugImportDialog
import numpy as np

class Plug(Project):

    def __init__(self, name):
        super(Plug, self).__init__(name)
        self._openDelay = None
        self._shortDelay = None
        self._loadSample = None
        self._dfOpenDelay = None
        self._dfShortDelay = None
        self._k1 = 0
        self._k2 = 0
        self._k3 = 0

    def getPlugNext(self):
        return self._loadSample.getParameters()["CNEXT"]

    def getNextDelay(self):
        return self._loadSample.getParameters()["NEXTDelay"]

    def setConstants(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3

    def recalculate(self):
        self._loadSample.recalculate(self._k1, self._k2, self._k3)

    def getConstants(self):
        return (self._k1, self._k2, self._k3)

    def nodeFromProject(self):
        return PlugNode(self)


from sample.sample import SampleNode
class PlugNode(ProjectNode):

    def openImportWindow(self, parent):
        dial = PlugImportDialog(parent)
        files = dial.getFiles()
        if files:
            dfOpen, dfShort, plugOpen, plugShort, plugLoad, k1, k2, k3 = files
            openSample = Delay(plugOpen)
            shortSample = Delay(plugShort)
            dfOpenSample = Delay(dfOpen)
            dfShortSample = Delay(dfShort)
            loadSample = PlugSample(plugLoad, 
                                    openSample.getParameters()["Propagation Delay"],
                                    shortSample.getParameters()["Propagation Delay"],
                                    dfOpenSample.getParameters()["Propagation Delay"],
                                    dfShortSample.getParameters()["Propagation Delay"],
                                    k1, k2, k3)

            samples = [openSample, shortSample, dfOpenSample, dfShortSample, loadSample]
            self.addChildren(samples)
            self._dataObject.setConstants(k1, k2, k3)
            self._dataObject._samples = samples
            self._dataObject._loadSample = loadSample

    def addChildren(self, samples):
        for sample in samples:
            self.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        self.addChildren(self._dataObject._samples)