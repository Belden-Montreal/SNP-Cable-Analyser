import app.alien_import_dialog
from PyQt5 import QtWidgets
from os.path import basename

class AlienImportDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(AlienImportDialog, self).__init__(parent)
        self._dial = app.alien_import_dialog.Ui_AlienImportDialog()
        self._dial.setupUi(self)
        self._dial.disturbersButton.pressed.connect(lambda: self.__getDisturbers())
        self._dial.victimButton.pressed.connect(lambda:self.__getVictim())
        self._disturbers = None
        self._victim = None


    def getFiles(self):
        res = self.exec_()
        if res:
            return self._disturbers, self._victim

    def __getDisturbers(self):
        files,_ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select disturbers", "", "sNp Files (*.s*p)")
        self._disturbers = files
        self._dial.disturbersList.clear()
        self._dial.disturbersList.insertItems(0, [basename(dist) for dist in self._disturbers])

    def __getVictim(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select victim", "", "sNp Files (*.s*p)")
        self._victim = fileName
        self._dial.victimLabel.setText(basename(self._victim))