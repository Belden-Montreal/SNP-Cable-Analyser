import app.embed_import_dialog
from PyQt5 import QtWidgets, QtCore
from os.path import basename

class EmbedImportDialog(QtWidgets.QDialog):

    def __init__(self, parent):
        super(EmbedImportDialog, self).__init__(parent)
        self._dial = app.embed_import_dialog.Ui_EmbedImportDialog()
        self._dial.setupUi(self)
        self._dial.revBox.stateChanged.connect(lambda state: self.__reverse(state))
        self._dial.openBtn.pressed.connect(lambda: self.__getOpen())
        self._dial.shortBtn.pressed.connect(lambda: self.__getShort())
        self._dial.loadBtn.pressed.connect(lambda: self.__getLoad())
        self._dial.plugBtn.pressed.connect(lambda: self.__getPlug())
        self._dial.buttonBox.accepted.connect(lambda: self.__verifyInputs())
        self._open = None
        self._short = None
        self._load = None
        self._plug = None
        self._k1, self._k2, self._k3 = None, None, None
        self._dial.sJ12LineEdit.setText("5e-12")
        self._dial.sJ36LineEdit.setText("14e-12")
        self._dial.thruCalibLineEdit.setText("20e-12")
        self._dial.openBtn.setDisabled(True)
        self._dial.shortBtn.setDisabled(True)

    def getFiles(self):
        res = self.exec_()
        if res:
            return self._load, self._plug, self._k1, self._k2, self._k3, self._open, self._short

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

    def __getPlug(self):
        fileName,_ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Plug Project", "projects/", "Belden Network Analyzer Project files (*.bnap)")
        self._dial.plugLabel.setText(basename(fileName))
        self._plug = fileName

    def __verifyInputs(self):
        try:
            self._k1 = float(self._dial.sJ12LineEdit.text())
            self._k2 = float(self._dial.sJ36LineEdit.text())
            self._k3 = float(self._dial.thruCalibLineEdit.text())
            if (self._load and self._dial.revBox.checkState == QtCore.Qt.Unchecked) or (self._open and self._short and self._load and self._dial.revBox.checkState == QtCore.Qt.Checked):
                self.accept()
            # else:
            #     raise Exception("No File Error")
        except Exception as e:
            error = QtWidgets.QErrorMessage(self)
            error.showMessage(str(e), "Invalid_Inputs")
            error.exec_()

    def __reverse(self, state):
        if state == QtCore.Qt.Unchecked:
            self._dial.openBtn.setDisabled(True)
            self._dial.shortBtn.setDisabled(True)
        elif state == QtCore.Qt.Checked:
            self._dial.openBtn.setDisabled(False)
            self._dial.shortBtn.setDisabled(False)