from gui.ui.scale import Ui_form
from analysis.scale import PlotScale

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class ScaleSelectionWidget(QWidget):
    # the signal emitted when the scale changes
    scaleChanged = pyqtSignal(PlotScale)

    def __init__(self, parent=None):
        super(ScaleSelectionWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # setup radios
        self.__radios = dict()
        self.__radios[PlotScale.LINEAR]      = self.__ui.linearRadioButton
        self.__radios[PlotScale.LOGARITHMIC] = self.__ui.logarithmicRadioButton

        # setup the radio button signals
        for (s, r) in self.__radios.items():
            r.toggled.connect(lambda c,s=s:self.scaleChanged.emit(s) if c else None)

        # default selection
        self.setScale(PlotScale.LOGARITHMIC)

    def setScale(self, scale):
        self.__scale = scale
        self.__radios[self.__scale].setChecked(True)

    def getScale(self):
        return self.__scale
        


