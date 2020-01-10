from snpanalyzer.gui.ui.format import Ui_form
from snpanalyzer.analysis.format import DataFormat

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class FormatSelectionWidget(QWidget):
    # the signal emitted when the format changes
    changed = pyqtSignal(DataFormat)

    def __init__(self, parent=None):
        super(FormatSelectionWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup radios
        self.__radios = dict()
        self.__radios[DataFormat.MAGNITUDE] = self.__ui.magnitudeRadioButton
        # self.__radios[DataFormat.PHASE]     = self.__ui.phaseRadioButton
        # self.__radios[DataFormat.IMAGINARY] = self.__ui.imaginaryRadioButton
        self.__radios[DataFormat.REAL]      = self.__ui.realRadioButton
        self.__radios[DataFormat.DELAY]     = self.__ui.delayRadioButton
        self._export = dict()
        self._export[DataFormat.MAGNITUDE] = [DataFormat.MAGNITUDE, DataFormat.PHASE]
        self._export[DataFormat.REAL] = [DataFormat.REAL, DataFormat.IMAGINARY]
        self._export[DataFormat.DELAY] = [DataFormat.DELAY]

        # setup the radio button signals
        for (f, r) in self.__radios.items():
            r.toggled.connect(lambda c,f=f:self.changed.emit(f) if c else None)

        # default selection
        self.setFormat(DataFormat.MAGNITUDE)

    def setAvailableFormats(self, formats, default=None):
        # select an available format if needed
        if self.__format not in formats:
            # select default format if it is available
            if default is not None:
                self.setFormat(default)

            # select a random available format
            self.setFormat(next(iter(formats)))

        # enable available formats
        {r.setEnabled(f in formats) for (f, r) in self.__radios.items()}

    def setFormat(self, pformat):
        self.__format = pformat
        self.__radios[self.__format].setChecked(True)

    def getFormat(self):
        return self.__format

    def getFormatExport(self):
        return self._export[self.__format]
        


