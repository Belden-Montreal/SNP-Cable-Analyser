class ExportConfiguration(object):
    def __init__(self, export=True):
        self._export = export

    def doExport(self):
        return self._export

    def setExport(self, export=True):
        self._export = export

    def generateDocumentObject(self, root, prefix):
        raise NotImplementedError
