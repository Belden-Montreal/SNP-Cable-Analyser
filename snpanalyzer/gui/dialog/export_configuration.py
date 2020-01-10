import os

from snpanalyzer.gui.ui.export.export import Ui_dialog
from tempfile import gettempdir
from pathlib import Path

from PyQt5.QtWidgets import QDialog, QFileDialog

class ExportConfigurationDialog(QDialog):
    def __init__(self, config):
        super(ExportConfigurationDialog, self).__init__()
        self.__config = config

        # setup UI
        self.__ui = Ui_dialog()
        self.__ui.setupUi(self)
        self.__ui.projectExportWidget.setExportConfiguration(config)

        # set default paths
        self.__ui.docLineEdit.setText(str(Path.home().joinpath("Desktop\document.pdf")))

        # setup signals
        self.__ui.docBrowsePushButton.clicked.connect(self.__browseOutputDocument)


    def __browseOutputDocument(self, clicked):
        filename = QFileDialog.getSaveFileName(
            self,
            "Save document as...",
            self.__ui.docLineEdit.text(),
            "Document (*.pdf)"
        )

        # update the filename if possible
        if not filename[0] == "":
            self.__ui.docLineEdit.setText(filename[0])

    def getTemporaryDirectory(self):
        return Path(os.getcwd()+"\Temp")

    def getDocumentFilename(self):
        return Path(self.__ui.docLineEdit.text())

