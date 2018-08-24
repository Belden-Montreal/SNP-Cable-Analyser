from snpanalyzer.gui.ui.unitinput import Ui_form
from snpanalyzer.analysis.unit import FrequencyUnit

from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

class UnitInputWidget(QWidget):
    # the signal emitted when either the value or the unit changes
    changed = pyqtSignal(int)

    def __init__(self, parent=None):
        super(UnitInputWidget, self).__init__(parent)

        # setup UI
        self.__ui = Ui_form()
        self.__ui.setupUi(self)

        # we only accept number
        self.__ui.valueLineEdit.setValidator(QIntValidator())
        self.__ui.valueLineEdit.setText(str(1))

        # default to frequency units
        self.setUnits([
            FrequencyUnit.HERTZ,
            FrequencyUnit.KILOHERTZ,
            FrequencyUnit.MEGAHERTZ,
            FrequencyUnit.GIGAHERTZ,
        ])

        # connect signals
        self.__ui.unitComboBox.currentIndexChanged.connect(self.__unitChanged)
        self.__ui.valueLineEdit.textChanged.connect(self.__valueChanged)

    def setValue(self, value):
        self.__ui.valueLineEdit.setText(str(value))

    def setUnits(self, units, default=0):
        # remove old items
        self.__ui.unitComboBox.clear()

        # add an item for each unit
        for unit in units:
            self.__ui.unitComboBox.addItem(unit.getUnit(), userData = unit)

        # select the default selection
        self.__ui.unitComboBox.setCurrentIndex(default)

    def getValue(self):
        value = int(self.__ui.valueLineEdit.text())
        unit = self.__ui.unitComboBox.currentData()
        return value*unit.getFactor()

    def __valueChanged(self, text):
        self.changed.emit(self.getValue())

    def __unitChanged(self, index):
        self.changed.emit(self.getValue())       


