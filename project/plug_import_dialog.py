import app.plug_import_dialog
from PyQt5 import QtWidgets
from os.path import basename

class PlugImportDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(PlugImportDialog, self).__init__(parent)
        self._dial = app.plug_import_dialog.Ui_PlugImportDialog()
        self._dial.setupUi(self)
        self._dial.dfOpenBtn.pressed.connect(lambda: self.__getDFOpen())
        self._dial.dfShortBtn.pressed.connect(lambda: self.__getDFShort())
        self._dial.openBtn.pressed.connect(lambda: self.__getOpen())
        self._dial.shortBtn.pressed.connect(lambda: self.__getShort())
        self._dial.loadBtn.pressed.connect(lambda: self.__getLoad())
        self._dial.buttonBox.accepted.connect(lambda: self.__verifyInputs())
        self._dfOpen = None
        self._dfShort = None
        self._open = None
        self._short = None
        self._load = None
        self._k1, self._k2, self._k3 = None, None, None

    def getFiles(self):
        res = self.exec_()
        if res:
            return self._dfOpen, self._dfShort, self._open, self._short, self._load, self._k1, self._k2, self._k3

    def __getDFOpen(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SNP", "", "sNp Files (*.s*p)")
        self._dial.dfOpenLabel.setText(basename(fileName))
        self._dfOpen = fileName

    def __getDFShort(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SNP", "", "sNp Files (*.s*p)")
        self._dial.dfShortLabel.setText(basename(fileName))
        self._dfShort = fileName

    def __getOpen(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SNP", "", "sNp Files (*.s*p)")
        self._dial.openLabel.setText(basename(fileName))
        self._open = fileName

    def __getShort(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SNP", "", "sNp Files (*.s*p)")
        self._dial.shortLabel.setText(basename(fileName))
        self._short = fileName

    def __getLoad(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select SNP", "", "sNp Files (*.s*p)")
        self._dial.loadLabel.setText(basename(fileName))
        self._load = fileName

    def __verifyInputs(self):
        try:
            self._k1 = float(self._dial.sJ12LineEdit.text())
            self._k2 = float(self._dial.sJ36LineEdit.text())
            self._k3 = float(self._dial.thruCalibLineEdit.text())
            self.accept()
        except:
            error = QtWidgets.QErrorMessage(self)
            error.showMessage("Invalid inputs", "Invalid_Inputs")
            error.exec_()