from project.project import Project
from sample.delay import Delay
from sample.plug_sample import PlugSample
from project.plug_import_dialog import PlugImportDialog
import numpy as np

class Filetype():
    OPEN = 0
    SHORT = 1
    LOAD = 2
    DFOPEN = 3
    DFSHORT = 4

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

    def importSamples(self, fileName, fileType=Filetype.OPEN):
        if fileType == Filetype.OPEN:
            openSample = Delay(fileName)
            self._samples.append(openSample)
            self._openDelay = openSample.getParameters()["Propagation Delay"]
        elif fileType == Filetype.SHORT:
            shortSample = Delay(fileName)
            self._samples.append(shortSample)
            self._shortDelay = shortSample.getParameters()["Propagation Delay"]
        elif fileType == Filetype.LOAD:
            self._loadSample = PlugSample(fileName, self._openDelay, self._shortDelay, self._dfOpenDelay, self._dfShortDelay, self._k1, self._k2, self._k3)
            self._samples.append(self._loadSample)
        elif fileType == Filetype.DFOPEN:
            dfOpenSample = Delay(fileName)
            self._samples.append(dfOpenSample)
            self._dfOpenDelay = dfOpenSample.getParameters()["Propagation Delay"]
        elif fileType == Filetype.DFSHORT:
            dfShortSample = Delay(fileName)
            self._samples.append(dfShortSample)
            self._dfShortDelay = dfShortSample.getParameters()["Propagation Delay"]

    def removeSamples(self, fileNames):
        super(Plug, self).removeSamples(fileNames)

    def getPlugNext(self):
        return self._loadSample.getParameters()["CNEXT"]

    def getNextDelay(self):
        return self._loadSample.getParameters()["NEXTDelay"]

    def setConstants(self, k1, k2, k3):
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3

    def openImportWindow(self, parent):
        dial = PlugImportDialog(parent)
        files = dial.getFiles()
        if files:
            dfOpen, dfShort, plugOpen, plugShort, plugLoad, k1, k2, k3 = files
            self._k1 = k1
            self._k2 = k2
            self._k3 = k3
            self.importSamples(dfOpen, Filetype.DFOPEN)
            self.importSamples(dfShort, Filetype.DFSHORT)
            self.importSamples(plugOpen, Filetype.OPEN)
            self.importSamples(plugShort, Filetype.SHORT)
            self.importSamples(plugLoad, Filetype.LOAD)
            self._generateTreeStructure()

   