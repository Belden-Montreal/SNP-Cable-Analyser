from snpanalyzer.gui.ui.presets import Ui_presetsWidget

from PyQt5.QtWidgets import QWidget

class PresetsWidget(QWidget):
    def __init__(self, parent=None):
        super(PresetsWidget, self).__init__(parent)
        self.__ui = Ui_presetsWidget()
        self.__ui.setupUi(self)
    
