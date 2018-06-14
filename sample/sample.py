from snpAnalyze import SNPManipulations
from os.path import splitext, basename, getctime
import time

class Sample(object):
    '''
    The sample class contains the measurements for one object
    '''

    def __init__(self, snpFile):
        self._parameters = dict()
        if snpFile:
            self._snp = SNPManipulations(snpFile)
            self._mm = self._snp.mm
            self._ports = self._snp.port_names
            self._freq = self._snp.freq
            self._name, self._extension = splitext(basename(snpFile))
            self._date = time.ctime(getctime(snpFile))
            self.addParameters()

    def addParameters(self):
        raise NotImplementedError


    