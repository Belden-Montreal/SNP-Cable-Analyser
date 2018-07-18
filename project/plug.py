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

    def importDfOpen(self, fileName):
        self._dfOpenDelay = Delay(fileName)
        return self._dfOpenDelay

    def importDfShort(self, fileName):
        self._dfShortDelay = Delay(fileName)
        return self._dfShortDelay

    def importOpen(self, fileName):
        self._openDelay = Delay(fileName)
        return self._openDelay

    def importShort(self, fileName):
        self._shortDelay = Delay(fileName)
        return self._shortDelay

    def importLoad(self, fileName):
        self._loadSample = PlugSample(fileName, 
            self._openDelay.getParameters()["Propagation Delay"],
            self._shortDelay.getParameters()["Propagation Delay"],
            self._dfOpenDelay.getParameters()["Propagation Delay"],
            self._dfShortDelay.getParameters()["Propagation Delay"],
            self._k1, self._k2, self._k3)
        return self._loadSample

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
from widgets.plug_widget import PlugWidget

class PlugNode(ProjectNode):
    def __init__(self, plug):
        super(PlugNode, self).__init__(plug)
        self._plugWidget = None

    def openImportWindow(self, parent):
        dial = PlugImportDialog(parent)
        files = dial.getFiles()
        if files:
            dfOpen, dfShort, plugOpen, plugShort, plugLoad, k1, k2, k3 = files
            openSample = self._dataObject.importOpen(plugOpen)
            shortSample = self._dataObject.importShort(plugShort)
            dfOpenSample = self._dataObject.importDfOpen(dfOpen)
            dfShortSample = self._dataObject.importDfShort(dfShort)
            self._dataObject.setConstants(k1, k2, k3)
            loadSample = self._dataObject.importLoad(plugLoad)

            samples = [openSample, shortSample, dfOpenSample, dfShortSample, loadSample]
            self.addChildren(samples)
            self._dataObject._samples = samples
            if self._plugWidget:
                self._plugWidget.createTabs()
                self._plugWidget.updateWidget()

    def addChildren(self, samples):
        for sample in samples:
            self.appendRow(SampleNode(sample, self._dataObject))

    def setupInitialData(self):
        samples = [self._dataObject._openDelay, self._dataObject._shortDelay, self._dataObject._dfOpenDelay, self._dataObject._dfShortDelay, self._dataObject._loadSample]
        self.addChildren(samples)

    def getWidgets(self):
        if not self._plugWidget:
            self._plugWidget = PlugWidget(self)
        return {"Plug": self._plugWidget}