from project.project import Project
from sample.single_ended import SingleEnded
from sample.deembed import Deembed

class Filetype():
    OPEN = 0
    SHORT = 1
    LOAD = 2

class Embedding(Project):
    '''
    This class represents a project for analyzing plug embedding
    '''
    def __init__(self):
        super(Embedding, self).__init__()
        self._openSample = None
        self._shortSample = None
        self._deembedded = None
        self._plug = None

    def importSamples(self, fileName, fileType=Filetype.LOAD):
        if fileType == Filetype.OPEN:
            self._openSample = SingleEnded(fileName)
            self._samples.append(self._openSample)
        elif fileType == Filetype.SHORT:
            self._shortSample = SingleEnded(fileName)
            self._samples.append(self._shortSample)
        else:
            self._deembedded = Deembed(fileName, self._plug.getPlugNext(), self._plug.getNextDelay())
            self._samples.append(self._deembedded)

    def setPlug(self, plug):
        self._plug = plug
    
    def removeSamples(self, fileNames):
        super(Embedding, self).removeSamples(fileNames)
        if self._openSample and self._openSample.getName() in fileNames:
            self._openSample = None
        if self._shortSample and self._shortSample.getName() in fileNames:
            self._shortSample = None
        if self._deembedded and self._deembedded.getName() in fileNames:
            self._deembedded = None


    def generateExcel(self, outputName, sampleNames, z=False):
        raise NotImplementedError