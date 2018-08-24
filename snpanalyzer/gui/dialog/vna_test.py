from snpanalyzer.gui.ui.vna_test import Ui_dialog
from tempfile import gettempdir
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QFileDialog

class VNATestDialog(QDialog):
    def __init__(self):
        super(VNATestDialog, self).__init__()

        # setup UI
        self.__ui = Ui_dialog()
        self.__ui.setupUi(self)

    def setVNAConfiguration(self, config):
        self.__ui.vna.setConfiguration(config)

    def getVNACOnfiguration(self):
        return self.__ui.vna.getVNAConfiguration()

    def getSampleName(self):
        return self.__ui.nameLineEdit.text()

    def getLimit(self):
        return self.__ui.limitLineEdit.text()
