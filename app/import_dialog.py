from PyQt5 import QtWidgets, QtCore, QtGui

class ImportSNPDialog(QtWidgets.QFileDialog):
    def __init__(self, parent):
        super(ImportSNPDialog, self).__init__(parent, caption="Select SNP(s)", directory="",filter="sNp Files (*.s*p)")
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, on=True)
        self.setFileMode(self.ExistingFiles)
        self._checkbox = QtWidgets.QCheckBox("Single-Ended?", self)
        self.layout().addWidget(self._checkbox)

    def getFiles(self):
        res = self.exec_()
        if res: 
            return self._checkbox.isChecked(), self.selectedFiles()
        return None